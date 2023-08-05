import os
import pandas as pd


def blast_results_to_pairwise_16s_iden_dict(blastn_output, align_len_cutoff, cov_cutoff):

    pairwise_iden_dict = {}
    for match in open(blastn_output):
        match_split = match.strip().split('\t')
        query = match_split[0]
        subject = match_split[1]
        iden = float(match_split[2])
        align_len = int(match_split[3])
        query_len = int(match_split[12])
        subject_len = int(match_split[13])
        coverage_q = float(align_len) * 100 / float(query_len)
        coverage_s = float(align_len) * 100 / float(subject_len)

        if (align_len >= align_len_cutoff) and (query != subject) and (coverage_q >= cov_cutoff) and (coverage_s >= cov_cutoff):
            query_to_subject_key = '__|__'.join(sorted([query, subject]))
            if query_to_subject_key not in pairwise_iden_dict:
                pairwise_iden_dict[query_to_subject_key] = iden
            else:
                if iden > pairwise_iden_dict[query_to_subject_key]:
                    pairwise_iden_dict[query_to_subject_key] = iden

    return pairwise_iden_dict


def get_GapFilling_stats_by_assembly(free_living_16s_ref_file,
                                     free_living_ctg_ref_file,
                                     mini_assembly_to_16s_reads,
                                     mini_assembly_to_ctg_reads,
                                     ctg_level_min_link,
                                     mini_assembly_to_16s_ctg_connector,
                                     gnm_to_ctg_connector,
                                     marker_to_ctg_gnm_Key_connector,
                                     max_within_cate_diff_pct,
                                     max_between_cate_diff_pct,
                                     stats_GapFilling_ctg,
                                     stats_GapFilling_gnm):

    round2_free_living_16s_ref_dict = {}
    for free_living_read_16s in open(free_living_16s_ref_file):
        free_living_read_16s_split = free_living_read_16s.strip().split('\t')
        if len(free_living_read_16s_split) > 1:
            read_16s_id = free_living_read_16s_split[0]
            read_16s_refs = free_living_read_16s_split[1].split(',')
            round2_free_living_16s_ref_dict[read_16s_id] = read_16s_refs

    round2_free_living_ctg_ref_dict = {}
    for free_living_read_ctg in open(free_living_ctg_ref_file):
        free_living_read_ctg_split = free_living_read_ctg.strip().split('\t')
        read_ctg_id = free_living_read_ctg_split[0]
        read_ctg_refs = free_living_read_ctg_split[1].split(',')
        read_ctg_refs_no_suffix = []
        for each_read_ctg_ref in read_ctg_refs:
            if each_read_ctg_ref[-2:] in ['_l', '_r']:
                each_read_ctg_ref_no_suffix = each_read_ctg_ref[:-2]
                read_ctg_refs_no_suffix.append(each_read_ctg_ref_no_suffix)
        round2_free_living_ctg_ref_dict[read_ctg_id] = read_ctg_refs_no_suffix

    mini_assembly_to_16s_dict = {}
    for each_mini_assembly in open(mini_assembly_to_16s_reads):
        mini_assembly_split = each_mini_assembly.strip().split('\t')
        mini_assembly_id = mini_assembly_split[0]
        mini_assembly_mapped_reads = mini_assembly_split[1].split(',')
        for each_mapped_read in mini_assembly_mapped_reads:
            mapped_read_16s_refs = round2_free_living_16s_ref_dict.get(each_mapped_read, [])
            for each_mapped_read_16s_ref in mapped_read_16s_refs:
                mini_assembly_to_16s_key = '%s%s%s' % (mini_assembly_id, mini_assembly_to_16s_ctg_connector, each_mapped_read_16s_ref)
                if mini_assembly_to_16s_key not in mini_assembly_to_16s_dict:
                    mini_assembly_to_16s_dict[mini_assembly_to_16s_key] = 1
                else:
                    mini_assembly_to_16s_dict[mini_assembly_to_16s_key] += 1

    mini_assembly_to_ctg_dict = {}
    for each_mini_assembly in open(mini_assembly_to_ctg_reads):
        mini_assembly_split = each_mini_assembly.strip().split('\t')
        mini_assembly_id = mini_assembly_split[0]
        mini_assembly_mapped_reads = mini_assembly_split[1].split(',')
        for each_mapped_read in mini_assembly_mapped_reads:
            mapped_read_ctg_refs = round2_free_living_ctg_ref_dict.get(each_mapped_read, [])
            for each_mapped_read_ctg_ref in mapped_read_ctg_refs:
                mini_assembly_to_ctg_key = '%s%s%s' % (mini_assembly_id, mini_assembly_to_16s_ctg_connector, each_mapped_read_ctg_ref)
                if mini_assembly_to_ctg_key not in mini_assembly_to_ctg_dict:
                    mini_assembly_to_ctg_dict[mini_assembly_to_ctg_key] = 1
                else:
                    mini_assembly_to_ctg_dict[mini_assembly_to_ctg_key] += 1

    mini_assembly_to_16s_dict_reformatted = {}
    max_link_nun_dict_16s = {}
    for each in mini_assembly_to_16s_dict:
        mini_assembly_id = each.split(mini_assembly_to_16s_ctg_connector)[0]
        seq_16s_id = each.split(mini_assembly_to_16s_ctg_connector)[1]
        linkage_num = mini_assembly_to_16s_dict[each]
        seq_16s_with_num = '%s__num__%s' % (seq_16s_id, linkage_num)
        if linkage_num >= ctg_level_min_link:

            # add to mini_assembly_to_16s_dict_reformatted
            if mini_assembly_id not in mini_assembly_to_16s_dict_reformatted:
                mini_assembly_to_16s_dict_reformatted[mini_assembly_id] = {seq_16s_with_num}
            else:
                mini_assembly_to_16s_dict_reformatted[mini_assembly_id].add(seq_16s_with_num)

            # add to max_link_nun_dict_16s
            if seq_16s_id not in max_link_nun_dict_16s:
                max_link_nun_dict_16s[seq_16s_id] = linkage_num
            else:
                if linkage_num > max_link_nun_dict_16s[seq_16s_id]:
                    max_link_nun_dict_16s[seq_16s_id] = linkage_num

    mini_assembly_to_ctg_dict_reformatted = {}
    max_link_nun_dict_ctg = {}
    for each in mini_assembly_to_ctg_dict:
        mini_assembly_id = each.split(mini_assembly_to_16s_ctg_connector)[0]
        ctg_id = each.split(mini_assembly_to_16s_ctg_connector)[1]
        linkage_num = mini_assembly_to_ctg_dict[each]
        ctg_with_num = '%s__num__%s' % (ctg_id, linkage_num)
        if linkage_num >= ctg_level_min_link:

            # add to mini_assembly_to_ctg_dict_reformatted
            if mini_assembly_id not in mini_assembly_to_ctg_dict_reformatted:
                mini_assembly_to_ctg_dict_reformatted[mini_assembly_id] = {ctg_with_num}
            else:
                mini_assembly_to_ctg_dict_reformatted[mini_assembly_id].add(ctg_with_num)

            # add to max_link_nun_dict_ctg
            if ctg_id not in max_link_nun_dict_ctg:
                max_link_nun_dict_ctg[ctg_id] = linkage_num
            else:
                if linkage_num > max_link_nun_dict_ctg[ctg_id]:
                    max_link_nun_dict_ctg[ctg_id] = linkage_num

    mini_assembly_linked_both = set(mini_assembly_to_16s_dict_reformatted).intersection(mini_assembly_to_ctg_dict_reformatted)

    stats_GapFilling_ctg_handle = open(stats_GapFilling_ctg, 'w')
    stats_GapFilling_gnm_dict = {}
    for each_mini_assembly in mini_assembly_linked_both:
        linked_16s = mini_assembly_to_16s_dict_reformatted[each_mini_assembly]
        linked_ctg = mini_assembly_to_ctg_dict_reformatted[each_mini_assembly]
        linked_16s_num_list = [int(i.split('__num__')[1]) for i in linked_16s]
        linked_ctg_num_list = [int(i.split('__num__')[1]) for i in linked_ctg]
        linked_16s_num_max = max(linked_16s_num_list)
        linked_ctg_num_max = max(linked_ctg_num_list)

        if (min(linked_16s_num_max, linked_ctg_num_max) * 100 / max(linked_16s_num_max, linked_ctg_num_max)) >= max_between_cate_diff_pct:

            linked_16s_filtered = [i for i in linked_16s if int(i.split('__num__')[1])*100/linked_16s_num_max >= max_within_cate_diff_pct]
            linked_ctg_filtered = [i for i in linked_ctg if int(i.split('__num__')[1])*100/linked_ctg_num_max >= max_within_cate_diff_pct]

            for each_linked_16s in linked_16s_filtered:
                linked_16s_id = each_linked_16s.split('__num__')[0]
                linked_16s_num = int(each_linked_16s.split('__num__')[1])
                linked_16s_num_pct_by_max = linked_16s_num * 100 / max_link_nun_dict_16s[linked_16s_id]

                for each_linked_ctg in linked_ctg_filtered:
                    linked_ctg_id = each_linked_ctg.split('__num__')[0]
                    linked_gnm_id = linked_ctg_id.split(gnm_to_ctg_connector)[0]
                    linked_ctg_num = int(each_linked_ctg.split('__num__')[1])
                    linked_ctg_num_pct_by_max = linked_ctg_num*100/max_link_nun_dict_ctg[linked_ctg_id]

                    if (linked_16s_num_pct_by_max >= 50) and (linked_ctg_num_pct_by_max >= 50):
                        stats_GapFilling_ctg_handle.write('%s\t%s\t%s\n' % (linked_16s_id, linked_ctg_id, (linked_16s_num + linked_ctg_num)))
                        marker_to_gnm_key = '%s%s%s' % (linked_16s_id, marker_to_ctg_gnm_Key_connector, linked_gnm_id)
                        if marker_to_gnm_key not in stats_GapFilling_gnm_dict:
                            stats_GapFilling_gnm_dict[marker_to_gnm_key] = (linked_16s_num + linked_ctg_num)
                        else:
                            stats_GapFilling_gnm_dict[marker_to_gnm_key] += (linked_16s_num + linked_ctg_num)
    stats_GapFilling_ctg_handle.close()

    stats_GapFilling_gnm_handle = open(stats_GapFilling_gnm, 'w')
    stats_GapFilling_gnm_handle.write('MarkerGene,GenomicSeq,Number\n')
    for each_16s_to_gnm in stats_GapFilling_gnm_dict:
        each_16s_to_gnm_split = each_16s_to_gnm.split(marker_to_ctg_gnm_Key_connector)
        id_16s = each_16s_to_gnm_split[0]
        id_gnm = each_16s_to_gnm_split[1]
        linkage_num = stats_GapFilling_gnm_dict[each_16s_to_gnm]
        stats_GapFilling_gnm_handle.write('MarkerGene__%s,GenomicSeq__%s,%s\n' % (id_16s, id_gnm, linkage_num))
    stats_GapFilling_gnm_handle.close()


