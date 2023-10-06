import os

import pydicom
from pydicom.uid import generate_uid
import getopt
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
    opts, args = getopt.getopt(argv,"is:ict:o:pr:pt:pm:an:at:bpe:ccn:",
                               ["ifile=","ofile="]) # need to change
    for opt, arg in opts:
      if opt in ("-is", "--is"):
         inputsegfile = arg
      elif opt in ("-ict", "--ict"):
         inputctpath = arg
      elif opt in ("-o", "--ofile"):
         outputpath = arg
      elif opt in ("-pr", "--propertycategory"):
         property.category = arg
      elif opt in ("-pt", "--propertytype"):
         property.type_ = arg
      elif opt in ("-pm", "--propertymodifier"):
         property.modifier = arg
      elif opt in ("-an", "--algorithmname"):
         algorithm.name = arg
      elif opt in ("-at", "--algorithmtype"):
         algorithm.type_ = arg
      elif opt in ("-bpe", "--bodypartexamined"):
         body_part_examined = arg
      elif opt in ("-ccn", "--contentcreatorname"):
         content_creator_name = arg

    NIFTI_FILEPATH = inputsegfile  # This is the segmentation nifti file
    REF_CT_PATH = inputctpath  # This is a CT directory with DICOM CT

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