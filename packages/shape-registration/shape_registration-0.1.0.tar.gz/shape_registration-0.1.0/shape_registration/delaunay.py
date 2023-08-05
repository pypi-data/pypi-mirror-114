import itertools
from typing import List, Mapping, Optional, Sequence, Union

import numpy as np

import torch
from pytorch_lightning.utilities.device_dtype_mixin import DeviceDtypeModuleMixin

from shape_registration.utils import (
    tri_angle_between,
    unit_vector,
    normalize_points,
)
from copy import deepcopy
from functools import wraps
from scipy.spatial import Delaunay as SPDelaunay
from abc import ABCMeta, abstractmethod


class Simplex(DeviceDtypeModuleMixin):
    def __init__(
        self,
        vertex_coordinates: torch.Tensor,
        vertex_indices: Optional[torch.Tensor] = None,
        values: Optional[torch.Tensor] = None,
    ):
        super().__init__()

        if not isinstance(vertex_coordinates, torch.Tensor):
            vertex_coordinates = torch.tensor(
                vertex_coordinates, device=self.device, dtype=self.dtype
            )

        if vertex_indices is None:
            vertex_indices = range(len(vertex_coordinates))

        if not isinstance(vertex_indices, torch.Tensor):
            vertex_indices = torch.tensor(
                vertex_indices, device=self.device, dtype=self.dtype
            )

        if values is not None and not isinstance(values, torch.Tensor):
            values = torch.tensor(values, device=self.device, dtype=self.dtype)

        if vertex_coordinates.size(0) != vertex_coordinates.size(1) + 1:
            raise AssertionError

        if values is not None:
            if vertex_coordinates.size(0) != values.size(0):
                raise AssertionError

        self.register_buffer("vertices", vertex_coordinates)
        self.register_buffer("vertex_indices", vertex_indices)
        self.register_buffer("values", values)

        edges = self.create_edges(self.vertex_indices, self.vertices)

        self.register_buffer(
            "edges", torch.tensor(edges, device=self.device, dtype=self.dtype)
        )

        self._circumcircle = None

    def __str__(self):
        return f"{self.__class__.__name__}(\n\t vertices: \t{self.vertices}\n\t vertex_indices: \t{self.vertex_indices}\n\t values: \t{self.values}"

    def __repr__(self):
        return self.__str__()

    def contains_edge(self, edge: torch.Tensor):
        if self.ndim == 2:
            return (self.edges == edge[None]).any()
        if self.ndim == 3:
            for e in self.edges:
                if (e == edge).all():
                    return True
            return False

    def __eq__(self, o: Union[object, torch.Tensor]) -> bool:
        if isinstance(o, torch.Tensor):
            return (self.vertex_indices == o).all()

        return (self.vertex_indices == o.vertex_indices).all()

    @property
    def ndim(self):
        return self.vertices.size(-1)

    @staticmethod
    def create_edges(vertex_indices, vertex_coordinates):
        dim = vertex_coordinates.size(-1)
        edges = sorted(itertools.combinations(vertex_indices.tolist(), dim))

        return edges

    @staticmethod
    def _point_dist(point1: torch.Tensor, point2: torch.Tensor) -> torch.Tensor:
        return torch.norm(point1 - point2)

    def circumcircle(self):
        """Compute circumcenter and circumradius of a triangle in 2D.
        Uses an extension of the method described here:
        http://www.ics.uci.edu/~eppstein/junkyard/circumcenter.html
        """
        if self._circumcircle is None:
            if self.ndim == 2:
                center, radius = self._circumcenter_triangle()
            elif self.ndim == 3:
                center, radius = self._circumcenter_tetrahedron()
            else:
                raise ValueError

            self._circumcircle = (center, radius)

        return self._circumcircle

    @staticmethod
    def _perp_bisector(x, y):
        """
        Calculate perpendicular bisector plane of `X-Y`

        Inputs:
        -------
        X,Y: 3D coordinates as Tensors.
        Returns:
        --------
        plane: tuple of [normal_vector, plane_constant]
        """
        plane_norm = (y - x) / torch.norm(y - x)
        mid = (y + x) / 2
        plane = [plane_norm, -torch.dot(plane_norm, mid)]

        return plane

    @staticmethod
    def _three_plane_intersection(plane_1, plane_2, plane_3):
        """
        Calculate intersection point of three planes.
        As long as the planes are not derived from edges on the same plane, it can be guaranteed that they intersect in a single point.

        Inputs:
        -------
        Three
        Returns:
        --------
        P: 1D Tensor with length 3
            Intersection point
        """
        n1, d1 = plane_1
        n2, d2 = plane_2
        n3, d3 = plane_3

        if torch.dot(n1, torch.cross(n2, n3)) == 0:
            assert (
                torch.dot(n1, torch.cross(n2, n3)) != 0
            ), "Normals are not linearly independent!"

        temp = -(
            d1 * (torch.cross(n2, n3))
            + d2 * (torch.cross(n3, n1))
            + d3 * (torch.cross(n1, n2))
        )
        p = temp / torch.dot(n1, torch.cross(n2, n3))

        return p

    def _circumcenter_tetrahedron(self):
        """
        Inputs:
        -------
        tetrahedron: [4,3] Tensor with set of 4 Coordinates in 3D space.

        Returns:
        --------
        center: 1D Tensor
            Coordinates of circumcenter
        radius: 1D Tensor
            Radius of sphere
        """
        tetrahedron = self.vertices.clone()
        pt_a, pt_b, pt_c, pt_d, *_ = tetrahedron
        plane_1 = self._perp_bisector(pt_a, pt_b)
        plane_2 = self._perp_bisector(pt_a, pt_c)
        plane_3 = self._perp_bisector(pt_a, pt_d)

        center = self._three_plane_intersection(plane_1, plane_2, plane_3)
        radius = torch.norm(center - pt_a)

        # if (torch.norm(center-tetrahedron, dim=1)-radius).abs().sum() > 0:
        #     print('circumsphere not exactt!')  # accuracy error

        return (center, radius)

    def _circumcenter_triangle(self):
        triangle = self.vertices

        pt_a, pt_b, pt_c, *_ = triangle

        sin_2a = torch.sin(2 * tri_angle_between(pt_c, pt_a, pt_b))
        sin_2b = torch.sin(2 * tri_angle_between(pt_a, pt_b, pt_c))
        sin_2c = torch.sin(2 * tri_angle_between(pt_a, pt_c, pt_b))

        # center in (y, x)
        center = (
            torch.stack(
                [
                    (pt_a[0] * sin_2a + pt_b[0] * sin_2b + pt_c[0] * sin_2c),
                    (pt_a[1] * sin_2a + pt_b[1] * sin_2b + pt_c[1] + sin_2c),
                ]
            )
            / (sin_2a + sin_2b + sin_2c)
        )

        radius = torch.norm(center - pt_a)

        return (center, radius)

    def point_in_circumcircle(self, p):
        """Check if point p is inside of precomputed circumcircle of tri."""
        center, radius = self.circumcircle()
        # check if p is inside the circumcircle with tolerance to avoid accuracy errors
        inside = torch.norm(center - p) < radius or torch.allclose(
            torch.norm(center - p), radius, rtol=1e-08, atol=1e-11
        )
        return inside

    def point_to_barycentric(self, point: torch.Tensor):
        # solve Rw=r for w
        R = torch.cat(
            [
                self.vertices.transpose(1, 0),
                torch.ones(
                    (1, self.vertices.size(0)), device=self.device, dtype=self.dtype
                ),
            ]
        )
        r = torch.cat([point, torch.ones(1, device=self.device, dtype=self.dtype)])

        return torch.linalg.solve(R, r.unsqueeze(1)).squeeze()

    def point_to_cartesian(self, point: torch.Tensor):
        R = torch.cat(
            [
                self.vertices.transpose(1, 0),
                torch.ones(
                    (1, self.vertices.size(0)), device=self.device, dtype=self.dtype
                ),
            ]
        )

        return torch.matmul(R, point)[:-1]

    def contains_point_cartesian(self, point):
        barycentric = self.point_to_barycentric(point)

        return self.contains_point_barycentric(barycentric)

    @staticmethod
    def contains_point_barycentric(point: torch.Tensor):
        return (point >= 0).all()

    def interpolate_cartesian(self, point: torch.Tensor, mode: str = "linear"):
        return self.interpolate_barycentric(self.point_to_barycentric(point), mode=mode)

    def interpolate_barycentric(self, point: torch.Tensor, mode: str = "linear"):

        if not self.contains_point_barycentric(point):
            raise ValueError

        if self.values is None:
            return None

        if mode == "nearest":
            return self.values[torch.argmax(point)]

        elif mode == "linear":

            # return torch.sum(point * self.values, 0)
            # return torch.sum(point * self.values.T, 1)
            return torch.matmul(point, self.values)

        elif mode == "root-squared":

            # return torch.sqrt(torch.sum((point * self.values)**2, 0))
            return torch.sqrt(torch.sum((point * self.values.T) ** 2, 1))

        raise NotImplementedError

    def add_values(self, values: Mapping, default_val: float = 0.0) -> "Simplex":
        if values is None:
            self.values = None
            return

        for idx, val in values.items():
            if self.values is None:
                self.values = (
                    torch.ones(
                        (self.vertices.size(0), *val.shape),
                        device=self.device,
                        dtype=self.vertices.dtype,
                    )
                    * default_val
                )

            self.values[idx] = values[idx]

        return self