def get_GapFilling_stats_by_assembly_separately(free_living_16s_ref_file,
                                                free_living_ctg_ref_file,
                                                mini_assembly_to_16s_reads,
                                                mini_assembly_to_ctg_reads,
                                                ctg_level_min_link,
                                                mini_assembly_to_16s_ctg_connector,
                                                gnm_to_ctg_connector,
                                                marker_to_ctg_gnm_Key_connector,
                                                max_within_cate_diff_pct,
                                                max_between_cate_diff_pct,
                                                stats_GapFilling_ctg,
                                                stats_GapFilling_gnm):

    round2_free_living_16s_ref_dict = {}
    for free_living_read_16s in open(free_living_16s_ref_file):
        free_living_read_16s_split = free_living_read_16s.strip().split('\t')
        if len(free_living_read_16s_split) > 1:
            read_16s_id = free_living_read_16s_split[0]
            read_16s_refs = free_living_read_16s_split[1].split(',')
            round2_free_living_16s_ref_dict[read_16s_id] = read_16s_refs

    round2_free_living_ctg_ref_dict = {}
    for free_living_read_ctg in open(free_living_ctg_ref_file):
        free_living_read_ctg_split = free_living_read_ctg.strip().split('\t')
        read_ctg_id = free_living_read_ctg_split[0]
        read_ctg_refs = free_living_read_ctg_split[1].split(',')
        read_ctg_refs_no_suffix = []
        for each_read_ctg_ref in read_ctg_refs:
            if each_read_ctg_ref[-2:] in ['_l', '_r']:
                each_read_ctg_ref_no_suffix = each_read_ctg_ref[:-2]
                read_ctg_refs_no_suffix.append(each_read_ctg_ref_no_suffix)
        round2_free_living_ctg_ref_dict[read_ctg_id] = read_ctg_refs_no_suffix

    mini_assembly_to_16s_dict = {}
    for each_mini_assembly in open(mini_assembly_to_16s_reads):
        mini_assembly_split = each_mini_assembly.strip().split('\t')
        mini_assembly_id = mini_assembly_split[0]
        mini_assembly_mapped_reads = mini_assembly_split[1].split(',')
        for each_mapped_read in mini_assembly_mapped_reads:
            mapped_read_16s_refs = round2_free_living_16s_ref_dict.get(each_mapped_read, [])
            for each_mapped_read_16s_ref in mapped_read_16s_refs:
                mini_assembly_to_16s_key = '%s%s%s' % (mini_assembly_id, mini_assembly_to_16s_ctg_connector, each_mapped_read_16s_ref)
                if mini_assembly_to_16s_key not in mini_assembly_to_16s_dict:
                    mini_assembly_to_16s_dict[mini_assembly_to_16s_key] = 1
                else:
                    mini_assembly_to_16s_dict[mini_assembly_to_16s_key] += 1

    mini_assembly_to_ctg_dict = {}
    for each_mini_assembly in open(mini_assembly_to_ctg_reads):
        mini_assembly_split = each_mini_assembly.strip().split('\t')
        mini_assembly_id = mini_assembly_split[0]
        mini_assembly_mapped_reads = mini_assembly_split[1].split(',')
        for each_mapped_read in mini_assembly_mapped_reads:
            mapped_read_ctg_refs = round2_free_living_ctg_ref_dict.get(each_mapped_read, [])
            for each_mapped_read_ctg_ref in mapped_read_ctg_refs:
                mini_assembly_to_ctg_key = '%s%s%s' % (mini_assembly_id, mini_assembly_to_16s_ctg_connector, each_mapped_read_ctg_ref)
                if mini_assembly_to_ctg_key not in mini_assembly_to_ctg_dict:
                    mini_assembly_to_ctg_dict[mini_assembly_to_ctg_key] = 1
                else:
                    mini_assembly_to_ctg_dict[mini_assembly_to_ctg_key] += 1

    mini_assembly_to_16s_dict_reformatted = {}
    max_link_nun_dict_16s = {}
    for each in mini_assembly_to_16s_dict:
        mini_assembly_id = each.split(mini_assembly_to_16s_ctg_connector)[0]
        seq_16s_id = each.split(mini_assembly_to_16s_ctg_connector)[1]
        linkage_num = mini_assembly_to_16s_dict[each]
        seq_16s_with_num = '%s__num__%s' % (seq_16s_id, linkage_num)
        if linkage_num >= ctg_level_min_link:

            # add to mini_assembly_to_16s_dict_reformatted
            if mini_assembly_id not in mini_assembly_to_16s_dict_reformatted:
                mini_assembly_to_16s_dict_reformatted[mini_assembly_id] = {seq_16s_with_num}
            else:
                mini_assembly_to_16s_dict_reformatted[mini_assembly_id].add(seq_16s_with_num)

            # add to max_link_nun_dict_16s
            if seq_16s_id not in max_link_nun_dict_16s:
                max_link_nun_dict_16s[seq_16s_id] = linkage_num
            else:
                if linkage_num > max_link_nun_dict_16s[seq_16s_id]:
                    max_link_nun_dict_16s[seq_16s_id] = linkage_num

    print(mini_assembly_to_16s_dict_reformatted)

    mini_assembly_to_ctg_dict_reformatted = {}
    max_link_nun_dict_ctg = {}
    for each in mini_assembly_to_ctg_dict:
        mini_assembly_id = each.split(mini_assembly_to_16s_ctg_connector)[0]
        ctg_id = each.split(mini_assembly_to_16s_ctg_connector)[1]
        linkage_num = mini_assembly_to_ctg_dict[each]
        ctg_with_num = '%s__num__%s' % (ctg_id, linkage_num)
        if linkage_num >= ctg_level_min_link:

            # add to mini_assembly_to_ctg_dict_reformatted
            if mini_assembly_id not in mini_assembly_to_ctg_dict_reformatted:
                mini_assembly_to_ctg_dict_reformatted[mini_assembly_id] = {ctg_with_num}
            else:
                mini_assembly_to_ctg_dict_reformatted[mini_assembly_id].add(ctg_with_num)

            # add to max_link_nun_dict_ctg
            if ctg_id not in max_link_nun_dict_ctg:
                max_link_nun_dict_ctg[ctg_id] = linkage_num
            else:
                if linkage_num > max_link_nun_dict_ctg[ctg_id]:
                    max_link_nun_dict_ctg[ctg_id] = linkage_num

    #print(mini_assembly_to_ctg_dict_reformatted)

    mini_assembly_linked_both = set(mini_assembly_to_16s_dict_reformatted).intersection(mini_assembly_to_ctg_dict_reformatted)

    stats_GapFilling_ctg_handle = open(stats_GapFilling_ctg, 'w')
    stats_GapFilling_gnm_dict = {}
    for each_mini_assembly in mini_assembly_linked_both:
        linked_16s = mini_assembly_to_16s_dict_reformatted[each_mini_assembly]
        linked_ctg = mini_assembly_to_ctg_dict_reformatted[each_mini_assembly]
        linked_16s_num_list = [int(i.split('__num__')[1]) for i in linked_16s]
        linked_ctg_num_list = [int(i.split('__num__')[1]) for i in linked_ctg]
        linked_16s_num_max = max(linked_16s_num_list)
        linked_ctg_num_max = max(linked_ctg_num_list)

        if (min(linked_16s_num_max, linked_ctg_num_max) * 100 / max(linked_16s_num_max, linked_ctg_num_max)) >= max_between_cate_diff_pct:

            linked_16s_filtered = [i for i in linked_16s if int(i.split('__num__')[1])*100/linked_16s_num_max >= max_within_cate_diff_pct]
            linked_ctg_filtered = [i for i in linked_ctg if int(i.split('__num__')[1])*100/linked_ctg_num_max >= max_within_cate_diff_pct]

            for each_linked_16s in linked_16s_filtered:
                linked_16s_id = each_linked_16s.split('__num__')[0]
                linked_16s_num = int(each_linked_16s.split('__num__')[1])
                linked_16s_num_pct_by_max = linked_16s_num * 100 / max_link_nun_dict_16s[linked_16s_id]

                for each_linked_ctg in linked_ctg_filtered:
                    linked_ctg_id = each_linked_ctg.split('__num__')[0]
                    linked_gnm_id = linked_ctg_id.split(gnm_to_ctg_connector)[0]
                    linked_ctg_num = int(each_linked_ctg.split('__num__')[1])
                    linked_ctg_num_pct_by_max = linked_ctg_num*100/max_link_nun_dict_ctg[linked_ctg_id]

                    if (linked_16s_num_pct_by_max >= 50) and (linked_ctg_num_pct_by_max >= 50):
                        stats_GapFilling_ctg_handle.write('%s\t%s\t%s\n' % (linked_16s_id, linked_ctg_id, (linked_16s_num + linked_ctg_num)))
                        marker_to_gnm_key = '%s%s%s' % (linked_16s_id, marker_to_ctg_gnm_Key_connector, linked_gnm_id)
                        if marker_to_gnm_key not in stats_GapFilling_gnm_dict:
                            stats_GapFilling_gnm_dict[marker_to_gnm_key] = (linked_16s_num + linked_ctg_num)
                        else:
                            stats_GapFilling_gnm_dict[marker_to_gnm_key] += (linked_16s_num + linked_ctg_num)
    stats_GapFilling_ctg_handle.close()

    stats_GapFilling_gnm_handle = open(stats_GapFilling_gnm, 'w')
    stats_GapFilling_gnm_handle.write('MarkerGene,GenomicSeq,Number\n')
    for each_16s_to_gnm in stats_GapFilling_gnm_dict:
        each_16s_to_gnm_split = each_16s_to_gnm.split(marker_to_ctg_gnm_Key_connector)
        id_16s = each_16s_to_gnm_split[0]
        id_gnm = each_16s_to_gnm_split[1]
        linkage_num = stats_GapFilling_gnm_dict[each_16s_to_gnm]
        stats_GapFilling_gnm_handle.write('MarkerGene__%s,GenomicSeq__%s,%s\n' % (id_16s, id_gnm, linkage_num))
    stats_GapFilling_gnm_handle.close()


