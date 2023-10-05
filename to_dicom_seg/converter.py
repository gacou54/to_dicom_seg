import os
from dataclasses import dataclass
from typing import List

import SimpleITK as sitk
import cc3d
import numpy
import pydicom
import pydicom_seg

from .template import make_template
from .segment import Segment


@dataclass
class Algorithm:
    name: str
    type_: str


@dataclass
class Property:
    category: str
    type_: str
    modifier: str = None


def generate_segments(segmentation: sitk.Image, algorithm: Algorithm, property_: Property):
    raise NotImplementedError


def nifti_to_dicom_seg(nifti_path: str,
                       ref_ct_directory_path: str,
                       creator_name: str,
                       body_part_examined: str,
                       segments: List[Segment],
                       algorithm: Algorithm,
                       property_: Property,
                       description: str = 'Segmentation') -> pydicom.FileDataset:
    segmentation = sitk.Cast(
        image=sitk.ReadImage(nifti_path),
        pixelID=sitk.sitkUInt16
    )
    cts = [pydicom.dcmread(os.path.join(ref_ct_directory_path, i)) for i in os.listdir(ref_ct_directory_path)]
    segmentation, number_of_segments = calculate_connected_components(segmentation)

    segments = generate_segments(segmentation, algorithm, property_, number_of_segments)

    template = make_template(
        creator_name,
        description,
        body_part_examined,
        segments
    )

    writer = pydicom_seg.MultiClassWriter(template)
    ds_seg = writer.write(segmentation, cts)

    return ds_seg


def calculate_connected_components(segmentation: sitk.Image, connectivity: int = 18) -> Tuple[sitk.Image, int]:
    segmentation_array = sitk.GetArrayFromImage(segmentation)

    new_segmentation_array = cc3d.connected_components(segmentation_array, connectivity=connectivity)
    number_of_segments = int(numpy.max(new_segmentation_array))

    new_segmentation = sitk.GetImageFromArray(new_segmentation_array)
    new_segmentation.CopyInformation(segmentation)

    return new_segmentation, number_of_segments
