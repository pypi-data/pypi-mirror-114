#!/usr/bin/env python3

# Copyright (C) 2020, Weizhi Song, Torsten Thomas.
# songwz03@gmail.com or t.thomas@unsw.edu.au

# MarkerMAG is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# MarkerMAG is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import shutil
import argparse
import numpy as np
import pandas as pd
import seaborn as sns
from Bio import SeqIO
from Bio.Seq import Seq
import multiprocessing as mp
from datetime import datetime
import plotly.graph_objects as go
from Bio.SeqRecord import SeqRecord
from distutils.spawn import find_executable

link_Marker_MAG_usage = '''
=================================== MarkerMAG example commands ===================================

# example commands
MarkerMAG link -p Test -r1 R1.fasta -r2 R2.fasta -marker 16S_seqs.fa -mag MAG_folder -x fa -t 6

==================================================================================================
'''


def get_rc(seq_in):
    seq_in_rc = str(SeqRecord(Seq(seq_in)).reverse_complement().seq)
    return seq_in_rc


def force_create_folder(folder_to_create):
    if os.path.isdir(folder_to_create):
        shutil.rmtree(folder_to_create, ignore_errors=True)
        if os.path.isdir(folder_to_create):
            shutil.rmtree(folder_to_create, ignore_errors=True)
    os.mkdir(folder_to_create)


def report_and_log(message_for_report, log_file, keep_quiet):

    time_format = '[%Y-%m-%d %H:%M:%S]'
    with open(log_file, 'a') as log_handle:
        log_handle.write('%s %s\n' % ((datetime.now().strftime(time_format)), message_for_report))

    if keep_quiet is False:
        print('%s %s' % ((datetime.now().strftime(time_format)), message_for_report))


def sep_path_basename_ext(file_in):

    # separate path and file name
    file_path, file_name = os.path.split(file_in)
    if file_path == '':
        file_path = '.'

    # separate file basename and extension
    file_basename, file_extension = os.path.splitext(file_name)

    return file_path, file_basename, file_extension


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


def split_list(list_in, subset_num):

    list_in_formatted = [i for i in list_in]

    # get the number of element per subset
    file_num_per_folder = round(len(list_in_formatted) / subset_num)

    n = 1
    lol_out = []
    while n <= subset_num:

        if n < subset_num:
            current_subset_elements = {i for i in list_in_formatted[(file_num_per_folder * (n - 1)):(file_num_per_folder * n)]}
            lol_out.append(current_subset_elements)
        else:
            current_subset_elements = {i for i in list_in_formatted[(file_num_per_folder * (n - 1)):]}
            lol_out.append(current_subset_elements)

        n += 1

    return lol_out


def sort_csv_by_col(file_in, file_out, col_header):
    df_in        = pd.read_csv(file_in)
    df_in_sorted = df_in.sort_values(by=[col_header], ascending=False)
    df_in_sorted.to_csv(file_out, index=False)


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


def get_mean_iden_list(linked_16s_list, pairwise_16s_iden_dict):

    mean_iden_list = []
    for each_16s_1 in linked_16s_list:
        current_16s_iden_list = []
        for each_16s_2 in linked_16s_list:
            if each_16s_1 != each_16s_2:
                key = '__|__'.join(sorted([each_16s_1, each_16s_2]))
                key_iden = pairwise_16s_iden_dict.get(key, 0)
                current_16s_iden_list.append(key_iden)
        mean_iden = sum(current_16s_iden_list) / len(current_16s_iden_list)
        mean_iden = float("{0:.3f}".format(mean_iden))
        mean_iden_list.append(mean_iden)

    return mean_iden_list


def filter_linkages_iteratively(file_in, sort_by_col_header, pairwise_16s_iden_dict, within_genome_16s_divergence_cutoff, min_linkages, min_linkages_for_uniq_linked_16s, within_gnm_linkage_num_diff, file_out):

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


def get_gnm_16s_to_ignore(link_stats_combined_sorted, pairwise_16s_iden_dict, min_iden_16s, min_linking_num):
    # get gnm_best_16s_dict
    gnm_best_16s_link_num_dict = {}
    gnm_best_16s_dict = {}
    for each_match in open(link_stats_combined_sorted):
        if not each_match.endswith(',Number\n'):
            match_split = each_match.strip().split(',')
            MarkerGene = match_split[0][12:]
            GenomicSeq = match_split[1][12:]
            linkage_num = int(match_split[2])
            if linkage_num >= min_linking_num:
                if GenomicSeq not in gnm_best_16s_link_num_dict:
                    gnm_best_16s_link_num_dict[GenomicSeq] = linkage_num
                    gnm_best_16s_dict[GenomicSeq] = {MarkerGene}
                else:
                    if linkage_num == gnm_best_16s_link_num_dict[GenomicSeq]:
                        gnm_best_16s_dict[GenomicSeq].add(MarkerGene)

    # get gnm to ignore and best markers to ignore
    gnm_to_ignore = set()
    markers_to_ignore_best = set()
    for each_gnm in gnm_best_16s_dict:
        gnm_best_16s_list = gnm_best_16s_dict[each_gnm]
        if len(gnm_best_16s_list) > 1:
            all_combination_set = set()
            for left_16s in gnm_best_16s_list:
                for right_16s in gnm_best_16s_list:
                    if left_16s != right_16s:
                        marker_to_marker_key = '__|__'.join(sorted([left_16s, right_16s]))
                        all_combination_set.add(marker_to_marker_key)

            best_16s_pairwise_iden_list = []
            for each_combination in all_combination_set:
                marker_to_marker_iden = pairwise_16s_iden_dict.get(each_combination, 0)
                best_16s_pairwise_iden_list.append(marker_to_marker_iden)

            min_best_16s_iden = min(best_16s_pairwise_iden_list)
            if min_best_16s_iden <= min_iden_16s:
                gnm_to_ignore.add(each_gnm)
                for j in gnm_best_16s_list:
                    markers_to_ignore_best.add(j)

    # get all markers to ignore
    markers_to_ignore_all = set()
    for each_pair_16s in pairwise_16s_iden_dict:
        each_pair_16s_split = each_pair_16s.split('__|__')
        l_16s = each_pair_16s_split[0]
        r_16s = each_pair_16s_split[1]
        iden_16s = pairwise_16s_iden_dict[each_pair_16s]
        if iden_16s >= min_iden_16s:
            if l_16s in markers_to_ignore_best:
                markers_to_ignore_all.add(r_16s)
            if r_16s in markers_to_ignore_best:
                markers_to_ignore_all.add(l_16s)

    return gnm_to_ignore, markers_to_ignore_best, markers_to_ignore_all


def filter_linkages_iteratively_new2(sorted_file_in, pairwise_16s_iden_dict, within_genome_16s_divergence_cutoff,
                                     marker_len_dict,
                                     min_linkages, within_gnm_linkage_num_diff, file_out,
                                     marker_to_gnm_linking_cigar_dict_16s_side,
                                     marker_to_gnm_linking_cigar_dict_ctg_side,
                                     marker_to_ctg_gnm_Key_connector):
    # filter linkage
    file_out_handle = open(file_out, 'w')
    MarkerGene_with_assignment = set()
    MarkerGene_to_be_ignored = set()
    gnm_with_assignment = set()
    gnm_best_16s_link_num_dict = {}
    gnm_assigned_16s_dict = {}
    for each_match in open(sorted_file_in):
        if each_match.startswith('MarkerGene,GenomicSeq,Number'):
            file_out_handle.write(each_match)
        else:
            match_split = each_match.strip().split(',')
            MarkerGene = match_split[0][12:]
            MarkerGene_len = marker_len_dict[MarkerGene]
            GenomicSeq = match_split[1][12:]
            linkage_num = int(match_split[2])
            MarkerGene_to_GenomicSeq_key = '%s%s%s' % (MarkerGene, marker_to_ctg_gnm_Key_connector, GenomicSeq)

            if linkage_num >= min_linkages:

                ########### quality pre-check (I guess) ###########
                # failed linkage will be added to MarkerGene_to_be_ignored

                # first check if linked to conserved regions ???
                already_assigned_16s_list = []
                iden_with_already_assigned_16s_list = []
                for already_assigned_16s in MarkerGene_with_assignment:
                    current_key = '__|__'.join(sorted([already_assigned_16s, MarkerGene]))
                    current_key_value = pairwise_16s_iden_dict.get(current_key, 0)
                    already_assigned_16s_list.append(already_assigned_16s)
                    iden_with_already_assigned_16s_list.append(current_key_value)

                if len(already_assigned_16s_list) > 0:
                    sorted_best_matched_16s_list = [[seq_id, mean_iden] for mean_iden, seq_id in sorted(
                        zip(iden_with_already_assigned_16s_list, already_assigned_16s_list), reverse=True)]
                    best_matched_marker = sorted_best_matched_16s_list[0][0]
                    best_matched_marker_iden = sorted_best_matched_16s_list[0][1]
                    best_matched_marker_len = marker_len_dict[best_matched_marker]
                    if ((best_matched_marker_len - MarkerGene_len) >= 200) and (best_matched_marker_iden >= 99):

                        # get clp pct at gnm level
                        linking_cigar_16s_side = marker_to_gnm_linking_cigar_dict_16s_side[MarkerGene_to_GenomicSeq_key]
                        linking_cigar_ctg_side = marker_to_gnm_linking_cigar_dict_ctg_side[MarkerGene_to_GenomicSeq_key]
                        linking_cigar_16s_side_clp = [i for i in linking_cigar_16s_side if (('S' in i) or ('s' in i))]
                        linking_cigar_ctg_side_clp = [i for i in linking_cigar_ctg_side if (('S' in i) or ('s' in i))]
                        linking_cigar_16s_side_clp_pct = len(linking_cigar_16s_side_clp) * 100 / len(
                            linking_cigar_16s_side)
                        linking_cigar_ctg_side_clp_pct = len(linking_cigar_ctg_side_clp) * 100 / len(
                            linking_cigar_ctg_side)

                        if (linking_cigar_16s_side_clp_pct >= 60) and (linking_cigar_ctg_side_clp_pct >= 60):
                            MarkerGene_to_be_ignored.add(MarkerGene)

                ###################### process here ######################

                # get gnm_to_ignore, markers_to_ignore_best, markers_to_ignore_all
                gnm_to_ignore_multi_best, markers_to_ignore_multi_best, markers_to_ignore_multi_best_all = get_gnm_16s_to_ignore(
                    sorted_file_in,
                    pairwise_16s_iden_dict,
                    within_genome_16s_divergence_cutoff,
                    linkage_num)

                if (MarkerGene not in markers_to_ignore_multi_best_all) and (
                        GenomicSeq not in gnm_to_ignore_multi_best):
                    if (MarkerGene not in MarkerGene_with_assignment) and (MarkerGene not in MarkerGene_to_be_ignored):

                        if GenomicSeq not in gnm_with_assignment:
                            file_out_handle.write(
                                'MarkerGene__%s,GenomicSeq__%s,%s\n' % (MarkerGene, GenomicSeq, linkage_num))
                            gnm_with_assignment.add(GenomicSeq)
                            MarkerGene_with_assignment.add(MarkerGene)
                            gnm_assigned_16s_dict[GenomicSeq] = [MarkerGene]
                            gnm_best_16s_link_num_dict[GenomicSeq] = linkage_num
                        else:
                            gnm_assigned_16s_list = gnm_assigned_16s_dict[GenomicSeq]
                            gnm_best_assigned_16s_link_num = gnm_best_16s_link_num_dict[GenomicSeq]

                            # get iden list with already assigned 16s
                            iden_with_assigned_16s_list = []
                            for each_assigned_16s in gnm_assigned_16s_list:
                                marker_to_maker_key = '__|__'.join(sorted([MarkerGene, each_assigned_16s]))
                                marker_key_iden = pairwise_16s_iden_dict.get(marker_to_maker_key, 0)
                                iden_with_assigned_16s_list.append(marker_key_iden)

                            # get min iden with already assigned 16s
                            min_iden_with_assigned_16s = min(iden_with_assigned_16s_list)

                            # if min iden higher than within_genome_16s_divergence_cutoff
                            if min_iden_with_assigned_16s >= within_genome_16s_divergence_cutoff:

                                # filter here
                                if (linkage_num * 100 / gnm_best_assigned_16s_link_num) >= within_gnm_linkage_num_diff:
                                    file_out_handle.write(
                                        'MarkerGene__%s,GenomicSeq__%s,%s\n' % (MarkerGene, GenomicSeq, linkage_num))
                                    MarkerGene_with_assignment.add(MarkerGene)
                                    gnm_assigned_16s_dict[GenomicSeq].append(MarkerGene)
                                else:
                                    MarkerGene_to_be_ignored.add(MarkerGene)
    file_out_handle.close()


def combine_paired_and_clipping_linkages(paired_linkages, clipping_linkages, file_out_summary, file_out_intersect_linkages):

    # file in:   file_in_paired    and  file_in_clipping
    # file out:  file_out_summary  and  file_out_intersection

    combined_paired_and_clipping_keys = set()

    # read in paired linkages
    paired_linkages_dict = {}
    for paired_linkage in open(paired_linkages):
        if not paired_linkage.startswith('MarkerGene,GenomicSeq,Number'):
            paired_linkage_split = paired_linkage.strip().split(',')
            paired_key = '%s__|__%s' % (paired_linkage_split[0], paired_linkage_split[1])
            paired_value = int(paired_linkage_split[2])
            paired_linkages_dict[paired_key] = paired_value
            combined_paired_and_clipping_keys.add(paired_key)

    # read in clipping linkages
    clipping_linkages_dict = {}
    for clipping_linkage in open(clipping_linkages):
        if not clipping_linkage.startswith('MarkerGene,GenomicSeq,Number'):
            clipping_linkage_split = clipping_linkage.strip().split(',')
            clipping_key = '%s__|__%s' % (clipping_linkage_split[0], clipping_linkage_split[1])
            clipping_value = int(clipping_linkage_split[2])
            clipping_linkages_dict[clipping_key] = clipping_value
            combined_paired_and_clipping_keys.add(clipping_key)

    combined_paired_and_clipping_keys_sorted = sorted([i for i in combined_paired_and_clipping_keys])

    # combine paired and clipping linkages
    file_out_summary_handle = open(file_out_summary, 'w')
    file_out_intersect_linkages_handle = open(file_out_intersect_linkages, 'w')
    file_out_summary_handle.write('MarkerGene\tGenomicSeq\tPaired\tClipping\n')
    file_out_intersect_linkages_handle.write('MarkerGene,GenomicSeq,Number\n')
    for each_key in combined_paired_and_clipping_keys_sorted:

        current_key_paired_value = 0
        if each_key in paired_linkages_dict:
            current_key_paired_value = paired_linkages_dict[each_key]

        current_key_clipping_value = 0
        if each_key in clipping_linkages_dict:
            current_key_clipping_value = clipping_linkages_dict[each_key]

        if current_key_paired_value > 0:

            current_key_combined = current_key_paired_value + current_key_clipping_value

            # write out
            file_out_summary_handle.write('%s\t%s\t%s\n' % ('\t'.join([i[12:] for i in each_key.split('__|__')]), current_key_paired_value, current_key_clipping_value))
            file_out_intersect_linkages_handle.write('%s,%s\n' % (','.join(each_key.split('__|__')), current_key_combined))

    file_out_summary_handle.close()
    file_out_intersect_linkages_handle.close()


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


def get_best_ctg_or_16s_for_gap_seq_iteratively(file_in, sort_by_col_header, min_linkages, file_out):

    file_in_path, file_in_basename, file_in_extension = sep_path_basename_ext(file_in)
    file_in_sorted = '%s/%s_sorted%s' % (file_in_path, file_in_basename, file_in_extension)

    # sort file in
    sort_csv_by_col(file_in, file_in_sorted, sort_by_col_header)

    # fileter linkage
    file_out_handle = open(file_out, 'w')
    gap_seq_with_assignment = set()
    for each_match in open(file_in_sorted):
        if each_match.startswith('Gap_seq,'):
            file_out_handle.write(each_match)
        else:
            match_split = each_match.strip().split(',')
            gap_seq_id = match_split[0]
            linkage_num = int(match_split[2])
            if (linkage_num >= min_linkages) and (gap_seq_id not in gap_seq_with_assignment):
                file_out_handle.write(each_match)
                gap_seq_with_assignment.add(gap_seq_id)
    file_out_handle.close()


def get_accuracy(file_in, marker_num):

    linkage_num_total = 0
    linkage_num_correct = 0
    recovered_markers = set()
    for each_match in open(file_in):
        if not each_match.startswith('MarkerGene\tGenomicSeq\tLinkage'):
            match_split = each_match.strip().split('\t')
            linkage_num = int(match_split[2])
            MarkerGene_genome = match_split[0][:2]
            GenomicSeq_genome = match_split[1]

            linkage_num_total += linkage_num
            if MarkerGene_genome == GenomicSeq_genome:
                linkage_num_correct += linkage_num
                recovered_markers.add(match_split[0])

    marker_recovery = float("{0:.2f}".format(len(recovered_markers)*100/marker_num))

    link_accuracy = 0
    if linkage_num_total > 0:
        link_accuracy = float("{0:.2f}".format(linkage_num_correct*100/linkage_num_total))

    marker_recovery = '%s/%s(%s)' % (len(recovered_markers), marker_num, marker_recovery)

    return marker_recovery, link_accuracy, recovered_markers


def get_accuracy_by_genome(file_in, mag_folder, mag_file_extension):

    # get MAG file list
    mag_file_re             = '%s/*%s' % (mag_folder, mag_file_extension)
    mag_file_list           = [os.path.basename(file_name) for file_name in glob.glob(mag_file_re)]
    mag_file_list_no_ext    = {'.'.join(i.split('.')[:-1]) for i in mag_file_list}

    genome_with_right_16s_assignment_tmp = set()
    genome_with_wrong_16s_assignment = set()
    for each_match in open(file_in):
        if not each_match.startswith('MarkerGene\tGenomicSeq\tLinkage'):
            match_split = each_match.strip().split('\t')
            MarkerGene_genome = match_split[0][:2]
            GenomicSeq_genome = match_split[1]

            if GenomicSeq_genome == MarkerGene_genome:
                genome_with_right_16s_assignment_tmp.add(GenomicSeq_genome)
            else:
                genome_with_wrong_16s_assignment.add(GenomicSeq_genome)

    genome_with_right_16s_assignment_always = []
    genome_without_right_16s_assignment = []
    for input_genome in mag_file_list_no_ext:
        if (input_genome in genome_with_right_16s_assignment_tmp) and (input_genome not in genome_with_wrong_16s_assignment):
            genome_with_right_16s_assignment_always.append(input_genome)
        else:
            genome_without_right_16s_assignment.append(input_genome)


    marker_gene_assignment_rate = float("{0:.2f}".format(len(genome_with_right_16s_assignment_always)*100/len(mag_file_list_no_ext)))

    marker_gene_assignment_accuracy = 0
    if (len(genome_with_right_16s_assignment_always) + len(genome_with_wrong_16s_assignment)) > 0:
        marker_gene_assignment_accuracy = float("{0:.2f}".format(len(genome_with_right_16s_assignment_always)*100/(len(genome_with_right_16s_assignment_always) + len(genome_with_wrong_16s_assignment))))
    marker_gene_assignment_rate = '%s/%s(%s)' % (len(genome_with_right_16s_assignment_always), len(mag_file_list_no_ext), marker_gene_assignment_rate)

    return marker_gene_assignment_rate, marker_gene_assignment_accuracy, genome_with_right_16s_assignment_always, genome_without_right_16s_assignment


def rename_seq(ctg_file_in, ctg_file_out, prefix, str_connector):

    ctg_file_out_handle = open(ctg_file_out, 'w')
    for Seq_record in SeqIO.parse(ctg_file_in, 'fasta'):
        Seq_record.id = '%s%s%s' % (prefix, str_connector, Seq_record.id)
        SeqIO.write(Seq_record, ctg_file_out_handle, 'fasta')
    ctg_file_out_handle.close()


def SeqIO_convert_worker(argument_list):

    file_in         = argument_list[0]
    file_in_fmt     = argument_list[1]
    file_out        = argument_list[2]
    file_out_fmt    = argument_list[3]
    SeqIO.convert(file_in, file_in_fmt, file_out, file_out_fmt)


def get_max_clp_and_index(r1_cigar_list, r2_cigar_list):

    r1_cigar_list_split = [cigar_splitter(i) for i in r1_cigar_list]
    r2_cigar_list_split = [cigar_splitter(i) for i in r2_cigar_list]

    r1_cigar_list_split_only_clp = []
    for each_r1_cigar_split in r1_cigar_list_split:
        clp_len_l = 0
        if each_r1_cigar_split[0][-1] in ['S', 's']:
            clp_len_l = int(each_r1_cigar_split[0][:-1])
        clp_len_r = 0
        if each_r1_cigar_split[-1][-1] in ['S', 's']:
            clp_len_r = int(each_r1_cigar_split[-1][:-1])
        r1_cigar_list_split_only_clp.append([clp_len_l, clp_len_r])

    r2_cigar_list_split_only_clp = []
    for each_r2_cigar_split in r2_cigar_list_split:
        clp_len_l = 0
        if each_r2_cigar_split[0][-1] in ['S', 's']:
            clp_len_l = int(each_r2_cigar_split[0][:-1])
        clp_len_r = 0
        if each_r2_cigar_split[-1][-1] in ['S', 's']:
            clp_len_r = int(each_r2_cigar_split[-1][:-1])
        r2_cigar_list_split_only_clp.append([clp_len_l, clp_len_r])

    cigar_list_split_only_clp_r1_r2 = [r1_cigar_list_split_only_clp, r2_cigar_list_split_only_clp]

    max_value = 0
    max_value_index = ''
    for num_list_1 in cigar_list_split_only_clp_r1_r2[0]:
        if num_list_1[0] > max_value:
            max_value = num_list_1[0]
            max_value_index = 'r1_l'
        if num_list_1[1] > max_value:
            max_value = num_list_1[1]
            max_value_index = 'r1_r'
    for num_list_2 in cigar_list_split_only_clp_r1_r2[1]:
        if num_list_2[0] > max_value:
            max_value = num_list_2[0]
            max_value_index = 'r2_l'
        if num_list_2[1] > max_value:
            max_value = num_list_2[1]
            max_value_index = 'r2_r'

    # get the best cigar
    best_cigar = ''
    if max_value_index == 'r1_l':
        if best_cigar == '':
            for each_cigar in r1_cigar_list:
                if (each_cigar.startswith('%sS' % max_value)) or (each_cigar.startswith('%ss' % max_value)):
                    best_cigar = each_cigar
    elif max_value_index == 'r1_r':
        if best_cigar == '':
            for each_cigar in r1_cigar_list:
                if (each_cigar.endswith('%sS' % max_value)) or (each_cigar.endswith('%ss' % max_value)):
                    best_cigar = each_cigar
    elif max_value_index == 'r2_l':
        if best_cigar == '':
            for each_cigar in r2_cigar_list:
                if (each_cigar.startswith('%sS' % max_value)) or (each_cigar.startswith('%ss' % max_value)):
                    best_cigar = each_cigar
    elif max_value_index == 'r2_r':
        if best_cigar == '':
            for each_cigar in r2_cigar_list:
                if (each_cigar.endswith('%sS' % max_value)) or (each_cigar.endswith('%ss' % max_value)):
                    best_cigar = each_cigar

    return best_cigar, max_value, max_value_index


class MappingRecord:

    def __init__(self):

        #################### overall ####################

        self.qualified_reads = False

        #################### round 1 16s ####################

        self.consider_r1_unmapped_mate = False
        self.consider_r2_unmapped_mate = False

        self.r1_16s_ref_dict = dict()
        self.r2_16s_ref_dict = dict()

        self.r1_16s_refs_lowest_mismatch = None
        self.r2_16s_refs_lowest_mismatch = None

        self.r1_16s_refs_no_ignored = dict()
        self.r2_16s_refs_no_ignored = dict()
        self.shared_16s_refs_no_ignored = dict()

        self.both_mapped_to_16s = False

        #################### round 1 ctg ####################

        self.r1_ctg_ref_dict = dict()
        self.r2_ctg_ref_dict = dict()

        self.r1_ctg_refs_lowest_mismatch = None
        self.r2_ctg_refs_lowest_mismatch = None

        self.r1_ctg_refs_no_ignored = dict()
        self.r2_ctg_refs_no_ignored = dict()
        self.shared_ctg_refs_no_ignored = dict()

        self.matched_to_ctg = False

        #################### round 2 ####################

        self.qualified_reads_rd2 = False

        self.r1_ctg_ref_dict_rd2 = dict()
        self.r2_ctg_ref_dict_rd2 = dict()

        self.r1_ctg_refs_lowest_mismatch_rd2 = None
        self.r2_ctg_refs_lowest_mismatch_rd2 = None

        #################### round 2 mini_assembly ####################

        self.r1_mini_ref_dict = dict()
        self.r2_mini_ref_dict = dict()

        self.r1_mini_refs_lowest_mismatch = None
        self.r2_mini_refs_lowest_mismatch = None

        self.r1_mini_refs_no_ignored = dict()
        self.r2_mini_refs_no_ignored = dict()
        self.shared_mini_refs_no_ignored = dict()


class LinkingRecord:

    def __init__(self):

        self.linked_seq_l = ''
        self.linked_seq_r = ''

        self.linked_seq_len_l = 0
        self.linked_seq_len_r = 0

        self.linking_reads_base = []

        self.linking_reads_l = []
        self.linking_reads_r = []

        self.linking_cigar_l = []
        self.linking_cigar_r = []

        self.linking_pos_l = []
        self.linking_pos_r = []

        self.min_dist_to_end_l = []
        self.min_dist_to_end_r = []


def get_cigar_aln_len(cigar_splitted):
    # aligned_len: M I X =
    aligned_len = 0
    for each_part in cigar_splitted:
        each_part_len = int(each_part[:-1])
        each_part_cate = each_part[-1]
        # get aligned_len
        if each_part_cate in {'M', 'm', 'I', 'i', 'X', 'x', '='}:
            aligned_len += each_part_len
    return aligned_len


def check_cigar_quality(cigar_str, consider_ref_min_mismatch, ref_min_mismatch, mismatch_cutoff, min_M_len, ref_pos, marker_len):

    # check the following:
    # 1. both end clip  2. mismatch     3. aligned length   4. clp in the middle    5. ref_min_mismatch

    cigar_splitted = cigar_splitter(cigar_str)
    qualified_cigar = False

    # check both end clip
    both_end_clp = check_both_ends_clipping(cigar_splitted)
    if both_end_clp is False:
        # check mismatch
        aln_len, aln_pct, clp_len, clp_pct, mismatch_pct = get_cigar_stats(cigar_splitted)

        # check mismatch
        passed_mismatch_check = False
        if consider_ref_min_mismatch is False:
            if mismatch_pct <= mismatch_cutoff:
                passed_mismatch_check = True
        else:
            if ref_min_mismatch != 'NA':
                if (mismatch_pct <= ref_min_mismatch) and (mismatch_pct <= mismatch_cutoff):
                    passed_mismatch_check = True

        if passed_mismatch_check is True:
            # check aligned length
            if aln_len >= min_M_len:
                # check if clp in the middle
                clip_in_middle = False
                if ('S' in cigar_str) or ('s' in cigar_str):
                    clip_in_middle = True
                    if (cigar_splitted[0][-1] in ['S', 's']) and (ref_pos == 1):
                        clip_in_middle = False
                    if (cigar_splitted[-1][-1] in ['S', 's']):
                        if (ref_pos + aln_len - 1) == marker_len:
                            clip_in_middle = False

                if clip_in_middle is False:
                    qualified_cigar = True

    return qualified_cigar