def sep_path_basename_ext(file_in):

    # separate path and file name
    file_path, file_name = os.path.split(file_in)
    if file_path == '':
        file_path = '..'

    # separate file basename and extension
    file_basename, file_extension = os.path.splitext(file_name)

    return file_path, file_basename, file_extension


def sort_csv_by_col(file_in, file_out, col_header):
    df_in        = pd.read_csv(file_in)
    df_in_sorted = df_in.sort_values(by=[col_header], ascending=False)
    df_in_sorted.to_csv(file_out, index=False)


def filter_linkages_iteratively(file_in, sort_by_col_header, pairwise_16s_iden_dict, genomic_seq_depth_dict, marker_gene_depth_dict, min_16s_gnm_multiple, within_genome_16s_divergence_cutoff, min_linkages, min_linkages_for_uniq_linked_16s, within_gnm_linkage_num_diff, file_out):

    # get MarkerGene_to_GenomicSeq_dict
    MarkerGene_to_GenomicSeq_dict = {}
    for each_linkage in open(file_in):
        if not each_linkage.startswith('MarkerGene,GenomicSeq,Number'):
            each_linkage_split = each_linkage.strip().split(',')
            MarkerGene_id = each_linkage_split[0][12:]
            GenomicSeq_id = each_linkage_split[1][12:]
            linkage_num = int(each_linkage_split[2])
            if linkage_num > 1:
                if MarkerGene_id not in MarkerGene_to_GenomicSeq_dict:
                    MarkerGene_to_GenomicSeq_dict[MarkerGene_id] = {GenomicSeq_id}
                else:
                    MarkerGene_to_GenomicSeq_dict[MarkerGene_id].add(GenomicSeq_id)

    file_in_path, file_in_basename, file_in_extension = sep_path_basename_ext(file_in)
    file_in_sorted = '%s/%s_sorted%s' % (file_in_path, file_in_basename, file_in_extension)

    # sort file in
    sort_csv_by_col(file_in, file_in_sorted, sort_by_col_header)

    # fileter linkage
    gnm_max_link_num_dict = {}
    file_out_handle = open(file_out, 'w')
    MarkerGene_with_assignment = set()
    GenomicSeq_best_marker_dict = {}
    for each_match in open(file_in_sorted):
        if each_match.startswith('MarkerGene,GenomicSeq,Number'):
            file_out_handle.write(each_match)
        else:
            match_split = each_match.strip().split(',')
            MarkerGene = match_split[0][12:]
            GenomicSeq = match_split[1][12:]
            linkage_num = int(match_split[2])

            current_min_linkage = min_linkages_for_uniq_linked_16s
            if MarkerGene in MarkerGene_to_GenomicSeq_dict:
                if len(MarkerGene_to_GenomicSeq_dict[MarkerGene]) > 1:
                    current_min_linkage = min_linkages

            if linkage_num >= current_min_linkage:
                if MarkerGene not in MarkerGene_with_assignment:

                    # consider depth
                    if min_16s_gnm_multiple > 0:

                        # get marker and genome depth
                        MarkerGene_depth = marker_gene_depth_dict.get(MarkerGene, 'na')
                        GenomicSeq_depth = genomic_seq_depth_dict.get(GenomicSeq, 'na')
                        marker_genome_depth_ratio = 'na'
                        if (MarkerGene_depth != 'na') and (GenomicSeq_depth != 'na'):
                            if GenomicSeq_depth > 0:
                                marker_genome_depth_ratio = MarkerGene_depth / GenomicSeq_depth

                        if marker_genome_depth_ratio >= min_16s_gnm_multiple:
                            if GenomicSeq not in GenomicSeq_best_marker_dict:
                                GenomicSeq_best_marker_dict[GenomicSeq] = MarkerGene
                                gnm_max_link_num_dict[GenomicSeq] = linkage_num
                                file_out_handle.write(each_match)
                                MarkerGene_with_assignment.add(MarkerGene)
                            else:
                                # get identity with best marker
                                current_GenomicSeq_best_marker = GenomicSeq_best_marker_dict[GenomicSeq]
                                key_str = '__|__'.join(sorted([MarkerGene, current_GenomicSeq_best_marker]))
                                iden_with_best_marker = pairwise_16s_iden_dict.get(key_str, 0)
                                if iden_with_best_marker >= within_genome_16s_divergence_cutoff:
                                    gnm_max_link_num = gnm_max_link_num_dict[GenomicSeq]
                                    if (linkage_num * 100 / gnm_max_link_num) >= within_gnm_linkage_num_diff:
                                        file_out_handle.write(each_match)
                                        MarkerGene_with_assignment.add(MarkerGene)
                                    else:
                                        MarkerGene_with_assignment.add(MarkerGene)
                    # ignore depth
                    else:
                        if GenomicSeq not in GenomicSeq_best_marker_dict:
                            GenomicSeq_best_marker_dict[GenomicSeq] = MarkerGene
                            gnm_max_link_num_dict[GenomicSeq] = linkage_num
                            file_out_handle.write(each_match)
                            MarkerGene_with_assignment.add(MarkerGene)
                        else:
                            # get identity with best marker
                            current_GenomicSeq_best_marker = GenomicSeq_best_marker_dict[GenomicSeq]
                            key_str = '__|__'.join(sorted([MarkerGene, current_GenomicSeq_best_marker]))
                            iden_with_best_marker = pairwise_16s_iden_dict.get(key_str, 0)
                            if iden_with_best_marker >= within_genome_16s_divergence_cutoff:
                                gnm_max_link_num = gnm_max_link_num_dict[GenomicSeq]
                                if (linkage_num*100/gnm_max_link_num) >= within_gnm_linkage_num_diff:
                                    file_out_handle.write(each_match)
                                    MarkerGene_with_assignment.add(MarkerGene)
                                else:
                                    MarkerGene_with_assignment.add(MarkerGene)
    file_out_handle.close()


