import os

import pydicom

from to_dicom_seg.converter import nifti_to_dicom_seg
from to_dicom_seg.segment import Segment

DATA = './data'
NIFTI_FILEPATH = os.path.join(DATA, 'seg.nii.gz')
REF_CT_PATH = os.path.join(DATA, 'CT')

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

ds = nifti_to_dicom_seg(NIFTI_FILEPATH, REF_CT_PATH, segments)

pydicom.dcmwrite('result/seg.dcm', ds)