def get_qualified_ref_dict(ref_dict, ref_len_dict, ref_min_mismatch, min_M_len, mismatch_cutoff, refs_to_ignore):

    refs_passed_qc = {}
    refs_passed_qc_with_pos = {}

    for each_ref in ref_dict:

        # one read can only mapped to on ref once
        matched_pos_dict = ref_dict[each_ref]
        if len(matched_pos_dict) > 1:
            refs_to_ignore.add(each_ref)
        else:
            ref_pos = list(matched_pos_dict.keys())[0]
            ref_cigar = matched_pos_dict[ref_pos]
            qualified_cigar = check_cigar_quality(ref_cigar, True, ref_min_mismatch, mismatch_cutoff, min_M_len, ref_pos, ref_len_dict[each_ref])

            if qualified_cigar is False:
                refs_to_ignore.add(each_ref)
            else:
                refs_passed_qc[each_ref] = [ref_cigar]
                refs_passed_qc_with_pos[each_ref] = {ref_pos: ref_cigar}

    return refs_passed_qc, refs_passed_qc_with_pos


def get_short_cigar_pct(cigar_list, short_M_len):
    short_cigar_num = 0
    for each_cigar in cigar_list:
        aln_len, aln_pct, clp_len, clp_pct, mis_pct = get_cigar_stats(cigar_splitter(each_cigar))
        if aln_len <= short_M_len:
            short_cigar_num += 1
    short_cigar_pct = short_cigar_num * 100 / len(cigar_list)
    return short_cigar_pct


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


def get_sankey_plot(node_list, source_list, target_list, value_list, color_list, plot_title, plot_height, output_html):

    node_index_dict = {y: x for x, y in enumerate(node_list)}
    source_index = [node_index_dict[x] for x in source_list]
    target_index = [node_index_dict[x] for x in target_list]

    # https://anvil.works/docs/api/plotly.graph_objs.sankey
    fig = go.Figure(data=[go.Sankey(node=dict(label=node_list,  # line=0,
                                              pad=5,  # space between node
                                              thickness=12,  # node width
                                              line=dict(width=0)),  # set width of node border to 0
                                    link=dict(source=source_index,
                                              target=target_index,
                                              value=value_list,
                                              color=color_list))])

    fig.update_layout(autosize=False, width=1200, height=plot_height, margin=dict(l=50, r=50, b=50, t=125), paper_bgcolor="white", title=plot_title)
    fig.update_traces(textfont_size=11)
    fig.write_html(output_html)


def sankey_linkages(combined_linkage_file_ctg_level, linkage_plot_rd1_html, linkage_plot_rd2_html):

    dict_for_sankey_key_connector   = '___X___'

    linkage_num_dict_rd1 = {}
    linkage_num_dict_rd2 = {}
    ctg_to_gnm_dict_rd1 = {}
    ctg_to_gnm_dict_rd2 = {}
    node_set_rd1 = set()
    node_set_rd2 = set()
    genome_set_rd1 = set()
    genome_set_rd2 = set()
    contig_set_rd1 = set()
    contig_set_rd2 = set()
    marker_gene_set_rd1 = set()
    marker_gene_set_rd2 = set()
    for each_linkage in open(combined_linkage_file_ctg_level):
        if not each_linkage.startswith('Marker___Genome(total)\tContig\tRd1\tRd2'):
            each_linkage_split = each_linkage.strip().split('\t')

            marker_id = each_linkage_split[0].split('___')[0]
            gnm_id = each_linkage_split[0].split('___')[1].split('(')[0]
            ctg_id = each_linkage_split[1]
            total_link_num = int(each_linkage_split[2]) + int(each_linkage_split[3])
            marker_to_ctg_key = '%s%s%s' % (marker_id, dict_for_sankey_key_connector, ctg_id)
            ctg_to_gnm_key = '%s%s%s' % (ctg_id, dict_for_sankey_key_connector, gnm_id)

            if int(each_linkage_split[3]) == 0:
                genome_set_rd1.add(gnm_id)
                contig_set_rd1.add(ctg_id)
                marker_gene_set_rd1.add(marker_id)
                node_set_rd1.add(marker_id)
                node_set_rd1.add(ctg_id)
                node_set_rd1.add(gnm_id)

                if ctg_id not in ctg_to_gnm_dict_rd1:
                    ctg_to_gnm_dict_rd1[ctg_id] = gnm_id

                if marker_to_ctg_key not in linkage_num_dict_rd1:
                    linkage_num_dict_rd1[marker_to_ctg_key] = total_link_num
                else:
                    linkage_num_dict_rd1[marker_to_ctg_key] += total_link_num

                if ctg_to_gnm_key not in linkage_num_dict_rd1:
                    linkage_num_dict_rd1[ctg_to_gnm_key] = total_link_num
                else:
                    linkage_num_dict_rd1[ctg_to_gnm_key] += total_link_num

            if int(each_linkage_split[2]) == 0:
                genome_set_rd2.add(gnm_id)
                contig_set_rd2.add(ctg_id)
                marker_gene_set_rd2.add(marker_id)
                node_set_rd2.add(marker_id)
                node_set_rd2.add(ctg_id)
                node_set_rd2.add(gnm_id)
                if ctg_id not in ctg_to_gnm_dict_rd2:
                    ctg_to_gnm_dict_rd2[ctg_id] = gnm_id

                if marker_to_ctg_key not in linkage_num_dict_rd2:
                    linkage_num_dict_rd2[marker_to_ctg_key] = total_link_num
                else:
                    linkage_num_dict_rd2[marker_to_ctg_key] += total_link_num

                if ctg_to_gnm_key not in linkage_num_dict_rd2:
                    linkage_num_dict_rd2[ctg_to_gnm_key] = total_link_num
                else:
                    linkage_num_dict_rd2[ctg_to_gnm_key] += total_link_num

    #################### plot rd1 linkages ####################

    source_list_rd1 = []
    target_list_rd1 = []
    value_list_rd1 = []
    for each_rd1_linkage in linkage_num_dict_rd1:
        each_rd1_linkage_split = each_rd1_linkage.split(dict_for_sankey_key_connector)
        source_list_rd1.append(each_rd1_linkage_split[0])
        target_list_rd1.append(each_rd1_linkage_split[1])
        value_list_rd1.append(linkage_num_dict_rd1[each_rd1_linkage])

    gnm_color_list_rd1 = sns.color_palette('tab20', len(genome_set_rd1)).as_hex()
    genome_to_color_dict_rd1 = {gnm: color for gnm, color in zip(genome_set_rd1, gnm_color_list_rd1)}

    color_list_rd1 = []
    for each_target in target_list_rd1:
        if each_target in genome_to_color_dict_rd1:
            color_list_rd1.append(genome_to_color_dict_rd1[each_target])
        else:
            target_genome = ctg_to_gnm_dict_rd1[each_target]
            color_list_rd1.append(genome_to_color_dict_rd1[target_genome])

    node_list_rd1 = sorted([i for i in node_set_rd1])
    plot_title_text_rd1 = 'MarkerMAG detected linkages (round 1)<br>Number of linked genomes: %s<br>Number of linked markers: %s' % (len(genome_set_rd1), len(marker_gene_set_rd1))
    plot_height_rd1 = 900 if max([len(contig_set_rd1), len(marker_gene_set_rd1)]) <= 25 else max([len(contig_set_rd1), len(marker_gene_set_rd1)]) * 32
    plot_title_dict_rd1 = dict(text=plot_title_text_rd1, x=0.05, y=(1-(50/plot_height_rd1)))
    get_sankey_plot(node_list_rd1, source_list_rd1, target_list_rd1, value_list_rd1, color_list_rd1, plot_title_dict_rd1, plot_height_rd1, linkage_plot_rd1_html)

    #################### plot rd1 linkages ####################

    if len(linkage_num_dict_rd2) > 0:
        source_list_rd2 = []
        target_list_rd2 = []
        value_list_rd2 = []
        for each_rd2_linkage in linkage_num_dict_rd2:
            each_rd2_linkage_split = each_rd2_linkage.split(dict_for_sankey_key_connector)
            source_list_rd2.append(each_rd2_linkage_split[0])
            target_list_rd2.append(each_rd2_linkage_split[1])
            value_list_rd2.append(linkage_num_dict_rd2[each_rd2_linkage])

        gnm_color_list_rd2 = sns.color_palette('tab20', len(genome_set_rd2)).as_hex()
        genome_to_color_dict_rd2 = {gnm: color for gnm, color in zip(genome_set_rd2, gnm_color_list_rd2)}

        color_list_rd2 = []
        for each_target in target_list_rd2:
            if each_target in genome_to_color_dict_rd2:
                color_list_rd2.append(genome_to_color_dict_rd2[each_target])
            else:
                target_genome = ctg_to_gnm_dict_rd2[each_target]
                color_list_rd2.append(genome_to_color_dict_rd2[target_genome])

        node_list_rd2 = sorted([i for i in node_set_rd2])
        plot_title_text_rd2 = 'MarkerMAG detected linkages (round 2)<br>Number of linked genomes: %s<br>Number of linked markers: %s' % (len(genome_set_rd2), len(marker_gene_set_rd2))
        plot_height_rd2 = 900 if max([len(contig_set_rd2), len(marker_gene_set_rd2)]) <= 25 else max([len(contig_set_rd2), len(marker_gene_set_rd2)]) * 32
        plot_title_dict_rd2 = dict(text=plot_title_text_rd2, x=0.05, y=(1-(50/plot_height_rd2)))
        get_sankey_plot(node_list_rd2, source_list_rd2, target_list_rd2, value_list_rd2, color_list_rd2, plot_title_dict_rd2, plot_height_rd2, linkage_plot_rd2_html)


def check_both_ends_clipping(cigar_splitted):

    both_ends_clipping = False
    if len(cigar_splitted) >= 3:
        if (cigar_splitted[0][-1] in ['S', 's']) and (cigar_splitted[-1][-1] in ['S', 's']):
            both_ends_clipping = True

    return both_ends_clipping


def remove_both_ends_clp(sam_in, sam_out):
    sam_out_handle = open(sam_out, 'w')
    for each_read in open(sam_in):
        each_read_split = each_read.strip().split('\t')
        if each_read.startswith('@'):
            sam_out_handle.write(each_read)
        else:
            cigar = each_read_split[5]
            if cigar == '*':
                sam_out_handle.write(each_read)
            else:
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    sam_out_handle.write(each_read)
    sam_out_handle.close()


def keep_best_matches_in_sam(sam_in, sam_out):
    # get read_to_cigar_dict
    read_to_cigar_dict = {}
    for each_line in open(sam_in):
        each_line_split = each_line.strip().split('\t')
        if not each_line.startswith('@'):
            read_id = each_line_split[0]
            cigar = each_line_split[5]
            if cigar != '*':
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    if read_id not in read_to_cigar_dict:
                        read_to_cigar_dict[read_id] = {cigar}
                    else:
                        read_to_cigar_dict[read_id].add(cigar)

    # get min_mismatch for each read
    read_min_mismatch_dict = {}
    for each_read in read_to_cigar_dict:
        read_mismatch_set = set()
        for each_cigar in read_to_cigar_dict[each_read]:
            aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_splitter(each_cigar))
            read_mismatch_set.add(mismatch_pct)
        read_min_mismatch = min(read_mismatch_set)
        read_min_mismatch_dict[each_read] = read_min_mismatch

    sam_file_best_match_handle = open(sam_out, 'w')
    for each_line in open(sam_in):
        if each_line.startswith('@'):
            sam_file_best_match_handle.write(each_line)
        else:
            each_line_split = each_line.strip().split('\t')
            read_id = each_line_split[0]
            cigar = each_line_split[5]
            if cigar == '*':
                sam_file_best_match_handle.write(each_line)
            else:
                cigar_split = cigar_splitter(cigar)
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_split)
                    if mismatch_pct <= (read_min_mismatch_dict[read_id] * 1.5):

                        sam_file_best_match_handle.write(each_line)
    sam_file_best_match_handle.close()


def keep_best_matches_in_sam_keep_short_M(sam_in, min_M_len, sam_out):

    # get read_to_cigar_dict
    read_to_cigar_dict = {}
    for each_line in open(sam_in):
        each_line_split = each_line.strip().split('\t')
        if not each_line.startswith('@'):
            read_id = each_line_split[0]
            cigar = each_line_split[5]
            if cigar != '*':
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    if read_id not in read_to_cigar_dict:
                        read_to_cigar_dict[read_id] = {cigar}
                    else:
                        read_to_cigar_dict[read_id].add(cigar)

    # get min_mismatch for each read
    read_min_mismatch_dict = {}
    for each_read in read_to_cigar_dict:
        read_mismatch_set_all_M = set()
        read_mismatch_set_long_M = set()
        for each_cigar in read_to_cigar_dict[each_read]:
            aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_splitter(each_cigar))
            read_mismatch_set_all_M.add(mismatch_pct)
            if aligned_len >= min_M_len:
                read_mismatch_set_long_M.add(mismatch_pct)
        read_min_mismatch = min(read_mismatch_set_all_M)
        if len(read_mismatch_set_long_M) > 0:
            read_min_mismatch = min(read_mismatch_set_long_M)
        read_min_mismatch_dict[each_read] = read_min_mismatch

    sam_file_best_match_handle = open(sam_out, 'w')
    for each_line in open(sam_in):
        if each_line.startswith('@'):
            sam_file_best_match_handle.write(each_line)
        else:
            each_line_split = each_line.strip().split('\t')
            cigar = each_line_split[5]
            if cigar == '*':
                sam_file_best_match_handle.write(each_line)
            else:
                read_id = each_line_split[0]
                cigar_split = cigar_splitter(cigar)
                both_ends_clp = check_both_ends_clipping(cigar_splitter(cigar))
                if both_ends_clp is False:
                    aligned_len, aligned_pct, clipping_len, clipping_pct, mismatch_pct = get_cigar_stats(cigar_split)
                    if mismatch_pct <= (read_min_mismatch_dict[read_id] * 1.5):
                        sam_file_best_match_handle.write(each_line)
    sam_file_best_match_handle.close()


def run_mira5(output_prefix, mira_tmp_dir, step_2_wd, mira_manifest, unpaired_fastq, mira_stdout, force_overwrite):

    # prepare manifest file
    mira_manifest_handle = open(mira_manifest, 'w')
    mira_manifest_handle.write('project = %s_mira_est_no_chimera\n' % output_prefix)
    mira_manifest_handle.write('job=est,denovo,accurate\n')
    mira_manifest_handle.write('parameters = -CL:ascdc\n')
    mira_manifest_handle.write('readgroup = SomeUnpairedIlluminaReadsIGotFromTheLab\n')
    mira_manifest_handle.write('data = %s\n' % os.path.abspath(unpaired_fastq))
    mira_manifest_handle.write('technology = solexa\n')
    mira_manifest_handle.close()

    if os.path.isdir(mira_tmp_dir) is False:
        os.mkdir(mira_tmp_dir)

    # run Mira
    mira_cmd = 'mira -c %s %s > %s' % (step_2_wd, os.path.abspath(mira_manifest), mira_stdout)
    if mira_tmp_dir is not None:
        mira_cmd = 'mira -c %s %s > %s' % (mira_tmp_dir, os.path.abspath(mira_manifest), mira_stdout)
    os.system(mira_cmd)

    # parse mira output
    if (mira_tmp_dir is not None) and (mira_tmp_dir != step_2_wd):
        os.system('cp -r %s/%s_mira_est_no_chimera_assembly %s/' % (mira_tmp_dir, output_prefix, step_2_wd))


def extract_reads_worker(argument_list):

    reads_file_in = argument_list[0]
    reads_fmt = argument_list[1]
    reads_to_extract = argument_list[2]
    reads_file_out = argument_list[3]

    reads_file_out_handle = open(reads_file_out, 'w')
    for read_record in SeqIO.parse(reads_file_in, reads_fmt):
        if read_record.id in reads_to_extract:
            if reads_fmt == 'fasta':
                reads_file_out_handle.write('>%s\n' % read_record.id)
                reads_file_out_handle.write('%s\n' % read_record.seq)
            if reads_fmt == 'fastq':
                SeqIO.write(read_record, reads_file_out_handle, 'fastq')
    reads_file_out_handle.close()


def get_GapFilling_stats_by_assembly(free_living_16s_ref_file, free_living_ctg_ref_file,
                                     mini_assembly_to_16s_reads, mini_assembly_to_ctg_reads,
                                     ctg_level_min_link,
                                     mini_assembly_to_16s_ctg_connector, gnm_to_ctg_connector, marker_to_ctg_gnm_Key_connector,
                                     max_within_cate_diff_pct, max_between_cate_diff_pct,
                                     stats_GapFilling_ctg, stats_GapFilling_gnm):

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


def get_unmapped_mates_seq(sam_file, input_r1_fasta, input_r2_fasta, extracted_seq_file, seqtk_exe):

    sam_path, sam_basename, sam_ext = sep_path_basename_ext(sam_file)
    reads_to_extract_r1_txt = '%s/%s_unmapped_mates_R1.txt' % (sam_path, sam_basename)
    reads_to_extract_r2_txt = '%s/%s_unmapped_mates_R2.txt' % (sam_path, sam_basename)
    reads_to_extract_r1_fa  = '%s/%s_unmapped_mates_R1.fa'  % (sam_path, sam_basename)
    reads_to_extract_r2_fa  = '%s/%s_unmapped_mates_R2.fa'  % (sam_path, sam_basename)

    prescreening_qualified_reads_set = set()
    prescreening_qualified_reads_base_set = set()
    for each_read in open(sam_file):
        each_read_split = each_read.strip().split('\t')
        if not each_read.startswith('@'):
            read_id = each_read_split[0]
            read_id_base = '.'.join(read_id.split('.')[:-1])
            prescreening_qualified_reads_set.add(read_id)
            prescreening_qualified_reads_base_set.add(read_id_base)

    # get id files
    reads_to_extract_r1 = set()
    reads_to_extract_r2 = set()
    for each_read_base in prescreening_qualified_reads_base_set:
        read_r1 = '%s.1' % each_read_base
        read_r2 = '%s.2' % each_read_base
        if (read_r1 not in prescreening_qualified_reads_set) and (read_r2 in prescreening_qualified_reads_set):
            reads_to_extract_r1.add(read_r1)
        if (read_r1 in prescreening_qualified_reads_set) and (read_r2 not in prescreening_qualified_reads_set):
            reads_to_extract_r2.add(read_r2)

    reads_to_extract_r1_txt_handle = open(reads_to_extract_r1_txt, 'w')
    reads_to_extract_r1_txt_handle.write('%s\n' % '\n'.join(reads_to_extract_r1))
    reads_to_extract_r1_txt_handle.close()

    reads_to_extract_r2_txt_handle = open(reads_to_extract_r2_txt, 'w')
    reads_to_extract_r2_txt_handle.write('%s\n' % '\n'.join(reads_to_extract_r2))
    reads_to_extract_r2_txt_handle.close()

    seqtk_extract_r1_read_cmd = '%s subseq %s %s > %s' % (seqtk_exe,
    input_r1_fasta, reads_to_extract_r1_txt, reads_to_extract_r1_fa)
    seqtk_extract_r2_read_cmd = '%s subseq %s %s > %s' % (seqtk_exe,
    input_r2_fasta, reads_to_extract_r2_txt, reads_to_extract_r2_fa)
    os.system(seqtk_extract_r1_read_cmd)
    os.system(seqtk_extract_r2_read_cmd)

    os.system('cat %s %s > %s' % (reads_to_extract_r1_fa, reads_to_extract_r2_fa, extracted_seq_file))

    # rm tmp files
    os.system('rm %s' % reads_to_extract_r1_txt)
    os.system('rm %s' % reads_to_extract_r2_txt)
    os.system('rm %s' % reads_to_extract_r1_fa)
    os.system('rm %s' % reads_to_extract_r2_fa)


def qc_16s(file_in, file_out_ffn, no_16s_polish, min_16s_len):

    file_out_path, file_out_base, file_out_ext = sep_path_basename_ext(file_out_ffn)
    barrnap_stdout   = '%s/%s.log'    % (file_out_path, file_out_base)
    file_out_ffn_tmp = '%s/%s_tmp%s'  % (file_out_path, file_out_base, file_out_ext)
    file_out_gff     = '%s/%s.gff'    % (file_out_path, file_out_base)

    # remove non-16S sequences, then filter by length
    if no_16s_polish is False:

        barrnap_cmd = 'barrnap --quiet -o %s %s 2> %s > %s' % (file_out_ffn_tmp, file_in, barrnap_stdout, file_out_gff)
        os.system(barrnap_cmd)

        wrote_id = []
        file_out_ffn_handle = open(file_out_ffn, 'w')
        for each_16s in SeqIO.parse(file_out_ffn_tmp, 'fasta'):
            seq_id = each_16s.id
            if seq_id.startswith('16S_rRNA::'):
                seq_id_polished = seq_id[10:].split(':')[0]
                if len(each_16s.seq) >= min_16s_len:
                    if seq_id_polished not in wrote_id:
                        file_out_ffn_handle.write('>%s\n' % seq_id_polished)
                        file_out_ffn_handle.write('%s\n' % str(each_16s.seq))
                        wrote_id.append(seq_id_polished)
                    else:
                        file_out_ffn_handle.write('>%s_%s\n' % (seq_id_polished, (wrote_id.count(seq_id_polished) + 1)))
                        file_out_ffn_handle.write('%s\n' % str(each_16s.seq))
                        wrote_id.append(seq_id_polished)
        file_out_ffn_handle.close()

        # remove tmp files
        os.system('rm %s' % file_out_ffn_tmp)
        os.system('rm %s.fai' % file_in)

    # only filter input 16S by length
    else:
        file_out_ffn_handle = open(file_out_ffn, 'w')
        for each_16s in SeqIO.parse(file_in, 'fasta'):
            if len(each_16s.seq) >= min_16s_len:
                file_out_ffn_handle.write('>%s\n' % each_16s.id)
                file_out_ffn_handle.write('%s\n' % str(each_16s.seq))
        file_out_ffn_handle.close()


def get_min_max_cigar_S(cigar_list):

    # get cigar_S_set
    cigar_S_set = set()
    for each_cigar in cigar_list:
        if ('S' not in each_cigar) and ('s' not in each_cigar):
            cigar_S_set.add(0)
        else:
            cigar_splitted = cigar_splitter(each_cigar)

            if cigar_splitted[0][-1] in ['S', 's']:
                cigar_S_set.add(int(cigar_splitted[0][:-1]))

            if cigar_splitted[-1][-1] in ['S', 's']:
                cigar_S_set.add(int(cigar_splitted[1][:-1]))

    # get min_cigar_S and max_cigar_S
    min_cigar_S = 0
    max_cigar_S = 0
    if len(cigar_S_set) > 0:
        min_cigar_S = min(cigar_S_set)
        max_cigar_S = max(cigar_S_set)

    return min_cigar_S, max_cigar_S


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


def get_r12_16s_ref_dict_from_str(r2_16s_ref_dict_str):

    ref_dict_from_str = {}
    if r2_16s_ref_dict_str != 'na':
        r2_16s_ref_dict_str_split = r2_16s_ref_dict_str.split(';;;')

        ref_dict_from_str = {}
        for each_sub_dict_str in r2_16s_ref_dict_str_split:
            each_sub_dict_str_split = each_sub_dict_str.split(':::')
            sub_dict_key = each_sub_dict_str_split[0]
            sub_dict_str = each_sub_dict_str_split[1]
            sub_dict_str_split = sub_dict_str.split(';')
            bottom_dict = dict()
            for each_bottom_dict_str in sub_dict_str_split:
                bottom_dict_str_split = each_bottom_dict_str.split(':')
                bottom_dict_key = int(bottom_dict_str_split[0])
                bottom_dict_value = bottom_dict_str_split[1]
                bottom_dict[bottom_dict_key] = bottom_dict_value
            ref_dict_from_str[sub_dict_key] = bottom_dict

    return ref_dict_from_str


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


def get_no_ignored_dict_from_str(r2_16s_refs_no_ignored_dict_str):

    no_ignored_dict_from_str = {}
    if r2_16s_refs_no_ignored_dict_str != 'na':
        r2_16s_refs_no_ignored_dict_str_split = r2_16s_refs_no_ignored_dict_str.split(';')
        for each_sub_dict_str in r2_16s_refs_no_ignored_dict_str_split:
            each_sub_dict_str_split = each_sub_dict_str.split(':')
            ref_id = each_sub_dict_str_split[0]
            cigar_list_str = each_sub_dict_str_split[1]
            cigar_list = cigar_list_str.split(',')
            no_ignored_dict_from_str[ref_id] = cigar_list

    return no_ignored_dict_from_str


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

                            r1_16s_ref_qualified_cigar = check_cigar_quality(r1_16s_ref_cigar, True, r1_ref_min_mismatch,
                                                                             mismatch_cutoff, min_M_len_16s, r1_16s_ref_pos,
                                                                             marker_len_dict[r1_16s_ref])

                            # exclude the ref if cigar not qualified
                            if r1_16s_ref_qualified_cigar is False:
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

                            r2_16s_ref_qualified_cigar = check_cigar_quality(r2_16s_ref_cigar, True, r2_ref_min_mismatch,
                                                                             mismatch_cutoff, min_M_len_16s, r2_16s_ref_pos,
                                                                             marker_len_dict[r2_16s_ref])

                            # exclude the ref if cigar not qualified
                            if r2_16s_ref_qualified_cigar is False:
                                refs_to_ignore.add(r2_16s_ref)
                            else:
                                r2_16s_refs_passed_qc[r2_16s_ref] = [r2_16s_ref_cigar]
                                r2_16s_refs_passed_qc_with_pos[r2_16s_ref] = {r2_16s_ref_pos: r2_16s_ref_cigar}

                    #################################

                    r1_16s_refs_no_ignored          = {key: value for key, value in r1_16s_refs_passed_qc.items() if key not in refs_to_ignore}
                    r2_16s_refs_no_ignored          = {key: value for key, value in r2_16s_refs_passed_qc.items() if key not in refs_to_ignore}
                    r1_16s_refs_no_ignored_with_pos = {key: value for key, value in r1_16s_refs_passed_qc_with_pos.items() if key not in refs_to_ignore}
                    r2_16s_refs_no_ignored_with_pos = {key: value for key, value in r2_16s_refs_passed_qc_with_pos.items() if key not in refs_to_ignore}

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
                        shared_16s_ref_dict = {key: [r1_16s_refs_no_ignored[key][0], r2_16s_refs_no_ignored[key][0]] for key
                                               in set(r1_16s_refs_no_ignored).intersection(set(r2_16s_refs_no_ignored))}
                        if len(shared_16s_ref_dict) > 0:

                            current_read_base___qualified_reads = 1
                            current_read_base___both_mapped_to_16s = 1
                            current_read_base___shared_16s_refs_no_ignored = shared_16s_ref_dict
                            current_read_base___r1_16s_ref_dict = current_read_base_r1_16s_ref_dict
                            current_read_base___r2_16s_ref_dict = current_read_base_r2_16s_ref_dict

                    if current_read_base___qualified_reads == 1:
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


