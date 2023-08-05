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


def check_both_ends_clipping(cigar_splitted):

    both_ends_clipping = False
    if len(cigar_splitted) >= 3:
        if (cigar_splitted[0][-1] in ['S', 's']) and (cigar_splitted[-1][-1] in ['S', 's']):
            both_ends_clipping = True

    return both_ends_clipping


def r12_16s_ref_dict_to_str(r2_16s_ref_dict):

    top_dict_str = 'na'

    if r2_16s_ref_dict != {}:
        top_dict_list = []
        for sub_dict_key in r2_16s_ref_dict:
            sub_dict_value = r2_16s_ref_dict[sub_dict_key]
            bottom_dict_list = []
            for bottom_dict_key in sub_dict_value:
                bottom_dict_value = sub_dict_value[bottom_dict_key]
                bottom_dict_list.append('%s:%s' % (bottom_dict_key, bottom_dict_value))
            bottom_dict_str = '%s' % (';'.join(bottom_dict_list))
            top_dict_list.append('%s:::%s' % (sub_dict_key, bottom_dict_str))

        top_dict_str = ';;;'.join(top_dict_list)

    return top_dict_str


def no_ignored_dict_to_str(r2_16s_refs_no_ignored_dict):
    top_dict_str = 'na'

    if r2_16s_refs_no_ignored_dict != {}:
        top_dict_list = []
        for each_ref in r2_16s_refs_no_ignored_dict:
            each_ref_cigar_list = r2_16s_refs_no_ignored_dict[each_ref]
            each_ref_cigar_str = ','.join(each_ref_cigar_list)
            top_dict_list.append('%s:%s' % (each_ref, each_ref_cigar_str))
        top_dict_str = ';'.join(top_dict_list)

    return top_dict_str


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


