import os

import pydicom

from to_dicom_seg.converter import nifti_to_dicom_seg
from to_dicom_seg.segment import Segment

DATA = './data'
NIFTI_FILEPATH = os.path.join(DATA, 'seg.nii.gz')  # This is the segmentation nifti file
REF_CT_PATH = os.path.join(DATA, 'CT')  # This is a CT directory with DICOM CT

# Segments have to be defined by hand (since this data is not in the nifti)
segments = [
    Segment(
        label_id=1,
        description='Nodule',
        algorithm_name='MySuperAlgorithm',
        algorithm_type='AUTOMATIC',
        property_category='Anatomical Structure',
        property_type='Lung',
        property_modifier='Right'
    ),
    Segment(
        label_id=2,
        description='Nodule2',
        algorithm_name='MySuperAlgorithm',
        algorithm_type='AUTOMATIC',
        property_category='Anatomical Structure',
        property_type='Lung',
        property_modifier='Right'
    )
]

# Create the DICOM Segmentation
ds = nifti_to_dicom_seg(NIFTI_FILEPATH, REF_CT_PATH, segments)

# Writing the DICOM Segmentation file
os.makedirs('results', exist_ok=True)
pydicom.dcmwrite('results/seg.dcm', ds)
