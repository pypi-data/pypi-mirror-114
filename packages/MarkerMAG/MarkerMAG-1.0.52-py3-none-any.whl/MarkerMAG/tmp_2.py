import time
from Bio import SeqIO


def cigar_splitter(cigar):

    # get the position of letters
    letter_pos_list = []
    n = 0
    for each_element in cigar:
        if (each_element.isalpha() is True) or (each_element == '='):
            letter_pos_list.append(n)
        n += 1

    # split cigar
    index = 0
    cigar_splitted = []
    while index <= len(letter_pos_list) - 1:
        if index == 0:
            cigar_splitted.append(cigar[:(letter_pos_list[index] + 1)])
        else:
            cigar_splitted.append(cigar[(letter_pos_list[index - 1] + 1):(letter_pos_list[index] + 1)])
        index += 1

    return cigar_splitted


def get_cigar_stats(cigar_splitted):

    # aligned_len: M I X =
    # clipping_len: S
    # mismatch_len: X I D
    # mismatch_pct = mismatch_len / aligned_len
    # aligned_pct  = aligned_len  / (aligned_len + clipping_len)
    # clipping_pct = clipping_len / (aligned_len + clipping_len)

    aligned_len = 0
    clipping_len = 0
    mismatch_len = 0
    for each_part in cigar_splitted:
        each_part_len = int(each_part[:-1])
        each_part_cate = each_part[-1]

        # get aligned_len
        if each_part_cate in {'M', 'm', 'I', 'i', 'X', 'x', '='}:
            aligned_len += each_part_len

        # get clipping_len
        if each_part_cate in ['S', 's']:
            clipping_len += each_part_len

        # get mismatch_len
        if each_part_cate in {'I', 'i', 'X', 'x', 'D', 'd'}:
            mismatch_len += each_part_len

    aligned_pct  = float("{0:.2f}".format(aligned_len * 100 / (aligned_len + clipping_len)))
    clipping_pct = float("{0:.2f}".format(clipping_len * 100 / (aligned_len + clipping_len)))
    mismatch_pct = float("{0:.2f}".format(mismatch_len * 100 / (aligned_len)))

    return aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct


def get_min_mismatch_from_cigar_list(r1_ref_cigar_set, min_M_len):

    mismatch_set_all_cigar = set()
    mismatch_set_long_M_cigars = set()
    for each_cigar in r1_ref_cigar_set:
        aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_splitter(each_cigar))
        mismatch_set_all_cigar.add(mismatch_pct)
        if aligned_len >= min_M_len:
            mismatch_set_long_M_cigars.add(mismatch_pct)

    min_mismatch = 'NA'
    if len(mismatch_set_all_cigar) > 0:
        min_mismatch = min(mismatch_set_all_cigar)
        if len(mismatch_set_long_M_cigars) > 0:
            min_mismatch = min(mismatch_set_long_M_cigars)

    return min_mismatch


def check_both_ends_clipping(cigar_splitted):

    both_ends_clipping = False
    if len(cigar_splitted) >= 3:
        if (cigar_splitted[0][-1] in ['S', 's']) and (cigar_splitted[-1][-1] in ['S', 's']):
            both_ends_clipping = True

    return both_ends_clipping