class Triangulation(DeviceDtypeModuleMixin):
    def __init__(
        self,
        simplices: Sequence[Simplex],
        values: Union[Sequence, Mapping, torch.Tensor, None] = None,
    ):
        super().__init__()

        self.simplices = torch.nn.ModuleList(simplices)
        self.register_buffer("_values", values)
        self._default_val = None

    def _get_values_for_single_simplex(self, simplex):
        if self._values is None:
            return None

        if isinstance(self._values, torch.Tensor):
            return self._get_values_for_simplex_tensor(simplex, self._values)

        if isinstance(self._values, Mapping):
            return self._get_values_for_simplex_mapping(simplex, self._values)

        if isinstance(self._values, Sequence):
            return self._get_values_for_simplex_sequence(simplex, self._values)

        raise TypeError

    @staticmethod
    def _get_values_for_simplex_mapping(simplex: Simplex, values: Mapping):
        # keys are vertex coordinates, map them to vertex indices
        # set values for all occurences of corresponding keys in all simplices

        keys_to_pop = []
        filtered_values = {}
        for idx, vert in enumerate(simplex.vertices):

            for key, val in values.items():

                # key found
                if torch.allclose(vert, key):

                    filtered_values[idx] = val
                    keys_to_pop.append(key)
                    break

        # for k in keys_to_pop:
        #     values.pop(k)

        return filtered_values

    @staticmethod
    def _get_values_for_simplex_sequence(simplex: Simplex, values: Sequence):
        # values are a sequence and align well with the order of inserted points. Mapping them to the indices

        filtered_values = {}
        for idx, vertex_idx in enumerate(simplex.vertex_indices):
            for key, val in enumerate(values):
                if key == vertex_idx:
                    filtered_values[idx] = val

        return filtered_values

    def _get_values_for_simplex_tensor(self, simplex: Simplex, values: torch.Tensor):
        # tensor is supposed to be an image/displacement field, use vertex coordinates
        filtered_values = {}

        # search for index where the vertex coordinates are in values
        for idx, vert in enumerate(simplex.vertices):
            coord = None
            # coord = torch.stack(torch.where(values==vert)).T[0][:-1]
            a = torch.stack(torch.where(values == vert[0])[:-1]).T
            b = torch.stack(torch.where(values == vert[1])[:-1]).T
            c = torch.stack(torch.where(values == vert[2])[:-1]).T
            for ia in range(a.size(0)):
                ib = torch.where(((a[ia] == b).sum(1) == 3))[0]
                ic = torch.where(((a[ia] == c).sum(1) == 3))[0]
                if len(ib) == 0 or len(ic) == 0:
                    continue
                if torch.allclose(values[tuple(a[ia])], vert):
                    coord = a[ia]
                    break
            if coord is None:
                raise RuntimeError(f"vertex {vert} not in values")
            else:
                filtered_values[idx] = self.normalize_points(
                    coord,
                    torch.tensor(
                        values.shape[: len(vert)], device=vert.device, dtype=vert.dtype
                    ),
                )

        return filtered_values

    @staticmethod
    def normalize_points(points: torch.Tensor, img_size: torch.Tensor):
        return points * 2.0 / img_size - 1

    @staticmethod
    def denormalize_points(points: torch.Tensor, img_size: torch.Tensor):
        return (points + 1) * img_size / 2.0

    def add_values(
        self, values: Union[Sequence, Mapping, torch.Tensor], default_val: float = 0.0
    ):
        if isinstance(values, Mapping):
            for simplex in self.simplices:
                simplex.add_values(
                    self._get_values_for_simplex_mapping(simplex, values),
                    default_val=default_val,
                )

        elif isinstance(values, Sequence):
            for simplex in self.simplices:
                simplex.add_values(
                    self._get_values_for_simplex_sequence(simplex, values),
                    default_val=default_val,
                )

        elif isinstance(values, torch.Tensor):
            # for simplex in self.simplices:
            #     self._set_values_single_simplex(simplex, self._get_values_for_simplex_tensor(simplex, values))
            self._values = values

        else:
            raise TypeError

        self._default_val = default_val

    def add_values_(
        self, values: Union[Sequence, Mapping, torch.Tensor], default_val: float = 0.0
    ):
        self.add_values(values, default_val)

        for simplex in self.simplices:
            simplex.add_values(
                self._get_values_for_single_simplex(simplex), self._default_val
            )

    def _get_simplex_for_point(self, point: torch.Tensor):
        for simplex in self.simplices:
            if simplex.contains_point_cartesian(point):
                return simplex

        return None

    def interpolate_cartesian(self, point: torch.Tensor, mode: str = "linear"):
        simplex = self._get_simplex_for_point(point)

        if simplex.values is None:
            simplex.add_values(
                self._get_values_for_single_simplex(simplex), self._default_val
            )

        return simplex.interpolate_cartesian(point, mode=mode)

    def interpolate_cartesian_multiple_points(
        self,
        points: torch.Tensor,
        mode: str = "linear",
        values: Optional[Union[Mapping, Sequence, torch.Tensor]] = None,
    ):
        if values is not None:
            self.add_values(values)
        return torch.stack(
            [self.interpolate_cartesian(point, mode=mode) for point in points]
        )


