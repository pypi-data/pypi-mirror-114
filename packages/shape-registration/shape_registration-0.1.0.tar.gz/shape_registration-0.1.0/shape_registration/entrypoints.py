import argparse
import os
from typing import Callable
import SimpleITK as sitk
import torch
from shape_registration.register import (transfer_points_on_segmentations as _transfer_points, 
                                         register_affine as _register_affine, 
                                         register_diffeomorphic as _register_diffeomorphic)


def _load_mask(path: str, binarize: bool = True) -> torch.Tensor:
    if os.path.isdir(path):
        # read dicom series
        reader = sitk.ImageSeriesReader()
        reader.SetFiles(reader.GetGDCMSeriesFileNames(path))
        img = reader.Execute()

    else:
        img = sitk.ReadImage(path)

    img_npy = sitk.GetArrayFromImage(img)

    if binarize:
        img_npy = (img_npy > 0).astype(img_npy.dtype)

    img_torch = torch.from_numpy(img_npy).squeeze()[None].float()
    return img_torch

def _add_parser_args_and_parse(parser: argparse.ArgumentParser):
    parser.add_argument('--input_path_source', type=str, help='Path to the source image')
    parser.add_argument('--input_path_target', type=str, help='Path to the target image')
    parser.add_argument('--no_binarization', action='store_true', help='disable binarization of masks')
    parser.add_argument('--trafo_out_path', type=str, help='Path where the transformation should be stored')
    parser.add_argument('--result_out_path', type=str, default=None, help='Path where the transformed image should be saved')
    parser.add_argument('--disable_gpus', action='store_true', help='disable gpu usage (if available)')
    parser.add_argument('--verbose', action='store_true', help='Enables more verbose outputs')
    return parser.parse_args()

def _optionally_save_transformed_image(args, trafo, source_image):
    
    if args.image_out_path is not None:
        sitk.WriteImage(sitk.GetImageFromArray(trafo(source_image).squeeze().cpu().detach().numpy()), args.result_out_path)

def __registration(reg_fn: Callable, **kwargs):
    parser = argparse.ArgumentParser()

    args = _add_parser_args_and_parse(parser)

    source_image = _load_mask(args.input_path_source, binarize=not args.no_binarization)
    target_image = _load_mask(args.input_path_target, binarize=not args.no_binarization)

    trafo = reg_fn(source_image=source_image, target_image=target_image, gpus=0 if args.disable_gpus else None, **kwargs)

    torch.save(trafo.state_dict(), args.trafo_out_path)
    _optionally_save_transformed_image(args, trafo, source_image)

def register_affine():
    __registration(_register_affine)

def register_diffeomorphic():
    __registration(_register_diffeomorphic)

def transfer_points():
    parser = argparse.ArgumentParser()
  
    parser.add_argument('--input_path_source', type=str, help='Path to the source image')
    parser.add_argument('--input_path_target', type=str, help='Path to the target image')
    parser.add_argument('--source_points', type=str, help='Path to the source points file (json)')
    parser.add_argument('--target_points', type=str, help='Path where to store the target points file (json)')
    parser.add_argument('--no_binarization', action='store_true', help='disable binarization of masks')
    parser.add_argument('--trafo_out_path', type=str, default=None, help='Path where the transformation should be stored')
    parser.add_argument('--disable_gpus', action='store_true', help='disable gpu usage (if available)')
    parser.add_argument('--verbose', action='store_true', help='Enables more verbose outputs')
    parser.add_argument('--disable_preregistration', action='store_true', help='Disables Preregistration')
    parser.add_argument('--disable_cropping', action='store_true', help='Disables cropping of mask to segmentation areas (can cause collapse of registration)')
    parser.add_argument('--crop_proportion', type=float, default=0.1, help='The proportion for boundary cropping')
    parser.add_argument('--contour_snap', action='store_true', help='Whether to snap the resulting points to the contour of the target mask')
    
    args = parser.parse_args()
    
    source_mask = _load_mask(args.input_path_source, binarize=not args.no_binarization)
    target_mask - _load_mask(args.input_path_target, binarize=not args.no_binarization)
    
    with open(args.source_points, 'r') as f:
        source_points = torch.tensor(json.load(f))
    
    result = _transfer_points(
        source_points=source_points, 
        source_image=source_mask,
        target_image=target_mask,
        include_preregistration=not args.disable_preregistration,
        crop_to_segmentation=not args.disable_cropping,
        crop_boundary_proportion=args.crop_proportion,
        contour_snap=args.contour_snap,
        verbose=args.verbose,
        gpus=0 if args.disable_gpus else None,
        return_trafo=args.trafo_out_path is not None
    )
    
    if args.trafo_out_path is not None:
        torch.save(result[1].state_dict(), args.trafo_out_path)
        result_points = result[0]
    else:
        result_points = result
        
    with open(args.target_points, 'w') as f:
        json.dump(result_points.tolist(), f)
    
