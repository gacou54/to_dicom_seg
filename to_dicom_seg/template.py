import json
import os
from dataclasses import dataclass
from typing import List

import pydicom
import pydicom_seg
import SimpleITK as sitk

from dicom_converter.nifti_to_dicom import nifti_seg_to_dicom


DATA = './tests/data'
NIFTI_FILEPATH = os.path.join(DATA, 'seg_nifti/Segmentation_2.nii')
REF_CT_PATH = os.path.join(DATA, 'ct')



@dataclass
class Segment:
    label: str
    description: str
    algorithm_name: str
    algorithm_type: str

    def to_dataset(self) -> pydicom.Dataset:
        ds = pydicom.Dataset()
        ds.SegmentNumber = 1
        ds.SegmentDescription = self.description
        ds.AlgorithmType = self.algorithm_type
        ds.AlgorithmName = self.algorithm_name

        segmented_property_category_code_sequence = pydicom.Dataset()
        segmented_property_category_code_sequence.CodeValue = ''
        ds.SegmentPropertyCategoryCodeSequence = pydicom.Sequence([

        ])
        # TODO: add elements to Segment dataset

        return ds


def make_template(content_creator_name: str,
                  description: str,
                  body_part_examined: str,
                  segments: List[Segment]) -> pydicom.Dataset:
    with open('tests/segmentation_metadata.json') as file:
        metadata = json.load(file)

    # Adapt the metadata
    metadata['SeriesDescription'] = description
    metadata['SeriesDescription'] = description
    metadata['BodyPartExamined'] = body_part_examined


    [
        {
            "labelID": 1,
            "SegmentDescription": "SegmentDescription",
            "SegmentAlgorithmType": "SEMIAUTOMATIC",
            "SegmentAlgorithmName": "TheAlgorithm",
            "SegmentedPropertyCategoryCodeSequence": {
                "CodeValue": "123037004",
                "CodingSchemeDesignator": "SCT",
                "CodeMeaning": "Anatomical Structure"
            },
            "SegmentedPropertyTypeCodeSequence": {
                "CodeValue": "39607008",
                "CodingSchemeDesignator": "SCT",
                "CodeMeaning": "Lung"
            },
            "SegmentedPropertyTypeModifierCodeSequence": {
                "CodeValue": "24028007",
                "CodingSchemeDesignator": "SCT",
                "CodeMeaning": "Right"
            }
        }
    ]

    template = pydicom_seg.template.from_dcmqi_metainfo(metadata)

    return template

    template = pydicom.Dataset()

    # Common DICOM metadata
    template.ContentCreatorName = content_creator_name
    template.ClinicalTrialSeriesID = 'ClinicalTrialSeries'  # TODO: what do we put here?
    template.ClinicalTrialTimePointID = '1'
    template.ClinicalTrialCoordinatingCenter = 'TODO'  # TODO: What to put here?
    template.SeriesDescription = description
    template.SeriesNumber = '300'  # TODO: What to put here?
    template.InstanceNumber = '1'
    template.BodyPartExamined = body_part_examined

    template.SegmentSequence = pydicom.Sequence(
        [seg.to_dataset() for seg in segments]
    )

    return template

