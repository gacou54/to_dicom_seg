from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Tuple

TERMINOLOGIES_PATH = Path(__file__).parent / 'terminologies'
SEGMENTATION_TERMINOLOGIES = TERMINOLOGIES_PATH / 'SegmentationCategoryTypeModifier.xml'

_root = ET.parse(SEGMENTATION_TERMINOLOGIES).getroot()


def find_code_values_from_snomed_ct(
        category_code_meaning: str,
        type_code_meaning: str,
        modifier_code_meaning: str) -> Tuple[str, str, str]:
    """Find the codes values of the category, type and modifier code meaning.

    Args:
        category_code_meaning:
        type_code_meaning:
        modifier_code_meaning:

    Returns:
        Tuple['Category CodeValue', 'Type CodeValue', 'Modifier CodeValue']
    """
    category_code_value, type_code_value, modifier_code_value = None, None, None

    # Search in categories
    for category_tag in _root.findall('Category'):
        # We only want the SNOMED CT terminologies
        if category_tag.get('codingScheme') != 'SCT':
            continue

        if category_tag.get('codeMeaning') == category_code_meaning:
            category_code_value = category_tag.get('codeValue')

            for type_tag in category_tag.findall('Type'):
                if type_tag.get('codeMeaning') == type_code_meaning:
                    type_code_value = type_tag.get('codeValue')

                    for modifier_tag in type_tag.findall('Modifier'):
                        if modifier_tag.get('codeMeaning') == modifier_code_meaning:
                            modifier_code_value = modifier_tag.get('codeValue')

    if category_code_value and type_code_value and modifier_code_value:
        return category_code_value, type_code_value, modifier_code_value

    raise ValueError(
        'At least one of the code meanings has not been found. '
        f'category_code_meaning: "{category_code_meaning}", '
        f'type_code_meaning: "{type_code_meaning}", '
        f'modifier_code_meaning: "{modifier_code_meaning}"'
    )
