
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


def continuous_mismatch_cigar(cigar_splitted):

    print(cigar_splitted)

    if cigar_splitted[0][-1] in ['S', 's']:
        cigar_splitted = cigar_splitted[1:]

    if cigar_splitted[-1][-1] in ['S', 's']:
        cigar_splitted = cigar_splitted[:-1]

    print(cigar_splitted)


    mismatch_len_list = []
    mismatch_len = 0
    for each_part in cigar_splitted:
        each_part_len = int(each_part[:-1])
        each_part_cate = each_part[-1]
        if (each_part_cate in ['=', 'S']) and (each_part_len > 10):
            if mismatch_len > 0:
                mismatch_len_list.append(mismatch_len)
            mismatch_len = 0
        else:
            if each_part_cate not in ['=', 'S']:
                mismatch_len += each_part_len

    print(mismatch_len_list)

    continuous_mismatch = False
    if max(mismatch_len_list) > 1:
        continuous_mismatch = True

    print(max(mismatch_len_list))
    return continuous_mismatch


'''
22=2X65=
22=1X1D65=
22=1X1I65=
22=2D65=
'''

cigar = '6S8=1D2=1X65S'

print(continuous_mismatch_cigar(cigar_splitter(cigar)))

