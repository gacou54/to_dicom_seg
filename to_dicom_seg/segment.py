from dataclasses import dataclass
from typing import Dict

from .terminologies import find_code_values_from_snomed_ct


@dataclass
class Segment:
    label: str
    description: str
    algorithm_name: str
    algorithm_type: str

    property_category: str  # e.g. 'Anatomical Structure'
    property_type: str  # e.g. 'Lung'
    property_modifier: str  # e.g. 'Right'

    def to_dataset(self) -> Dict:
        category_code_value, type_code_value, modifier_code_value = find_code_values_from_snomed_ct(self.property_category, self.property_type, self.property_modifier)

        return {
            'labelID': self.label,
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
            'SegmentedPropertyTypeModifierCodeSequence': {
                'CodeValue': modifier_code_value,
                'CodingSchemeDesignator': 'SCT',
                'CodeMeaning': self.property_modifier
            }
        }