def parse_rd2_sam_gnm_worker(arguments_list):

    rd1_unlinked_mags_sam_bowtie_reformat_sorted = arguments_list[0]
    free_living_ctg_ref_file                     = arguments_list[1]
    free_living_ctg_ref_file_with_pos_cigar      = arguments_list[2]
    min_M_len_ctg                                = arguments_list[3]
    mismatch_cutoff                              = arguments_list[4]
    round_2_ctg_end_seq_len_dict                 = arguments_list[5]
    rd2_with_both_mates                          = arguments_list[6]
    ctg_ignore_region_dict_2rd                   = arguments_list[7]

    free_living_ctg_ref_file_handle = open(free_living_ctg_ref_file, 'w')
    free_living_ctg_ref_file_with_pos_cigar_handle = open(free_living_ctg_ref_file_with_pos_cigar, 'w')
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
                    r1_ctg_refs_passed_qc_with_pos = {}
                    for r1_ctg_ref_rd2 in current_read_base_r1_ctg_ref_dict_rd2:
                        r1_matched_pos_dict = current_read_base_r1_ctg_ref_dict_rd2[r1_ctg_ref_rd2]
                        if len(r1_matched_pos_dict) > 1:
                            ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)
                        else:
                            r1_ctg_ref_pos = list(r1_matched_pos_dict.keys())[0]
                            r1_ctg_ref_cigar = r1_matched_pos_dict[r1_ctg_ref_pos]

                            r1_ctg_ref_qualified_cigar = check_cigar_quality(r1_ctg_ref_cigar, True, r1_ref_min_mismatch, mismatch_cutoff,
                                                                  min_M_len_ctg, r1_ctg_ref_pos, round_2_ctg_end_seq_len_dict[r1_ctg_ref_rd2])

                            if r1_ctg_ref_qualified_cigar is False:
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
                                    r1_ctg_refs_passed_qc_with_pos[r1_ctg_ref_rd2] = {r1_ctg_ref_pos: r1_ctg_ref_cigar}
                                else:
                                    ctg_refs_to_ignore_rd2.add(r1_ctg_ref_rd2)

                    ########## filter r2 ctg refs ##########
                    r2_ctg_refs_passed_qc = {}
                    r2_ctg_refs_passed_qc_with_pos = {}
                    for r2_ctg_ref_rd2 in current_read_base_r2_ctg_ref_dict_rd2:
                        r2_matched_pos_dict = current_read_base_r2_ctg_ref_dict_rd2[r2_ctg_ref_rd2]
                        if len(r2_matched_pos_dict) > 1:
                            ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)
                        else:
                            r2_ctg_ref_pos = list(r2_matched_pos_dict.keys())[0]
                            r2_ctg_ref_cigar = r2_matched_pos_dict[r2_ctg_ref_pos]

                            r2_ctg_ref_qualified_cigar = check_cigar_quality(r2_ctg_ref_cigar, True, r2_ref_min_mismatch, mismatch_cutoff,
                                                                  min_M_len_ctg, r2_ctg_ref_pos, round_2_ctg_end_seq_len_dict[r2_ctg_ref_rd2])

                            if r2_ctg_ref_qualified_cigar is False:
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
                                    r2_ctg_refs_passed_qc_with_pos[r2_ctg_ref_rd2] = {r2_ctg_ref_pos: r2_ctg_ref_cigar}
                                else:
                                    ctg_refs_to_ignore_rd2.add(r2_ctg_ref_rd2)

                    ####################################################################################################

                    r1_ctg_refs_rd2_no_ignored          = {key: value for key, value in r1_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}
                    r2_ctg_refs_rd2_no_ignored          = {key: value for key, value in r2_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}
                    r1_ctg_refs_rd2_no_ignored_with_pos = {key: value for key, value in r1_ctg_refs_passed_qc_with_pos.items() if key not in ctg_refs_to_ignore_rd2}
                    r2_ctg_refs_rd2_no_ignored_with_pos = {key: value for key, value in r2_ctg_refs_passed_qc_with_pos.items() if key not in ctg_refs_to_ignore_rd2}
                    r1_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r1_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}
                    r2_ctg_refs_rd2_no_ignored_str_list = {('%s__cigar__%s' % (key, value[0])) for key, value in r2_ctg_refs_passed_qc.items() if key not in ctg_refs_to_ignore_rd2}

                    r1_ctg_refs_rd2_no_ignored_str_list_with_pos = set()
                    for each_16s in r1_ctg_refs_rd2_no_ignored_with_pos:
                        cigar_dict = r1_ctg_refs_rd2_no_ignored_with_pos[each_16s]
                        for each_cigar_pos in cigar_dict:
                            cigar_str = cigar_dict[each_cigar_pos]
                            r1_ctg_refs_rd2_no_ignored_str_list_with_pos.add( '%s__pc__%s__pc__%s' % (each_16s, each_cigar_pos, cigar_str))

                    r2_ctg_refs_rd2_no_ignored_str_list_with_pos = set()
                    for each_16s in r2_ctg_refs_rd2_no_ignored_with_pos:
                        cigar_dict = r2_ctg_refs_rd2_no_ignored_with_pos[each_16s]
                        for each_cigar_pos in cigar_dict:
                            cigar_str = cigar_dict[each_cigar_pos]
                            r2_ctg_refs_rd2_no_ignored_str_list_with_pos.add( '%s__pc__%s__pc__%s' % (each_16s, each_cigar_pos, cigar_str))

                    # only r1 has no_ignored alignments
                    if (len(r1_ctg_refs_rd2_no_ignored) > 0) and (len(r2_ctg_refs_rd2_no_ignored) == 0):
                        if rd2_with_both_mates is True:
                            free_living_ctg_ref_file_handle.write('%s\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored)))
                            free_living_ctg_ref_file_with_pos_cigar_handle.write('%s\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored_str_list_with_pos)))
                        else:
                            free_living_ctg_ref_file_handle.write('%s.2\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored)))
                            free_living_ctg_ref_file_with_pos_cigar_handle.write('%s.2\t%s\n' % (current_read_base, ','.join(r1_ctg_refs_rd2_no_ignored_str_list_with_pos)))

                    # only r2 has no_ignored alignments
                    if (len(r1_ctg_refs_rd2_no_ignored) == 0) and (len(r2_ctg_refs_rd2_no_ignored) > 0):
                        if rd2_with_both_mates is True:
                            free_living_ctg_ref_file_handle.write('%s\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored)))
                            free_living_ctg_ref_file_with_pos_cigar_handle.write('%s\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored_str_list_with_pos)))
                        else:
                            free_living_ctg_ref_file_handle.write('%s.1\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored)))
                            free_living_ctg_ref_file_with_pos_cigar_handle.write('%s.1\t%s\n' % (current_read_base, ','.join(r2_ctg_refs_rd2_no_ignored_str_list_with_pos)))

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
    free_living_ctg_ref_file_with_pos_cigar_handle.close()


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


def filter_linkages_iteratively_mini_assembly_to_ctg(file_in_sorted, min_linkages, file_out):

    # do mini-assemblies assigned to the same mag need to have roughly the same number of linkages? think about this later
    mag_ctg_max_link_num_dict = {}
    mini_assembly_to_mag_dict = {}
    mini_assembly_to_ctg_dict = {}
    file_out_handle = open(file_out, 'w')
    mini_assembly_with_assignment = set()
    mag_ctg_set_with_linked_mini_assembly = set()
    for each_match in open(file_in_sorted):
        if each_match.startswith('MiniAssembly,GenomicSeq,Number'):
            file_out_handle.write(each_match)
        else:
            match_split = each_match.strip().split(',')
            mini_assembly = match_split[0]
            mag_ctg_id = match_split[1]
            mag_id = mag_ctg_id.split('___C___')[0]

            linkage_num = int(match_split[2])
            if linkage_num >= min_linkages:
                if mini_assembly not in mini_assembly_with_assignment:
                    if mag_ctg_id not in mag_ctg_max_link_num_dict:
                        mag_ctg_max_link_num_dict[mag_ctg_id] = linkage_num
                        file_out_handle.write(each_match)
                        mini_assembly_to_ctg_dict[mini_assembly] = mag_ctg_id
                        mini_assembly_to_mag_dict[mini_assembly] = mag_id
                        mini_assembly_with_assignment.add(mini_assembly)
                        mag_ctg_set_with_linked_mini_assembly.add(mag_ctg_id)
                    else:
                        ratio_with_best_assignment = linkage_num / (mag_ctg_max_link_num_dict[mag_ctg_id])
                        if ratio_with_best_assignment >= 0.8:
                            file_out_handle.write(each_match)
                            mini_assembly_to_ctg_dict[mini_assembly] = mag_ctg_id
                            mini_assembly_to_mag_dict[mini_assembly] = mag_id
                            mini_assembly_with_assignment.add(mini_assembly)
                            mag_ctg_set_with_linked_mini_assembly.add(mag_ctg_id)
                        else:
                            mini_assembly_with_assignment.add(mini_assembly)
    file_out_handle.close()

    return mini_assembly_to_ctg_dict, mini_assembly_to_mag_dict, mag_ctg_set_with_linked_mini_assembly


def linkage_vis_worker(arguments_list):

    reads_file_base = arguments_list[0]
    mafft_seq_folder = arguments_list[1]
    marker_seq = arguments_list[2]
    contig_seq = arguments_list[3]
    end_ctg_len_for_mafft = arguments_list[4]
    gap_N_num = arguments_list[5]
    bowtie_parameter = arguments_list[6]
    marker_pos_list = arguments_list[7]
    contig_pos_list = arguments_list[8]
    pwd_bowtie2_build_exe = arguments_list[9]
    pwd_bowtie2_exe = arguments_list[10]
    marker_seq_name = arguments_list[11]
    contig_seq_name = arguments_list[12]

    marker_len = len(marker_seq)
    contig_len = len(contig_seq)

    # get marker linked end
    marker_pos_median = np.median(marker_pos_list)
    linked_end_marker = 'middle'
    if marker_pos_median <= (marker_len / 3):
        linked_end_marker = 'left'
    elif marker_pos_median >= (marker_len * 2 / 3):
        linked_end_marker = 'right'

    # get contig linked end
    contig_pos_median = np.median(contig_pos_list)
    contig_pos_middle = int(round(float(contig_pos_median)))
    linked_end_contig = 'middle(%s)' % contig_pos_middle
    if contig_pos_median <= 200:
        linked_end_contig = 'left'
    elif (contig_len - contig_pos_median) <= 200:
        linked_end_contig = 'right'

    # get contig end sequence
    if linked_end_contig == 'left':
        contig_seq_for_mafft = contig_seq[:end_ctg_len_for_mafft]
    elif linked_end_contig == 'right':
        contig_seq_for_mafft = contig_seq[-end_ctg_len_for_mafft:]
    else:
        left_end_pos = 0
        if (contig_pos_middle - end_ctg_len_for_mafft) > 0:
            left_end_pos = contig_pos_middle - end_ctg_len_for_mafft
        right_end_pos = contig_pos_middle + end_ctg_len_for_mafft
        if right_end_pos > contig_len:
            right_end_pos = contig_len
        contig_seq_for_mafft = contig_seq[left_end_pos:(right_end_pos - 1)]

    # concatenate 16s and contig sequences
    to_concatenate = False
    concatenated_seq_id = ''
    concatenated_seq = ''
    concatenate_pos = 0
    if linked_end_contig in ['left', 'right']:
        if (linked_end_marker == 'right') and (linked_end_contig == 'left'):
            concatenated_seq_id = '%s_NNN_%s' % (marker_seq_name, contig_seq_name)
            concatenated_seq = '%s%s%s' % (marker_seq, 'N' * gap_N_num, contig_seq_for_mafft)
            to_concatenate = True
            concatenate_pos = len(marker_seq) + round(gap_N_num / 2)

        if (linked_end_marker == 'left') and (linked_end_contig == 'right'):
            concatenated_seq_id = '%s_NNN_%s' % (contig_seq_name, marker_seq_name)
            concatenated_seq = '%s%s%s' % (contig_seq_for_mafft, 'N' * gap_N_num, marker_seq)
            to_concatenate = True
            concatenate_pos = len(contig_seq_for_mafft) + round(gap_N_num / 2)

        if (linked_end_marker == 'left') and (linked_end_contig == 'left'):
            marker_seq_rc = get_rc(marker_seq)
            concatenated_seq_id = '%s_RC_NNN_%s' % (marker_seq_name, contig_seq_name)
            concatenated_seq = '%s%s%s' % (marker_seq_rc, 'N' * gap_N_num, contig_seq_for_mafft)
            to_concatenate = True
            concatenate_pos = len(marker_seq_rc) + round(gap_N_num / 2)

        if (linked_end_marker == 'right') and (linked_end_contig == 'right'):
            marker_seq_rc = get_rc(marker_seq)
            concatenated_seq_id = '%s_NNN_%s_RC' % (contig_seq_name, marker_seq_name)
            concatenated_seq = '%s%s%s' % (contig_seq_for_mafft, 'N' * gap_N_num, marker_seq_rc)
            to_concatenate = True
            concatenate_pos = len(contig_seq_for_mafft) + round(gap_N_num / 2)

    # write out sequences
    pwd_seq_file_cbd = '%s/%s/%s_cbd.fa' % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s = '%s/%s/%s_16s.fa' % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg = '%s/%s/%s_ctg.fa' % (mafft_seq_folder, reads_file_base, reads_file_base)
    if to_concatenate is True:
        pwd_seq_file_cbd_handle = open(pwd_seq_file_cbd, 'w')
        pwd_seq_file_cbd_handle.write('>%s\n' % concatenated_seq_id)
        pwd_seq_file_cbd_handle.write('%s\n' % concatenated_seq)
        pwd_seq_file_cbd_handle.close()
    else:
        # write out 16s sequence
        pwd_seq_file_16s_handle = open(pwd_seq_file_16s, 'w')
        pwd_seq_file_16s_handle.write('>%s\n' % marker_seq_name)
        pwd_seq_file_16s_handle.write('%s\n' % marker_seq)
        pwd_seq_file_16s_handle.close()
        # write out ctg sequence
        pwd_seq_file_ctg_handle = open(pwd_seq_file_ctg, 'w')
        pwd_seq_file_ctg_handle.write('>%s\n' % contig_seq_name)
        pwd_seq_file_ctg_handle.write('%s\n' % contig_seq_for_mafft)
        pwd_seq_file_ctg_handle.close()

    ########## mapping ##########

    pwd_seq_file_cbd            = '%s/%s/%s_cbd.fa'     % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s            = '%s/%s/%s_16s.fa'     % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg            = '%s/%s/%s_ctg.fa'     % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_reads_r1       = '%s/%s/%s_R1.fa'      % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_reads_r2       = '%s/%s/%s_R2.fa'      % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_cbd_index      = '%s/%s/%s_cbd'        % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s_index      = '%s/%s/%s_16s'        % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg_index      = '%s/%s/%s_ctg'        % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_cbd_sam        = '%s/%s/%s_cbd.sam'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s_sam        = '%s/%s/%s_16s.sam'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg_sam        = '%s/%s/%s_ctg.sam'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_cbd_sam_log    = '%s/%s/%s_cbd.log'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s_sam_log    = '%s/%s/%s_16s.log'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg_sam_log    = '%s/%s/%s_ctg.log'    % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_cbd_Tablet_xml = '%s/%s/%s_cbd.tablet' % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_16s_Tablet_xml = '%s/%s/%s_16s.tablet' % (mafft_seq_folder, reads_file_base, reads_file_base)
    pwd_seq_file_ctg_Tablet_xml = '%s/%s/%s_ctg.tablet' % (mafft_seq_folder, reads_file_base, reads_file_base)

    if to_concatenate is True:
        index_ref_cmd = '%s --quiet -f %s %s' % (pwd_bowtie2_build_exe, pwd_seq_file_cbd, pwd_seq_file_cbd_index)
        bowtie2_cmd = '%s -x %s -U %s,%s -S %s -p 1 -f %s 2> %s' % (
            pwd_bowtie2_exe, pwd_seq_file_cbd_index, pwd_seq_file_reads_r1, pwd_seq_file_reads_r2,
            pwd_seq_file_cbd_sam, bowtie_parameter, pwd_seq_file_cbd_sam_log)
        os.system(index_ref_cmd)
        os.system(bowtie2_cmd)

        # write out Tablet xml file
        pwd_seq_file_cbd_Tablet_xml_handle = open(pwd_seq_file_cbd_Tablet_xml, 'w')
        pwd_seq_file_cbd_Tablet_xml_handle.write('<tablet>\n')
        pwd_seq_file_cbd_Tablet_xml_handle.write('        <assembly>%s_cbd.sam</assembly>\n' % reads_file_base)
        pwd_seq_file_cbd_Tablet_xml_handle.write('        <reference>%s_cbd.fa</reference>\n' % reads_file_base)
        pwd_seq_file_cbd_Tablet_xml_handle.write('        <contig>%s</contig>\n' % concatenated_seq_id)
        pwd_seq_file_cbd_Tablet_xml_handle.write('        <position>%s</position>\n' % concatenate_pos)
        pwd_seq_file_cbd_Tablet_xml_handle.write('</tablet>\n')
        pwd_seq_file_cbd_Tablet_xml_handle.close()
    else:
        index_ref_cmd_16s = '%s --quiet -f %s %s' % (pwd_bowtie2_build_exe, pwd_seq_file_16s, pwd_seq_file_16s_index)
        index_ref_cmd_ctg = '%s --quiet -f %s %s' % (pwd_bowtie2_build_exe, pwd_seq_file_ctg, pwd_seq_file_ctg_index)
        os.system(index_ref_cmd_16s)
        os.system(index_ref_cmd_ctg)
        bowtie2_cmd_16s = '%s -x %s -U %s,%s -S %s -p 6 -f %s 2> %s' % (
            pwd_bowtie2_exe, pwd_seq_file_16s_index, pwd_seq_file_reads_r1, pwd_seq_file_reads_r2, pwd_seq_file_16s_sam,
            bowtie_parameter, pwd_seq_file_16s_sam_log)
        bowtie2_cmd_ctg = '%s -x %s -U %s,%s -S %s -p 6 -f %s 2> %s' % (
            pwd_bowtie2_exe, pwd_seq_file_ctg_index, pwd_seq_file_reads_r1, pwd_seq_file_reads_r2, pwd_seq_file_ctg_sam,
            bowtie_parameter, pwd_seq_file_ctg_sam_log)
        os.system(bowtie2_cmd_16s)
        os.system(bowtie2_cmd_ctg)

        # write out Tablet xml file
        pwd_seq_file_16s_Tablet_xml_handle = open(pwd_seq_file_16s_Tablet_xml, 'w')
        pwd_seq_file_16s_Tablet_xml_handle.write('<tablet>\n')
        pwd_seq_file_16s_Tablet_xml_handle.write('        <assembly>%s_16s.sam</assembly>\n' % reads_file_base)
        pwd_seq_file_16s_Tablet_xml_handle.write('        <reference>%s_16s.fa</reference>\n' % reads_file_base)
        pwd_seq_file_16s_Tablet_xml_handle.write('        <contig>Marker</contig>\n')
        pwd_seq_file_16s_Tablet_xml_handle.write('</tablet>\n')
        pwd_seq_file_16s_Tablet_xml_handle.close()

        pwd_seq_file_ctg_Tablet_xml_handle = open(pwd_seq_file_ctg_Tablet_xml, 'w')
        pwd_seq_file_ctg_Tablet_xml_handle.write('<tablet>\n')
        pwd_seq_file_ctg_Tablet_xml_handle.write('        <assembly>%s_ctg.sam</assembly>\n' % reads_file_base)
        pwd_seq_file_ctg_Tablet_xml_handle.write('        <reference>%s_ctg.fa</reference>\n' % reads_file_base)
        pwd_seq_file_ctg_Tablet_xml_handle.write('        <contig>Contig</contig>\n')
        pwd_seq_file_ctg_Tablet_xml_handle.write('</tablet>\n')
        pwd_seq_file_ctg_Tablet_xml_handle.close()

    # remove tmp files
    os.system('rm %s/%s/%s*.bt2' % (mafft_seq_folder, reads_file_base, reads_file_base))


def get_min_dist_to_ref_end(cigar_str, cigar_pos, ref_len):
    cigar_aln_len = get_cigar_aln_len(cigar_splitter(cigar_str))
    cigar_dist_to_left = cigar_pos - 1
    cigar_dist_to_right = ref_len - cigar_pos - cigar_aln_len + 1
    min_dist_to_mini_end = min(cigar_dist_to_left, cigar_dist_to_right)
    return min_dist_to_mini_end


def get_linked_to_ref_end_cigar_num_and_pct(min_dist_to_ref_end_list):
    linked_to_ref_end_cigar_num = 0
    for each_min_dist in min_dist_to_ref_end_list:
        if each_min_dist <= 10:
            linked_to_ref_end_cigar_num += 1
    linked_to_ref_end_cigar_pct = linked_to_ref_end_cigar_num * 100 / len(min_dist_to_ref_end_list)
    return linked_to_ref_end_cigar_num, linked_to_ref_end_cigar_pct


def get_all_matched_pos(linking_cigar_list, linking_pos_list):

    all_matched_pos = set()
    for (each_linking_cigar, each_linking_pos) in zip(linking_cigar_list, linking_pos_list):
        current_cigar_aligned_len = get_cigar_aln_len(cigar_splitter(each_linking_cigar))
        matched_seq_end = each_linking_pos + current_cigar_aligned_len
        pos_list = list(range(each_linking_pos, matched_seq_end))
        all_matched_pos.update(pos_list)
    return all_matched_pos


def add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                      ref_dict_16s, ref_dict_16s_from,
                                      ref_dict_ctg, ref_dict_ctg_from,
                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                      marker_to_ctg_gnm_Key_connector):

    for each_16s_ref in ref_dict_16s:
        for each_ctg_ref in ref_dict_ctg:
            marker_to_ctg_key = '%s%s%s' % (each_16s_ref, marker_to_ctg_gnm_Key_connector, each_ctg_ref)

            if marker_to_ctg_key not in marker_to_ctg_LinkingRecord_dict:
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key] = LinkingRecord()
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_l = each_16s_ref
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_r = each_ctg_ref
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_len_l = marker_len_dict[each_16s_ref]
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linked_seq_len_r = ctg_len_dict[each_ctg_ref]

            marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_reads_base.append(qualified_read)

            if ref_dict_16s_from in ['r1', 'both']:
                marker_side_cigar_r1 = list(MappingRecord_dict[qualified_read].r1_16s_ref_dict[each_16s_ref].values())[0]
                marker_side_cigar_pos_r1 = list(MappingRecord_dict[qualified_read].r1_16s_ref_dict[each_16s_ref].keys())[0]
                marker_side_cigar_r1_min_end_dist = get_min_dist_to_ref_end(marker_side_cigar_r1,
                                                                            marker_side_cigar_pos_r1,
                                                                            marker_len_dict[each_16s_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_l.append(marker_side_cigar_pos_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_l.append(marker_side_cigar_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_l.append(
                    marker_side_cigar_r1_min_end_dist)

            if ref_dict_16s_from in ['r2', 'both']:
                marker_side_cigar_r2 = list(MappingRecord_dict[qualified_read].r2_16s_ref_dict[each_16s_ref].values())[0]
                marker_side_cigar_pos_r2 = list(MappingRecord_dict[qualified_read].r2_16s_ref_dict[each_16s_ref].keys())[0]
                marker_side_cigar_r2_min_end_dist = get_min_dist_to_ref_end(marker_side_cigar_r2,
                                                                            marker_side_cigar_pos_r2,
                                                                            marker_len_dict[each_16s_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_l.append(marker_side_cigar_pos_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_l.append(marker_side_cigar_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_l.append(
                    marker_side_cigar_r2_min_end_dist)

            if ref_dict_ctg_from in ['r1', 'both']:
                ctg_side_cigar_r1 = list(MappingRecord_dict[qualified_read].r1_ctg_ref_dict[each_ctg_ref].values())[
                    0]
                ctg_side_cigar_pos_r1 = \
                list(MappingRecord_dict[qualified_read].r1_ctg_ref_dict[each_ctg_ref].keys())[0]
                ctg_side_cigar_r1_min_end_dist = get_min_dist_to_ref_end(ctg_side_cigar_r1, ctg_side_cigar_pos_r1,
                                                                         ctg_len_dict[each_ctg_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_r.append(ctg_side_cigar_pos_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_r.append(ctg_side_cigar_r1)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_r.append(
                    ctg_side_cigar_r1_min_end_dist)

            if ref_dict_ctg_from in ['r2', 'both']:
                ctg_side_cigar_r2 = list(MappingRecord_dict[qualified_read].r2_ctg_ref_dict[each_ctg_ref].values())[
                    0]
                ctg_side_cigar_pos_r2 = \
                list(MappingRecord_dict[qualified_read].r2_ctg_ref_dict[each_ctg_ref].keys())[0]
                ctg_side_cigar_r2_min_end_dist = get_min_dist_to_ref_end(ctg_side_cigar_r2, ctg_side_cigar_pos_r2,
                                                                         ctg_len_dict[each_ctg_ref])
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_pos_r.append(ctg_side_cigar_pos_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].linking_cigar_r.append(ctg_side_cigar_r2)
                marker_to_ctg_LinkingRecord_dict[marker_to_ctg_key].min_dist_to_end_r.append(
                    ctg_side_cigar_r2_min_end_dist)


def get_unrecovered_markers(marker_all, marker_recovered):
    unrecovered_markers = []
    for each_marker in marker_all:
        if each_marker not in marker_recovered:
            unrecovered_markers.append(each_marker)
    return sorted(unrecovered_markers)


def link_16s(args):

    ###################################################### file in/out #####################################################

    # file in
    output_prefix                       = args['p']
    reads_file_r1                       = args['r1']
    reads_file_r2                       = args['r2']
    mag_folder                          = args['mag']
    mag_file_extension                  = args['x']
    marker_gene_seqs                    = args['marker']
    min_iden_16s                        = args['min_iden_16s']
    min_cov_16s                         = args['min_cov_16s']
    min_aln_16s                         = args['min_aln_16s']
    min_link_num                        = args['min_link']
    num_threads                         = args['t']
    keep_quiet                          = args['quiet']
    force_overwrite                     = args['force']
    keep_tmp                           = args['tmp']
    test_mode                           = args['test_mode']
    mismatch_cutoff                     = args['mismatch']
    min_M_pct                           = args['min_M_pct']
    within_gnm_linkage_num_diff         = args['link_num_diff']
    min_len_16s                         = args['min_len_16s']
    min_M_len_16s                       = args['min_M_len_16s']
    min_M_len_ctg                       = args['min_M_len_ctg']
    reads_vs_16s_sam                    = args['sorted_sam16s']
    no_polish                           = args['no_polish']
    round_2_mira                        = args['mira']
    mira_tmp_dir                        = args['mira_tmp']
    keep_ctg_end_16s                    = args['keep_ctg_end_16s']
    vis_all                             = args['vis_all']

    pwd_barrnap_exe                     = 'barrnap'
    pwd_makeblastdb_exe                 = 'makeblastdb'
    pwd_blastn_exe                      = 'blastn'
    pwd_bowtie2_build_exe               = 'bowtie2-build'
    pwd_bowtie2_exe                     = 'bowtie2'
    pwd_samtools_exe                    = 'samtools'
    pwd_spades_exe                      = 'spades.py'
    seqtk_exe                           = 'seqtk'

    marker_to_ctg_gnm_Key_connector     = '___M___'
    gnm_to_ctg_connector                = '___C___'
    mini_assembly_to_16s_ctg_connector  = '___Mini___'
    read_to_marker_connector            = '___r___'
    end_seq_len                         = 500
    ctg_level_min_link                  = 3
    end_ctg_len_for_vis                 = 600
    keep_short_M                        = True
    gap_N_num                           = 50
    min_M_len_mini                      = 75
    short_M_len                         = 75
    max_short_cigar_pct_cutoff          = 85
    linked_to_ctg_end_cigar_num_cutoff  = 1
    linked_to_ctg_end_cigar_pct_cutoff  = 20

    blast_parameters = '-evalue 1e-5 -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen" -task blastn -num_threads %s' % num_threads
    bowtie_parameter = '--xeq --local --all --no-unal -N 1 -L 30'

    remove_ending_16s_seqs = True
    if keep_ctg_end_16s is True:
        remove_ending_16s_seqs = False

    ################################################ check dependencies ################################################

    # check whether executables exist
    program_list = [pwd_barrnap_exe, pwd_makeblastdb_exe, pwd_blastn_exe, pwd_bowtie2_build_exe, pwd_bowtie2_exe, pwd_samtools_exe]
    not_detected_programs = []
    for needed_program in program_list:
        if find_executable(needed_program) is None:
            not_detected_programs.append(needed_program)

    if not_detected_programs != []:
        print('%s not detected, program exited!' % ','.join(not_detected_programs))
        exit()

    ################################################# check input files ################################################

    if os.path.isfile(marker_gene_seqs) is False:
        print('%s not found, program exited!' % os.path.basename(marker_gene_seqs))
        exit()

    # get input mag file list
    mag_file_re = '%s/*%s' % (mag_folder, mag_file_extension)
    mag_file_list = [os.path.basename(file_name) for file_name in glob.glob(mag_file_re)]
    if len(mag_file_list) == 0:
        print('No MAG detected, program exited!')
        exit()

    ############################################# create working directory #############################################

    # create working directory
    working_directory = '%s_MarkerMAG_wd' % output_prefix
    pwd_log_file      = '%s/%s.log'       % (working_directory, output_prefix)

    if (os.path.isdir(working_directory) is True) and (force_overwrite is False):
        print('Working directory detected, program exited!')
        exit()
    else:
        force_create_folder(working_directory)

    step_1_wd = '%s/%s_rd1_wd' % (working_directory, output_prefix)
    step_2_wd = '%s/%s_rd2_wd' % (working_directory, output_prefix)
    os.mkdir(step_1_wd)

    ############################################## check input reads format ############################################

    r1_path, r1_basename, r1_ext = sep_path_basename_ext(reads_file_r1)
    r2_path, r2_basename, r2_ext = sep_path_basename_ext(reads_file_r2)

    reads_file_r1_fasta = reads_file_r1
    reads_file_r2_fasta = reads_file_r2
    if ('q' in r1_ext) and ('q' in r2_ext):

        reads_file_r1_fasta_to_check = '%s/%s.fasta' % (r1_path, r1_basename)
        reads_file_r2_fasta_to_check = '%s/%s.fasta' % (r2_path, r2_basename)

        if (os.path.isfile(reads_file_r1_fasta_to_check) is True) and (os.path.isfile(reads_file_r2_fasta_to_check) is True):
            reads_file_r1_fasta = reads_file_r1_fasta_to_check
            reads_file_r2_fasta = reads_file_r2_fasta_to_check

        else:
            reads_file_r1_fasta = '%s/%s.fasta' % (step_1_wd, r1_basename)
            reads_file_r2_fasta = '%s/%s.fasta' % (step_1_wd, r2_basename)

            if num_threads >= 2:
                num_threads_SeqIO_convert_worker = 2
            else:
                num_threads_SeqIO_convert_worker = 1

            pool = mp.Pool(processes=num_threads_SeqIO_convert_worker)
            pool.map(SeqIO_convert_worker, [[reads_file_r1, 'fastq', reads_file_r1_fasta, 'fasta-2line'], [reads_file_r2, 'fastq', reads_file_r2_fasta, 'fasta-2line']])
            pool.close()
            pool.join()

    ################################################ prepare preset parameters to use ################################################

    report_and_log(('mismatch_cutoff:\t%s%s'                % (mismatch_cutoff, '%')), pwd_log_file, keep_quiet)
    report_and_log(('min_M_len_16s:\t%s bp'                 % min_M_len_16s), pwd_log_file, keep_quiet)
    report_and_log(('min_M_len_ctg:\t%s bp'                 % min_M_len_ctg), pwd_log_file, keep_quiet)
    report_and_log(('min_M_pct:\t%s%s'                      % (min_M_pct, '%')), pwd_log_file, keep_quiet)
    report_and_log(('min_link_num:\t%s'                     % min_link_num), pwd_log_file, keep_quiet)
    report_and_log(('ctg_level_min_link:\t%s'               % (ctg_level_min_link)), pwd_log_file, keep_quiet)
    report_and_log(('end_seq_len:\t%s bp'                   % (end_seq_len)), pwd_log_file, keep_quiet)

    ######################## check genomic sequence type and prepare files for making blast db #########################

    input_mag_folder_no_path            = mag_folder.split('/')[-1]
    mag_folder_in_wd                    = '%s/input_MAGs'                       % step_1_wd
    prefixed_mag_folder                 = '%s/%s_prefixed'                      % (mag_folder_in_wd, input_mag_folder_no_path)
    combined_input_gnms                 = '%s/%s_combined.fa'                   % (mag_folder_in_wd, input_mag_folder_no_path)
    combined_input_gnms_no_ending_16s   = '%s/%s_combined_no_ending_16s.fa'     % (mag_folder_in_wd, input_mag_folder_no_path)
    barrnap_wd                          = '%s/input_MAGs/barrnap_wd'            % step_1_wd
    combined_barrnap_gff                = '%s/input_MAGs/combined_barrnap.gff'  % step_1_wd

    # create folder
    os.mkdir(mag_folder_in_wd)
    os.mkdir(prefixed_mag_folder)

    # add mag id to its sequences
    argument_list_for_barrnap = []
    for mag_in in mag_file_list:
        mag_basename    = '.'.join(mag_in.split('.')[:-1])
        pwd_mag_in      = '%s/%s' % (mag_folder, mag_in)
        pwd_mag_renamed = '%s/%s' % (prefixed_mag_folder, mag_in)
        pwd_barrnap_ffn = '%s/%s.ffn' % (barrnap_wd, mag_basename)
        pwd_barrnap_gff = '%s/%s.gff' % (barrnap_wd, mag_basename)
        pwd_barrnap_log = '%s/%s.log' % (barrnap_wd, mag_basename)
        barrnap_cmd = '%s --quiet -o %s %s > %s 2> %s' % (pwd_barrnap_exe, pwd_barrnap_ffn, pwd_mag_renamed, pwd_barrnap_gff, pwd_barrnap_log)
        argument_list_for_barrnap.append(barrnap_cmd)
        rename_seq(pwd_mag_in, pwd_mag_renamed, mag_basename, gnm_to_ctg_connector)

    # combine prefixed MAGs
    os.system('cat %s/*%s > %s' % (prefixed_mag_folder, mag_file_extension, combined_input_gnms))

    ########## run barrnap on prefixed MAGs ##########

    os.mkdir(barrnap_wd)

    # run barrnap with multiprocessing
    pool = mp.Pool(processes=num_threads)
    pool.map(os.system, argument_list_for_barrnap)
    pool.close()
    pool.join()

    # remove index files
    os.system('rm %s/*.fai' % prefixed_mag_folder)
    os.system('cat %s/*.gff > %s' % (barrnap_wd, combined_barrnap_gff))

    ########## remove 16S sequences at the end of contigs ##########

    ctg_len_dict = {}
    for each_ctg_record in SeqIO.parse(combined_input_gnms, 'fasta'):
        ctg_len_dict[each_ctg_record.id] = len(each_ctg_record.seq)

    ctg_ended_16s_to_keep_part_dict = dict()
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
            if left_gap <= 100:
                ctg_ended_16s_to_keep_part_dict[ctg_id] = '%s-%s' % ((end_pos + 1), ctg_len)
            elif right_gap <= 100:
                ctg_ended_16s_to_keep_part_dict[ctg_id] = '%s-%s' % (1, start_pos)

    combined_input_gnms_no_ending_16s_handle = open(combined_input_gnms_no_ending_16s, 'w')
    for each_ctg in SeqIO.parse(combined_input_gnms, 'fasta'):
        ctg_id = each_ctg.id
        ctg_seq = str(each_ctg.seq)
        if ctg_id not in ctg_ended_16s_to_keep_part_dict:
            combined_input_gnms_no_ending_16s_handle.write('>%s\n' % ctg_id)
            combined_input_gnms_no_ending_16s_handle.write('%s\n' % ctg_seq)
        else:
            keep_region_str = ctg_ended_16s_to_keep_part_dict[ctg_id].split('-')
            keep_region_l = int(keep_region_str[0])
            keep_region_r = int(keep_region_str[1])
            combined_input_gnms_no_ending_16s_handle.write('>%s\n' % ctg_id)
            combined_input_gnms_no_ending_16s_handle.write('%s\n' % ctg_seq[(keep_region_l - 1): keep_region_r])
    combined_input_gnms_no_ending_16s_handle.close()

    ########################################### define folder and file name ############################################

    input_16s_folder_in_wd                      = '%s/input_16S'                                           % step_1_wd
    input_reads_to_16s_sam_bowtie               = '%s/%s_input_reads_to_16S.sam'                           % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_bowtie_log           = '%s/%s_input_reads_to_16S.log'                           % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_sorted               = '%s/%s_input_reads_to_16S_sorted.sam'                    % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_sorted_log           = '%s/%s_input_reads_to_16S_sorted.log'                    % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_sorted_line_num      = '%s/%s_input_reads_to_16S_sorted_lines.txt'              % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_sorted_split_folder  = '%s/%s_input_reads_to_16S_sorted_split'                  % (step_1_wd, output_prefix)
    input_reads_to_16s_sam_MappingRecord_folder = '%s/%s_input_reads_to_16S_MappingRecord'                 % (step_1_wd, output_prefix)
    blast_results_all_vs_all_16s                = '%s/%s_16S_all_vs_all_blastn.tab'                        % (step_1_wd, output_prefix)
    pairwise_marker_similarity                  = '%s/%s_pairwise_marker_similarity.txt'                   % (step_1_wd, output_prefix)
    linkages_QC_txt                             = '%s/%s_linkages_QC.txt'                                  % (step_1_wd, output_prefix)
    link_stats_combined                         = '%s/%s_stats_combined.txt'                               % (step_1_wd, output_prefix)
    link_stats_combined_sorted                  = '%s/%s_stats_combined_sorted.txt'                        % (step_1_wd, output_prefix)
    link_stats_combined_filtered_s1             = '%s/%s_stats_combined_filtered.txt'                      % (step_1_wd, output_prefix)
    linking_reads_rd1                           = '%s/%s_linking_reads_rd1.txt'                            % (step_1_wd, output_prefix)
    rd1_r1_to_extract                           = '%s/rd1_r1_to_extract.txt'                               % step_1_wd
    rd1_r2_to_extract                           = '%s/rd1_r2_to_extract.txt'                               % step_1_wd
    rd1_extracted_p_r1                          = '%s/rd1_extracted_R1.fasta'                              % step_1_wd
    rd1_extracted_p_r2                          = '%s/rd1_extracted_R2.fasta'                              % step_1_wd
    rd1_extracted_to_gnm_sam                    = '%s/rd1_extracted_to_gnm.sam'                            % step_1_wd
    rd1_extracted_to_gnm_sam_log                = '%s/rd1_extracted_to_gnm.sam.log'                        % step_1_wd
    rd1_extracted_to_gnm_sam_sorted             = '%s/rd1_extracted_to_gnm_sorted.sam'                     % step_1_wd
    rd1_extracted_to_gnm_sam_sorted_log         = '%s/rd1_extracted_to_gnm_sorted.log'                     % step_1_wd
    linking_reads_tab                           = '%s/linking_reads.txt'                                   % step_1_wd
    linking_reads_r1_txt                        = '%s/rd1_linking_reads_R1.txt'                            % step_1_wd
    linking_reads_r2_txt                        = '%s/rd1_linking_reads_R2.txt'                            % step_1_wd
    linking_reads_r1_fasta                      = '%s/rd1_linking_reads_R1.fasta'                          % step_1_wd
    linking_reads_r2_fasta                      = '%s/rd1_linking_reads_R2.fasta'                          % step_1_wd
    linked_contigs_txt                          = '%s/linked_contigs_rd1.txt'                              % step_1_wd
    linked_contigs_fasta                        = '%s/linked_contigs_rd1.fasta'                            % step_1_wd
    link_vis_folder_rd1                         = '%s/%s_linkage_visualization_rd1'                        % (working_directory, output_prefix)
    link_vis_folder_rd1_for_debugging           = '%s/%s_linkage_visualization_rd1_for_debugging'          % (step_1_wd, output_prefix)

    ###################################### quality filter 16S sequences ######################################

    # copy input 16S into wd
    os.mkdir(input_16s_folder_in_wd)
    os.system('cp %s %s/' % (marker_gene_seqs, input_16s_folder_in_wd))

    # polish input 16S by default
    marker_path, marker_base, marker_ext = sep_path_basename_ext(marker_gene_seqs)
    input_16s_in_wd        = '%s/%s%s'       % (input_16s_folder_in_wd, marker_base, marker_ext)
    input_16s_qc           = '%s/%s.QC%s'    % (input_16s_folder_in_wd, marker_base, marker_ext)
    input_16s_qc_no_ext    = '%s/%s.QC'      % (input_16s_folder_in_wd, marker_base)
    input_16s_qc_in_wd     = '%s/%s.QC%s'    % (working_directory, marker_base, marker_ext)

    # QC 16S
    if no_polish is False:
        report_and_log(('Round 1: quality filtering input 16S rRNA genes to'), pwd_log_file, keep_quiet)
        report_and_log('Round 1: 1) remove non-16S fragements on input 16S gene sequences ', pwd_log_file, keep_quiet)
        report_and_log(('Round 1: 2) remove 16S gene sequences shorter than %s bp' % min_len_16s), pwd_log_file, keep_quiet)
    else:
        report_and_log(('Round 1: Removing input 16S rRNA sequences shorter than %s bp' % min_len_16s), pwd_log_file, keep_quiet)

    qc_16s(input_16s_in_wd, input_16s_qc, no_polish, min_len_16s)
    os.system('cp %s %s/' % (input_16s_qc, working_directory))
    os.system('rm %s' % input_16s_in_wd)
    report_and_log(('Round 1: quality-filtered 16S rRNA gene sequences exported to:'), pwd_log_file, keep_quiet)
    report_and_log((input_16s_qc_in_wd), pwd_log_file, keep_quiet)

    ####################################################################################################################
    ############################################### first round linking ################################################
    ####################################################################################################################

    ######################################## map reads to marker gene sequences ########################################

    bowtie_build_cmd = '%s --quiet --threads %s -f %s %s' % (pwd_bowtie2_build_exe, num_threads, input_16s_qc, input_16s_qc_no_ext)
    os.system(bowtie_build_cmd)
    report_and_log((bowtie_build_cmd), pwd_log_file, True)

    if reads_vs_16s_sam is None:
        report_and_log(('Round 1: Mapping input reads to marker genes'), pwd_log_file, keep_quiet)
        bowtie_read_to_16s_cmd = '%s -x %s -U %s,%s -S %s -p %s -f %s 2> %s' % (pwd_bowtie2_exe, input_16s_qc_no_ext, reads_file_r1_fasta, reads_file_r2_fasta, input_reads_to_16s_sam_bowtie, num_threads, bowtie_parameter, input_reads_to_16s_sam_bowtie_log)
        report_and_log((bowtie_read_to_16s_cmd), pwd_log_file, True)
        os.system(bowtie_read_to_16s_cmd)
        os.remove(input_reads_to_16s_sam_bowtie_log)

        # sort sam file first
        report_and_log(('Round 1: sorting mappping results'), pwd_log_file, keep_quiet)
        sort_by_read_cmd = '%s sort -n -O sam --threads %s -o %s %s 2> %s' % (pwd_samtools_exe, num_threads, input_reads_to_16s_sam_sorted, input_reads_to_16s_sam_bowtie, input_reads_to_16s_sam_sorted_log)
        os.system(sort_by_read_cmd)
        os.remove(input_reads_to_16s_sam_bowtie)
        os.remove(input_reads_to_16s_sam_sorted_log)
    else:
        report_and_log(('Round 1: Sorted sam file detected'), pwd_log_file, keep_quiet)
        input_reads_to_16s_sam_sorted = reads_vs_16s_sam

    ##################################################### read in sam file ####################################################

    # get marker len dict
    marker_seq_dict = {}
    marker_len_dict = {}
    for each_marker_record in SeqIO.parse(input_16s_qc, 'fasta'):
        marker_seq_dict[each_marker_record.id] = str(each_marker_record.seq)
        marker_len_dict[each_marker_record.id] = len(each_marker_record.seq)

    # get the number of lines per file
    report_and_log(('Round 1: calculating the number of lines per subset'), pwd_log_file, keep_quiet)
    os.system('wc -l %s > %s' % (input_reads_to_16s_sam_sorted, input_reads_to_16s_sam_sorted_line_num))
    sam16s_line_num = int(open(input_reads_to_16s_sam_sorted_line_num).readline().strip().split(' ')[0])
    os.remove(input_reads_to_16s_sam_sorted_line_num)
    line_num_per_file = int(round(sam16s_line_num/(num_threads*10))) + 10

    report_and_log(('Round 1: splitting sam file'), pwd_log_file, keep_quiet)
    os.mkdir(input_reads_to_16s_sam_sorted_split_folder)
    split_sam_cmd = 'split -l %s %s %s/splitted_sam_ ' % (line_num_per_file, input_reads_to_16s_sam_sorted, input_reads_to_16s_sam_sorted_split_folder)
    os.system(split_sam_cmd)

    report_and_log(('Round 1: analysing mappping results with %s threads' % num_threads), pwd_log_file, keep_quiet)
    os.mkdir(input_reads_to_16s_sam_MappingRecord_folder)

    # get splitted sam file list
    splitted_sam_file_list = [os.path.basename(file_name) for file_name in glob.glob('%s/splitted_sam_*' % input_reads_to_16s_sam_sorted_split_folder)]

    # prepare lol for mp worker
    list_for_parse_sam16s_worker = []
    splitted_sam_mp_file_set = set()
    for splitted_sam_file in splitted_sam_file_list:
        pwd_splitted_sam_file    = '%s/%s'        % (input_reads_to_16s_sam_sorted_split_folder, splitted_sam_file)
        pwd_splitted_sam_mp_file = '%s/%s_mp.txt' % (input_reads_to_16s_sam_MappingRecord_folder, splitted_sam_file)
        splitted_sam_mp_file_set.add(pwd_splitted_sam_mp_file)
        list_for_parse_sam16s_worker.append([pwd_splitted_sam_file,
                                             pwd_splitted_sam_mp_file,
                                             min_M_len_16s,
                                             mismatch_cutoff,
                                             marker_len_dict])

    pool_parse_sam16s = mp.Pool(processes=num_threads)
    pool_parse_sam16s.map(parse_sam16s_worker, list_for_parse_sam16s_worker)
    pool_parse_sam16s.close()
    pool_parse_sam16s.join()

    report_and_log(('Round 1: removing splitted subsets from disk'), pwd_log_file, keep_quiet)
    os.system('rm -r %s' % input_reads_to_16s_sam_sorted_split_folder)

    # reads filter results into dict
    report_and_log(('Round 1: reading filtered alignments into dict'), pwd_log_file, keep_quiet)
    MappingRecord_dict = {}
    read_base_to_pop = set()
    for each_mp_file in splitted_sam_mp_file_set:
        first_line_base = True
        with open(each_mp_file) as each_mp_file_opened:
            for each_read_base in each_mp_file_opened:
                each_read_base_split = each_read_base.strip().split('\t')
                current_read_base___id = each_read_base_split[0]
                current_read_base___qualified_reads = each_read_base_split[1]
                current_read_base___consider_r1_unmapped_mate = each_read_base_split[2]
                current_read_base___consider_r2_unmapped_mate = each_read_base_split[3]
                current_read_base___both_mapped_to_16s = each_read_base_split[4]
                current_read_base___r1_16s_ref_dict = get_r12_16s_ref_dict_from_str(each_read_base_split[5])
                current_read_base___r2_16s_ref_dict = get_r12_16s_ref_dict_from_str(each_read_base_split[6])
                current_read_base___r1_16s_refs_no_ignored = get_no_ignored_dict_from_str(each_read_base_split[7])
                current_read_base___r2_16s_refs_no_ignored = get_no_ignored_dict_from_str(each_read_base_split[8])
                current_read_base___shared_16s_refs_no_ignored = get_no_ignored_dict_from_str(each_read_base_split[9])

                if first_line_base is True:
                    read_base_to_pop.add(current_read_base___id)
                    first_line_base = False
                else:
                    MappingRecord_dict[current_read_base___id] = MappingRecord()
                    MappingRecord_dict[current_read_base___id].qualified_reads = True

                    if current_read_base___consider_r1_unmapped_mate == '1':
                        MappingRecord_dict[current_read_base___id].consider_r1_unmapped_mate = True
                    if current_read_base___consider_r2_unmapped_mate == '1':
                        MappingRecord_dict[current_read_base___id].consider_r2_unmapped_mate = True
                    if current_read_base___both_mapped_to_16s == '1':
                        MappingRecord_dict[current_read_base___id].both_mapped_to_16s = True

                    MappingRecord_dict[current_read_base___id].r1_16s_ref_dict = current_read_base___r1_16s_ref_dict
                    MappingRecord_dict[current_read_base___id].r2_16s_ref_dict = current_read_base___r2_16s_ref_dict
                    MappingRecord_dict[current_read_base___id].r1_16s_refs_no_ignored = current_read_base___r1_16s_refs_no_ignored
                    MappingRecord_dict[current_read_base___id].r2_16s_refs_no_ignored = current_read_base___r2_16s_refs_no_ignored
                    MappingRecord_dict[current_read_base___id].shared_16s_refs_no_ignored = current_read_base___shared_16s_refs_no_ignored

    ############################# extract sequences of both mates of qualified reads #############################

    report_and_log(('Round 1: extracting sequences of reads matched to 16S'), pwd_log_file, keep_quiet)

    # write out id of reads to extract
    to_extract_read_base_list = sorted(list(MappingRecord_dict.keys()))
    with open(rd1_r1_to_extract, 'w') as rd1_r1_to_extract_handle:
        rd1_r1_to_extract_handle.write('%s\n' % '\n'.join([('%s.1' % i) for i in to_extract_read_base_list]))
    with open(rd1_r2_to_extract, 'w') as rd1_r2_to_extract_handle:
        rd1_r2_to_extract_handle.write('%s\n' % '\n'.join([('%s.2' % i) for i in to_extract_read_base_list]))

    # extract reads with seqtk
    seqtk_extract_cmd_rd1_r1 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r1_fasta, rd1_r1_to_extract, rd1_extracted_p_r1)
    seqtk_extract_cmd_rd1_r2 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r2_fasta, rd1_r2_to_extract, rd1_extracted_p_r2)
    report_and_log((seqtk_extract_cmd_rd1_r1), pwd_log_file, True)
    report_and_log((seqtk_extract_cmd_rd1_r2), pwd_log_file, True)
    os.system(seqtk_extract_cmd_rd1_r1)
    os.system(seqtk_extract_cmd_rd1_r2)
    if keep_tmp is False:
        os.remove(rd1_r1_to_extract)
        os.remove(rd1_r2_to_extract)

    ############################# map extracted reads to combined input genomes #############################

    report_and_log(('Round 1: mapping extracted reads to input genomes'), pwd_log_file, keep_quiet)

    combined_input_gnms_no_ext                  = '.'.join(combined_input_gnms.split('.')[:-1])
    combined_input_gnms_no_ending_16s_no_ext    = '.'.join(combined_input_gnms_no_ending_16s.split('.')[:-1])

    bowtie_build_input_gnm_cmd          = '%s --quiet --threads %s -f %s %s'            % (pwd_bowtie2_build_exe, num_threads, combined_input_gnms, combined_input_gnms_no_ext)
    bowtie_cmd_rd1_extracted_to_mag     = '%s -x %s -U %s,%s -S %s -p %s -f %s 2> %s'   % (pwd_bowtie2_exe, combined_input_gnms_no_ext, rd1_extracted_p_r1, rd1_extracted_p_r2, rd1_extracted_to_gnm_sam, num_threads, bowtie_parameter, rd1_extracted_to_gnm_sam_log)
    if remove_ending_16s_seqs is True:
        bowtie_build_input_gnm_cmd      = '%s --quiet --threads %s -f %s %s'            % (pwd_bowtie2_build_exe, num_threads, combined_input_gnms_no_ending_16s, combined_input_gnms_no_ending_16s_no_ext)
        bowtie_cmd_rd1_extracted_to_mag = '%s -x %s -U %s,%s -S %s -p %s -f %s 2> %s'   % (pwd_bowtie2_exe, combined_input_gnms_no_ending_16s_no_ext, rd1_extracted_p_r1, rd1_extracted_p_r2, rd1_extracted_to_gnm_sam, num_threads, bowtie_parameter, rd1_extracted_to_gnm_sam_log)

    # index ref
    os.system(bowtie_build_input_gnm_cmd)
    report_and_log((bowtie_cmd_rd1_extracted_to_mag), pwd_log_file, True)
    os.system(bowtie_cmd_rd1_extracted_to_mag)
    os.remove(rd1_extracted_to_gnm_sam_log)

    # sort sam file first
    sort_by_read_cmd = '%s sort -n -O sam --threads %s -o %s %s 2> %s' % (pwd_samtools_exe, num_threads, rd1_extracted_to_gnm_sam_sorted, rd1_extracted_to_gnm_sam, rd1_extracted_to_gnm_sam_sorted_log)
    os.system(sort_by_read_cmd)
    os.remove(rd1_extracted_to_gnm_sam_sorted_log)

    ######################################### read mapping results of rd1 extracted mates into mp dict  #########################################

    report_and_log(('Round 1: analysing mappping results'), pwd_log_file, keep_quiet)

    ctg_len_dict = {}
    if remove_ending_16s_seqs is False:
        for each_ctg_record in SeqIO.parse(combined_input_gnms, 'fasta'):
            ctg_len_dict[each_ctg_record.id] = len(each_ctg_record.seq)
    else:
        for each_ctg_record in SeqIO.parse(combined_input_gnms_no_ending_16s, 'fasta'):
            ctg_len_dict[each_ctg_record.id] = len(each_ctg_record.seq)

    ctg_ignore_region_dict = {}
    if remove_ending_16s_seqs is False:
        ctg_ignore_region_dict = get_regions_to_ignore_from_barrnap_output(combined_barrnap_gff, ctg_len_dict)

    processed_num = 0
    current_read_base = ''
    current_read_base_r1_ctg_ref_dict = dict()
    current_read_base_r2_ctg_ref_dict = dict()
    with open(rd1_extracted_to_gnm_sam_sorted) as rd1_extracted_to_gnm_sam_reformatted_opened:
        for each_read in rd1_extracted_to_gnm_sam_reformatted_opened:
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
                            current_read_base_r1_ctg_ref_dict[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r2_ctg_ref_dict[ref_id] = {ref_pos: cigar}

                elif read_id_base == current_read_base:
                    if cigar != '*':
                        if read_strand == '1':
                            if ref_id not in current_read_base_r1_ctg_ref_dict:
                                current_read_base_r1_ctg_ref_dict[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r1_ctg_ref_dict[ref_id][ref_pos] = cigar

                        if read_strand == '2':
                            if ref_id not in current_read_base_r2_ctg_ref_dict:
                                current_read_base_r2_ctg_ref_dict[ref_id] = {ref_pos: cigar}
                            else:
                                current_read_base_r2_ctg_ref_dict[ref_id][ref_pos] = cigar
                else:
                    ################################### analysis previous read refs ####################################

                    refs_to_ignore_ctg = set()

                    ########## filter r1 ctg refs ##########

                    r1_ctg_refs_passed_qc = {}
                    for r1_ctg_ref in current_read_base_r1_ctg_ref_dict:
                        r1_ctg_ref_matched_pos_dict = current_read_base_r1_ctg_ref_dict[r1_ctg_ref]

                        # one read need to mapped to one ctg only for one time
                        if len(r1_ctg_ref_matched_pos_dict) > 1:
                            refs_to_ignore_ctg.add(r1_ctg_ref)
                        else:
                            r1_ctg_ref_pos = list(r1_ctg_ref_matched_pos_dict.keys())[0]
                            r1_ctg_ref_cigar = r1_ctg_ref_matched_pos_dict[r1_ctg_ref_pos]
                            r1_ctg_ref_len = ctg_len_dict[r1_ctg_ref]
                            qualified_cigar = check_cigar_quality(r1_ctg_ref_cigar, False, 'NA', mismatch_cutoff, min_M_len_ctg, r1_ctg_ref_pos, r1_ctg_ref_len)
                            if qualified_cigar is True:

                                # check if matched to regions need to be ignored
                                matched_to_r1_ref_ignored_region = False
                                if r1_ctg_ref in ctg_ignore_region_dict:
                                    r1_ctg_ref_ends_to_ignore = ctg_ignore_region_dict[r1_ctg_ref]
                                    for to_ignore_region in r1_ctg_ref_ends_to_ignore:
                                        if to_ignore_region == 'left_end':
                                            if r1_ctg_ref_pos <= 50:
                                                matched_to_r1_ref_ignored_region = True
                                        if to_ignore_region == 'right_end':
                                            aln_len, aln_pct, clp_len, clp_pct, mis_pct = get_cigar_stats(cigar_splitter(r1_ctg_ref_cigar))
                                            if (ctg_len_dict[r1_ctg_ref] - r1_ctg_ref_pos - aln_len) <= 50:
                                                matched_to_r1_ref_ignored_region = True

                                if matched_to_r1_ref_ignored_region is False:
                                    r1_ctg_refs_passed_qc[r1_ctg_ref] = [r1_ctg_ref_cigar]
                            else:
                                refs_to_ignore_ctg.add(r1_ctg_ref)

                    ########## filter r2 ctg refs ##########

                    r2_ctg_refs_passed_qc = {}
                    for r2_ctg_ref in current_read_base_r2_ctg_ref_dict:
                        r2_ctg_ref_matched_pos_dict = current_read_base_r2_ctg_ref_dict[r2_ctg_ref]

                        # one read need to mapped to one ctg only for one time
                        if len(r2_ctg_ref_matched_pos_dict) > 1:
                            refs_to_ignore_ctg.add(r2_ctg_ref)
                        else:
                            r2_ctg_ref_pos = list(r2_ctg_ref_matched_pos_dict.keys())[0]
                            r2_ctg_ref_cigar = r2_ctg_ref_matched_pos_dict[r2_ctg_ref_pos]
                            r2_ctg_ref_len = ctg_len_dict.get(r2_ctg_ref, 0)
                            qualified_cigar = check_cigar_quality(r2_ctg_ref_cigar, False, 'NA', mismatch_cutoff, min_M_len_ctg, r2_ctg_ref_pos, r2_ctg_ref_len)
                            if qualified_cigar is True:

                                # check if matched to regions need to be ignored
                                matched_to_r2_ref_ignored_region = False
                                if r2_ctg_ref in ctg_ignore_region_dict:
                                    r2_ctg_ref_ends_to_ignore = ctg_ignore_region_dict[r2_ctg_ref]
                                    for to_ignore_region in r2_ctg_ref_ends_to_ignore:
                                        if to_ignore_region == 'left_end':
                                            if r2_ctg_ref_pos <= 50:
                                                matched_to_r2_ref_ignored_region = True
                                        if to_ignore_region == 'right_end':
                                            aln_len, aln_pct, clp_len, clp_pct, mis_pct = get_cigar_stats(cigar_splitter(r2_ctg_ref_cigar))
                                            if (ctg_len_dict[r2_ctg_ref] - r2_ctg_ref_pos - aln_len) <= 50:
                                                matched_to_r2_ref_ignored_region = True

                                if matched_to_r2_ref_ignored_region is False:
                                    r2_ctg_refs_passed_qc[r2_ctg_ref] = [r2_ctg_ref_cigar]
                            else:
                                refs_to_ignore_ctg.add(r2_ctg_ref)

                    ####################################################################################################

                    r1_ctg_refs_no_ignored = {key: value for key, value in r1_ctg_refs_passed_qc.items() if key not in refs_to_ignore_ctg}
                    r2_ctg_refs_no_ignored = {key: value for key, value in r2_ctg_refs_passed_qc.items() if key not in refs_to_ignore_ctg}

                    # no mate matched to ctg
                    if (len(r1_ctg_refs_no_ignored) == 0) and (len(r2_ctg_refs_no_ignored) == 0):
                        pass

                    # only r1 matched to ctg
                    elif (len(r1_ctg_refs_no_ignored) > 0) and (len(r2_ctg_refs_no_ignored) == 0):
                        MappingRecord_dict[current_read_base].matched_to_ctg = True
                        MappingRecord_dict[current_read_base].r1_ctg_refs_no_ignored = r1_ctg_refs_no_ignored
                        MappingRecord_dict[current_read_base].r1_ctg_ref_dict = current_read_base_r1_ctg_ref_dict
                    # only r2 matched to ctg
                    elif (len(r1_ctg_refs_no_ignored) == 0) and (len(r2_ctg_refs_no_ignored) > 0):
                        MappingRecord_dict[current_read_base].matched_to_ctg = True
                        MappingRecord_dict[current_read_base].r2_ctg_refs_no_ignored = r2_ctg_refs_no_ignored
                        MappingRecord_dict[current_read_base].r2_ctg_ref_dict = current_read_base_r2_ctg_ref_dict

                    # both r1 and r2 matched to ctg
                    else:
                        shared_ctg_ref_set = {key: [r1_ctg_refs_no_ignored[key][0], r2_ctg_refs_no_ignored[key][0]] for key in set(r1_ctg_refs_no_ignored).intersection(set(r2_ctg_refs_no_ignored))}
                        if len(shared_ctg_ref_set) > 0:
                            MappingRecord_dict[current_read_base].matched_to_ctg = True
                            MappingRecord_dict[current_read_base].shared_ctg_refs_no_ignored = shared_ctg_ref_set
                            MappingRecord_dict[current_read_base].r1_ctg_ref_dict = current_read_base_r1_ctg_ref_dict
                            MappingRecord_dict[current_read_base].r2_ctg_ref_dict = current_read_base_r2_ctg_ref_dict

                    ########################################### reset values ###########################################

                    current_read_base = read_id_base
                    current_read_base_r1_ctg_ref_dict = dict()
                    current_read_base_r2_ctg_ref_dict = dict()

                    if cigar != '*':
                        if read_strand == '1':
                            current_read_base_r1_ctg_ref_dict[ref_id] = {ref_pos: cigar}
                        if read_strand == '2':
                            current_read_base_r2_ctg_ref_dict[ref_id] = {ref_pos: cigar}

                    ########################################### report ###########################################

                    processed_num += 1
                    if (processed_num % 50000 == 0):
                        report_and_log(('Round 1: processed %sk pairs of reads' % int(processed_num / 1000)), pwd_log_file, keep_quiet)

        report_and_log(('Round 1: processed %sk' % float("{0:.2f}".format(processed_num / 1000))), pwd_log_file, keep_quiet)

    # remove sam files from disk
    os.remove(rd1_extracted_to_gnm_sam)


    ##################################################### get linkages from MappingRecord_dict #####################################################

    report_and_log(('Round 1: Parsing MappingRecord dict to get linkages'), pwd_log_file, keep_quiet)

    marker_to_ctg_LinkingRecord_dict = {}
    for qualified_read in MappingRecord_dict:

        r1_16s_refs = MappingRecord_dict[qualified_read].r1_16s_refs_no_ignored
        r2_16s_refs = MappingRecord_dict[qualified_read].r2_16s_refs_no_ignored
        shared_16s_refs = MappingRecord_dict[qualified_read].shared_16s_refs_no_ignored
        r1_ctg_refs = MappingRecord_dict[qualified_read].r1_ctg_refs_no_ignored
        r2_ctg_refs = MappingRecord_dict[qualified_read].r2_ctg_refs_no_ignored
        shared_ctg_refs = MappingRecord_dict[qualified_read].shared_ctg_refs_no_ignored

        if (len(shared_16s_refs) > 0) or (len(shared_ctg_refs) > 0):
            if (len(shared_16s_refs) > 0) and (len(shared_ctg_refs) > 0):
                add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                                  shared_16s_refs, 'both', shared_ctg_refs, 'both',
                                                  marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                                  marker_to_ctg_gnm_Key_connector)

            # elif (len(shared_16s_refs) > 0) and (len(shared_ctg_refs) == 0):
            #
            #     if len(r1_ctg_refs) > 0:
            #         add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
            #                                           shared_16s_refs, 'both', r1_ctg_refs, 'r1',
            #                                           marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
            #                                           marker_to_ctg_gnm_Key_connector)
            #
            #     if len(r2_ctg_refs) > 0:
            #         add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
            #                                           shared_16s_refs, 'both', r2_ctg_refs, 'r2',
            #                                           marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
            #                                           marker_to_ctg_gnm_Key_connector)
            #
            # elif (len(shared_16s_refs) == 0) and (len(shared_ctg_refs) > 0):
            #     if len(r1_16s_refs) > 0:
            #         add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
            #                                           r1_16s_refs, 'r1', shared_ctg_refs, 'both',
            #                                           marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
            #                                           marker_to_ctg_gnm_Key_connector)
            #
            #     if len(r2_16s_refs) > 0:
            #         add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
            #                                           r2_16s_refs, 'r2', shared_ctg_refs, 'both',
            #                                           marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
            #                                           marker_to_ctg_gnm_Key_connector)

        else:
            if (len(r1_16s_refs) > 0) and (len(r2_ctg_refs) > 0):
                r2_gnm_refs = {ctg.split(gnm_to_ctg_connector)[0] for ctg in r2_ctg_refs}
                if len(r2_gnm_refs) == 1:
                    add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                                      r1_16s_refs, 'r1', r2_ctg_refs, 'r2',
                                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                                      marker_to_ctg_gnm_Key_connector)

            if (len(r2_16s_refs) > 0) and (len(r1_ctg_refs) > 0):
                r1_gnm_refs = {ctg.split(gnm_to_ctg_connector)[0] for ctg in r1_ctg_refs}
                if len(r1_gnm_refs) == 1:
                    add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                                      r2_16s_refs, 'r2', r1_ctg_refs, 'r1',
                                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                                      marker_to_ctg_gnm_Key_connector)

            if (len(r1_16s_refs) > 0) and (len(r1_ctg_refs) > 0):
                r1_gnm_refs = {ctg.split(gnm_to_ctg_connector)[0] for ctg in r1_ctg_refs}
                if len(r1_gnm_refs) == 1:
                    add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                                      r1_16s_refs, 'r1', r1_ctg_refs, 'r1',
                                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                                      marker_to_ctg_gnm_Key_connector)

            if (len(r2_16s_refs) > 0) and (len(r2_ctg_refs) > 0):
                r2_gnm_refs = {ctg.split(gnm_to_ctg_connector)[0] for ctg in r2_ctg_refs}
                if len(r2_gnm_refs) == 1:
                    add_linkage_to_LinkingRecord_dict(MappingRecord_dict, qualified_read,
                                                      r2_16s_refs, 'r2', r2_ctg_refs, 'r2',
                                                      marker_to_ctg_LinkingRecord_dict, marker_len_dict, ctg_len_dict,
                                                      marker_to_ctg_gnm_Key_connector)

    # filter with link num, short cigar pct and linked to ref end pct
    linkages_QC_txt_handle = open(linkages_QC_txt, 'w')
    linkages_QC_txt_handle.write('Marker\tContig\tLinkages\tLinked_to_16s_end(num pct)\tLinked_to_ctg_end(num pct)\tshort_cigar_pct_16s\tshort_cigar_pct_ctg\tmatched_len_marker\tmatched_len_contig\n')
    marker_to_ctg_linkage_num_dict_after_qc = {}
    for each_link in marker_to_ctg_LinkingRecord_dict:
        linking_reads = marker_to_ctg_LinkingRecord_dict[each_link].linking_reads_base
        if len(linking_reads) >= 3:
            each_link_split = each_link.split(marker_to_ctg_gnm_Key_connector)
            marker_id = each_link_split[0]
            gnm_id = each_link_split[1].split(gnm_to_ctg_connector)[0]
            ctg_id = each_link_split[1].split(gnm_to_ctg_connector)[1]

            linkage_cigar_16s_side_all = marker_to_ctg_LinkingRecord_dict[each_link].linking_cigar_l
            linkage_cigar_ctg_side_all = marker_to_ctg_LinkingRecord_dict[each_link].linking_cigar_r

            # get pct of short aligned cigar
            short_cigar_pct_16s = get_short_cigar_pct(linkage_cigar_16s_side_all, short_M_len)
            short_cigar_pct_ctg = get_short_cigar_pct(linkage_cigar_ctg_side_all, short_M_len)

            # check num/pct of reads linked to 16s and ctg end
            min_dist_list_to_16s_end = marker_to_ctg_LinkingRecord_dict[each_link].min_dist_to_end_l
            min_dist_list_to_ctg_end = marker_to_ctg_LinkingRecord_dict[each_link].min_dist_to_end_r
            linked_to_16s_end_cigar_num, linked_to_16s_end_cigar_pct = get_linked_to_ref_end_cigar_num_and_pct(min_dist_list_to_16s_end)
            linked_to_ctg_end_cigar_num, linked_to_ctg_end_cigar_pct = get_linked_to_ref_end_cigar_num_and_pct(min_dist_list_to_ctg_end)

            # get all matched positions
            all_matched_pos_l = get_all_matched_pos(marker_to_ctg_LinkingRecord_dict[each_link].linking_cigar_l, marker_to_ctg_LinkingRecord_dict[each_link].linking_pos_l)
            all_matched_pos_r = get_all_matched_pos(marker_to_ctg_LinkingRecord_dict[each_link].linking_cigar_r, marker_to_ctg_LinkingRecord_dict[each_link].linking_pos_r)

            linked_to_16s_end = False
            if (linked_to_16s_end_cigar_num > 0) and (linked_to_16s_end_cigar_pct >= 5):
                linked_to_16s_end = True

            linked_to_ctg_end = False
            if (linked_to_ctg_end_cigar_num >= linked_to_ctg_end_cigar_num_cutoff) and (linked_to_ctg_end_cigar_pct >= linked_to_ctg_end_cigar_pct_cutoff):
                linked_to_ctg_end = True

            # write out qc
            linkages_QC_txt_handle.write('%s\t%s\t%s(%s %s)\t%s(%s %s)\t%s\t%s\t%sbp\t%sbp\n' % ('\t'.join(each_link.split('___M___')), len(linking_reads),
                                                                  linked_to_16s_end, linked_to_16s_end_cigar_num, float("{0:.2f}".format(linked_to_16s_end_cigar_pct)),
                                                                  linked_to_ctg_end, linked_to_ctg_end_cigar_num, float("{0:.2f}".format(linked_to_ctg_end_cigar_pct)),
                                                                  float("{0:.2f}".format(short_cigar_pct_16s)),
                                                                  float("{0:.2f}".format(short_cigar_pct_ctg)),
                                                                  len(all_matched_pos_l),
                                                                  len(all_matched_pos_r)))

            if (short_cigar_pct_16s < max_short_cigar_pct_cutoff) and (short_cigar_pct_ctg < max_short_cigar_pct_cutoff):
                if (linked_to_16s_end is True) and (linked_to_ctg_end is True):
                    marker_to_ctg_linkage_num_dict_after_qc[each_link] = len(linking_reads)
                else:
                    if (len(all_matched_pos_l) >= 750) and (len(all_matched_pos_r) >= 750):
                        marker_to_ctg_linkage_num_dict_after_qc[each_link] = len(linking_reads)
    linkages_QC_txt_handle.close()

    # get number of linkages at genome level
    marker_to_gnm_linkage_cigar_dict_16s_side = {}
    marker_to_gnm_linkage_cigar_dict_ctg_side = {}
    marker_to_gnm_link_num = {}
    for each_marker_to_ctg_key in marker_to_ctg_linkage_num_dict_after_qc:
        marker_id = each_marker_to_ctg_key.split(marker_to_ctg_gnm_Key_connector)[0]
        ctg_id = each_marker_to_ctg_key.split(marker_to_ctg_gnm_Key_connector)[1]
        gnm_id = ctg_id.split(gnm_to_ctg_connector)[0]
        marker_to_gnm_key = '%s%s%s' % (marker_id, marker_to_ctg_gnm_Key_connector, gnm_id)
        marker_to_ctg_linkage_cigar_16s_side = marker_to_ctg_LinkingRecord_dict[each_marker_to_ctg_key].linking_cigar_l
        marker_to_ctg_linkage_cigar_ctg_side = marker_to_ctg_LinkingRecord_dict[each_marker_to_ctg_key].linking_cigar_r

        if marker_to_gnm_key not in marker_to_gnm_link_num:
            marker_to_gnm_link_num[marker_to_gnm_key] = marker_to_ctg_linkage_num_dict_after_qc[each_marker_to_ctg_key]
            marker_to_gnm_linkage_cigar_dict_16s_side[marker_to_gnm_key] = marker_to_ctg_linkage_cigar_16s_side
            marker_to_gnm_linkage_cigar_dict_ctg_side[marker_to_gnm_key] = marker_to_ctg_linkage_cigar_ctg_side
        else:
            marker_to_gnm_link_num[marker_to_gnm_key] += marker_to_ctg_linkage_num_dict_after_qc[each_marker_to_ctg_key]
            for each in marker_to_ctg_linkage_cigar_16s_side:
                marker_to_gnm_linkage_cigar_dict_16s_side[marker_to_gnm_key].append(each)
            for each in marker_to_ctg_linkage_cigar_ctg_side:
                marker_to_gnm_linkage_cigar_dict_ctg_side[marker_to_gnm_key].append(each)

    # write out linkages at genome level
    sankey_file_in_handle = open(link_stats_combined, 'w')
    sankey_file_in_handle.write('MarkerGene,GenomicSeq,Number\n')
    for each_linkage in marker_to_gnm_link_num:
        sankey_file_in_handle.write('MarkerGene__%s,GenomicSeq__%s,%s\n' % (
            each_linkage.split(marker_to_ctg_gnm_Key_connector)[0],
            each_linkage.split(marker_to_ctg_gnm_Key_connector)[1],
            marker_to_gnm_link_num[each_linkage]))
    sankey_file_in_handle.close()

    # write out linking reads
    linking_reads_rd1_handle = open(linking_reads_rd1, 'w')
    for each_link in marker_to_ctg_LinkingRecord_dict:
        current_linking_reads = marker_to_ctg_LinkingRecord_dict[each_link].linking_reads_base
        linking_reads_rd1_handle.write('%s\t%s\n' % (each_link, ','.join(current_linking_reads)))
    linking_reads_rd1_handle.close()


    ############################################## get pairwise_16s_iden_dict ##############################################

    report_and_log(('Round 1: Get pairwise 16S rRNA gene identities'), pwd_log_file, keep_quiet)

    # makeblastdn with marker gene sequences
    makeblastdb_16s_cmd = '%s -in %s -dbtype nucl -parse_seqids -logfile /dev/null' % (pwd_makeblastdb_exe, input_16s_qc)
    os.system(makeblastdb_16s_cmd)

    all_vs_all_16s_blastn_cmd = '%s -query %s -db %s -out %s %s' % (pwd_blastn_exe, input_16s_qc, input_16s_qc, blast_results_all_vs_all_16s, blast_parameters)
    os.system(all_vs_all_16s_blastn_cmd)

    pairwise_16s_iden_dict = blast_results_to_pairwise_16s_iden_dict(blast_results_all_vs_all_16s, min_aln_16s, min_cov_16s)

    # write out to file
    pairwise_marker_similarity_handle = open(pairwise_marker_similarity, 'w')
    pairwise_marker_similarity_handle.write('Marker1\tMarker2\tSimilarity\n')
    for marker_pair in pairwise_16s_iden_dict:
        pairwise_marker_similarity_handle.write('%s\t%s\n' % ('\t'.join(marker_pair.split('__|__')), pairwise_16s_iden_dict[marker_pair]))
    pairwise_marker_similarity_handle.close()


    ####################################### filter_linkages_iteratively ########################################

    report_and_log(('Round 1: filtering linkages iteratively'), pwd_log_file, keep_quiet)

    # sort file in
    sort_csv_by_col(link_stats_combined, link_stats_combined_sorted, 'Number')

    filter_linkages_iteratively_new2(link_stats_combined_sorted, pairwise_16s_iden_dict, min_iden_16s, marker_len_dict,
                                    min_link_num, within_gnm_linkage_num_diff, link_stats_combined_filtered_s1,
                                    marker_to_gnm_linkage_cigar_dict_16s_side,
                                    marker_to_gnm_linkage_cigar_dict_ctg_side,
                                    marker_to_ctg_gnm_Key_connector)


    ####################################### get linking reads for visualization ########################################

    report_and_log(('Round 1: Extracting linking reads for visualization'), pwd_log_file, keep_quiet)

    os.mkdir(link_vis_folder_rd1_for_debugging)
    os.mkdir(link_vis_folder_rd1)

    ctgs_to_extract = set()
    all_linking_reads_base_set = set()
    linking_reads_txt_handle = open(linking_reads_tab, 'w')
    for marker_to_ctg in marker_to_ctg_LinkingRecord_dict:
        marker_id = marker_to_ctg.split(marker_to_ctg_gnm_Key_connector)[0]
        ctg_id = marker_to_ctg.split(marker_to_ctg_gnm_Key_connector)[1]
        linking_reads = marker_to_ctg_LinkingRecord_dict[marker_to_ctg].linking_reads_base
        all_linking_reads_base_set.update(linking_reads)
        ctgs_to_extract.add(ctg_id)
        linking_reads_txt_handle.write('%s\t%s\t%s\n' % (marker_id, ctg_id, ','.join(linking_reads)))
    linking_reads_txt_handle.close()

    # write out id of linking reads for extraction
    with open(linking_reads_r1_txt, 'w') as linking_reads_r1_txt_handle:
        linking_reads_r1_txt_handle.write('%s\n' % '\n'.join(sorted([('%s.1' % i) for i in all_linking_reads_base_set])))
    with open(linking_reads_r2_txt, 'w') as linking_reads_r2_txt_handle:
        linking_reads_r2_txt_handle.write('%s\n' % '\n'.join(sorted([('%s.2' % i) for i in all_linking_reads_base_set])))

    # extract linking reads with seqtk
    seqtk_extract_cmd_rd1_linking_r1 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r1_fasta, linking_reads_r1_txt, linking_reads_r1_fasta)
    seqtk_extract_cmd_rd1_linking_r2 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r2_fasta, linking_reads_r2_txt, linking_reads_r2_fasta)
    os.system(seqtk_extract_cmd_rd1_linking_r1)
    os.system(seqtk_extract_cmd_rd1_linking_r2)
    if keep_tmp is False:
        os.remove(linking_reads_r1_txt)
        os.remove(linking_reads_r2_txt)

    # subset combined genome file
    linked_contigs_txt_handle = open(linked_contigs_txt, 'w')
    linked_contigs_txt_handle.write('\n'.join(ctgs_to_extract) + '\n')
    linked_contigs_txt_handle.close()
    subset_linked_ctgs_cmd = '%s subseq %s %s > %s' % (seqtk_exe, combined_input_gnms, linked_contigs_txt, linked_contigs_fasta)
    if remove_ending_16s_seqs is True:
        subset_linked_ctgs_cmd = '%s subseq %s %s > %s' % (seqtk_exe, combined_input_gnms_no_ending_16s, linked_contigs_txt, linked_contigs_fasta)
    os.system(subset_linked_ctgs_cmd)

    # read sequence of linked contigs into dict
    linked_ctg_seq_dict = {}
    for linked_ctg in SeqIO.parse(linked_contigs_fasta, 'fasta'):
        linked_ctg_seq_dict[linked_ctg.id] = str(linked_ctg.seq)

    # read sequence of linking reads into dict
    linking_read_seq_dict = {}
    for linking_r1 in SeqIO.parse(linking_reads_r1_fasta, 'fasta'):
        linking_read_seq_dict[linking_r1.id] = str(linking_r1.seq)
    for linking_r2 in SeqIO.parse(linking_reads_r2_fasta, 'fasta'):
        linking_read_seq_dict[linking_r2.id] = str(linking_r2.seq)

    ########## prepare seq with multi-processing ##########

    # read in linked maker to gnm
    linked_16s_to_gnm_set = set()
    for each_link in open(link_stats_combined_filtered_s1):
        if not each_link.startswith('MarkerGene,GenomicSeq,Number'):
            each_link_split = each_link.strip().split(',')
            id_16s = each_link_split[0][12:]
            id_gnm = each_link_split[1][12:]
            linked_16s_to_gnm_set.add('%s%s%s' % (id_16s, marker_to_ctg_gnm_Key_connector, id_gnm))

    argument_lol_for_linkage_vis_worker = []
    for marker_to_ctg in marker_to_ctg_LinkingRecord_dict:

        linking_reads = marker_to_ctg_LinkingRecord_dict[marker_to_ctg].linking_reads_base

        if len(linking_reads) >= 3:

            marker_id = marker_to_ctg_LinkingRecord_dict[marker_to_ctg].linked_seq_l
            ctg_id = marker_to_ctg_LinkingRecord_dict[marker_to_ctg].linked_seq_r
            gnm_id = ctg_id.split(gnm_to_ctg_connector)[0]
            marker_to_gnm_key = '%s%s%s' % (marker_id, marker_to_ctg_gnm_Key_connector, gnm_id)
            reads_file_base_tmp = marker_to_ctg.replace(marker_to_ctg_gnm_Key_connector, '___')
            reads_file_base = reads_file_base_tmp.replace(gnm_to_ctg_connector, '___')
            marker_seq = marker_seq_dict[marker_id]
            contig_seq = linked_ctg_seq_dict[ctg_id]

            linkage_passed_filter = False
            if marker_to_gnm_key in linked_16s_to_gnm_set:
                if marker_to_ctg in marker_to_ctg_linkage_num_dict_after_qc:
                    linkage_passed_filter = True

            if linkage_passed_filter is True:
                current_link_vis_folder_rd1 = '%s/%s___%s' % (link_vis_folder_rd1, marker_id, gnm_id)
            else:
                current_link_vis_folder_rd1 = '%s/%s___%s' % (link_vis_folder_rd1_for_debugging, marker_id, gnm_id)

            current_to_plot = False
            if linkage_passed_filter is True:
                current_to_plot = True
            else:
                if vis_all is True:
                    current_to_plot = True

            if current_to_plot is True:
                # create sub folders
                if os.path.isdir(current_link_vis_folder_rd1) is False:
                    os.mkdir(current_link_vis_folder_rd1)
                os.mkdir('%s/%s' % (current_link_vis_folder_rd1, reads_file_base))
                vis_reads_file_r1 = '%s/%s/%s_R1.fa' % (current_link_vis_folder_rd1, reads_file_base, reads_file_base)
                vis_reads_file_r2 = '%s/%s/%s_R2.fa' % (current_link_vis_folder_rd1, reads_file_base, reads_file_base)

                # get marker_pos_list and contig_pos_list and write out sequences of linking reads
                marker_pos_list = []
                contig_pos_list = []
                vis_reads_file_r1_handle = open(vis_reads_file_r1, 'w')
                vis_reads_file_r2_handle = open(vis_reads_file_r2, 'w')
                for each_linking_read in linking_reads:
                    linking_r1_id = '%s.1' % each_linking_read
                    linking_r1_seq = linking_read_seq_dict[linking_r1_id]
                    linking_r2_id = '%s.2' % each_linking_read
                    linking_r2_seq = linking_read_seq_dict[linking_r2_id]
                    vis_reads_file_r1_handle.write('>%s\n' % linking_r1_id)
                    vis_reads_file_r1_handle.write('%s\n' % linking_r1_seq)
                    vis_reads_file_r2_handle.write('>%s\n' % linking_r2_id)
                    vis_reads_file_r2_handle.write('%s\n' % linking_r2_seq)
                    # get matched position on makrer and contig
                    marker_pos_r1 = list(MappingRecord_dict[each_linking_read].r1_16s_ref_dict.get(marker_id, dict()).keys())
                    marker_pos_r2 = list(MappingRecord_dict[each_linking_read].r2_16s_ref_dict.get(marker_id, dict()).keys())
                    contig_pos_r1 = list(MappingRecord_dict[each_linking_read].r1_ctg_ref_dict.get(ctg_id, dict()).keys())
                    contig_pos_r2 = list(MappingRecord_dict[each_linking_read].r2_ctg_ref_dict.get(ctg_id, dict()).keys())
                    if len(marker_pos_r1) == 1:
                        marker_pos_list.append(marker_pos_r1[0])
                    if len(marker_pos_r2) == 1:
                        marker_pos_list.append(marker_pos_r2[0])
                    if len(contig_pos_r1) == 1:
                        contig_pos_list.append(contig_pos_r1[0])
                    if len(contig_pos_r2) == 1:
                        contig_pos_list.append(contig_pos_r2[0])
                vis_reads_file_r1_handle.close()
                vis_reads_file_r2_handle.close()

                argument_lol_for_linkage_vis_worker.append([reads_file_base, current_link_vis_folder_rd1,
                                                            marker_seq, contig_seq,
                                                            end_ctg_len_for_vis, gap_N_num, bowtie_parameter,
                                                            marker_pos_list, contig_pos_list,
                                                            pwd_bowtie2_build_exe, pwd_bowtie2_exe,
                                                            'Marker', 'MAG'])

    # visualize linkages
    report_and_log(('Round 1: visualizing %s rd1 linkages with %s threads' % (len(argument_lol_for_linkage_vis_worker), num_threads)), pwd_log_file, keep_quiet)
    vis_linkages_pool = mp.Pool(processes=num_threads)
    vis_linkages_pool.map(linkage_vis_worker, argument_lol_for_linkage_vis_worker)
    vis_linkages_pool.close()
    vis_linkages_pool.join()

    ####################################################################################################################
    ############################################### second round linking ###############################################
    ####################################################################################################################

    ################################################# define file name #################################################

    combined_1st_round_unlinked_mags                = '%s/round_1_unlinked_gnm.fa'                      % step_2_wd
    combined_1st_round_unlinked_mag_end_seq         = '%s/round_1_unlinked_gnm_end_%sbp.fa'             % (step_2_wd, end_seq_len)
    rd1_unlinked_mag_end_seq_no_ext                 = '%s/round_1_unlinked_gnm_end_%sbp'                % (step_2_wd, end_seq_len)
    rd1_unlinked_mag_end_seq_index_file_re          = '%s/round_1_unlinked_gnm_end_%sbp.*.bt2'          % (step_2_wd, end_seq_len)
    rd1_unlinked_mags_sam_bowtie_log                = '%s/round_1_unlinked_gnm.log'                     % step_2_wd
    rd1_unlinked_mags_sam_bowtie                    = '%s/round_1_unlinked_gnm.sam'                     % step_2_wd
    rd1_unlinked_mags_sam_bowtie_sorted             = '%s/round_1_unlinked_gnm_sorted.sam'              % step_2_wd
    rd1_unlinked_mags_sam_bowtie_sorted_log         = '%s/round_1_unlinked_gnm_sorted.log'              % step_2_wd
    rd1_unlinked_mags_sam_line_num                  = '%s/round_1_unlinked_gnm_line_num.txt'            % step_2_wd
    rd1_unlinked_mags_sam_split_folder              = '%s/round_1_unlinked_gnm_split'                   % step_2_wd
    rd1_unlinked_mags_sam_MappingRecord_folder      = '%s/round_1_unlinked_gnm_MappingRecord'           % step_2_wd
    free_living_16s_ref_file                        = '%s/round2_free_living_16s_refs.txt'              % step_2_wd
    free_living_ctg_ref_file                        = '%s/round2_free_living_ctg_refs.txt'              % step_2_wd
    free_living_ctg_ref_file_with_pos_cigar         = '%s/round2_free_living_ctg_refs_with_pos_cigar.txt' % step_2_wd
    free_living_16s_ref_file_no_linked              = '%s/round2_free_living_16s_refs_no_linked.txt'    % step_2_wd
    free_living_ctg_ref_file_no_linked              = '%s/round2_free_living_ctg_refs_no_linked.txt'    % step_2_wd
    free_living_all_fq_r1                           = '%s/round2_free_living_all_R1.fastq'              % step_2_wd
    free_living_all_fq_r2                           = '%s/round2_free_living_all_R2.fastq'              % step_2_wd
    free_living_all_fq                              = '%s/round2_free_living_all.fastq'                 % step_2_wd
    spades_wd                                       = '%s/mini_assembly_SPAdes_wd'                      % step_2_wd
    spades_log                                      = '%s/SPAdes_stdout.txt'                            % step_2_wd
    mira_manifest                                   = '%s/mira_manifest.txt'                            % step_2_wd
    mira_stdout                                     = '%s/mira_stdout.txt'                              % step_2_wd
    stats_GapFilling_ctg                            = '%s/stats_GapFilling_ctg.txt'                     % step_2_wd
    rd2_read_extracted_flanking_both_r12_seq        = '%s/rd2_read_to_extract_flanking_both_R12.fa'     % step_2_wd
    rd2_to_extract_flking_both_r1_id                = '%s/rd2_to_extract_flking_both_r1_id.txt'         % step_2_wd
    rd2_to_extract_flking_both_r2_id                = '%s/rd2_to_extract_flking_both_r2_id.txt'         % step_2_wd
    rd2_to_extract_flking_both_r1_fa                = '%s/rd2_to_extract_flking_both_r1.fa'             % step_2_wd
    rd2_to_extract_flking_both_r2_fa                = '%s/rd2_to_extract_flking_both_r2.fa'             % step_2_wd
    rd2_read_extracted_flanking_both_r12_up_seq     = '%s/rd2_read_to_extract_flanking_both_R12_up.fa'  % step_2_wd
    sam_file_mini_assembly                          = '%s/scaffolds_bowtie.sam'                         % step_2_wd
    sam_file_mini_assembly_log                      = '%s/scaffolds_bowtie.log'                         % step_2_wd
    sam_file_mini_assembly_reformatted_sorted       = '%s/scaffolds_bowtie_sorted.sam'                  % step_2_wd
    sam_file_mini_assembly_reformatted_sorted_log   = '%s/scaffolds_bowtie_sorted.log'                  % step_2_wd

    stats_mini_assembly_to_ctg                      = '%s/stats_mini_assembly_to_ctg.txt'               % step_2_wd
    stats_mini_assembly_to_ctg_sorted               = '%s/stats_mini_assembly_to_ctg_sorted.txt'        % step_2_wd
    stats_mini_assembly_to_ctg_filtered             = '%s/stats_mini_assembly_to_ctg_filtered.txt'      % step_2_wd

    ##########
    stats_mini_assembly_to_16s                      = '%s/stats_mini_assembly_to_16s.txt'                                   % step_2_wd
    stats_mini_assembly_to_16s_sorted               = '%s/stats_mini_assembly_to_16s_sorted.txt'                            % step_2_wd
    stats_mini_assembly_to_16s_filtered             = '%s/stats_mini_assembly_to_16s_filtered.txt'                          % step_2_wd
    stats_GapFilling_ctg                            = '%s/stats_GapFilling_ctg.txt'                                         % step_2_wd
    stats_GapFilling_file                           = '%s/stats_GapFilling_gnm.txt'                                         % step_2_wd
    stats_GapFilling_file_filtered                  = '%s/stats_GapFilling_gnm_filtered.txt'                                % step_2_wd
    ##########

    stats_GapFilling_file                           = '%s/stats_GapFilling_gnm.txt'                     % step_2_wd
    stats_GapFilling_file_filtered                  = '%s/stats_GapFilling_gnm_filtered.txt'            % step_2_wd

    linking_reads_tab_rd2                           = '%s/linking_reads_rd2.txt'                        % step_2_wd
    mafft_seq_folder_mini_to_16s                    = '%s/vis_folder_mini_to_16S'                       % step_2_wd
    mafft_seq_folder_mini_to_ctg                    = '%s/vis_folder_mini_to_ctg'                       % step_2_wd
    rd2_mini_to_16s_short_M_pct                     = '%s/rd2_mini_to_16s_short_M_pct.txt'              % step_2_wd
    link_vis_folder_rd2                             = '%s/%s_linkage_visualization_rd2'                 % (working_directory, output_prefix)

    rd2_with_both_mates = False

    #################### get the sequences of 1st round unlinked marker genes and genomic sequences ####################

    os.mkdir(step_2_wd)
    report_and_log(('Round 2: get unlinked marker genes and genomes'), pwd_log_file, keep_quiet)

    # get gnm_to_ignore, markers_to_ignore_best, markers_to_ignore_all
    linked_genomic_seq_set, markers_to_ignore_multi_best, linked_marker_gene_set = get_gnm_16s_to_ignore(
        link_stats_combined_sorted,
        pairwise_16s_iden_dict,
        min_iden_16s,
        min_link_num)

    # get linked marker genes and genomic sequences in step 1
    linked_16s_to_gnm_set = set()
    for each_link in open(link_stats_combined_filtered_s1):
        if not each_link.startswith('MarkerGene,GenomicSeq,Number'):
            each_link_split = each_link.strip().split(',')
            id_16s = each_link_split[0][12:]
            id_gnm = each_link_split[1][12:]
            linked_marker_gene_set.add(id_16s)
            linked_genomic_seq_set.add(id_gnm)
            linked_16s_to_gnm_set.add('%s%s%s' % (id_16s, marker_to_ctg_gnm_Key_connector, id_gnm))

    # get input genome name list
    renamed_gnm_re = '%s/*.%s' % (prefixed_mag_folder, mag_file_extension)
    renamed_gnm_list = [os.path.basename(file_name) for file_name in glob.glob(renamed_gnm_re)]
    renamed_gnm_list_no_ext = ['.'.join(i.split('.')[:-1]) for i in renamed_gnm_list]

    # keep only unlinked mags
    unlinked_mag_list_with_pwd = []
    for renamed_mag in renamed_gnm_list_no_ext:
        if renamed_mag not in linked_genomic_seq_set:
            pwd_renamed_mag = '%s/%s.%s' % (prefixed_mag_folder, renamed_mag, mag_file_extension)
            unlinked_mag_list_with_pwd.append(pwd_renamed_mag)

    # combine unlinked mags
    cat_cmd = 'cat %s > %s' % (' '.join(unlinked_mag_list_with_pwd), combined_1st_round_unlinked_mags)

    if remove_ending_16s_seqs is False:
        os.system(cat_cmd)
    else:
        combined_1st_round_unlinked_mags_handle = open(combined_1st_round_unlinked_mags, 'w')
        for each_seq in SeqIO.parse(combined_input_gnms_no_ending_16s, 'fasta'):
            each_seq_id = each_seq.id
            gnm_id = each_seq_id.split(gnm_to_ctg_connector)[0]
            if gnm_id not in linked_genomic_seq_set:
                combined_1st_round_unlinked_mags_handle.write('>%s\n' % each_seq.id)
                combined_1st_round_unlinked_mags_handle.write('%s\n' % str(each_seq.seq))
        combined_1st_round_unlinked_mags_handle.close()

    ######################################## extract reads matched to unlinked 16S #######################################

    # get all rd1 linking reads
    all_linking_reads_for_rd1_linkages = set()
    for each_link in marker_to_ctg_linkage_num_dict_after_qc:
        current_linking_reads = marker_to_ctg_LinkingRecord_dict[each_link].linking_reads_base
        marker_to_gnm_key = each_link.split(gnm_to_ctg_connector)[0]
        if marker_to_gnm_key in linked_16s_to_gnm_set:
            all_linking_reads_for_rd1_linkages.update(current_linking_reads)

    # get the id of reads to extract
    free_living_16s_ref_file_handle = open(free_living_16s_ref_file, 'w')
    rd2_read_to_extract_flanking_16s = set()
    rd2_read_to_extract_flanking_16s_r1_up = set()
    rd2_read_to_extract_flanking_16s_r2_up = set()
    for each_mp in MappingRecord_dict.copy():
        if each_mp in all_linking_reads_for_rd1_linkages:
            MappingRecord_dict.pop(each_mp)
        else:
            r1_16s_refs_no_ignored = MappingRecord_dict[each_mp].r1_16s_refs_no_ignored
            r2_16s_refs_no_ignored = MappingRecord_dict[each_mp].r2_16s_refs_no_ignored
            if len(MappingRecord_dict[each_mp].shared_16s_refs_no_ignored) > 0:
                MappingRecord_dict.pop(each_mp)
            elif (len(r1_16s_refs_no_ignored) > 0) or (len(r2_16s_refs_no_ignored) == 0):
                rd2_read_to_extract_flanking_16s.add(each_mp)
                rd2_read_to_extract_flanking_16s_r2_up.add('%s.2' % each_mp)
                if rd2_with_both_mates is True:
                    free_living_16s_ref_file_handle.write('%s\t%s\n' % (each_mp, ','.join(r1_16s_refs_no_ignored)))
                else:
                    free_living_16s_ref_file_handle.write('%s.2\t%s\n' % (each_mp, ','.join(r1_16s_refs_no_ignored)))

            elif (len(r1_16s_refs_no_ignored) == 0) or (len(r2_16s_refs_no_ignored) > 0):
                rd2_read_to_extract_flanking_16s.add(each_mp)
                rd2_read_to_extract_flanking_16s_r1_up.add('%s.1' % each_mp)
                if rd2_with_both_mates is True:
                    free_living_16s_ref_file_handle.write('%s\t%s\n' % (each_mp, ','.join(r2_16s_refs_no_ignored)))
                else:
                    free_living_16s_ref_file_handle.write('%s.1\t%s\n' % (each_mp, ','.join(r2_16s_refs_no_ignored)))
    free_living_16s_ref_file_handle.close()

    #################################### Mapping input reads to the ends of contigs from unlinked genomes ###################################

    report_and_log(('Round 2: Mapping input reads to the ends of contigs from unlinked genomes'), pwd_log_file, keep_quiet)

    ctg_ignore_region_dict_rd2 = get_unlinked_mag_end_seq(combined_1st_round_unlinked_mags, combined_1st_round_unlinked_mag_end_seq, end_seq_len, ctg_ignore_region_dict)

    # index reference
    bowtie_build_unlinked_ctg_cmd = '%s --quiet --threads %s -f %s %s' % (pwd_bowtie2_build_exe, num_threads, combined_1st_round_unlinked_mag_end_seq, rd1_unlinked_mag_end_seq_no_ext)
    os.system(bowtie_build_unlinked_ctg_cmd)

    # mapping with bowtie
    bowtie_cmd_unlinked_ctg = '%s -x %s -U %s,%s -S %s -p %s -f %s 2> %s' % (pwd_bowtie2_exe, rd1_unlinked_mag_end_seq_no_ext, reads_file_r1_fasta, reads_file_r2_fasta, rd1_unlinked_mags_sam_bowtie, num_threads, bowtie_parameter, rd1_unlinked_mags_sam_bowtie_log)
    os.system(bowtie_cmd_unlinked_ctg)
    os.remove(rd1_unlinked_mags_sam_bowtie_log)
    os.system('rm %s' % rd1_unlinked_mag_end_seq_index_file_re)

    # sort sam file first
    report_and_log(('Round 2: sorting mappping results'), pwd_log_file, keep_quiet)
    sort_by_read_cmd = 'samtools sort -n -O sam --threads %s -o %s %s 2> %s' % (num_threads, rd1_unlinked_mags_sam_bowtie_sorted, rd1_unlinked_mags_sam_bowtie, rd1_unlinked_mags_sam_bowtie_sorted_log)
    os.system(sort_by_read_cmd)
    os.remove(rd1_unlinked_mags_sam_bowtie)
    os.remove(rd1_unlinked_mags_sam_bowtie_sorted_log)

    ####################################### read in sam file with multiple cores #######################################

    round_2_ctg_end_seq_len_dict = {}
    for each_ctg_end_record in SeqIO.parse(combined_1st_round_unlinked_mag_end_seq, 'fasta'):
        round_2_ctg_end_seq_len_dict[each_ctg_end_record.id] = len(each_ctg_end_record.seq)

    # get the number of lines per file
    report_and_log(('Round 2: calculating the number of lines per subset'), pwd_log_file, keep_quiet)
    os.system('wc -l %s > %s' % (rd1_unlinked_mags_sam_bowtie_sorted, rd1_unlinked_mags_sam_line_num))
    rd1_unlinked_mag_sam_line_num = int(open(rd1_unlinked_mags_sam_line_num).readline().strip().split(' ')[0])
    os.remove(rd1_unlinked_mags_sam_line_num)
    line_num_per_file = int(round(rd1_unlinked_mag_sam_line_num/(num_threads*10))) + 10

    report_and_log(('Round 2: splitting sam file'), pwd_log_file, keep_quiet)
    os.mkdir(rd1_unlinked_mags_sam_split_folder)
    split_gnm_sam_cmd = 'split -l %s %s %s/splitted_sam_ ' % (line_num_per_file, rd1_unlinked_mags_sam_bowtie_sorted, rd1_unlinked_mags_sam_split_folder)
    os.system(split_gnm_sam_cmd)

    report_and_log(('Round 2: read in mappping results with %s threads' % num_threads), pwd_log_file, keep_quiet)
    os.mkdir(rd1_unlinked_mags_sam_MappingRecord_folder)

    # get splitted sam file list
    splitted_gnm_sam_file_list = [os.path.basename(file_name) for file_name in glob.glob('%s/splitted_sam_*' % rd1_unlinked_mags_sam_split_folder)]

    # prepare lol for mp worker
    list_for_parse_sam_gnm_worker = []
    splitted_sam_mp_file_set = set()
    splitted_sam_mp_file_set_with_pos_cigar = set()
    for splitted_gnm_sam_file in splitted_gnm_sam_file_list:
        pwd_splitted_gnm_sam_file                                    = '%s/%s'                                          % (rd1_unlinked_mags_sam_split_folder, splitted_gnm_sam_file)
        pwd_splitted_gnm_sam_free_living_ctg_ref_file                = '%s/%s_free_living_ctg_refs.txt'                 % (rd1_unlinked_mags_sam_MappingRecord_folder, splitted_gnm_sam_file)
        pwd_splitted_gnm_sam_free_living_ctg_ref_file_with_pos_cigar = '%s/%s_free_living_ctg_refs_with_pos_cigar.txt'  % (rd1_unlinked_mags_sam_MappingRecord_folder, splitted_gnm_sam_file)
        splitted_sam_mp_file_set.add(pwd_splitted_gnm_sam_free_living_ctg_ref_file)
        splitted_sam_mp_file_set_with_pos_cigar.add(pwd_splitted_gnm_sam_free_living_ctg_ref_file_with_pos_cigar)
        list_for_parse_sam_gnm_worker.append([pwd_splitted_gnm_sam_file,
                                              pwd_splitted_gnm_sam_free_living_ctg_ref_file,
                                              pwd_splitted_gnm_sam_free_living_ctg_ref_file_with_pos_cigar,
                                              min_M_len_ctg,
                                              mismatch_cutoff,
                                              round_2_ctg_end_seq_len_dict,
                                              rd2_with_both_mates,
                                              ctg_ignore_region_dict_rd2])

    pool_parse_sam_gnm = mp.Pool(processes=num_threads)
    pool_parse_sam_gnm.map(parse_rd2_sam_gnm_worker, list_for_parse_sam_gnm_worker)
    pool_parse_sam_gnm.close()
    pool_parse_sam_gnm.join()

    report_and_log(('Round 2: removing splitted subsets from disk'), pwd_log_file, keep_quiet)
    os.system('rm -r %s' % rd1_unlinked_mags_sam_split_folder)

    # combine free_living_ctg_ref_files
    os.system('cat %s > %s' % (' '.join(splitted_sam_mp_file_set), free_living_ctg_ref_file))
    os.system('cat %s > %s' % (' '.join(splitted_sam_mp_file_set_with_pos_cigar), free_living_ctg_ref_file_with_pos_cigar))

    ############################# put base of reads flanking 16S and unlinked ctg together #############################

    to_extract_read_base_rd2_flk_both = rd2_read_to_extract_flanking_16s
    for each_flk_read in open(free_living_ctg_ref_file_with_pos_cigar):
        flk_read_id = each_flk_read.strip().split('\t')[0]
        if rd2_with_both_mates is False:
            flk_read_id = '.'.join(flk_read_id.split('.')[:-1])
        to_extract_read_base_rd2_flk_both.add(flk_read_id)

    # write out id of linking reads for extraction
    with open(rd2_to_extract_flking_both_r1_id, 'w') as rd2_to_extract_flking_both_r1_id_handle:
        rd2_to_extract_flking_both_r1_id_handle.write('%s\n' % '\n'.join(sorted([('%s.1' % i) for i in to_extract_read_base_rd2_flk_both])))
    with open(rd2_to_extract_flking_both_r2_id, 'w') as rd2_to_extract_flking_both_r2_id_handle:
        rd2_to_extract_flking_both_r2_id_handle.write('%s\n' % '\n'.join(sorted([('%s.2' % i) for i in to_extract_read_base_rd2_flk_both])))

    # extract reads with seqtk
    seqtk_extract_cmd_rd2_flk_both_r1 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r1_fasta, rd2_to_extract_flking_both_r1_id, rd2_to_extract_flking_both_r1_fa)
    seqtk_extract_cmd_rd2_flk_both_r2 = '%s subseq %s %s > %s' % (seqtk_exe, reads_file_r2_fasta, rd2_to_extract_flking_both_r2_id, rd2_to_extract_flking_both_r2_fa)
    os.system(seqtk_extract_cmd_rd2_flk_both_r1)
    os.system(seqtk_extract_cmd_rd2_flk_both_r2)
    if keep_tmp is False:
        os.remove(rd2_to_extract_flking_both_r1_id)
        os.remove(rd2_to_extract_flking_both_r2_id)

    # read sequence of flanking reads into dict
    flk_both_read_seq_dict = {}
    for linking_r1 in SeqIO.parse(rd2_to_extract_flking_both_r1_fa, 'fasta'):
        flk_both_read_seq_dict[linking_r1.id] = str(linking_r1.seq)
    for linking_r2 in SeqIO.parse(rd2_to_extract_flking_both_r2_fa, 'fasta'):
        flk_both_read_seq_dict[linking_r2.id] = str(linking_r2.seq)

    ##################################################### get reads flanking 16s and ctg ####################################################

    # remove already linked ref from free_living_16s_ref_file
    free_living_16s_ref_file_no_linked_handle = open(free_living_16s_ref_file_no_linked, 'w')
    for each_16s_ref in open(free_living_16s_ref_file):
        each_16s_ref_split = each_16s_ref.strip().split('\t')
        read_id = each_16s_ref_split[0]
        linked_refs = each_16s_ref_split[1].split(',')
        linked_to_linked_ref = False
        for each_linked_ref in linked_refs:
            if each_linked_ref in linked_marker_gene_set:
                linked_to_linked_ref = True
        if linked_to_linked_ref is False:
           free_living_16s_ref_file_no_linked_handle.write(each_16s_ref)
    free_living_16s_ref_file_no_linked_handle.close()

    # remove already linked ref from free_living_ctg_ref_file
    free_living_ctg_ref_file_no_linked_handle = open(free_living_ctg_ref_file_no_linked, 'w')
    for each_ctg_ref in open(free_living_ctg_ref_file):
        each_ctg_ref_split = each_ctg_ref.strip().split('\t')
        read_id = each_ctg_ref_split[0]
        linked_ctgs = each_ctg_ref_split[1].split(',')
        linked_to_linked_gnm = False
        for each_linked_ctg in linked_ctgs:
            linked_gnm = each_linked_ctg.split(gnm_to_ctg_connector)[0]
            if linked_gnm in linked_genomic_seq_set:
                linked_to_linked_gnm = True
        if linked_to_linked_gnm is False:
           free_living_ctg_ref_file_no_linked_handle.write(each_ctg_ref)
    free_living_ctg_ref_file_no_linked_handle.close()

    flanking_16s_reads = set()
    flanking_16s_reads_base = set()
    for free_living_read_16s in open(free_living_16s_ref_file_no_linked):
        free_living_read_16s_split = free_living_read_16s.strip().split('\t')
        if len(free_living_read_16s_split) > 1:
            read_16s_id = free_living_read_16s_split[0]
            read_16s_id_base = '.'.join(read_16s_id.split('.')[:-1])
            flanking_16s_reads.add(read_16s_id)
            flanking_16s_reads_base.add(read_16s_id_base)

    flanking_ctg_reads = set()
    flanking_ctg_reads_base = set()
    for each_read_to_ctg_ref in open(free_living_ctg_ref_file_no_linked):
        read_id = each_read_to_ctg_ref.strip().split('\t')[0]
        read_id_base = '.'.join(read_id.split('.')[:-1])
        flanking_ctg_reads.add(read_id)
        flanking_ctg_reads_base.add(read_id_base)

    ##################################################### combine reads flanking 16s and contig ####################################################

    rd2_read_to_extract_flanking_both = set.union(flanking_16s_reads, flanking_ctg_reads)
    rd2_read_to_extract_flanking_both_base = set.union(flanking_16s_reads_base, flanking_ctg_reads_base)

    # this step produce the input file for spades
    rd2_read_extracted_flanking_both_r12_up_seq_handle = open(rd2_read_extracted_flanking_both_r12_up_seq, 'w')
    for each_flk_read in flk_both_read_seq_dict:
        if each_flk_read in rd2_read_to_extract_flanking_both:
            rd2_read_extracted_flanking_both_r12_up_seq_handle.write('>%s\n' % each_flk_read)
            rd2_read_extracted_flanking_both_r12_up_seq_handle.write('%s\n' % flk_both_read_seq_dict[each_flk_read])
    rd2_read_extracted_flanking_both_r12_up_seq_handle.close()

    # file produced here will be mapped to mini-assemblies
    rd2_read_extracted_flanking_both_r12_seq_handle = open(rd2_read_extracted_flanking_both_r12_seq, 'w')
    for flanking_both_base in rd2_read_to_extract_flanking_both_base:
        flanking_both_r1 = '%s.1' % flanking_both_base
        flanking_both_r2 = '%s.2' % flanking_both_base
        flanking_both_r1_seq = flk_both_read_seq_dict[flanking_both_r1]
        flanking_both_r2_seq = flk_both_read_seq_dict[flanking_both_r2]
        rd2_read_extracted_flanking_both_r12_seq_handle.write('>%s\n' % flanking_both_r1)
        rd2_read_extracted_flanking_both_r12_seq_handle.write('%s\n'  % flanking_both_r1_seq)
        rd2_read_extracted_flanking_both_r12_seq_handle.write('>%s\n' % flanking_both_r2)
        rd2_read_extracted_flanking_both_r12_seq_handle.write('%s\n'  % flanking_both_r2_seq)
    rd2_read_extracted_flanking_both_r12_seq_handle.close()

    ######################################### second round linking by assembly #########################################

    # assemble
    if round_2_mira is True:

        free_living_all_id_r1 = set()
        free_living_all_id_r2 = set()
        for each_read in open(rd2_read_extracted_flanking_both_r12_up_seq):
            if each_read.startswith('>'):
                read_id = each_read.strip()[1:].split(' ')[0]
                if read_id[-1] == '1':
                    free_living_all_id_r1.add(read_id)
                if read_id[-1] == '2':
                    free_living_all_id_r2.add(read_id)

        argument_list_r1 = [reads_file_r1, 'fastq', free_living_all_id_r1, free_living_all_fq_r1]
        argument_list_r2 = [reads_file_r2, 'fastq', free_living_all_id_r2, free_living_all_fq_r2]

        # extract reads with multiprocessing
        pool = mp.Pool(processes=2)
        pool.map(extract_reads_worker, [argument_list_r1, argument_list_r2])
        pool.close()
        pool.join()

        os.system('cat %s %s > %s' % (free_living_all_fq_r1, free_living_all_fq_r2, free_living_all_fq))
        report_and_log(('Round 2: running Mira on extracted reads'), pwd_log_file, keep_quiet)
        run_mira5(output_prefix, mira_tmp_dir, step_2_wd, mira_manifest, free_living_all_fq, mira_stdout, force_overwrite)
        mini_assemblies = '%s/%s_mira_est_no_chimera_assembly/%s_mira_est_no_chimera_d_results/%s_mira_est_no_chimera_out.unpadded.fasta' % (step_2_wd, output_prefix, output_prefix, output_prefix)
    else:
        report_and_log(('Round 2: running SPAdes on extracted reads'), pwd_log_file, keep_quiet)
        spades_cmd = '%s --only-assembler -s %s -o %s -t %s -k 75,99,123 > %s' % (pwd_spades_exe, rd2_read_extracted_flanking_both_r12_up_seq, spades_wd, num_threads, spades_log)

        report_and_log((spades_cmd), pwd_log_file, True)
        os.system(spades_cmd)
        mini_assemblies = '%s/scaffolds.fasta' % spades_wd

    ##################################################### mapping reads to mini_assemblies ####################################################

    if os.path.isfile(mini_assemblies) is False:
        report_and_log(('Mini-assembly not found! will report 1st round linkages only!'), pwd_log_file, keep_quiet)
    else:
        # index miniassembly
        mini_assemblies_no_ext = '.'.join(mini_assemblies.split('.')[:-1])
        bowtie_build_mini_assemblies_cmd = '%s --quiet --threads %s -f %s %s' % (pwd_bowtie2_build_exe, num_threads, mini_assemblies, mini_assemblies_no_ext)
        os.system(bowtie_build_mini_assemblies_cmd)

        # mapping with bowtie
        bowtie_cmd_miniassembly = '%s -x %s -U %s -S %s -p %s -f %s 2> %s'    % (pwd_bowtie2_exe, mini_assemblies_no_ext, rd2_read_extracted_flanking_both_r12_seq, sam_file_mini_assembly, num_threads, bowtie_parameter, sam_file_mini_assembly_log)
        report_and_log((bowtie_cmd_miniassembly), pwd_log_file, True)
        os.system(bowtie_cmd_miniassembly)
        if keep_tmp is False:
            os.remove(sam_file_mini_assembly_log)

        # sort sam files
        sort_by_read_cmd_mini_assembly = 'samtools sort -n -O sam --threads %s -o %s %s 2> %s' % (num_threads, sam_file_mini_assembly_reformatted_sorted, sam_file_mini_assembly, sam_file_mini_assembly_reformatted_sorted_log)
        report_and_log((sort_by_read_cmd_mini_assembly), pwd_log_file, True)
        os.system(sort_by_read_cmd_mini_assembly)
        if keep_tmp is False:
            os.remove(sam_file_mini_assembly_reformatted_sorted_log)

        ##################################################### read in mini-assembly sam file ####################################################

        report_and_log(('Round 2: read in mini-assembly sam file'), pwd_log_file, keep_quiet)

        mini_assembly_len_dict = {}
        MappingRecord_dict_mini = {}
        current_read_base = ''
        current_read_base_r1_mini_ref_dict = dict()
        current_read_base_r2_mini_ref_dict = dict()
        with open(sam_file_mini_assembly_reformatted_sorted) as sam_file_mini_assembly_reformatted_sorted_opened:
            for each_line in sam_file_mini_assembly_reformatted_sorted_opened:
                each_line_split = each_line.strip().split('\t')
                if each_line.startswith('@'):
                    mini_assembly_id = ''
                    mini_assembly_len = 0
                    for each_element in each_line_split:
                        if each_element.startswith('SN:'):
                            mini_assembly_id = each_element[3:]
                        if each_element.startswith('LN:'):
                            mini_assembly_len = int(each_element[3:])
                    mini_assembly_len_dict[mini_assembly_id] = mini_assembly_len
                else:
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
                                current_read_base_r1_mini_ref_dict[ref_id] = {ref_pos: cigar}
                            if read_strand == '2':
                                current_read_base_r2_mini_ref_dict[ref_id] = {ref_pos: cigar}

                    elif read_id_base == current_read_base:

                        if cigar != '*':
                            if read_strand == '1':
                                if ref_id not in current_read_base_r1_mini_ref_dict:
                                    current_read_base_r1_mini_ref_dict[ref_id] = {ref_pos: cigar}
                                else:
                                    current_read_base_r1_mini_ref_dict[ref_id][ref_pos] = cigar
                            if read_strand == '2':
                                if ref_id not in current_read_base_r2_mini_ref_dict:
                                    current_read_base_r2_mini_ref_dict[ref_id] = {ref_pos: cigar}
                                else:
                                    current_read_base_r2_mini_ref_dict[ref_id][ref_pos] = cigar
                    else:
                        ################################### analysis previous read refs ####################################

                        mini_refs_to_ignore = set()

                        ########## get lowest mismatch for r1/r2 mini refs ##########

                        # get r1_ref_cigar_set
                        r1_ref_cigar_set = set()
                        for each_pos_dict in current_read_base_r1_mini_ref_dict.values():
                            each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                            r1_ref_cigar_set.update(each_pos_dict_values)

                        # get r2_ref_cigar_set
                        r2_ref_cigar_set = set()
                        for each_pos_dict in current_read_base_r2_mini_ref_dict.values():
                            each_pos_dict_values = {each_pos_dict[i] for i in each_pos_dict}
                            r2_ref_cigar_set.update(each_pos_dict_values)

                        r1_ref_min_mismatch = get_min_mismatch_from_cigar_list(r1_ref_cigar_set, min_M_len_mini)
                        r2_ref_min_mismatch = get_min_mismatch_from_cigar_list(r2_ref_cigar_set, min_M_len_mini)

                        ########## filter mini refs for r1 and r2 ##########

                        r1_mini_refs_passed_qc, r1_mini_refs_passed_qc_with_pos = get_qualified_ref_dict(current_read_base_r1_mini_ref_dict, mini_assembly_len_dict, r1_ref_min_mismatch, min_M_len_mini, mismatch_cutoff, mini_refs_to_ignore)
                        r2_mini_refs_passed_qc, r2_mini_refs_passed_qc_with_pos = get_qualified_ref_dict(current_read_base_r2_mini_ref_dict, mini_assembly_len_dict, r2_ref_min_mismatch, min_M_len_mini, mismatch_cutoff, mini_refs_to_ignore)

                        ####################################################################################################

                        r1_mini_refs_no_ignored = {key: value for key, value in r1_mini_refs_passed_qc.items() if key not in mini_refs_to_ignore}
                        r2_mini_refs_no_ignored = {key: value for key, value in r2_mini_refs_passed_qc.items() if key not in mini_refs_to_ignore}

                        # no mate has no_ignored alignments
                        if (len(r1_mini_refs_no_ignored) == 0) and (len(r2_mini_refs_no_ignored) == 0):
                            pass

                        # only r1 has no_ignored alignments
                        elif (len(r1_mini_refs_no_ignored) > 0) and (len(r2_mini_refs_no_ignored) == 0):
                            if current_read_base not in MappingRecord_dict_mini:
                                MappingRecord_dict_mini[current_read_base] = MappingRecord()
                            MappingRecord_dict_mini[current_read_base].r1_mini_ref_dict = current_read_base_r1_mini_ref_dict
                            MappingRecord_dict_mini[current_read_base].r1_mini_refs_no_ignored = r1_mini_refs_no_ignored

                        # only r2 has no_ignored alignments
                        elif (len(r1_mini_refs_no_ignored) == 0) and (len(r2_mini_refs_no_ignored) > 0):
                            if current_read_base not in MappingRecord_dict_mini:
                                MappingRecord_dict_mini[current_read_base] = MappingRecord()
                            MappingRecord_dict_mini[current_read_base].r2_mini_ref_dict = current_read_base_r2_mini_ref_dict
                            MappingRecord_dict_mini[current_read_base].r2_mini_refs_no_ignored = r2_mini_refs_no_ignored

                        # both r1 and r2 have no_ignored alignments
                        else:
                            shared_mini_refs_no_ignored = {key: [r1_mini_refs_no_ignored[key][0], r2_mini_refs_no_ignored[key][0]] for key in set(r1_mini_refs_no_ignored).intersection(set(r2_mini_refs_no_ignored))}
                            if len(shared_mini_refs_no_ignored) > 0:
                                if current_read_base not in MappingRecord_dict_mini:
                                    MappingRecord_dict_mini[current_read_base] = MappingRecord()
                                MappingRecord_dict_mini[current_read_base].r1_mini_ref_dict = current_read_base_r1_mini_ref_dict
                                MappingRecord_dict_mini[current_read_base].r2_mini_ref_dict = current_read_base_r2_mini_ref_dict
                                MappingRecord_dict_mini[current_read_base].shared_mini_refs_no_ignored = shared_mini_refs_no_ignored

                        ########################################### reset values ###########################################

                        current_read_base = read_id_base
                        current_read_base_r1_mini_ref_dict = dict()
                        current_read_base_r2_mini_ref_dict = dict()

                        if cigar != '*':
                            if read_strand == '1':
                                current_read_base_r1_mini_ref_dict[ref_id] = {ref_pos: cigar}
                            if read_strand == '2':
                                current_read_base_r2_mini_ref_dict[ref_id] = {ref_pos: cigar}

        #################### read sequences into dict ####################

        # read sequence of mini_assembly into dict
        mini_assembly_seq_dict = {}
        for linked_ctg in SeqIO.parse(mini_assemblies, 'fasta'):
            mini_assembly_seq_dict[linked_ctg.id] = str(linked_ctg.seq)

        # read sequence of unlinked mag end seq into dict
        unlinked_mag_end_seq_dict = {}
        for linked_ctg in SeqIO.parse(combined_1st_round_unlinked_mag_end_seq, 'fasta'):
            unlinked_mag_end_seq_dict[linked_ctg.id] = str(linked_ctg.seq)

        ############################################ link mini-assembly to MAGs ############################################

        # read ctg side aln_pos and cigar into dict
        mini_ctg_side_pos_dict = dict()
        mini_ctg_side_cigar_dict = dict()
        for each_read_to_ctg_ref in open(free_living_ctg_ref_file_with_pos_cigar):
            each_read_to_ctg_ref_split = each_read_to_ctg_ref.strip().split('\t')
            read_id = each_read_to_ctg_ref_split[0]
            ctg_refs = each_read_to_ctg_ref_split[1].split(',')
            for each_ctg_ref in ctg_refs:
                each_ctg_ref_split = each_ctg_ref.split('__pc__')
                ctg_ref_id = each_ctg_ref_split[0]
                ctg_ref_pos = int(each_ctg_ref_split[1])
                ctg_ref_cigar = each_ctg_ref_split[2]
                read_to_ctg_ref_key = '%s__ctg__%s' % (read_id, ctg_ref_id)
                mini_ctg_side_pos_dict[read_to_ctg_ref_key] = ctg_ref_pos
                mini_ctg_side_cigar_dict[read_to_ctg_ref_key] = ctg_ref_cigar

        mini_to_mag_LinkingRecord_dict = {}
        for free_living_read_ctg in open(free_living_ctg_ref_file_no_linked):
            free_living_read_ctg_split = free_living_read_ctg.strip().split('\t')
            read_id = free_living_read_ctg_split[0]
            read_id_base = '.'.join(read_id.split('.')[:-1])
            read_strand = read_id.split('.')[-1]
            read_ctg_refs = free_living_read_ctg_split[1].split(',')
            read_mini_mp = MappingRecord_dict_mini.get(read_id_base, None)
            if read_mini_mp is not None:

                read_mini_refs = set()
                for mini_ref in read_mini_mp.shared_mini_refs_no_ignored:
                    read_mini_refs.add(mini_ref)
                if read_strand == '1':
                    for mini_ref in read_mini_mp.r1_mini_refs_no_ignored:
                        read_mini_refs.add(mini_ref)
                if read_strand == '2':
                    for mini_ref in read_mini_mp.r2_mini_refs_no_ignored:
                        read_mini_refs.add(mini_ref)

                for each_mini_ref in read_mini_refs:
                    for each_ctg_ref in read_ctg_refs:
                        mini_to_ctg_key_with_l_r = '%s%s%s' % (
                        each_mini_ref, mini_assembly_to_16s_ctg_connector, each_ctg_ref)
                        mini_ref_len = mini_assembly_len_dict[each_mini_ref]
                        ctg_ref_len = len(unlinked_mag_end_seq_dict[each_ctg_ref])
                        if mini_to_ctg_key_with_l_r not in mini_to_mag_LinkingRecord_dict:
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r] = LinkingRecord()
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linked_seq_l = each_mini_ref
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linked_seq_r = each_ctg_ref
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linked_seq_len_l = mini_ref_len
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linked_seq_len_r = ctg_ref_len

                        # get mini side cigar here
                        current_mini_mp = MappingRecord_dict_mini[read_id_base]
                        current_linking_cigar = ''
                        current_linking_pos = ''
                        if read_strand == '1':
                            current_linking_cigar = list(current_mini_mp.r1_mini_ref_dict[each_mini_ref].values())[0]
                            current_linking_pos = list(current_mini_mp.r1_mini_ref_dict[each_mini_ref].keys())[0]
                        if read_strand == '2':
                            current_linking_cigar = list(current_mini_mp.r2_mini_ref_dict[each_mini_ref].values())[0]
                            current_linking_pos = list(current_mini_mp.r2_mini_ref_dict[each_mini_ref].keys())[0]

                        # get min dist to mini end
                        current_linking_cigar_aln_len = get_cigar_aln_len(cigar_splitter(current_linking_cigar))
                        current_linking_cigar_dist_to_left = current_linking_pos - 1
                        current_linking_cigar_dist_to_right = mini_ref_len - current_linking_pos - current_linking_cigar_aln_len + 1
                        min_dist_to_mini_end = min(current_linking_cigar_dist_to_left, current_linking_cigar_dist_to_right)

                        mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linking_reads_base.append(read_id_base)
                        mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linking_cigar_l.append(current_linking_cigar)
                        mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linking_pos_l.append(current_linking_pos)
                        mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].min_dist_to_end_l.append(min_dist_to_mini_end)

                        # get ctg side cigar here
                        read_to_ctg_ref_key = '%s__ctg__%s' % (read_id, each_ctg_ref)
                        current_linking_cigar_ctg_side = mini_ctg_side_cigar_dict.get(read_to_ctg_ref_key, None)
                        current_linking_pos_ctg_side = mini_ctg_side_pos_dict.get(read_to_ctg_ref_key, None)
                        if current_linking_cigar_ctg_side is not None:
                            # get min dist to ctg end
                            current_linking_cigar_ctg_side_aln_len = get_cigar_aln_len(
                                cigar_splitter(current_linking_cigar_ctg_side))
                            current_linking_cigar_ctg_side_dist_to_left = current_linking_pos_ctg_side - 1
                            current_linking_cigar_ctg_side_dist_to_right = ctg_ref_len - current_linking_pos_ctg_side - current_linking_cigar_ctg_side_aln_len + 1
                            min_dist_to_mini_end_ctg_side = min(current_linking_cigar_ctg_side_dist_to_left, current_linking_cigar_ctg_side_dist_to_right)

                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linking_cigar_r.append(current_linking_cigar_ctg_side)
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].linking_pos_r.append(current_linking_pos_ctg_side)
                            mini_to_mag_LinkingRecord_dict[mini_to_ctg_key_with_l_r].min_dist_to_end_r.append(min_dist_to_mini_end_ctg_side)

        all_linking_reads_base_set_rd2_mini_to_ctg = set()
        stats_mini_assembly_to_ctg_handle = open(stats_mini_assembly_to_ctg, 'w')
        stats_mini_assembly_to_ctg_handle.write('MiniAssembly,GenomicSeq,Number\n')
        mini_assembly_to_ctg_dict_with_l_r_read_base_min3 = {}
        for each_link in mini_to_mag_LinkingRecord_dict.copy():
            current_linkage_linking_read_base = mini_to_mag_LinkingRecord_dict[each_link].linking_reads_base
            if len(current_linkage_linking_read_base) < 3:
                mini_to_mag_LinkingRecord_dict.pop(each_link)
            else:
                id_mini_assembly = mini_to_mag_LinkingRecord_dict[each_link].linked_seq_l
                id_ctg = mini_to_mag_LinkingRecord_dict[each_link].linked_seq_r
                current_linkage_cigar_mini_side = mini_to_mag_LinkingRecord_dict[each_link].linking_cigar_l
                current_linkage_cigar_ctg_side = mini_to_mag_LinkingRecord_dict[each_link].linking_cigar_r

                # get pct of short aligned cigar
                short_cigar_pct_mini = get_short_cigar_pct(current_linkage_cigar_mini_side, short_M_len)
                short_cigar_pct_ctg = get_short_cigar_pct(current_linkage_cigar_ctg_side, short_M_len)

                # check num/pct of reads linked to mini end
                min_dist_list_to_mini_end = mini_to_mag_LinkingRecord_dict[each_link].min_dist_to_end_l
                linked_to_mini_end_cigar_num = 0
                for each_min_dist in min_dist_list_to_mini_end:
                    if each_min_dist <= 10:
                        linked_to_mini_end_cigar_num += 1
                linked_to_mini_end_cigar_pct = linked_to_mini_end_cigar_num * 100 / len(min_dist_list_to_mini_end)

                # check num/pct of reads linked to ctg end
                min_dist_list_to_ctg_end = mini_to_mag_LinkingRecord_dict[each_link].min_dist_to_end_r
                linked_to_ctg_end_cigar_num = 0
                for each_min_dist in min_dist_list_to_ctg_end:
                    if each_min_dist <= 10:
                        linked_to_ctg_end_cigar_num += 1
                linked_to_ctg_end_cigar_pct = linked_to_ctg_end_cigar_num * 100 / len(min_dist_list_to_ctg_end)

                linked_to_mini_end = False
                if (linked_to_mini_end_cigar_num > 0) and (linked_to_mini_end_cigar_pct >= 5):
                    linked_to_mini_end = True

                linked_to_ctg_end = False
                if (linked_to_ctg_end_cigar_num >= linked_to_ctg_end_cigar_num_cutoff) and (linked_to_ctg_end_cigar_pct >= linked_to_ctg_end_cigar_pct_cutoff):
                    linked_to_ctg_end = True

                if (short_cigar_pct_mini < 85) and (short_cigar_pct_ctg < 85) and (linked_to_ctg_end is True) and (linked_to_mini_end is True):
                    mini_assembly_to_ctg_dict_with_l_r_read_base_min3[each_link] = current_linkage_linking_read_base
                    all_linking_reads_base_set_rd2_mini_to_ctg.update(current_linkage_linking_read_base)
                    stats_mini_assembly_to_ctg_handle.write('%s,%s,%s\n' % (id_mini_assembly, id_ctg, len(current_linkage_linking_read_base)))
        stats_mini_assembly_to_ctg_handle.close()

        # sort and filter
        sort_csv_by_col(stats_mini_assembly_to_ctg, stats_mini_assembly_to_ctg_sorted, 'Number')
        mini_assembly_to_ctg_dict, mini_assembly_to_mag_dict, mag_ctg_set_with_linked_mini_assembly = filter_linkages_iteratively_mini_assembly_to_ctg(stats_mini_assembly_to_ctg_sorted, 3,
                                                                                     stats_mini_assembly_to_ctg_filtered)

        os.remove(stats_mini_assembly_to_ctg)

        ################################## link 16S to mini-assemblies #################################

        mini_to_16s_LinkingRecord_dict = {}  # left: mini, right: 16S
        for free_living_read_16s in open(free_living_16s_ref_file_no_linked):
            free_living_read_16s_split = free_living_read_16s.strip().split('\t')
            if len(free_living_read_16s_split) > 1:
                read_id = free_living_read_16s_split[0]
                read_id_base = '.'.join(read_id.split('.')[:-1])
                read_strand = read_id.split('.')[-1]
                read_16s_refs = free_living_read_16s_split[1].split(',')
                read_mini_mp = MappingRecord_dict_mini.get(read_id_base, None)
                read_16s_mp = MappingRecord_dict[read_id_base]
                if read_mini_mp is not None:

                    read_mini_refs = set()
                    for mini_ref in read_mini_mp.shared_mini_refs_no_ignored:
                        read_mini_refs.add(mini_ref)
                    if read_strand == '1':
                        for mini_ref in read_mini_mp.r1_mini_refs_no_ignored:
                            read_mini_refs.add(mini_ref)
                    if read_strand == '2':
                        for mini_ref in read_mini_mp.r2_mini_refs_no_ignored:
                            read_mini_refs.add(mini_ref)

                    for each_mini_ref in read_mini_refs:
                        for each_16s_ref in read_16s_refs:
                            mini_assembly_to_16s_key = '%s%s%s' % (
                            each_mini_ref, mini_assembly_to_16s_ctg_connector, each_16s_ref)
                            mini_ref_len = mini_assembly_len_dict[each_mini_ref]
                            s16_ref_len = len(marker_seq_dict[each_16s_ref])

                            if mini_assembly_to_16s_key not in mini_to_16s_LinkingRecord_dict:
                                mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key] = LinkingRecord()
                                mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linked_seq_l = each_mini_ref
                                mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linked_seq_r = each_16s_ref
                                mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linked_seq_len_l = mini_ref_len
                                mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linked_seq_len_r = s16_ref_len

                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linking_reads_base.append(read_id_base)

                            # get mini side cigar here
                            current_linking_cigar_mini_side = ''
                            current_linking_pos_mini_side = ''
                            if read_strand == '1':
                                current_linking_cigar_mini_side = \
                                list(read_mini_mp.r1_mini_ref_dict[each_mini_ref].values())[0]
                                current_linking_pos_mini_side = \
                                list(read_mini_mp.r1_mini_ref_dict[each_mini_ref].keys())[0]
                            if read_strand == '2':
                                current_linking_cigar_mini_side = \
                                list(read_mini_mp.r2_mini_ref_dict[each_mini_ref].values())[0]
                                current_linking_pos_mini_side = \
                                list(read_mini_mp.r2_mini_ref_dict[each_mini_ref].keys())[0]
                            min_dist_to_mini_end = get_min_dist_to_ref_end(current_linking_cigar_mini_side, current_linking_pos_mini_side, mini_ref_len)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linking_cigar_l.append(current_linking_cigar_mini_side)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linking_pos_l.append(current_linking_pos_mini_side)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].min_dist_to_end_l.append(min_dist_to_mini_end)

                            # get 16s side cigar here
                            current_linking_cigar_16s_side = ''
                            current_linking_pos_16s_side = ''
                            if read_strand == '1':
                                current_linking_cigar_16s_side = \
                                list(read_16s_mp.r2_16s_ref_dict[each_16s_ref].values())[0]
                                current_linking_pos_16s_side = list(read_16s_mp.r2_16s_ref_dict[each_16s_ref].keys())[0]
                            if read_strand == '2':
                                current_linking_cigar_16s_side = \
                                list(read_16s_mp.r1_16s_ref_dict[each_16s_ref].values())[0]
                                current_linking_pos_16s_side = list(read_16s_mp.r1_16s_ref_dict[each_16s_ref].keys())[0]
                            min_dist_to_16s_end = get_min_dist_to_ref_end(current_linking_cigar_16s_side,
                                                                          current_linking_pos_16s_side, s16_ref_len)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linking_cigar_r.append(
                                current_linking_cigar_16s_side)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].linking_pos_r.append(
                                current_linking_pos_16s_side)
                            mini_to_16s_LinkingRecord_dict[mini_assembly_to_16s_key].min_dist_to_end_r.append(
                                min_dist_to_16s_end)

        # filter with link num
        all_linking_reads_base_set_rd2_mini_to_16s = set()
        stats_mini_assembly_to_16s_handle = open(stats_mini_assembly_to_16s, 'w')
        stats_mini_assembly_to_16s_handle.write('Marker,MiniAssembly,Number\n')
        rd2_mini_to_16s_short_M_pct_handle= open(rd2_mini_to_16s_short_M_pct, 'w')
        rd2_mini_to_16s_short_M_pct_handle.write('linkage\tMini-assembly\tMarker\n')
        mini_to_16s_linkage_num_dict_after_qc = {}
        for each_link in mini_to_16s_LinkingRecord_dict.copy():
            linking_reads = mini_to_16s_LinkingRecord_dict[each_link].linking_reads_base
            if len(linking_reads) < ctg_level_min_link:
                mini_to_16s_LinkingRecord_dict.pop(each_link)
            else:
                id_mini = mini_to_16s_LinkingRecord_dict[each_link].linked_seq_l
                id_16s  = mini_to_16s_LinkingRecord_dict[each_link].linked_seq_r
                current_linkage_cigar_mini_side = mini_to_16s_LinkingRecord_dict[each_link].linking_cigar_l
                current_linkage_cigar_16s_side  = mini_to_16s_LinkingRecord_dict[each_link].linking_cigar_r

                # get pct of short aligned cigar
                short_cigar_pct_mini = get_short_cigar_pct(current_linkage_cigar_mini_side, short_M_len)
                short_cigar_pct_16s = get_short_cigar_pct(current_linkage_cigar_16s_side, short_M_len)
                short_cigar_pct_mini = float("{0:.2f}".format(short_cigar_pct_mini))
                short_cigar_pct_16s = float("{0:.2f}".format(short_cigar_pct_16s))

                # check num/pct of reads linked to mini end
                min_dist_list_to_mini_end = mini_to_16s_LinkingRecord_dict[each_link].min_dist_to_end_l
                linked_to_mini_end_cigar_num = 0
                for each_min_dist in min_dist_list_to_mini_end:
                    if each_min_dist <= 10:
                        linked_to_mini_end_cigar_num += 1
                linked_to_mini_end_cigar_pct = linked_to_mini_end_cigar_num * 100 / len(min_dist_list_to_mini_end)

                # check num/pct of reads linked to 16s end
                min_dist_list_to_16s_end = mini_to_16s_LinkingRecord_dict[each_link].min_dist_to_end_r
                linked_to_16s_end_cigar_num = 0
                for each_min_dist in min_dist_list_to_16s_end:
                    if each_min_dist <= 10:
                        linked_to_16s_end_cigar_num += 1
                linked_to_16s_end_cigar_pct = linked_to_16s_end_cigar_num * 100 / len(min_dist_list_to_16s_end)

                linked_to_mini_end = False
                if (linked_to_mini_end_cigar_num > 0) and (linked_to_mini_end_cigar_pct >= 5):
                    linked_to_mini_end = True

                linked_to_16s_end = False
                if (linked_to_16s_end_cigar_num > 0) and (linked_to_16s_end_cigar_pct >= 5):
                    linked_to_16s_end = True

                if (short_cigar_pct_mini < 85) and (short_cigar_pct_16s < 85) and (linked_to_mini_end is True) and (linked_to_16s_end is True):
                    mini_to_16s_linkage_num_dict_after_qc[each_link] = len(linking_reads)
                    all_linking_reads_base_set_rd2_mini_to_16s.update(linking_reads)
                    stats_mini_assembly_to_16s_handle.write('%s,%s,%s\n' % (id_16s, id_mini, len(linking_reads)))
                    rd2_mini_to_16s_short_M_pct_handle.write('%s\t%s(%s/%s)\t%s(%s/%s)\n' % (each_link, short_cigar_pct_mini, short_cigar_num_mini, len(current_linkage_cigar_mini_side), short_cigar_pct_16s, short_cigar_num_16s, len(current_linkage_cigar_16s_side)))
        stats_mini_assembly_to_16s_handle.close()
        rd2_mini_to_16s_short_M_pct_handle.close()


        # write out linkages at contig level
        ctgs_to_extract_mini = set()
        marker_to_gnm_link_num_dict_rd2 = {}
        linking_reads_tab_rd2_handle = open(linking_reads_tab_rd2, 'w')
        for each_mini_assembly_to_16s in mini_to_16s_linkage_num_dict_after_qc:
            linking_reads = mini_to_16s_LinkingRecord_dict[each_mini_assembly_to_16s].linking_reads_base
            id_mini = each_mini_assembly_to_16s.split(mini_assembly_to_16s_ctg_connector)[0]
            id_16s = each_mini_assembly_to_16s.split(mini_assembly_to_16s_ctg_connector)[1]
            mini_assembly_mag = mini_assembly_to_mag_dict.get(id_mini, None)
            if mini_assembly_mag != None:
                linking_reads_tab_rd2_handle.write('%s\t%s%s%s\t%s\n' % (id_16s, mini_assembly_mag, gnm_to_ctg_connector, id_mini, ','.join(linking_reads)))
                ctgs_to_extract_mini.add(id_mini)
                marker_to_gnm_key_rd2 = '%s%s%s' % (id_16s, marker_to_ctg_gnm_Key_connector, mini_assembly_mag)
                if marker_to_gnm_key_rd2 not in marker_to_gnm_link_num_dict_rd2:
                    marker_to_gnm_link_num_dict_rd2[marker_to_gnm_key_rd2] = len(linking_reads)
                else:
                    marker_to_gnm_link_num_dict_rd2[marker_to_gnm_key_rd2] += len(linking_reads)
        linking_reads_tab_rd2_handle.close()

        # write out linkages at genome level
        stats_GapFilling_gnm_handle = open(stats_GapFilling_file, 'w')
        stats_GapFilling_gnm_handle.write('MarkerGene,GenomicSeq,Number\n')
        for each_linkage in marker_to_gnm_link_num_dict_rd2:
            stats_GapFilling_gnm_handle.write('MarkerGene__%s,GenomicSeq__%s,%s\n' % (
                each_linkage.split(marker_to_ctg_gnm_Key_connector)[0],
                each_linkage.split(marker_to_ctg_gnm_Key_connector)[1],
                marker_to_gnm_link_num_dict_rd2[each_linkage]))
        stats_GapFilling_gnm_handle.close()

        # filter_linkages_iteratively
        filter_linkages_iteratively(stats_GapFilling_file, 'Number', pairwise_16s_iden_dict,
                                    min_iden_16s, min_link_num, min_link_num,
                                    within_gnm_linkage_num_diff, stats_GapFilling_file_filtered)

        os.remove(stats_GapFilling_file)

        ################################################# rd2 visualizing ##################################################

        if os.path.isdir(mafft_seq_folder_mini_to_ctg) is True:
            os.system('rm -r %s' % mafft_seq_folder_mini_to_ctg)
        os.mkdir(mafft_seq_folder_mini_to_ctg)

        if os.path.isdir(mafft_seq_folder_mini_to_16s) is True:
            os.system('rm -r %s' % mafft_seq_folder_mini_to_16s)
        os.mkdir(mafft_seq_folder_mini_to_16s)

        #################### prepare seqs for vis with multi-processing (mini_to_ctg) ####################

        argument_lol_for_linkage_vis_worker_mini_to_ctg = []
        for mini_to_ctg in mini_assembly_to_ctg_dict_with_l_r_read_base_min3:
            reads_file_base_tmp = mini_to_ctg.replace(mini_assembly_to_16s_ctg_connector, '___')
            reads_file_base     = reads_file_base_tmp.replace(gnm_to_ctg_connector, '___')
            mini_id             = mini_to_ctg.split(mini_assembly_to_16s_ctg_connector)[0]
            ctg_id              = mini_to_ctg.split(mini_assembly_to_16s_ctg_connector)[1]
            mini_linked_ctg = mini_assembly_to_ctg_dict.get(mini_id, None)

            if mini_linked_ctg == ctg_id:
                mini_seq = mini_assembly_seq_dict[mini_id]
                ctg_seq  = unlinked_mag_end_seq_dict[ctg_id]
                linking_reads       = mini_assembly_to_ctg_dict_with_l_r_read_base_min3[mini_to_ctg]

                # create sub folders
                os.mkdir('%s/%s' % (mafft_seq_folder_mini_to_ctg, reads_file_base))
                vis_reads_file_r1 = '%s/%s/%s_R1.fa' % (mafft_seq_folder_mini_to_ctg, reads_file_base, reads_file_base)
                vis_reads_file_r2 = '%s/%s/%s_R2.fa' % (mafft_seq_folder_mini_to_ctg, reads_file_base, reads_file_base)

                # get marker_pos_list and contig_pos_list and write out sequences of linking reads
                marker_pos_list = []
                contig_pos_list = []
                vis_reads_file_r1_handle = open(vis_reads_file_r1, 'w')
                vis_reads_file_r2_handle = open(vis_reads_file_r2, 'w')
                for each_linking_read in linking_reads:
                    linking_r1_id = '%s.1' % each_linking_read
                    linking_r1_seq = flk_both_read_seq_dict[linking_r1_id]
                    linking_r2_id = '%s.2' % each_linking_read
                    linking_r2_seq = flk_both_read_seq_dict[linking_r2_id]
                    vis_reads_file_r1_handle.write('>%s\n' % linking_r1_id)
                    vis_reads_file_r1_handle.write('%s\n'  % linking_r1_seq)
                    vis_reads_file_r2_handle.write('>%s\n' % linking_r2_id)
                    vis_reads_file_r2_handle.write('%s\n'  % linking_r2_seq)
                vis_reads_file_r1_handle.close()
                vis_reads_file_r2_handle.close()
                fake_pos_list = [1, 1, 1, 1, 1, 1, 1, 1, 1]
                argument_lol_for_linkage_vis_worker_mini_to_ctg.append([reads_file_base, mafft_seq_folder_mini_to_ctg,
                                                            mini_seq, ctg_seq,
                                                            end_ctg_len_for_vis, gap_N_num, bowtie_parameter,
                                                            fake_pos_list, fake_pos_list,
                                                            pwd_bowtie2_build_exe, pwd_bowtie2_exe,
                                                            'Mini', 'MAG'])

        # visualize linkages
        report_and_log(('Round 2: visualizing %s mini_to_ctg linkages with %s threads' % (len(argument_lol_for_linkage_vis_worker_mini_to_ctg), num_threads)), pwd_log_file, keep_quiet)

        vis_linkages_pool = mp.Pool(processes=num_threads)
        vis_linkages_pool.map(linkage_vis_worker, argument_lol_for_linkage_vis_worker_mini_to_ctg)
        vis_linkages_pool.close()
        vis_linkages_pool.join()


        #################### prepare seqs for vis with multi-processing (mini_to_16s) ####################

        argument_lol_for_linkage_vis_worker = []
        for marker_to_mini in mini_assembly_to_16s_dict_read_base_min3:

            reads_file_base_tmp = marker_to_mini.replace(mini_assembly_to_16s_ctg_connector, '___')
            reads_file_base = reads_file_base_tmp.replace(gnm_to_ctg_connector, '___')
            linking_reads = mini_assembly_to_16s_dict_read_base_min3[marker_to_mini]
            marker_id  = marker_to_mini.split(mini_assembly_to_16s_ctg_connector)[1]
            mini_id    = marker_to_mini.split(mini_assembly_to_16s_ctg_connector)[0]
            marker_seq = marker_seq_dict[marker_id]
            contig_seq = mini_assembly_seq_dict[mini_id]
            mini_assembly_mag = mini_assembly_to_mag_dict.get(mini_id, None)

            if mini_assembly_mag != None:

                # create sub folders
                os.mkdir('%s/%s' % (mafft_seq_folder_mini_to_16s, reads_file_base))
                vis_reads_file_r1 = '%s/%s/%s_R1.fa' % (mafft_seq_folder_mini_to_16s, reads_file_base, reads_file_base)
                vis_reads_file_r2 = '%s/%s/%s_R2.fa' % (mafft_seq_folder_mini_to_16s, reads_file_base, reads_file_base)

                # get marker_pos_list and contig_pos_list and write out sequences of linking reads
                marker_pos_list = []
                contig_pos_list = []
                vis_reads_file_r1_handle = open(vis_reads_file_r1, 'w')
                vis_reads_file_r2_handle = open(vis_reads_file_r2, 'w')
                for each_linking_read in linking_reads:
                    linking_r1_id = '%s.1' % each_linking_read
                    linking_r1_seq = flk_both_read_seq_dict[linking_r1_id]
                    linking_r2_id = '%s.2' % each_linking_read
                    linking_r2_seq = flk_both_read_seq_dict[linking_r2_id]
                    vis_reads_file_r1_handle.write('>%s\n' % linking_r1_id)
                    vis_reads_file_r1_handle.write('%s\n' % linking_r1_seq)
                    vis_reads_file_r2_handle.write('>%s\n' % linking_r2_id)
                    vis_reads_file_r2_handle.write('%s\n' % linking_r2_seq)

                    # get matched position on makrer and contig
                    marker_pos_r1 = list(MappingRecord_dict[each_linking_read].r1_16s_ref_dict.get(marker_id, dict()).keys())
                    marker_pos_r2 = list(MappingRecord_dict[each_linking_read].r2_16s_ref_dict.get(marker_id, dict()).keys())
                    mini_pos_r1   = list(MappingRecord_dict_mini[each_linking_read].r1_mini_ref_dict.get(mini_id, dict()).keys())
                    mini_pos_r2   = list(MappingRecord_dict_mini[each_linking_read].r2_mini_ref_dict.get(mini_id, dict()).keys())

                    if len(marker_pos_r1) == 1:
                        marker_pos_list.append(marker_pos_r1[0])
                    if len(marker_pos_r2) == 1:
                        marker_pos_list.append(marker_pos_r2[0])
                    if len(mini_pos_r1) == 1:
                        contig_pos_list.append(mini_pos_r1[0])
                    if len(mini_pos_r2) == 1:
                        contig_pos_list.append(mini_pos_r2[0])
                vis_reads_file_r1_handle.close()
                vis_reads_file_r2_handle.close()

                argument_lol_for_linkage_vis_worker.append([reads_file_base, mafft_seq_folder_mini_to_16s,
                                                            marker_seq, contig_seq,
                                                            end_ctg_len_for_vis, gap_N_num, bowtie_parameter,
                                                            marker_pos_list, contig_pos_list,
                                                            pwd_bowtie2_build_exe, pwd_bowtie2_exe,
                                                            'Marker', 'Mini'])

        # visualize linkages
        report_and_log(('Round 2: visualizing %s mini_to_16s linkages with %s threads' % (len(argument_lol_for_linkage_vis_worker), num_threads)), pwd_log_file, keep_quiet)

        vis_linkages_pool = mp.Pool(processes=num_threads)
        vis_linkages_pool.map(linkage_vis_worker, argument_lol_for_linkage_vis_worker)
        vis_linkages_pool.close()
        vis_linkages_pool.join()

        ##################################################### organize vis plot ####################################################

        if os.path.isdir(link_vis_folder_rd2) is True:
            os.system('rm -r %s' % link_vis_folder_rd2)
        os.mkdir(link_vis_folder_rd2)

        mag_to_mini_assembly_dict = {}
        for each_mini_assembly in mini_assembly_to_mag_dict:
            assigned_mag = mini_assembly_to_mag_dict[each_mini_assembly]
            if assigned_mag not in mag_to_mini_assembly_dict:
                mag_to_mini_assembly_dict[assigned_mag] = {each_mini_assembly}
            else:
                mag_to_mini_assembly_dict[assigned_mag].add(each_mini_assembly)

        # read in final linkages
        matam_16s_to_mag_rd2 = {}
        for each_rd2_link in open(stats_GapFilling_file_filtered):
            if ',Number\n' not in each_rd2_link:
                each_rd2_link_split = each_rd2_link.strip().split(',')
                id_16s = each_rd2_link_split[0][12:]
                id_mag = each_rd2_link_split[1][12:]
                matam_16s_to_mag_rd2[id_16s] = id_mag

        for each_linked_16s in matam_16s_to_mag_rd2:
            linked_mag = matam_16s_to_mag_rd2[each_linked_16s]
            linked_mini_set = mag_to_mini_assembly_dict[linked_mag]
            matam_to_mag_folder = '%s/%s___%s' % (link_vis_folder_rd2, each_linked_16s, linked_mag)
            os.mkdir(matam_to_mag_folder)

            for each_linked_mini in linked_mini_set:
                vis_mini_to_16s_folder_name = '%s/%s___%s' % (mafft_seq_folder_mini_to_16s, each_linked_mini, each_linked_16s)
                if os.path.isdir(vis_mini_to_16s_folder_name) is True:
                    os.system('cp -r %s %s/' % (vis_mini_to_16s_folder_name, matam_to_mag_folder))

                    vis_mini_to_ctg_folder_re = '%s/%s___%s___*' % (mafft_seq_folder_mini_to_ctg, each_linked_mini, linked_mag)
                    vis_mini_to_ctg_folder_list = glob.glob(vis_mini_to_ctg_folder_re)
                    for each_vis_mini_to_ctg_folder in vis_mini_to_ctg_folder_list:
                        if os.path.isdir(each_vis_mini_to_ctg_folder) is True:
                            os.system('cp -r %s %s/' % (each_vis_mini_to_ctg_folder, matam_to_mag_folder))


    ####################################################################################################################
    ####################################### combine linkages from step 1 and 2  ########################################
    ####################################################################################################################

    if os.path.isfile(mini_assemblies) is True:
        report_and_log(('Combining linkages from step 1 and 2'), pwd_log_file, keep_quiet)

    combined_linkage_file_by_gnm = '%s/%s_linkages_by_genome.txt'    % (working_directory, output_prefix)
    combined_linkage_file_by_ctg = '%s/%s_linkages_by_contig.txt'    % (working_directory, output_prefix)
    linkage_plot_rd1_html        = '%s/%s_linkages_plot_round1.html' % (working_directory, output_prefix)
    linkage_plot_rd2_html        = '%s/%s_linkages_plot_round2.html' % (working_directory, output_prefix)

    combined_linkage_file_handle     = open(combined_linkage_file_by_gnm, 'w')
    combined_linkage_file_handle.write('MarkerGene\tGenomicSeq\tLinkage\tRound\n')
    for step_1_link in open(link_stats_combined_filtered_s1):
        if not step_1_link.startswith('MarkerGene,GenomicSeq,Number'):
            marker_id = step_1_link.strip().split(',')[0][12:]
            genome_id = step_1_link.strip().split(',')[1][12:]
            link_num  = step_1_link.strip().split(',')[2]
            combined_linkage_file_handle.write('%s\t%s\t%s\tRd1\n' % (marker_id, genome_id, link_num))
    if os.path.isfile(mini_assemblies) is True:
        for step_2_link in open(stats_GapFilling_file_filtered):
            if not step_2_link.startswith('MarkerGene,GenomicSeq,Number'):
                marker_id = step_2_link.strip().split(',')[0][12:]
                genome_id = step_2_link.strip().split(',')[1][12:]
                link_num  = step_2_link.strip().split(',')[2]
                combined_linkage_file_handle.write('%s\t%s\t%s\tRd2\n' % (marker_id, genome_id, link_num))
    combined_linkage_file_handle.close()

    #################### summarize linkages at contig level ####################

    free_living_16s_to_ctg_linkage_dict_to_use = {}
    for each_ctg_level_link in open(stats_GapFilling_ctg):
        if ',Number\n' not in each_ctg_level_link:
            each_ctg_level_link_split = each_ctg_level_link.split(',')
            marker_id = each_ctg_level_link_split[0]
            ctg_id = each_ctg_level_link_split[1]
            link_num = int(each_ctg_level_link_split[2])
            current_key = '%s%s%s' % (marker_id, marker_to_ctg_gnm_Key_connector, ctg_id)
            free_living_16s_to_ctg_linkage_dict_to_use[current_key] = link_num

    combined_linkage_file_ctg_level_handle = open(combined_linkage_file_by_ctg, 'w')
    combined_linkage_file_ctg_level_handle.write('Marker___Genome(total)\tContig\tRd1\tRd2\n')
    for each_linkage in open(combined_linkage_file_by_gnm):
        if not each_linkage.startswith('MarkerGene\tGenomicSeq\tLinkage\tRound'):
            each_linkage_split = each_linkage.strip().split('\t')
            marker_id = each_linkage_split[0]
            mag_id = each_linkage_split[1]
            total_link_num = int(each_linkage_split[2])
            link_step = each_linkage_split[3]

            if link_step == 'Rd1':
                for each_link in marker_to_ctg_linkage_num_dict_after_qc:
                    link_16s_id = each_link.split(marker_to_ctg_gnm_Key_connector)[0]
                    link_ctg_id = each_link.split(marker_to_ctg_gnm_Key_connector)[1]
                    link_ctg_id_no_gnm = link_ctg_id.split(gnm_to_ctg_connector)[1]
                    link_gnm_id = link_ctg_id.split(gnm_to_ctg_connector)[0]
                    if (link_16s_id == marker_id) and (link_gnm_id == mag_id):
                        current_link_num = len(marker_to_ctg_LinkingRecord_dict[each_link].linking_reads_base)
                        combined_linkage_file_ctg_level_handle.write('%s___%s(%s)\t%s\t%s\t0\n' % (link_16s_id, link_gnm_id, total_link_num, link_ctg_id_no_gnm, current_link_num))

            if link_step == 'Rd2':
                for each_rd2_linkage in free_living_16s_to_ctg_linkage_dict_to_use:
                    rd2_link_16s_id = each_rd2_linkage.split(marker_to_ctg_gnm_Key_connector)[0]
                    rd2_link_ctg_id = each_rd2_linkage.split(marker_to_ctg_gnm_Key_connector)[1]
                    rd2_link_ctg_id_no_gnm = rd2_link_ctg_id.split(gnm_to_ctg_connector)[1]
                    rd2_link_gnm_id = rd2_link_ctg_id.split(gnm_to_ctg_connector)[0]
                    if (rd2_link_16s_id == marker_id) and (rd2_link_gnm_id == mag_id):
                        current_ctg_link_num = free_living_16s_to_ctg_linkage_dict_to_use[each_rd2_linkage]
                        combined_linkage_file_ctg_level_handle.write('%s___%s(%s)\t%s\t0\t%s\n' % (rd2_link_16s_id, rd2_link_gnm_id, total_link_num, rd2_link_ctg_id_no_gnm, current_ctg_link_num))

    combined_linkage_file_ctg_level_handle.close()

    # plot
    report_and_log(('Visualising linkages'), pwd_log_file, keep_quiet)
    sankey_linkages(combined_linkage_file_by_ctg, linkage_plot_rd1_html, linkage_plot_rd2_html)

    ######################################## report assessment under test mode #########################################

    if test_mode is True:

        report_and_log(('Test mode on, assessing linkages'), pwd_log_file, keep_quiet)

        marker_id_set = set()
        for marker_seq_record in SeqIO.parse(marker_gene_seqs, 'fasta'):
            marker_id_set.add(marker_seq_record.id)

        # get recovery and accuracy
        recovery_combined, accuracy_combined, recovered_combined = get_accuracy(combined_linkage_file_by_gnm, len(marker_id_set))

        # get unrecovered markers
        unrecovered_markers_paired = get_unrecovered_markers(marker_id_set, recovered_combined)
        unrecovered_markers_paired_str = 'Unrecovered(%s):%s' % (len(unrecovered_markers_paired), ','.join(sorted([i for i in unrecovered_markers_paired])))

        # assessment by genome
        assign_rate, assign_accuracy, right_assign, wrong_assign = get_accuracy_by_genome(combined_linkage_file_by_gnm, mag_folder, mag_file_extension)
        unrecovered_paired_report_str = 'Unrecovered(%s):%s' % (len(wrong_assign), ','.join(sorted([i for i in wrong_assign])))

        # report
        report_and_log(('Prefix\tBy\tRecovery\tAccuracy\tUnrecovered'), pwd_log_file, keep_quiet)
        report_and_log(('%s\tMarker\t%s\t%s\t%s' % (output_prefix, recovery_combined, accuracy_combined, unrecovered_markers_paired_str)), pwd_log_file, keep_quiet)
        report_and_log(('%s\tGenome\t%s\t%s\t%s' % (output_prefix, assign_rate, assign_accuracy, unrecovered_paired_report_str)), pwd_log_file, keep_quiet)

    ################################################### remove tmp files ###################################################

    # Final report
    report_and_log(('Done!'), pwd_log_file, keep_quiet)

######################################################### main #########################################################

if __name__ == '__main__':

    default_prefix = 'MyRun_%s' % datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    link_16s_parser = argparse.ArgumentParser(description='Linking MAGs with 16S rRNA marker genes', usage=link_Marker_MAG_usage)

    # specify argument group
    link_16s_parser_input_files = link_16s_parser.add_argument_group("input files")
    link_16s_parser_16s         = link_16s_parser.add_argument_group("16S rRNA gene related parameters")
    link_16s_parser_both_rds    = link_16s_parser.add_argument_group("parameters for linking (round 1 and 2)")
    link_16s_parser_rd1         = link_16s_parser.add_argument_group("parameters for linking (round 1)")
    link_16s_parser_rd2         = link_16s_parser.add_argument_group("parameters for linking (round 2)")
    link_16s_parser_preset      = link_16s_parser.add_argument_group("preset parameters, decide automatically if not specified")
    link_16s_parser_dependency  = link_16s_parser.add_argument_group("provide if dependencies are not in your system path")
    link_16s_parser_others      = link_16s_parser.add_argument_group("program settings")
    link_16s_parser_debug       = link_16s_parser.add_argument_group("for debugging, do NOT specify")

    # input files
    link_16s_parser_input_files.add_argument('-p',          required=False, metavar='',             default=default_prefix, help='output prefix, (default: MyRun_SystemTime)')
    link_16s_parser_input_files.add_argument('-r1',         required=True,  metavar='',                                     help='paired reads r1 (fasta format)')
    link_16s_parser_input_files.add_argument('-r2',         required=True,  metavar='',                                     help='paired reads r2 (fasta format)')
    link_16s_parser_input_files.add_argument('-marker',     required=True,  metavar='',                                     help='marker gene sequences')
    link_16s_parser_input_files.add_argument('-mag',        required=True,  metavar='',                                     help='metagenome-assembled-genome (MAG) folder')
    link_16s_parser_input_files.add_argument('-x',          required=False, metavar='',             default='fasta',        help='MAG file extension, (default: %(default)s)')

    # 16S rRNA gene related parameters
    link_16s_parser_16s.add_argument('-min_len_16s',        required=False, metavar='', type=int,   default=1200,           help='minimum length of 16S (in bp) for linking, (default: %(default)s)')
    link_16s_parser_16s.add_argument('-no_polish',          required=False, action="store_true",                            help='skip polishing 16S before linking')
    link_16s_parser_16s.add_argument('-min_iden_16s',       required=False, metavar='', type=float, default=98.5,           help='minimum similarity for 16S sequences to be assigned to the same genome, (default: %(default)s)')
    link_16s_parser_16s.add_argument('-min_cov_16s',        required=False, metavar='', type=float, default=50,             help='coverage cutoff for calculating pairwise 16S similarity, (default: %(default)s)')
    link_16s_parser_16s.add_argument('-min_aln_16s',        required=False, metavar='', type=int,   default=500,            help='alignment length cutoff for calculating pairwise 16S similarity, (default: %(default)s)')
    link_16s_parser_16s.add_argument('-keep_ctg_end_16s',   required=False, action="store_true",                            help='do not mask 16S sequences at the end of MAG contig')

    # parameters for both rounds linking
    link_16s_parser_both_rds.add_argument('-mismatch',      required=False, metavar='', type=float, default=2,              help='maximum mismatch percentage, (default: %(default)s)')
    link_16s_parser_both_rds.add_argument('-min_M_len_16s', required=False, metavar='', type=int,   default=45,             help='minimum length aligned to 16S, (default: %(default)s)')
    link_16s_parser_both_rds.add_argument('-min_M_len_ctg', required=False, metavar='', type=int,   default=45,             help='minimum length aligned to ctg, (default: %(default)s)')
    link_16s_parser_both_rds.add_argument('-min_M_pct',     required=False, metavar='', type=float, default=35,             help='minimum aligned percentage, (default: %(default)s)')
    link_16s_parser_both_rds.add_argument('-min_link',      required=False, metavar='', type=int,   default=8,              help='minimum number of linkages to report, (default: %(default)s)')
    link_16s_parser_both_rds.add_argument('-link_num_diff', required=False, metavar='', type=float, default=80,             help='within_gnm_linkage_num_diff, (default: %(default)s)')

    # parameters for 2nd round linking
    link_16s_parser_rd2.add_argument('-mira',               required=False, action="store_true",                            help='run Mira, instead of Spades')
    link_16s_parser_rd2.add_argument('-mira_tmp',           required=False,                         default=None,           help='tmp dir for mira')

    # program settings
    link_16s_parser_others.add_argument('-t',               required=False, metavar='', type=int,   default=1,              help='number of threads, (default: %(default)s)')
    link_16s_parser_others.add_argument('-tmp',             required=False, action="store_true",                            help='keep temporary files')
    link_16s_parser_others.add_argument('-quiet',           required=False, action="store_true",                            help='not report progress')
    link_16s_parser_others.add_argument('-force',           required=False, action="store_true",                            help='force overwrite existing results')

    # for debugging
    link_16s_parser_debug.add_argument('-test_mode',        required=False, action="store_true",                            help='only for debugging, do not provide')
    link_16s_parser_debug.add_argument('-rd2_only',         required=False, action="store_true",                            help='run round 2 only')
    link_16s_parser_debug.add_argument('-sorted_sam16s',    required=False,                         default=None,           help='mapping of input reads to 16S')
    link_16s_parser_debug.add_argument('-vis_all',          required=False, action="store_true",                            help='vis all linkages, including those filtered out ')

    args = vars(link_16s_parser.parse_args())
    link_16s(args)


'''
2. with no_ambiguous option, 16S rRNA gene sequences need to be dereplicated. (include dereplication step? with identity and coverage cutoffs?)
3. (doesn't work)!!! to ignore list even without assignment (to handle situations like DM_m4, meanwhile capicable of not assign very diverde 16S (e.g. <98% identity) to the same genome)
4. for clipping mapped reads, the mismatch of clipping part must be 0
5. insert size is important
6. check duplicate sequences in input files
7. a genome depth of 0 will triggle error !!!!!!
8. no header in mag depth and 16s depth files !!!!!!
9. remove short mini-assemblies?
10. ignore reads with two continuous mismatch  56=2x55=
11. no mismatch in clipping reads?
12. put vis at the final step
'''