def get_unlinked_mag_end_seq(ref_in, ref_in_end_seq, end_seq_len, ctg_ignore_region_dict_rd1):
    ctg_ignore_region_dict_rd2 = dict()

    # get ref seqs subset
    ref_subset_handle = open(ref_in_end_seq, 'w')
    for ref_seq in SeqIO.parse(ref_in, 'fasta'):

        ref_seq_id = ref_seq.id
        ref_seq_len = len(ref_seq.seq)

        if ref_seq_len < end_seq_len * 2:
            ref_subset_handle.write('>%s\n' % ref_seq_id)
            ref_subset_handle.write('%s\n' % ref_seq.seq)

            # add to ctg_ignore_region_dict_rd2
            if ref_seq_id in ctg_ignore_region_dict_rd1:
                ctg_ignore_region_dict_rd2[ref_seq_id] = ctg_ignore_region_dict_rd1[ref_seq_id]
        else:
            ref_seq_left_end_id = '%s_l' % ref_seq_id
            ref_seq_right_end_id = '%s_r' % ref_seq_id
            ref_seq_left_end = ref_seq.seq[:end_seq_len]
            ref_seq_right_end = ref_seq.seq[-end_seq_len:]

            # write out left end
            ref_subset_handle.write('>%s\n' % ref_seq_left_end_id)
            ref_subset_handle.write('%s\n' % ref_seq_left_end)

            # write out right end
            ref_subset_handle.write('>%s\n' % ref_seq_right_end_id)
            ref_subset_handle.write('%s\n' % ref_seq_right_end)

            # add to ctg_ignore_region_dict_rd2
            if ref_seq_id in ctg_ignore_region_dict_rd1:
                current_seq_to_ignore_ends = ctg_ignore_region_dict_rd1[ref_seq_id]
                for end_to_ignore in current_seq_to_ignore_ends:
                    if end_to_ignore == 'left_end':
                        ctg_ignore_region_dict_rd2[ref_seq_left_end_id] = {'left_end'}
                    if end_to_ignore == 'right_end':
                        ctg_ignore_region_dict_rd2[ref_seq_right_end_id] = {'right_end'}
    ref_subset_handle.close()

    return ctg_ignore_region_dict_rd2


