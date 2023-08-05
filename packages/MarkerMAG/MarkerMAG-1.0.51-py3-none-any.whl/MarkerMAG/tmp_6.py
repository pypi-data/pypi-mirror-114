
def check_cigar_quality_consider_ref_min_mismatch(cigar_str, ref_min_mismatch, mismatch_cutoff, min_M_len, ref_pos, marker_len):

    cigar_splitted = cigar_splitter(cigar_str)
    qualified_cigar = False

    # check both end clip
    both_end_clp = check_both_ends_clipping(cigar_splitted)
    if both_end_clp is False:
        # check mismatch
        aln_len, aln_pct, clp_len, clp_pct, mismatch_pct = get_cigar_stats(cigar_splitted)

        if ref_min_mismatch != 'NA':
            if (mismatch_pct <= ref_min_mismatch) and (mismatch_pct <= mismatch_cutoff):
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