def parse_sam16s_worker(argument_list):

    sorted_sam          = argument_list[0]
    MappingRecord_file  = argument_list[1]
    min_M_len_16s       = argument_list[2]
    mismatch_cutoff     = argument_list[3]
    marker_len_dict     = argument_list[4]

    MappingRecord_file_handle = open(MappingRecord_file, 'w')
    current_read_base = ''
    current_read_base_r1_16s_ref_dict = dict()
    current_read_base_r2_16s_ref_dict = dict()
    with open(sorted_sam) as sorted_sam_opened:
        for each_read in sorted_sam_opened:
            if not each_read.startswith('@'):
                each_read_split = each_read.strip().split('\t')
                cigar = each_read_split[5]
                read_id = each_read_split[0]
                read_id_base = '.'.join(read_id.split('.')[:-1])
                read_strand = read_id.split('.')[-1]
                ref_id = each_read_split[2]
                ref_pos = int(each_read_split[3])

                if current_read_base == '':
                    current_read_base = read_id_base

                    if cigar != '*':
                        if read_strand == '1':
                            current_read_base_r1_16s_ref_dict[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r2_16s_ref_dict[ref_id] = {ref_pos: cigar}

                elif read_id_base == current_read_base:

                    if cigar != '*':
                        if read_strand == '1':
                            if ref_id not in current_read_base_r1_16s_ref_dict:
                                current_read_base_r1_16s_ref_dict[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r1_16s_ref_dict[ref_id][ref_pos] = cigar
                        if read_strand == '2':
                            if ref_id not in current_read_base_r2_16s_ref_dict:
                                current_read_base_r2_16s_ref_dict[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r2_16s_ref_dict[ref_id][ref_pos] = cigar
                else:
                    ################################### analysis previous read refs ####################################

                    current_read_base___qualified_reads             = 0
                    current_read_base___consider_r1_unmapped_mate   = 0
                    current_read_base___consider_r2_unmapped_mate   = 0
                    current_read_base___both_mapped_to_16s          = 0
                    current_read_base___r1_16s_ref_dict             = dict()
                    current_read_base___r2_16s_ref_dict             = dict()
                    current_read_base___r1_16s_refs_no_ignored      = dict()
                    current_read_base___r2_16s_refs_no_ignored      = dict()
                    current_read_base___shared_16s_refs_no_ignored  = dict()

                    ########## get lowest mismatch for r1/r2 16s refs ##########

                    # get r1_ref_cigar_set
                    r1_ref_cigar_set = set()
                    for each_pos_dict in current_read_base_r1_16s_ref_dict.values():
                        each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                        r1_ref_cigar_set.update(each_pos_dict_values)

                    # get r2_ref_cigar_set
                    r2_ref_cigar_set = set()
                    for each_pos_dict in current_read_base_r2_16s_ref_dict.values():
                        each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                        r2_ref_cigar_set.update(each_pos_dict_values)

                    r1_ref_min_mismatch = get_min_mismatch_from_cigar_list(r1_ref_cigar_set, min_M_len_16s)
                    r2_ref_min_mismatch = get_min_mismatch_from_cigar_list(r2_ref_cigar_set, min_M_len_16s)

                    refs_to_ignore = set()

                    ########## filter r1 16s refs ##########

                    r1_16s_refs_passed_qc = {}
                    r1_16s_refs_passed_qc_with_pos = {}
                    for r1_16s_ref in current_read_base_r1_16s_ref_dict:
                        r1_matched_pos_dict = current_read_base_r1_16s_ref_dict[r1_16s_ref]

                        # one read need to mapped to one 16S only for one time
                        if len(r1_matched_pos_dict) > 1:
                            refs_to_ignore.add(r1_16s_ref)
                        else:
                            r1_16s_ref_pos = list(r1_matched_pos_dict.keys())[0]
                            r1_16s_ref_cigar = r1_matched_pos_dict[r1_16s_ref_pos]
                            r1_16s_ref_cigar_splitted = cigar_splitter(r1_16s_ref_cigar)

                            # check both end clip
                            both_end_clp = check_both_ends_clipping(r1_16s_ref_cigar_splitted)
                            if both_end_clp is True:
                                refs_to_ignore.add(r1_16s_ref)
                            else:
                                # check mismatch
                                r1_aligned_len, r1_aligned_pct, r1_clipping_len, r1_clipping_pct, r1_mismatch_pct = get_cigar_stats(
                                    r1_16s_ref_cigar_splitted)
                                if r1_ref_min_mismatch == 'NA':
                                    refs_to_ignore.add(r1_16s_ref)
                                elif (r1_mismatch_pct > r1_ref_min_mismatch) or (r1_mismatch_pct > mismatch_cutoff):
                                    refs_to_ignore.add(r1_16s_ref)
                                else:
                                    # check aligned length
                                    if r1_aligned_len < min_M_len_16s:
                                        refs_to_ignore.add(r1_16s_ref)
                                    else:
                                        # check if clp in the middle
                                        clip_in_middle = False
                                        if ('S' in r1_16s_ref_cigar) or ('s' in r1_16s_ref_cigar):
                                            clip_in_middle = True
                                            if (r1_16s_ref_cigar_splitted[0][-1] in ['S', 's']) and (
                                                    r1_16s_ref_pos == 1):
                                                clip_in_middle = False
                                            if (r1_16s_ref_cigar_splitted[-1][-1] in ['S', 's']):
                                                if (r1_16s_ref_pos + r1_aligned_len - 1) == marker_len_dict[r1_16s_ref]:
                                                    clip_in_middle = False

                                        # exclude the ref if clp in the middle is True
                                        if clip_in_middle is True:
                                            refs_to_ignore.add(r1_16s_ref)
                                        else:
                                            r1_16s_refs_passed_qc[r1_16s_ref] = [r1_16s_ref_cigar]
                                            r1_16s_refs_passed_qc_with_pos[r1_16s_ref] = {r1_16s_ref_pos: r1_16s_ref_cigar}

                    ########## filter r2 16s refs ##########

                    r2_16s_refs_passed_qc = {}
                    r2_16s_refs_passed_qc_with_pos = {}
                    for r2_16s_ref in current_read_base_r2_16s_ref_dict:
                        r2_matched_pos_dict = current_read_base_r2_16s_ref_dict[r2_16s_ref]

                        # one read need to mapped to one 16S only once
                        if len(r2_matched_pos_dict) > 1:
                            refs_to_ignore.add(r2_16s_ref)
                        else:
                            r2_16s_ref_pos = list(r2_matched_pos_dict.keys())[0]
                            r2_16s_ref_cigar = r2_matched_pos_dict[r2_16s_ref_pos]
                            r2_16s_ref_cigar_splitted = cigar_splitter(r2_16s_ref_cigar)

                            # check both end clip
                            both_end_clp = check_both_ends_clipping(r2_16s_ref_cigar_splitted)
                            if both_end_clp is True:
                                refs_to_ignore.add(r2_16s_ref)
                            else:
                                # check mismatch
                                r2_aligned_len, r2_aligned_pct, r2_clipping_len, r2_clipping_pct, r2_mismatch_pct = get_cigar_stats(
                                    r2_16s_ref_cigar_splitted)
                                if r2_ref_min_mismatch == 'NA':
                                    refs_to_ignore.add(r2_16s_ref)
                                elif (r2_mismatch_pct > r2_ref_min_mismatch) or (r2_mismatch_pct > mismatch_cutoff):
                                    refs_to_ignore.add(r2_16s_ref)
                                else:
                                    # check aligned length
                                    if r2_aligned_len < min_M_len_16s:
                                        refs_to_ignore.add(r2_16s_ref)
                                    else:
                                        # check if clp in the middle
                                        clip_in_middle = False
                                        if ('S' in r2_16s_ref_cigar) or ('s' in r2_16s_ref_cigar):
                                            clip_in_middle = True
                                            if (r2_16s_ref_cigar_splitted[0][-1] in ['S', 's']) and (
                                                    r2_16s_ref_pos == 1):
                                                clip_in_middle = False
                                            if (r2_16s_ref_cigar_splitted[-1][-1] in ['S', 's']):
                                                if (r2_16s_ref_pos + r2_aligned_len - 1) == marker_len_dict[r2_16s_ref]:
                                                    clip_in_middle = False

                                        # exclude the ref if clp in the middle is True
                                        if clip_in_middle is True:
                                            refs_to_ignore.add(r2_16s_ref)
                                        else:
                                            r2_16s_refs_passed_qc[r2_16s_ref] = [r2_16s_ref_cigar]
                                            r2_16s_refs_passed_qc_with_pos[r2_16s_ref] = {r2_16s_ref_pos: r2_16s_ref_cigar}

                    #################################

                    r1_16s_refs_no_ignored          = {key: value for key, value in r1_16s_refs_passed_qc.items() if key not in refs_to_ignore}
                    r2_16s_refs_no_ignored          = {key: value for key, value in r2_16s_refs_passed_qc.items() if key not in refs_to_ignore}
                    r1_16s_refs_no_ignored_with_pos = {key: value for key, value in r1_16s_refs_passed_qc_with_pos.items() if key not in refs_to_ignore}
                    r2_16s_refs_no_ignored_with_pos = {key: value for key, value in r2_16s_refs_passed_qc_with_pos.items() if key not in refs_to_ignore}

                    r1_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r1_16s_refs_passed_qc.items() if key not in refs_to_ignore}
                    r2_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r2_16s_refs_passed_qc.items() if key not in refs_to_ignore}

                    r1_ctg_refs_rd2_no_ignored_str_list_with_pos = set()
                    for each_16s in r1_16s_refs_no_ignored_with_pos:
                        cigar_dict = r1_16s_refs_no_ignored_with_pos[each_16s]
                        for each_cigar_pos in cigar_dict:
                            cigar_str = cigar_dict[each_cigar_pos]
                            r1_ctg_refs_rd2_no_ignored_str_list_with_pos.add( '%s__pc__%s__pc__%s' % (each_16s, each_cigar_pos, cigar_str))




                    print(r1_16s_refs_no_ignored)
                    print(r1_16s_refs_no_ignored_with_pos)
                    print(r1_ctg_refs_rd2_no_ignored_str_list)
                    print(r1_ctg_refs_rd2_no_ignored_str_list_with_pos)
                    print()





                    # print('\n----------------------------------\n')
                    #
                    # print('r1_16s_refs_passed_qc: %s' % r1_16s_refs_passed_qc)
                    # print('r1_16s_refs_passed_qc_with_pos: %s' % r1_16s_refs_passed_qc_with_pos)
                    # print()
                    # print('r1_16s_refs_no_ignored: %s' % r1_16s_refs_no_ignored)
                    # print('r1_16s_refs_no_ignored_with_pos: %s' % r1_16s_refs_no_ignored_with_pos)
                    # print()
                    # print('r2_16s_refs_passed_qc: %s' % r2_16s_refs_passed_qc)
                    # print('r2_16s_refs_passed_qc_with_pos: %s' % r2_16s_refs_passed_qc_with_pos)
                    # print()
                    # print('r2_16s_refs_no_ignored: %s' % r2_16s_refs_no_ignored)
                    # print('r2_16s_refs_no_ignored_with_pos: %s' % r2_16s_refs_no_ignored_with_pos)


                    # no mate has no_ignored alignments
                    if (len(r1_16s_refs_no_ignored) == 0) and (len(r2_16s_refs_no_ignored) == 0):
                        pass

                    # only r1 has no_ignored alignments
                    elif (len(r1_16s_refs_no_ignored) > 0) and (len(r2_16s_refs_no_ignored) == 0):

                        current_read_base___qualified_reads = 1
                        current_read_base___consider_r1_unmapped_mate = 1
                        current_read_base___r1_16s_refs_no_ignored = r1_16s_refs_no_ignored
                        current_read_base___r1_16s_ref_dict = current_read_base_r1_16s_ref_dict

                    # only r2 has no_ignored alignments
                    elif (len(r1_16s_refs_no_ignored) == 0) and (len(r2_16s_refs_no_ignored) > 0):

                        current_read_base___qualified_reads = 1
                        current_read_base___consider_r2_unmapped_mate = 1
                        current_read_base___r2_16s_refs_no_ignored = r2_16s_refs_no_ignored
                        current_read_base___r2_16s_ref_dict = current_read_base_r2_16s_ref_dict

                    # both r1 and r2 have no_ignored alignments
                    else:
                        shared_16s_ref_dict          = {key: [r1_16s_refs_no_ignored[key][0], r2_16s_refs_no_ignored[key][0]] for key in set(r1_16s_refs_no_ignored).intersection(set(r2_16s_refs_no_ignored))}
                        shared_16s_ref_dict_with_pos = {key: [r1_16s_refs_no_ignored[key][0], r2_16s_refs_no_ignored[key][0]] for key in set(r1_16s_refs_no_ignored).intersection(set(r2_16s_refs_no_ignored))}

                        if len(shared_16s_ref_dict) > 0:
                            # print('\n-----\n')
                            # print(r1_16s_refs_no_ignored)
                            # print(r2_16s_refs_no_ignored)
                            # print(shared_16s_ref_dict)
                            # print(shared_16s_ref_dict_with_pos)
                            # print(r1_16s_refs_no_ignored_with_pos)
                            # print(r2_16s_refs_no_ignored_with_pos)
                            # print(shared_16s_ref_dict_with_pos)
                            current_read_base___qualified_reads = 1
                            current_read_base___both_mapped_to_16s = 1
                            current_read_base___shared_16s_refs_no_ignored = shared_16s_ref_dict
                            current_read_base___r1_16s_ref_dict = current_read_base_r1_16s_ref_dict
                            current_read_base___r2_16s_ref_dict = current_read_base_r2_16s_ref_dict

                    if current_read_base___qualified_reads == 1:

                        # print('\n----------------------------------\n')
                        # print('current_read_base___r1_16s_ref_dict: %s' % current_read_base___r1_16s_ref_dict)
                        # print('current_read_base___r2_16s_ref_dict: %s' % current_read_base___r2_16s_ref_dict)
                        # print('current_read_base___r1_16s_refs_no_ignored: %s' % current_read_base___r1_16s_refs_no_ignored)
                        # print('current_read_base___r2_16s_refs_no_ignored: %s' % current_read_base___r2_16s_refs_no_ignored)
                        # print('current_read_base___shared_16s_refs_no_ignored: %s' % current_read_base___shared_16s_refs_no_ignored)


                        current_read_base___r1_16s_ref_dict_str            = r12_16s_ref_dict_to_str(current_read_base___r1_16s_ref_dict)
                        current_read_base___r2_16s_ref_dict_str            = r12_16s_ref_dict_to_str(current_read_base___r2_16s_ref_dict)
                        current_read_base___r1_16s_refs_no_ignored_str     = no_ignored_dict_to_str(current_read_base___r1_16s_refs_no_ignored)
                        current_read_base___r2_16s_refs_no_ignored_str     = no_ignored_dict_to_str(current_read_base___r2_16s_refs_no_ignored)
                        current_read_base___shared_16s_refs_no_ignored_str = no_ignored_dict_to_str(current_read_base___shared_16s_refs_no_ignored)
                        MappingRecord_file_handle.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (current_read_base,
                                                                                                      current_read_base___qualified_reads,
                                                                                                      current_read_base___consider_r1_unmapped_mate,
                                                                                                      current_read_base___consider_r2_unmapped_mate,
                                                                                                      current_read_base___both_mapped_to_16s,
                                                                                                      current_read_base___r1_16s_ref_dict_str,
                                                                                                      current_read_base___r2_16s_ref_dict_str,
                                                                                                      current_read_base___r1_16s_refs_no_ignored_str,
                                                                                                      current_read_base___r2_16s_refs_no_ignored_str,
                                                                                                      current_read_base___shared_16s_refs_no_ignored_str))


                    ########################################### reset values ###########################################

                    current_read_base = read_id_base
                    current_read_base_r1_16s_ref_dict = dict()
                    current_read_base_r2_16s_ref_dict = dict()

                    if cigar != '*':
                        if read_strand == '1':
                            current_read_base_r1_16s_ref_dict[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r2_16s_ref_dict[ref_id] = {ref_pos: cigar}

    MappingRecord_file_handle.close()


pwd_splitted_sam_file       = '/Users/songweizhi/Desktop/666/subset.sam'
input_16s_qc                = '/Users/songweizhi/Desktop/666/CAMI_Oral_138_16S_0.999.polished_min1200.QC.fa'
pwd_splitted_sam_mp_file    = '/Users/songweizhi/Desktop/666/subset_mp.txt'
min_M_len_16s               = 45
mismatch_cutoff             = 2

# head -100000 Oral_0715_60_60_min1200_input_reads_to_16S_sorted.sam > subset.sam

marker_len_dict = {}
for each_marker_record in SeqIO.parse(input_16s_qc, 'fasta'):
    marker_len_dict[each_marker_record.id] = len(each_marker_record.seq)

arg_list = [pwd_splitted_sam_file, pwd_splitted_sam_mp_file,
            min_M_len_16s, mismatch_cutoff, marker_len_dict]

parse_sam16s_worker(arg_list)

