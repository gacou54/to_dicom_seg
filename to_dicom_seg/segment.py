import json
import os
from dataclasses import dataclass
from typing import List

import pydicom
import pydicom_seg
import SimpleITK as sitk

from dicom_converter.nifti_to_dicom import nifti_seg_to_dicom