def parse_rd2_sam_gnm_worker(arguments_list):

    rd1_unlinked_mags_sam_bowtie_reformat_sorted = arguments_list[0]
    free_living_ctg_ref_file                     = arguments_list[1]
    min_M_len_ctg                                = arguments_list[2]
    mismatch_cutoff                              = arguments_list[3]
    round_2_ctg_end_seq_len_dict                 = arguments_list[4]
    rd2_with_both_mates                          = arguments_list[5]
    ctg_ignore_region_dict_2rd                   = arguments_list[6]

    free_living_ctg_ref_file_handle = open(free_living_ctg_ref_file, 'w')
    current_read_base = ''
    current_read_base_r1_ctg_ref_dict_rd2 = dict()
    current_read_base_r2_ctg_ref_dict_rd2 = dict()
    with open(rd1_unlinked_mags_sam_bowtie_reformat_sorted) as rd1_unlinked_mags_sam_bowtie_reformat_sorted_opened:
        for each_line in rd1_unlinked_mags_sam_bowtie_reformat_sorted_opened:
            if not each_line.startswith('@'):
                each_line_split = each_line.strip().split('\t')
                cigar = each_line_split[5]
                read_id = each_line_split[0]
                read_id_base = '.'.join(read_id.split('.')[:-1])
                read_strand = read_id.split('.')[-1]
                ref_id = each_line_split[2]
                ref_pos = int(each_line_split[3])

                if current_read_base == '':
                    current_read_base = read_id_base

                    if cigar != '*':
                        if read_strand == '1':
                            current_read_base_r1_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r2_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}

                elif read_id_base == current_read_base:

                    if cigar != '*':
                        if read_strand == '1':
                            if ref_id not in current_read_base_r1_ctg_ref_dict_rd2:
                                current_read_base_r1_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r1_ctg_ref_dict_rd2[ref_id][ref_pos] = cigar
                        if read_strand == '2':
                            if ref_id not in current_read_base_r2_ctg_ref_dict_rd2:
                                current_read_base_r2_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r2_ctg_ref_dict_rd2[ref_id][ref_pos] = cigar
                else:
                    ################################### analysis previous read refs ####################################

                    ctg_refs_to_ignore_rd2 = set()

                    ########## get lowest mismatch for r1/r2 ctg refs ##########

                    # get r1_ref_cigar_set
                    r1_ref_cigar_set = set()
                    for each_pos_dict in current_read_base_r1_ctg_ref_dict_rd2.values():
                        each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                        r1_ref_cigar_set.update(each_pos_dict_values)

                    # get r2_ref_cigar_set
                    r2_ref_cigar_set = set()
                    for each_pos_dict in current_read_base_r2_ctg_ref_dict_rd2.values():
                        each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                        r2_ref_cigar_set.update(each_pos_dict_values)

                    r1_ref_min_mismatch = get_min_mismatch_from_cigar_list(r1_ref_cigar_set, min_M_len_ctg)
                    r2_ref_min_mismatch = get_min_mismatch_from_cigar_list(r2_ref_cigar_set, min_M_len_ctg)

                    ########## filter r1 ctg refs ##########
                    r1_ctg_refs_passed_qc = {}
                    for r1_ctg_ref_rd2 in current_read_base_r1_ctg_ref_dict_rd2:
                        r1_matched_pos_dict = current_read_base_r1_ctg_ref_dict_rd2[r1_ctg_ref_rd2]
                        if len(r1_matched_pos_dict) > 1:
                            ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                        else:
                            r1_ctg_ref_pos = list(r1_matched_pos_dict.keys())[0]
                            r1_ctg_ref_cigar = r1_matched_pos_dict[r1_ctg_ref_pos]
                            r1_ctg_ref_cigar_splitted = cigar_splitter(r1_ctg_ref_cigar)

                            # check both end clip
                            both_end_clp = check_both_ends_clipping(r1_ctg_ref_cigar_splitted)
                            if both_end_clp is True:
                                ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                            else:
                                # check mismatch
                                r1_aligned_len, r1_aligned_pct, r1_clipping_len, r1_clipping_pct, r1_mismatch_pct = get_cigar_stats(r1_ctg_ref_cigar_splitted)
                                if r1_ref_min_mismatch == 'NA':
                                    ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                                elif (r1_mismatch_pct > r1_ref_min_mismatch) or (r1_mismatch_pct > mismatch_cutoff):
                                    ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                                else:
                                    # check aligned length
                                    if r1_aligned_len < min_M_len_ctg:
                                        ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                                    else:
                                        # check if clp in the middle
                                        clip_in_middle = False
                                        if ('S' in r1_ctg_ref_cigar) or ('s' in r1_ctg_ref_cigar):
                                            clip_in_middle = True
                                            if (r1_ctg_ref_cigar_splitted[0][-1] in ['S', 's']) and (r1_ctg_ref_pos == 1):
                                                clip_in_middle = False
                                            if (r1_ctg_ref_cigar_splitted[-1][-1] in ['S', 's']):
                                                if (r1_ctg_ref_pos + r1_aligned_len - 1) == round_2_ctg_end_seq_len_dict[r1_ctg_ref_rd2]:
                                                    clip_in_middle = False

                                        if clip_in_middle is True:
                                            ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                                        else:
                                            # check if matched to regions need to be ignored
                                            matched_to_r1_ref_ignored_region_rd2 = False

                                            if r1_ctg_ref_rd2 in ctg_ignore_region_dict_2rd:
                                                r1_ctg_ref_ends_to_ignore_rd2 = ctg_ignore_region_dict_2rd[r1_ctg_ref_rd2]
                                                for to_ignore_region_rd2 in r1_ctg_ref_ends_to_ignore_rd2:
                                                    if to_ignore_region_rd2 == 'left_end':
                                                        if r1_ctg_ref_pos <= 50:
                                                            matched_to_r1_ref_ignored_region_rd2 = True
                                                    if to_ignore_region_rd2 == 'right_end':
                                                        aln_len, aln_pct, clp_len, clp_pct, mis_pct = get_cigar_stats(cigar_splitter(r1_ctg_ref_cigar))
                                                        if (round_2_ctg_end_seq_len_dict[r1_ctg_ref_rd2] - r1_ctg_ref_pos - aln_len) <= 50:
                                                            matched_to_r1_ref_ignored_region_rd2 = True

                                            if matched_to_r1_ref_ignored_region_rd2 is False:
                                                r1_ctg_refs_passed_qc[r1_ctg_ref_rd2] = [r1_ctg_ref_cigar]
                                            else:
                                                ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)

                    ########## filter r2 ctg refs ##########
                    r2_ctg_refs_passed_qc = {}
                    for r2_ctg_ref_rd2 in current_read_base_r2_ctg_ref_dict_rd2:
                        r2_matched_pos_dict = current_read_base_r2_ctg_ref_dict_rd2[r2_ctg_ref_rd2]
                        if len(r2_matched_pos_dict) > 1:
                            ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                        else:
                            r2_ctg_ref_pos = list(r2_matched_pos_dict.keys())[0]
                            r2_ctg_ref_cigar = r2_matched_pos_dict[r2_ctg_ref_pos]
                            r2_ctg_ref_cigar_splitted = cigar_splitter(r2_ctg_ref_cigar)

                            # check both end clip
                            both_end_clp = check_both_ends_clipping(r2_ctg_ref_cigar_splitted)
                            if both_end_clp is True:
                                ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                            else:
                                # check mismatch
                                r2_aligned_len, r2_aligned_pct, r2_clipping_len, r2_clipping_pct, r2_mismatch_pct = get_cigar_stats(r2_ctg_ref_cigar_splitted)
                                if r2_ref_min_mismatch == 'NA':
                                    ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                                elif (r2_mismatch_pct > r2_ref_min_mismatch) or (r2_mismatch_pct > mismatch_cutoff):
                                    ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                                else:
                                    # check aligned length
                                    if r2_aligned_len < min_M_len_ctg:
                                        ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                                    else:
                                        # check if clp in the middle
                                        clip_in_middle = False
                                        if ('S' in r2_ctg_ref_cigar) or ('s' in r2_ctg_ref_cigar):
                                            clip_in_middle = True
                                            if (r2_ctg_ref_cigar_splitted[0][-1] in ['S', 's']) and (r2_ctg_ref_pos == 1):
                                                clip_in_middle = False
                                            if (r2_ctg_ref_cigar_splitted[-1][-1] in ['S', 's']):
                                                if (r2_ctg_ref_pos + r2_aligned_len - 1) == round_2_ctg_end_seq_len_dict[r2_ctg_ref_rd2]:
                                                    clip_in_middle = False

                                        if clip_in_middle is True:
                                            ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                                        else:
                                            # check if matched to regions need to be ignored
                                            matched_to_r2_ref_ignored_region_rd2 = False

                                            if r2_ctg_ref_rd2 in ctg_ignore_region_dict_2rd:
                                                r2_ctg_ref_ends_to_ignore_rd2 = ctg_ignore_region_dict_2rd[r2_ctg_ref_rd2]
                                                for to_ignore_region_rd2 in r2_ctg_ref_ends_to_ignore_rd2:
                                                    if to_ignore_region_rd2 == 'left_end':
                                                        if r2_ctg_ref_pos <= 50:
                                                            matched_to_r2_ref_ignored_region_rd2 = True
                                                    if to_ignore_region_rd2 == 'right_end':
                                                        aln_len, aln_pct, clp_len, clp_pct, mis_pct = get_cigar_stats(cigar_splitter(r2_ctg_ref_cigar))
                                                        if (round_2_ctg_end_seq_len_dict[r2_ctg_ref_rd2] - r2_ctg_ref_pos - aln_len) <= 50:
                                                            matched_to_r2_ref_ignored_region_rd2 = True

                                            if matched_to_r2_ref_ignored_region_rd2 is False:
                                                r2_ctg_refs_passed_qc[r2_ctg_ref_rd2] = [r2_ctg_ref_cigar]
                                            else:
                                                ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)

                    ####################################################################################################

                    r1_ctg_refs_rd2_no_ignored = {key: value for key, value in r1_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}
                    r2_ctg_refs_rd2_no_ignored = {key: value for key, value in r2_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}

                    r1_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r1_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}
                    r2_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r2_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}

                    # print(r1_ctg_refs_passed_qc)
                    # print(r1_ctg_refs_rd2_no_ignored)
                    # print(r2_ctg_refs_passed_qc)
                    # print(r2_ctg_refs_rd2_no_ignored)
                    # print()

                    # only r1 has no_ignored alignments
                    if (len(r1_ctg_refs_rd2_no_ignored) > 0) and (len(r2_ctg_refs_rd2_no_ignored) == 0):
                        print(r1_ctg_refs_passed_qc)
                        print(r1_ctg_refs_rd2_no_ignored)
                        print(r1_ctg_refs_rd2_no_ignored_str_list)
                        print('%s.2\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored)))
                        print('%s.2\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored_str_list)))



                        if rd2_with_both_mates is True:
                            free_living_ctg_ref_file_handle.write('%s\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored)))
                        else:
                            free_living_ctg_ref_file_handle.write('%s.2\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored)))

                    # only r2 has no_ignored alignments
                    if (len(r1_ctg_refs_rd2_no_ignored) == 0) and (len(r2_ctg_refs_rd2_no_ignored) > 0):
                        if rd2_with_both_mates is True:
                            free_living_ctg_ref_file_handle.write('%s\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored)))
                        else:
                            free_living_ctg_ref_file_handle.write('%s.1\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored)))


                    ########################################### reset values ###########################################

                    current_read_base = read_id_base
                    current_read_base_r1_ctg_ref_dict_rd2 = dict()
                    current_read_base_r2_ctg_ref_dict_rd2 = dict()

                    if cigar != '*':
                        if read_strand == '1':
                            current_read_base_r1_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r1_ctg_ref_dict_rd2[ref_id] = {ref_pos: cigar}

    free_living_ctg_ref_file_handle.close()


def get_regions_to_ignore_from_barrnap_output(combined_barrnap_gff, ctg_len_dict):

    ctg_ignore_region_dict = {}

    for each_line in open(combined_barrnap_gff):
        if (not each_line.startswith('#')) and ('16S_rRNA' in each_line):
            each_line_split = each_line.strip().split('\t')
            ctg_id = each_line_split[0]
            ctg_len = ctg_len_dict[ctg_id]
            start_pos = int(each_line_split[3])
            end_pos = int(each_line_split[4])
            len_16s = end_pos - start_pos + 1
            left_gap = start_pos - 1
            right_gap = ctg_len - end_pos - 1

            if left_gap <= 50:
                if ctg_id not in ctg_ignore_region_dict:
                    ctg_ignore_region_dict[ctg_id] = {'left_end'}
                else:
                    ctg_ignore_region_dict[ctg_id].add('left_end')

            if right_gap <= 50:
                if ctg_id not in ctg_ignore_region_dict:
                    ctg_ignore_region_dict[ctg_id] = {'right_end'}
                else:
                    ctg_ignore_region_dict[ctg_id].add('right_end')

    return ctg_ignore_region_dict



step_2_wd = '/Users/songweizhi/Desktop/tunning_rd2_Oral'

combined_1st_round_unlinked_mag_end_seq         = '%s/file_in/round_1_unlinked_gnm_end_500bp.fa' % step_2_wd
pwd_splitted_gnm_sam_file                       = '/Users/songweizhi/Desktop/tunning_rd2_Oral/file_in/round_1_unlinked_gnm_sorted.sam'
pwd_splitted_gnm_sam_free_living_ctg_ref_file   = '/Users/songweizhi/Desktop/tunning_rd2_Oral/file_in/round_1_unlinked_gnm_sorted.txt'
combined_1st_round_unlinked_mags                = '%s/file_in/round_1_unlinked_gnm.fa' % step_2_wd
combined_barrnap_gff                            = '%s/file_in/combined_barrnap.gff' % step_2_wd
combined_input_gnms                             = '%s/file_in/3_Oral_refined_MAGs_combined.fa' % step_2_wd
min_M_len_ctg       = 60
mismatch_cutoff     = 2
rd2_with_both_mates = False
end_seq_len         = 500

ctg_len_dict = {}
for each_ctg_record in SeqIO.parse(combined_input_gnms, 'fasta'):
    ctg_len_dict[each_ctg_record.id] = len(each_ctg_record.seq)

round_2_ctg_end_seq_len_dict = {}
for each_ctg_end_record in SeqIO.parse(combined_1st_round_unlinked_mag_end_seq, 'fasta'):
    round_2_ctg_end_seq_len_dict[each_ctg_end_record.id] = len(each_ctg_end_record.seq)

ctg_ignore_region_dict = get_regions_to_ignore_from_barrnap_output(combined_barrnap_gff, ctg_len_dict)

ctg_ignore_region_dict_rd2 = get_unlinked_mag_end_seq(combined_1st_round_unlinked_mags, combined_1st_round_unlinked_mag_end_seq, end_seq_len, ctg_ignore_region_dict)

arguments_list = [pwd_splitted_gnm_sam_file, pwd_splitted_gnm_sam_free_living_ctg_ref_file,
                  min_M_len_ctg, mismatch_cutoff, round_2_ctg_end_seq_len_dict,
                  rd2_with_both_mates, ctg_ignore_region_dict_rd2]

parse_rd2_sam_gnm_worker(arguments_list)

