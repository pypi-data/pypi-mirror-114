from Bio import SeqIO


reads_0              = '/Users/songweizhi/Desktop/test_spades/rd2_read_to_extract_flanking_both_R12_up_failed.fa'
reads_1              = '/Users/songweizhi/Desktop/test_spades/rd2_read_to_extract_flanking_both_R12_up_succeed.fa'
shared_reads_from_r0 = '/Users/songweizhi/Desktop/test_spades/shared_reads_from_r0.fa'
shared_reads_from_r1 = '/Users/songweizhi/Desktop/test_spades/shared_reads_from_r1.fa'
uniq_reads_from_r0   = '/Users/songweizhi/Desktop/test_spades/uniq_reads_from_r0.fa'
uniq_reads_from_r1   = '/Users/songweizhi/Desktop/test_spades/uniq_reads_from_r1.fa'


reads_0_id_set = set()
for each in SeqIO.parse(reads_0, 'fasta'):
    reads_0_id_set.add(each.id)
reads_1_id_set = set()
for each in SeqIO.parse(reads_1, 'fasta'):
    reads_1_id_set.add(each.id)


shared_reads = set(reads_0_id_set).intersection(reads_1_id_set)


shared_reads_from_r0_handle = open(shared_reads_from_r0, 'w')
uniq_reads_from_r0_handle = open(uniq_reads_from_r0, 'w')
for each in SeqIO.parse(reads_0, 'fasta'):
    if each.id in shared_reads:
        shared_reads_from_r0_handle.write('>%s\n' % each.id)
        shared_reads_from_r0_handle.write('%s\n' % str(each.seq))
    else:
        uniq_reads_from_r0_handle.write('>%s\n' % each.id)
        uniq_reads_from_r0_handle.write('%s\n' % str(each.seq))
shared_reads_from_r0_handle.close()
uniq_reads_from_r0_handle.close()


shared_reads_from_r1_handle = open(shared_reads_from_r1, 'w')
uniq_reads_from_r1_handle = open(uniq_reads_from_r1, 'w')
for each in SeqIO.parse(reads_1, 'fasta'):
    if each.id in shared_reads:
        shared_reads_from_r1_handle.write('>%s\n' % each.id)
        shared_reads_from_r1_handle.write('%s\n' % str(each.seq))
    else:
        uniq_reads_from_r1_handle.write('>%s\n' % each.id)
        uniq_reads_from_r1_handle.write('%s\n' % str(each.seq))
shared_reads_from_r1_handle.close()
uniq_reads_from_r1_handle.close()


print(len(reads_0_id_set))
print(len(reads_1_id_set))
print(len(shared_reads))
print(len(reads_0_id_set) - len(shared_reads))
print(len(reads_1_id_set) - len(shared_reads))