def check_both_ends_clipping(cigar_splitted):

    both_ends_clipping = False
    if len(cigar_splitted) >= 3:
        if (cigar_splitted[0][-1] in ['S', 's']) and (cigar_splitted[-1][-1] in ['S', 's']):
            both_ends_clipping = True

    return both_ends_clipping


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


####################################################################################################################
############################################### second round linking ###############################################
####################################################################################################################

step_2_wd                                       = '/Users/songweizhi/Desktop/tunning_rd2_up'
sam_file_mini_assembly_reformatted              = '%s/scaffolds_bowtie_reformatted.sam'                     % step_2_wd
blast_results_all_vs_all_16s                    = '%s/file_in/GI_0527_128_60_60_16S_all_vs_all_blastn.tab'  % step_2_wd
free_living_16s_ref_file                        = '%s/file_in/round2_free_living_16s_refs.txt'              % step_2_wd
free_living_ctg_ref_file                        = '%s/file_in/round2_free_living_ctg_refs.txt'              % step_2_wd
mini_assembly_to_16s_reads                      = '%s/file_in/mini_assembly_to_16s_reads.txt'               % step_2_wd
mini_assembly_to_ctg_reads                      = '%s/file_in/mini_assembly_to_ctg_reads.txt'               % step_2_wd
sam_file_mini_assembly_reformatted_sorted_16s   = '%s/file_in/scaffolds_bowtie_reformatted_sorted_16s.sam'  % step_2_wd
sam_file_mini_assembly_reformatted_sorted_ctg   = '%s/file_in/scaffolds_bowtie_reformatted_sorted_ctg.sam'  % step_2_wd


