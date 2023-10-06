import os

import pydicom
from pydicom.uid import generate_uid
import argparse
import sys

from to_dicom_seg.converter import nifti_to_dicom_seg
from to_dicom_seg.segment import Segment
from to_dicom_seg.converter import Property, Algorithm


def main(argv):
    property = Property(category='', type_='', modifier='')
    algorithm = Algorithm(name='', type_='')


    body_part_examined = ''
    content_creator_name = ''

    inputsegfile = ''
    inputctpath = ''
    outputpath = ''

    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-is', '--is', help='Description', required=True)
    parser.add_argument('-ict', '--ict', help='Description', required=True)
    parser.add_argument('-o', '--output', help='Description', required=True)
    parser.add_argument('-pt', '--pt', help='Description', required=True)
    parser.add_argument('-pc', '--pc', help='Description', required=True)
    parser.add_argument('-pm', '--pm', help='Description', required=False)
    parser.add_argument('-an', '--an', help='Description', required=True)
    parser.add_argument('-at', '--at', help='Description', required=True)
    parser.add_argument('-bpe', '--bpe', help='Description', required=False)
    parser.add_argument('-ccn', '--ccn', help='Description', required=False)
    args = vars(parser.parse_args())

    property = Property(category=args['pc'], type_=args['pt'], modifier=args['pm'])
    algorithm = Algorithm(name=args['an'], type_=args['at'])

    NIFTI_FILEPATH = args['is']  # This is the segmentation nifti file
    REF_CT_PATH = args['ict']  # This is a CT directory with DICOM CT
    outputpath = args['output']

    # Create the DICOM Segmentation
    ds = nifti_to_dicom_seg(NIFTI_FILEPATH, REF_CT_PATH,
                            content_creator_name, body_part_examined,
                            algorithm, property)

    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()

    # Writing the DICOM Segmentation file
    os.makedirs('results', exist_ok=True)
    pydicom.dcmwrite(f'{outputpath}/seg.dcm', ds)

if __name__ == "__main__":
   main(sys.argv[1:])