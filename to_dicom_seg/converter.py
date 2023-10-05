import os

import SimpleITK as sitk
import cc3d
import pydicom
import pydicom_seg

from .template import make_template
from .segment import Segment


def nifti_to_dicom_seg(nifti_path: str, ref_ct_directory_path: str) -> pydicom.FileDataset:
    segmentation = sitk.Cast(
        image=sitk.ReadImage(nifti_path),
        pixelID=sitk.sitkUInt16
    )
    cts = [pydicom.dcmread(os.path.join(ref_ct_directory_path, i)) for i in os.listdir(ref_ct_directory_path)]
    segmentation = calculate_connected_components(segmentation)

    # New way to generate templates
    segments = [
        Segment(
            label=1,
            description='This is a nodule',
            algorithm_name='MySuperAlgorithm',
            algorithm_type='AUTOMATIC',
            property_category='Anatomical Structure',
            property_type='Lung',
            property_modifier='Right'
        )
    ]
    template = make_template(
        'COUTURE^Gabriel',
        'my_desc',
        'lung',
        segments
    )

    writer = pydicom_seg.MultiClassWriter(template)
    ds_seg = writer.write(segmentation, cts)

    return ds_seg


def calculate_connected_components(segmentation: sitk.Image, connectivity: int = 18) -> sitk.Image:
    segmentation_array = sitk.GetArrayFromImage(segmentation)

    new_segmentation_array = cc3d.connected_components(segmentation_array, connectivity=connectivity)

    new_segmentation = sitk.GetImageFromArray(new_segmentation_array)
    new_segmentation.CopyInformation(segmentation)

    return new_segmentation