marker_to_ctg_gnm_Key_connector                 = '___M___'
gnm_to_ctg_connector                            = '___C___'
mini_assembly_to_16s_ctg_connector              = '___Mini___'
ctg_level_min_link                              = 3
min_aln_16s                                     = 500
min_cov_16s                                     = 30
mean_depth_dict_gnm                             = {}
mean_depth_dict_16s                             = {}
min_16s_gnm_multiple                            = 0
min_iden_16s                                    = 98
min_link_num                                    = 8
within_gnm_linkage_num_diff                     = 80
max_mini_assembly_link_num_diff_between_ctg_16s = 10
min_M_len_ctg                                   = 60
mismatch_cutoff = 2

stats_GapFilling_file                           = '%s/stats_GapFilling_gnm.txt'                             % step_2_wd
stats_GapFilling_file_filtered                  = '%s/stats_GapFilling_gnm_filtered.txt'                    % step_2_wd
stats_GapFilling_ctg                            = '%s/stats_GapFilling_ctg.txt'                             % step_2_wd

filter_mini_assembly_separately = True


############################################# get mini_assembly_to_16s_reads_dict #############################################

# mini_assembly_to_16s_reads_dict = {}
# mini_assembly_len_dict = {}
# current_read = ''
# current_read_ref_dict = dict()
# with open(sam_file_mini_assembly_reformatted_sorted_16s) as sam_file_mini_assembly_reformatted_sorted_16s_opened:
#     for each_read in sam_file_mini_assembly_reformatted_sorted_16s_opened:
#         each_read_split = each_read.strip().split('\t')
#         if each_read.startswith('@'):
#             mini_assembly_id = ''
#             mini_assembly_len = 0
#             for each_element in each_read_split:
#                 if each_element.startswith('SN:'):
#                     mini_assembly_id = each_element[3:]
#                 if each_element.startswith('LN:'):
#                     mini_assembly_len = int(each_element[3:])
#             mini_assembly_len_dict[mini_assembly_id] = mini_assembly_len
#         else:
#             cigar = each_read_split[5]
#             read_id = each_read_split[0]
#             read_id_base = '.'.join(read_id.split('.')[:-1])
#             read_strand = read_id.split('.')[-1]
#             ref_id = each_read_split[2]
#             ref_pos = int(each_read_split[3])
#
#             if current_read == '':
#                 current_read = read_id
#                 if cigar != '*':
#                     current_read_ref_dict[ref_id] = {ref_pos: cigar}
#
#             elif read_id == current_read:
#                 if cigar != '*':
#                     if ref_id not in current_read_ref_dict:
#                         current_read_ref_dict[ref_id] = {ref_pos: cigar}
#                     else:
#                         current_read_ref_dict[ref_id][ref_pos] = cigar
#             else:
#                 ################################### analysis previous read refs ####################################
#
#                 ########## get lowest mismatch for current read refs ##########
#
#                 # get r1_ref_cigar_set
#                 ref_cigar_set = set()
#                 for each_pos_dict in current_read_ref_dict.values():
#                     each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
#                     ref_cigar_set.update(each_pos_dict_values)
#
#                 ref_min_mismatch = get_min_mismatch_from_cigar_list(ref_cigar_set, min_M_len_ctg)
#
#                 ########## filter refs ##########
#
#                 r1_16s_refs_passed_qc = {}
#                 for each_ref in current_read_ref_dict:
#                     matched_pos_dict = current_read_ref_dict[each_ref]
#
#                     # one read need to mapped to one 16S only for one time
#                     if len(matched_pos_dict) == 1:
#                         ref_pos = list(matched_pos_dict.keys())[0]
#                         ref_cigar = matched_pos_dict[ref_pos]
#                         ref_cigar_splitted = cigar_splitter(ref_cigar)
#
#                         # check both end clip
#                         both_end_clp = check_both_ends_clipping(ref_cigar_splitted)
#                         if both_end_clp is False:
#                             # check mismatch
#                             aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(ref_cigar_splitted)
#                             if (ref_min_mismatch != 'NA'):
#                                 if (mismatch_pct <= ref_min_mismatch) and (mismatch_pct <= mismatch_cutoff):
#                                     # check aligned length
#                                     if aligned_len >= min_M_len_ctg:
#                                         # check if clp in the middle
#                                         clip_in_middle = False
#                                         if ('S' in ref_cigar) or ('s' in ref_cigar):
#                                             clip_in_middle = True
#                                             if (ref_cigar_splitted[0][-1] in ['S', 's']) and (ref_pos == 1):
#                                                 clip_in_middle = False
#                                             if (ref_cigar_splitted[-1][-1] in ['S', 's']):
#                                                 if (ref_pos + aligned_len - 1) == mini_assembly_len_dict[each_ref]:
#                                                     clip_in_middle = False
#
#                                         # exclude the ref if clp in the middle is True
#                                         if clip_in_middle is False:
#                                             if each_ref not in mini_assembly_to_16s_reads_dict:
#                                                 mini_assembly_to_16s_reads_dict[each_ref] = {current_read}
#                                             else:
#                                                 mini_assembly_to_16s_reads_dict[each_ref].add(current_read)
#
#                 ########################################### reset values ###########################################
#
#                 current_read = read_id
#                 current_read_ref_dict = dict()
#                 if cigar != '*':
#                     current_read_ref_dict[ref_id] = {ref_pos: cigar}
#
#
# ############################################# get mini_assembly_to_ctg_reads_dict #############################################
#
# mini_assembly_to_ctg_reads_dict = {}
# mini_assembly_len_dict = {}
# current_read = ''
# current_read_ref_dict = dict()
# with open(sam_file_mini_assembly_reformatted_sorted_ctg) as sam_file_mini_assembly_reformatted_sorted_ctg_opened:
#     for each_read in sam_file_mini_assembly_reformatted_sorted_ctg_opened:
#         each_read_split = each_read.strip().split('\t')
#         if each_read.startswith('@'):
#             mini_assembly_id = ''
#             mini_assembly_len = 0
#             for each_element in each_read_split:
#                 if each_element.startswith('SN:'):
#                     mini_assembly_id = each_element[3:]
#                 if each_element.startswith('LN:'):
#                     mini_assembly_len = int(each_element[3:])
#             mini_assembly_len_dict[mini_assembly_id] = mini_assembly_len
#         else:
#             cigar = each_read_split[5]
#             read_id = each_read_split[0]
#             read_id_base = '.'.join(read_id.split('.')[:-1])
#             read_strand = read_id.split('.')[-1]
#             ref_id = each_read_split[2]
#             ref_pos = int(each_read_split[3])
#
#             if current_read == '':
#                 current_read = read_id
#                 if cigar != '*':
#                     current_read_ref_dict[ref_id] = {ref_pos: cigar}
#
#             elif read_id == current_read:
#                 if cigar != '*':
#                     if ref_id not in current_read_ref_dict:
#                         current_read_ref_dict[ref_id] = {ref_pos: cigar}
#                     else:
#                         current_read_ref_dict[ref_id][ref_pos] = cigar
#             else:
#                 ################################### analysis previous read refs ####################################
#
#                 ########## get lowest mismatch for current read refs ##########
#
#                 # get r1_ref_cigar_set
#                 ref_cigar_set = set()
#                 for each_pos_dict in current_read_ref_dict.values():
#                     each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
#                     ref_cigar_set.update(each_pos_dict_values)
#
#                 ref_min_mismatch = get_min_mismatch_from_cigar_list(ref_cigar_set, min_M_len_ctg)
#
#                 ########## filter refs ##########
#
#                 r1_16s_refs_passed_qc = {}
#                 for each_ref in current_read_ref_dict:
#                     matched_pos_dict = current_read_ref_dict[each_ref]
#
#                     # one read need to mapped to one 16S only for one time
#                     if len(matched_pos_dict) == 1:
#                         ref_pos = list(matched_pos_dict.keys())[0]
#                         ref_cigar = matched_pos_dict[ref_pos]
#                         ref_cigar_splitted = cigar_splitter(ref_cigar)
#
#                         # check both end clip
#                         both_end_clp = check_both_ends_clipping(ref_cigar_splitted)
#                         if both_end_clp is False:
#                             # check mismatch
#                             aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(ref_cigar_splitted)
#                             if (ref_min_mismatch != 'NA'):
#                                 if (mismatch_pct <= ref_min_mismatch) and (mismatch_pct <= mismatch_cutoff):
#                                     # check aligned length
#                                     if aligned_len >= min_M_len_ctg:
#
#                                         # check if clp in the middle
#                                         clip_in_middle = False
#                                         if ('S' in ref_cigar) or ('s' in ref_cigar):
#                                             clip_in_middle = True
#                                             if (ref_cigar_splitted[0][-1] in ['S', 's']) and (ref_pos == 1):
#                                                 clip_in_middle = False
#                                             if (ref_cigar_splitted[-1][-1] in ['S', 's']):
#                                                 if (ref_pos + aligned_len - 1) == mini_assembly_len_dict[each_ref]:
#                                                     clip_in_middle = False
#
#                                         # exclude the ref if clp in the middle is True
#                                         if clip_in_middle is False:
#                                             if each_ref not in mini_assembly_to_ctg_reads_dict:
#                                                 mini_assembly_to_ctg_reads_dict[each_ref] = {current_read}
#                                             else:
#                                                 mini_assembly_to_ctg_reads_dict[each_ref].add(current_read)
#
#                 ########################################### reset values ###########################################
#
#                 current_read = read_id
#                 current_read_ref_dict = dict()
#                 if cigar != '*':
#                     current_read_ref_dict[ref_id] = {ref_pos: cigar}
#
#
# mini_assembly_to_16s_reads_handle = open(mini_assembly_to_16s_reads, 'w')
# for each_mini_assembly in mini_assembly_to_16s_reads_dict:
#     mini_assembly_to_16s_reads_handle.write('%s\t%s\n' % (each_mini_assembly, ','.join(mini_assembly_to_16s_reads_dict[each_mini_assembly])))
# mini_assembly_to_16s_reads_handle.close()
#
# mini_assembly_to_ctg_reads_handle = open(mini_assembly_to_ctg_reads, 'w')
# for each_mini_assembly in mini_assembly_to_ctg_reads_dict:
#     mini_assembly_to_ctg_reads_handle.write('%s\t%s\n' % (each_mini_assembly, ','.join(mini_assembly_to_ctg_reads_dict[each_mini_assembly])))
# mini_assembly_to_ctg_reads_handle.close()