class _DelaunayInterface(DeviceDtypeModuleMixin):  # , metaclass=ABCMeta):
    vertex_coordinates: List[torch.Tensor]
    simplices: List[Simplex]
    ndim: int

    @torch.no_grad()
    def forward(
        self, points: torch.Tensor, finalize_inplace: bool = True, verbose: bool = False
    ) -> None:
        self.reset()
        from tqdm import tqdm

        if verbose:
            points = tqdm(points)
        for p in points:
            if p in self.vertex_coordinates:
                raise RuntimeError
            if verbose:
                points.set_postfix_str(str(p))
            p = p.to(torch.double)
            self.add_point(p)

        return self.finalize(inplace=finalize_inplace)

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def finalize(self, inplace: bool = True) -> Triangulation:
        raise NotImplementedError

    @abstractmethod
    def add_point(self, point: torch.Tensor):
        raise NotImplementedError


class _DelaunayTorch(_DelaunayInterface):
    """
    Class to compute a Delaunay triangulation in 2D + 3D
    ref: http://en.wikipedia.org/wiki/Bowyer-Watson_algorithm
    ref: http://www.geom.uiuc.edu/~samuelp/del_project.html
    """

    def __init__(self, dim: int, center=0, radius=9999):
        """Init and create a new frame to contain the triangulation
        center -- Optional position for the center of the frame. Default (0,0)
        radius -- Optional distance from corners to the center.
        """
        super().__init__()

        center = [center] * dim

        self.ndim = dim

        self.register_buffer(
            "_center", torch.tensor(center, device=self.device, dtype=self.dtype)
        )
        self.register_buffer(
            "_radius", torch.tensor(radius, device=self.device, dtype=self.dtype)
        )

        self.vertex_coordinates = None
        self.simplices = None
        self._num_super_simplices = 1
        self._reset()

    def _reset(self):

        self.simplices = []
        self.vertex_coordinates = []

        super_simplices = self._create_super_simplex()

        for simplex in super_simplices:
            self.simplices.append(simplex)
            for vertex in simplex.vertices:
                self.vertex_coordinates.append(vertex)

        self.to(torch.double)

    def reset(self):
        self.simplices = []
        self.vertex_coordinates = []

    def to(self, *args, **kwargs):
        for idx, v in enumerate(self.simplices):
            self.simplices[idx] = v.to(*args, **kwargs)

        for idx, v in enumerate(self.vertex_coordinates):
            self.vertex_coordinates[idx] = v.to(*args, **kwargs)

        if hasattr(self, "values"):
            for idx, v in enumerate(self.values):
                if v is not None:
                    self.values[idx] = v.to(*args, **kwargs)

        return super().to(*args, **kwargs)

    def _create_super_simplex(self):

        coords = [
            self._center
            + self._radius * torch.tensor(x, device=self.device, dtype=self.dtype)
            for x in sorted(
                set(itertools.product(*[[-1, 1] for _ in range(self.ndim)]))
            )
        ]

        for i in range(len(coords)):
            coords[i] = coords[i].double()

        if self.ndim == 2:
            return [
                Simplex(
                    torch.stack([coords[idx] for idx in [0, 1, 2]]),
                    torch.tensor([0, 1, 2], device=self.device, dtype=self.dtype),
                ),
                Simplex(
                    torch.stack([coords[idx] for idx in [1, 3, 2]]),
                    torch.tensor([1, 3, 2], device=self.device, dtype=self.dtype),
                ),
            ][: self._num_super_simplices]

        if self.ndim == 3:
            return [
                Simplex(
                    torch.stack([coords[idx] for idx in [0, 5, 3, 6]]),
                    torch.tensor([0, 1, 2, 3], device=self.device, dtype=self.dtype),
                )
            ][: self._num_super_simplices]

        else:
            raise NotImplementedError

    def add_point(self, p: torch.Tensor):
        # initial simplex creation to avoid super simplices
        if len(self.simplices) == 0:
            if len(self.vertex_coordinates) == 4:
                self.simplices.append(
                    Simplex(torch.stack(self.vertex_coordinates), torch.arange(4))
                )
            # return

        bad_simplices = []

        for simplex in self.simplices:
            if not isinstance(simplex, Simplex):
                raise AssertionError
            if simplex.point_in_circumcircle(p):
                bad_simplices.append(simplex)

        if len(bad_simplices) == 0:
            raise RuntimeError(f"Point {p[0]} not in any circumcircle")

        # check if linear dependency occurs for p with any edge
        # repeat until nothing is changed anymore
        changed = True
        while changed:
            changed = False
            for idx, simplex in enumerate(bad_simplices):
                for edge in simplex.edges:
                    pts = [self.vertex_coordinates[e.long()] for e in edge]
                    if (
                        torch.dot(
                            unit_vector(pts[0] - pts[1]),
                            torch.cross(
                                unit_vector(pts[0] - pts[2]), unit_vector(pts[0] - p)
                            ),
                        )
                        == 0
                    ):  # linear dependency of p and edge
                        # check if other simplex containing edge is in bad_simplices (= edge is shared)
                        is_shared = False
                        for other_simplex in (
                            bad_simplices[:idx] + bad_simplices[idx + 1 :]
                        ):
                            if other_simplex.contains_edge(edge):
                                is_shared = True
                                break

                        if (
                            not is_shared
                        ):  # other simplex is not in bad_simplices becuse of accuracy errors
                            changed = True
                            # check if p should be inside or outside the circumcircles
                            # by checking with the circumcircle of edge
                            center = pts[0] + (
                                torch.norm(pts[2] - pts[0]) ** 2
                                * torch.cross(
                                    torch.cross(pts[1] - pts[0], pts[2] - pts[0]),
                                    pts[1] - pts[0],
                                )
                                + torch.norm(pts[1] - pts[0]) ** 2
                                * torch.cross(
                                    torch.cross(pts[2] - pts[0], pts[1] - pts[0]),
                                    pts[2] - pts[0],
                                )
                            ) / (
                                2
                                * torch.norm(
                                    torch.cross(pts[1] - pts[0], pts[2] - pts[0])
                                )
                                ** 2
                            )
                            radius = torch.norm(center - pts[0])
                            if (
                                torch.norm(center - p) < radius
                            ):  # p is inside the circumcircle
                                bad_simplices.remove(simplex)
                                # search for other simplex containing edge
                                for other_simplex in self.simplices:
                                    if other_simplex.contains_edge(edge):
                                        bad_simplices.append(
                                            other_simplex
                                        )  # add both simplices to bad_simplices
                            else:  # p is outside the circumcircle
                                bad_simplices.remove(
                                    simplex
                                )  # delete simplex from bad_simplices
                            break
                if changed:
                    break

        # create polygon out of bad_simplices by just choosing the unshared edges
        polygon = []
        for idx, simplex in enumerate(bad_simplices):
            for edge in simplex.edges:

                is_shared = False
                for other_simplex in bad_simplices[:idx] + bad_simplices[idx + 1 :]:

                    if other_simplex.contains_edge(edge):
                        is_shared = True
                        break

                if not is_shared:
                    polygon.append(edge)

        for simplex in bad_simplices:
            self.simplices.remove(simplex)

        # create new simplex for each edge out of polygon together with p
        for edge in polygon:
            new_vertex_coords = torch.stack(
                [self.vertex_coordinates[e.long()] for e in edge] + [p.view(-1)]
            )
            new_vertex_indices = torch.cat(
                (
                    edge,
                    torch.tensor(
                        [len(self.vertex_coordinates)],
                        device=self.device,
                        dtype=self.dtype,
                    ),
                ),
                0,
            )

            self.simplices.append(Simplex(new_vertex_coords, new_vertex_indices))

        self.vertex_coordinates.append(p)

    def _finalize_triangulation(self, inplace=True):
        # remove super simplices and all simplices sharing an edge with it as well as
        # decreasing all indices by the number of the vertices of the super simplices

        # find indices of the vertices from the super simplices
        super_vertices = []
        for idx, v in enumerate(self.vertex_coordinates):
            if self._radius in torch.abs(v):
                super_vertices.append(idx)
            else:
                break  # vertices of super_simplex are the first vertices in vertex_coordinates

        # search for simplices containing min. one super vertex and remove them
        remove_simplices = []
        for simplex in self.simplices:
            for i in simplex.vertex_indices:
                if i in super_vertices:
                    remove_simplices.append(simplex)
                    break

        if inplace:
            all_simplices = self.simplices
        else:
            all_simplices = [
                Simplex(
                    vertex_coordinates=x.vertices.clone(),
                    vertex_indices=x.vertex_indices.clone(),
                    values=deepcopy(x.values)
                    if not isinstance(x.values, torch.Tensor)
                    else x.values.clone(),
                )
                for x in self.simplices
            ]
        for simplex in remove_simplices:
            all_simplices.remove(simplex)

        if inplace:
            self.vertex_coordinates = self.vertex_coordinates[len(super_vertices) :]

        # decrease the indices by the number of vertices of super simplices
        for simplex in all_simplices:
            simplex.vertex_indices -= len(super_vertices)
            simplex.edges -= len(super_vertices)

        return all_simplices

    def finalize(self, inplace: bool = True):
        simplices = self._finalize_triangulation(inplace=inplace)
        return Triangulation(simplices)


