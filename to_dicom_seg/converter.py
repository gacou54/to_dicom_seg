import SimpleITK as sitk

segmentation = sitk.Cast(
    image=sitk.ReadImage(NIFTI_FILEPATH),
    pixelID=sitk.sitkUInt16
)
cts = [pydicom.dcmread(os.path.join(REF_CT_PATH, i)) for i in os.listdir(REF_CT_PATH)]


# TODO generate the template automatically
template = pydicom_seg.template.from_dcmqi_metainfo('tests/segmentation_metadata.json')

# New way to generate templates
segmentations = [Segment('label', 'descr', 'algo_name', 'AUTOMATIC')]
template_1 = make_template('COUTURE^Gabriel', 'my_desc', 'lung', segmentations)

writer = pydicom_seg.MultiClassWriter(template)
ds_seg = writer.write(segmentation, cts)


