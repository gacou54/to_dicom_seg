import json
from pathlib import Path
from typing import List

import pydicom
import pydicom_seg

from .segment import Segment

TEMPLATES_PATH = Path(__file__).parent / 'templates'
SEGMENTATION_METADATA_TEMPLATE_PATH = TEMPLATES_PATH / 'segmentation_metadata.json'


def make_template(creator_name: str,
                  description: str,
                  body_part_examined: str,
                  segments: List[Segment],
                  segmentation_metadata_template: str = SEGMENTATION_METADATA_TEMPLATE_PATH) -> pydicom.Dataset:
    with open(segmentation_metadata_template) as file:
        metadata = json.load(file)

    # Adapt the metadata
    metadata['ContentCreatorName'] = creator_name
    metadata['SeriesDescription'] = description
    metadata['BodyPartExamined'] = body_part_examined
    metadata['SeriesNumber'] = ''  # TODO: how do we handle this
                                   # (i.e. how do we generate the SeriesNumber to ensure
                                   # it will always be different from the other)

    metadata['segmentAttributes'] = [[seg.to_dataset() for seg in segments]]

    template = pydicom_seg.template.from_dcmqi_metainfo(metadata)

    return template