############################################# get_GapFilling_stats #############################################

pairwise_16s_iden_dict = blast_results_to_pairwise_16s_iden_dict(blast_results_all_vs_all_16s, min_aln_16s, min_cov_16s)

if filter_mini_assembly_separately is False:

    get_GapFilling_stats_by_assembly(free_living_16s_ref_file,
                                     free_living_ctg_ref_file,
                                     mini_assembly_to_16s_reads,
                                     mini_assembly_to_ctg_reads,
                                     ctg_level_min_link,
                                     mini_assembly_to_16s_ctg_connector,
                                     gnm_to_ctg_connector,
                                     marker_to_ctg_gnm_Key_connector,
                                     within_gnm_linkage_num_diff,
                                     max_mini_assembly_link_num_diff_between_ctg_16s,
                                     stats_GapFilling_ctg,
                                     stats_GapFilling_file)

    filter_linkages_iteratively(stats_GapFilling_file, 'Number', pairwise_16s_iden_dict, mean_depth_dict_gnm, mean_depth_dict_16s, min_16s_gnm_multiple, min_iden_16s, min_link_num, min_link_num, within_gnm_linkage_num_diff, stats_GapFilling_file_filtered)

else:
    get_GapFilling_stats_by_assembly_separately(free_living_16s_ref_file,
                                                free_living_ctg_ref_file,
                                                mini_assembly_to_16s_reads,
                                                mini_assembly_to_ctg_reads,
                                                ctg_level_min_link,
                                                mini_assembly_to_16s_ctg_connector,
                                                gnm_to_ctg_connector,
                                                marker_to_ctg_gnm_Key_connector,

                                                within_gnm_linkage_num_diff,
                                                max_mini_assembly_link_num_diff_between_ctg_16s,
                                                stats_GapFilling_ctg,
                                                stats_GapFilling_file)

    #filter_linkages_iteratively(stats_GapFilling_file, 'Number', pairwise_16s_iden_dict, mean_depth_dict_gnm, mean_depth_dict_16s, min_16s_gnm_multiple, min_iden_16s, min_link_num, min_link_num, within_gnm_linkage_num_diff, stats_GapFilling_file_filtered)

