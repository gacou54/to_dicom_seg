from dataclasses import dataclass
from typing import Dict

from .terminologies import find_code_values_from_snomed_ct


@dataclass
class Segment:
    label_id: int
    description: str
    algorithm_name: str
    algorithm_type: str

    property_category: str  # e.g. 'Anatomical Structure'
    property_type: str  # e.g. 'Lung'
    property_modifier: str = None  # e.g. 'Right'

    def to_dataset(self) -> Dict:
        category_code_value, type_code_value, modifier_code_value = find_code_values_from_snomed_ct(self.property_category, self.property_type, self.property_modifier)

        segment_dataset = {
            'labelID': self.label_id,
            'SegmentDescription': self.description,
            'SegmentAlgorithmType': self.algorithm_type,
            'SegmentAlgorithmName': self.algorithm_name,
            'SegmentedPropertyCategoryCodeSequence': {
                'CodeValue': category_code_value,
                'CodingSchemeDesignator': 'SCT',
                'CodeMeaning': self.property_category
            },
            'SegmentedPropertyTypeCodeSequence': {
                'CodeValue': type_code_value,
                'CodingSchemeDesignator': 'SCT',
                'CodeMeaning': self.property_type
            },
        }

        if self.property_modifier is not None:
            segment_dataset['SegmentedPropertyTypeModifierCodeSequence'] = {
                'CodeValue': modifier_code_value,
                'CodingSchemeDesignator': 'SCT',
                'CodeMeaning': self.property_modifier
            }

        return segment_dataset