class _DelaunayScipy(_DelaunayInterface):
    def __init__(self, dim: int):
        super().__init__()
        self.ndim = dim
        self._scipy_delaunay: Optional[SPDelaunay] = None
        self._points_cache: Optional[List[np.ndarray]] = None

    def add_point(self, p: torch.Tensor):
        if self._scipy_delaunay is None:
            if self._points_cache is None:
                self._points_cache = [p.cpu().detach().numpy()]

            # need p.shape[-1]+1 points for one simplex and one more for triangulation
            if len(self._points_cache) >= p.shape[-1] + 2:
                self._scipy_delaunay = SPDelaunay(np.array(self._points_cache), incremental=True)
                self._points_cache = None
        else:
            self._scipy_delaunay.add_points(p.cpu().detach().numpy())

    @property
    def simplices(self) -> List[Simplex]:
        simplices = []
        if self._scipy_delaunay is None:
            return simplices

        for simplex in self._scipy_delaunay.simplices:
            simplices.append(
                Simplex(
                    torch.from_numpy(self._scipy_delaunay.points[simplex]),
                    torch.from_numpy(simplex),
                    values=None,
                ).to(self.device, self.dtype)
            )

        return simplices

    @property
    def vertex_coordinates(self) -> torch.Tensor:
        if self._scipy_delaunay is None:
            return []

        return list(
            torch.from_numpy(self._scipy_delaunay.points).to(self.device, self.dtype)
        )

    def finalize(self, *_, **__):

        return Triangulation(self.simplices)

    def reset(self):
        self._scipy_delaunay = None


