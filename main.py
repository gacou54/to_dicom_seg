import os

import pydicom

from to_dicom_seg.converter import nifti_to_dicom_seg

DATA = './data'
NIFTI_FILEPATH = os.path.join(DATA, 'seg_nifti/Segmentation_2.nii')
REF_CT_PATH = os.path.join(DATA, 'ct')

ds = nifti_to_dicom_seg(NIFTI_FILEPATH, REF_CT_PATH)

pydicom.dcmwrite('seg.dcm', ds)
