import argparse
import json
import sys
from typing import Optional

import pydicom

from to_dicom_seg.converter import Algorithm, Property, nifti_to_dicom_seg


def _read_property(property_as_str: str) -> Property:
    property_dict = json.loads(property_as_str.replace("\'", '\"'))
    try:
        return Property(
            category=property_dict['category'],
            type_=property_dict['type'],
            modifier=property_dict['modifier'],

        )
    except KeyError as e:
        sys.exit(f'Error: "{e}" missing from {property_dict}')


def _read_algorithm(algorithm_as_str: str) -> Algorithm:
    algorithm_dict = json.loads(algorithm_as_str.replace("\'", '\"'))
    try:
        return Algorithm(
            name=algorithm_dict['name'],
            type_=algorithm_dict['type']
        )
    except KeyError as e:
        sys.exit(f'Error: "{e}" missing from {algorithm_dict}')


def _write_dicom_dataset(output_path: Optional[str], ds: pydicom.FileDataset) -> None:
    if output_path is None:
        output_path = 'seg.dcm'

    pydicom.dcmwrite(output_path, ds)


def main():
    parser = argparse.ArgumentParser(description='Convert nifti segmentation file to a DICOM SEG file.')
    parser.add_argument('-i', '--nifti-path', help='Nifti segmentation filepath', required=True)
    parser.add_argument('-ct', '--ct-dicom-directory-path', help='Path to a directory of the CT reference DICOM files', required=True)
    parser.add_argument('-o', '--output', help='Output path for the DICOM (e.g. `seg.dcm`)', required=False)
    parser.add_argument('-p', '--property', help="Property definition about the segmented object (e.g. \"{'category': 'Anatomical Structure', 'type': 'Lung', 'modifier': 'Right'}\")", required=True)
    parser.add_argument('-a', '--algorithm', help="Algorithm information that generated the segmentation (e.g. \"{'name': 'my-algo', 'type': 'AUTOMATIC'}\")", required=True)
    parser.add_argument('-bpe', '--body-part-examined', help="Name of the examined body part (e.g. 'Thorax')", required=True)
    parser.add_argument('-ccn', '--content-creator-name', help="Content creator name in the DICOM format (e.g. 'COUTURE^Gabriel')", required=True)

    args = parser.parse_args()

    property_ = _read_property(args.property)
    algorithm = _read_algorithm(args.algorithm)

    ds = nifti_to_dicom_seg(
        nifti_path=args.nifti_path,
        ref_ct_directory_path=args.ct_dicom_directory_path,
        creator_name=args.content_creator_name,
        body_part_examined=args.body_part_examined,
        algorithm=algorithm,
        property_=property_
    )

    _write_dicom_dataset(args.output, ds)

if __name__ == '__main__':
    main()