class HybridDelaunay(_DelaunayInterface):
    def __init__(self, dim: int, center=0, radius=9999, default_backend: str = "scipy"):
        super().__init__()
        self._dim = dim
        self._center = center
        self._radius = radius

        self.delaunay_impl = None
        if default_backend == 'scipy':
            self.delaunay_impl = _DelaunayScipy(dim)
        elif default_backend == 'torch':
            self.delaunay_impl = _DelaunayTorch(dim)
        else:
            raise ValueError(f"Unknown backend {default_backend}")
        self.reset = self.qhull_watcher(self.reset)
        self.add_point = self.qhull_watcher(self.add_point)
        self.finalize = self.qhull_watcher(self.finalize)

    def _switch_backend(self):
        if isinstance(self.delaunay_impl, _DelaunayScipy):
            self._switch_to_torch_backend()
        elif isinstance(self.delaunay_impl, _DelaunayTorch):
            self._switch_to_scipy_backend()
        else:
            raise TypeError("Unknown backend")

    def _switch_to_torch_backend(self):

        # there already is another instance, so cache previous state
        if self.delaunay_impl is not None:
            if isinstance(self.delaunay_impl, _DelaunayScipy):
                # not yet triangulated points
                if self.delaunay_impl._scipy_delaunay is None and self.delaunay_impl._points_cache is not None:
                    points = torch.tensor(self.delaunay_impl._points_cache).to(self.device, self.dtype)
                else:
                    points = []

            simplices, vertex_coords = (
                        self.delaunay_impl.simplices,
                        self.delaunay_impl.vertex_coordinates,
                    )

        # setup new delaunay instance
        self.delaunay_impl = _DelaunayTorch(
                    self._dim, self._center, self._radius
                ).to(self.device, self.dtype)

        # add old state to new instance
        if self.delaunay_impl is not None:
            if self.delaunay_impl.simplices is None:
                self.delaunay_impl.simplices = []
            self.delaunay_impl.simplices.extend(simplices)

            if self.delaunay_impl.vertex_coordinates is None:
                self.delaunay_impl.vertex_coordinates = []
            self.delaunay_impl.vertex_coordinates.extend(vertex_coords)

            for p in points:
                self.delaunay_impl.add_point(p)
        

    def _switch_to_scipy_backend(self):

        # there already is another instance, so cache previous state
        if self.delaunay_impl is not None:
            vertex_coords = self.delaunay_impl.vertex_coordinates

        # cannot set simplices on qhull so only adding the points in order
        self.delaunay_impl = _DelaunayScipy(self._dim).to(self.device, self.dtype)

        # add old state to new instance
        if self.delaunay_impl is not None:
            for p in vertex_coords:
                self.add_point(p)

    @property
    def backend(self):
        if isinstance(self.delaunay_impl, _DelaunayScipy):
            return "scipy"
        elif isinstance(self.delaunay_impl, _DelaunayTorch):
            return "torch"

        raise TypeError("Unknown backend")

    @property
    def vertex_coordinates(self) -> List[torch.Tensor]:
        return self.delaunay_impl.vertex_coordinates

    @property
    def simplices(self) -> List[Simplex]:
        return self.delaunay_impl.simplices

    def reset(self) -> None:
        return self.delaunay_impl.reset()

    def add_point(self, point: torch.Tensor):
        return self.delaunay_impl.add_point(point)

    def finalize(self, *args, **kwargs) -> Triangulation:

        if isinstance(self.delaunay_impl, _DelaunayScipy):
            # To few points for scipy delaunay. Moving to custom torch delaunay
            if self.delaunay_impl._scipy_delaunay is None and self.delaunay_impl._points_cache is not None:
                self._switch_to_torch_backend()
        return self.delaunay_impl.finalize(*args, **kwargs)

    def qhull_watcher(self, func):
        @wraps(func)
        def new_fn(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except:
                self._switch_backend()
                return func(*args, **kwargs)

        return new_fn


def interpolate_normalized_point(
    point: torch.Tensor,
    displacement: torch.Tensor,
    initial_num_pts: int = 10,
    normalize_output: bool = False,
    default_delaunay_backend: bool = 'scipy'
):

    # zyx to xyz since displacement is in xyz
    point = torch.flip(point, (-1,))
    # calc distances
    distances = (
        (displacement - point.view(*([1] * (displacement.ndim - 1)), -1))
        .pow(2)
        .sum(-1)
        .sqrt()
    )
    reshaped_displacement = displacement.flatten(end_dim=-2)

    # sort them to use minimum distances
    reshaped_distances = (reshaped_displacement - point[None]).pow(2).sum(-1).sqrt()
    indices = reshaped_distances.argsort()

    delaunay = HybridDelaunay(point.size(-1), default_backend=default_delaunay_backend).to(point.device)

    index_iter = iter(indices.unbind())

    # add a certain number of points
    for _ in range(initial_num_pts):
        delaunay.add_point(reshaped_displacement[next(index_iter)])

    # add points as long as no triangle includes the current point
    while True:
        simplex = delaunay.finalize(inplace=False)._get_simplex_for_point(point)
        if simplex is None:
            delaunay.add_point(reshaped_displacement[next(index_iter)])
            continue
        elif isinstance(simplex, Simplex):
            break

    values = {}

    for idx, vert in enumerate(simplex.vertices):
        dist = (vert - point).pow(2).sum(-1).sqrt()
        # find indices of current vertex and use as value
        pot_indices = (distances == dist).nonzero()
        for indices in pot_indices.unbind():
            if torch.allclose(displacement[tuple(indices)], vert):
                values[idx] = indices[1:].to(delaunay.device, delaunay.dtype)
                break

    simplex.add_values(values)

    # do interpolation
    interpolated = simplex.interpolate_cartesian(point)

    # normalize if necessary
    if normalize_output:
        interpolated = normalize_points(
            interpolated,
            torch.tensor(
                displacement.shape[-(point.size(-1) + 1) : -1],
                device=interpolated.device,
                dtype=interpolated.dtype,
            ),
        )

    interpolated = interpolated.to(point)
    return interpolated

