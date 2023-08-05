quality_folder = '/Users/songweizhi/Desktop/bin_quality_folder'

for each_uc in open('/Users/songweizhi/Desktop/32_unclassified.tsv'):
    #print(each_uc)
    mag_id = each_uc.split('\t')[0]
    #print(mag_id)
    report_str = each_uc.split('\t')[1].strip()
    #print(report_str)
    sample_id = mag_id.split('_Refined_')[0]
    mag_id_no_sample_id = 'Refined_' + mag_id.split('_Refined_')[1].strip()
    #print(mag_id_no_sample_id)

    pwd_quality_file = '%s/%s_Refined_qualified.txt' % (quality_folder, sample_id)

    mag_quality_str = ''
    for each_qual in open(pwd_quality_file):
        each_qual_split = each_qual.strip().split('\t')
        bin_id = each_qual.split('\t')[0]
        if bin_id == mag_id_no_sample_id:
            mag_quality_str = '%s\t%s' % (each_qual_split[3], each_qual_split[4])
    #print(mag_quality_str)



    print('%s\t%s' % (each_uc.strip(), mag_quality_str))