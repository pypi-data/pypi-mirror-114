
## MarkerMAG (linking MAGs with 16S rRNA marker genes)

![logo](doc/images/MarkerMAG_logo.jpg) 

[![pypi licence](https://img.shields.io/pypi/l/MarkerMAG.svg)](https://opensource.org/licenses/gpl-3.0.html)
[![pypi version](https://img.shields.io/pypi/v/MarkerMAG.svg)](https://pypi.python.org/pypi/MarkerMAG) 


Publication
---
+ In preparation
+ Dr. Weizhi Song (songwz03[at]gmail.com), Prof. Torsten Thomas (t.thomas[at]unsw.edu.au)
+ Center for Marine Science & Innovation, University of New South Wales, Sydney, Australia


How it works
---
to be added


MarkerMAG modules:
---

1. Main module

    + `link`: linking MAGs with 16S rRNA marker genes
    
1. Supplementary modules

    + `rename_reads`: rename paired reads ([manual](doc/README_rename_reads.md))
    + `matam_16s`: assemble 16S rRNA genes with Matam, including subsample and dereplication ([manual](doc/README_matam_16s.md))
    + `uclust_16s`: cluster marker genes with Usearch ([manual](doc/README_uclust_16s.md))
    + `barrnap_16s`: identify 16S gene sequences with Barrnap ([manual](doc/README_barrnap_16s.md))
    + `subsample_reads`: subsample reads with Usearch ([manual](doc/README_subsample_reads.md))


Dependencies
---
 
+ Dependencies for the `link` module:
  + [BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download)
  + [Barrnap](https://github.com/tseemann/barrnap)
  + [seqtk](https://github.com/lh3/seqtk)
  + [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
  + [Samtools](http://www.htslib.org)
  + [metaSPAdes](https://cab.spbu.ru/software/meta-spades/)

+ Dependencies for supplementary modules can be found from their own manual page.
 

How to install:
---

+ BioSAK has been tested on Linux/Mac, but NOT on Windows.
+ MarkerMAG is implemented in [python3](https://www.python.org), you can install it with pip3:

      # install with 
      pip3 install MarkerMAG
        
      # upgrade with 
      pip3 install --upgrade MarkerMAG

+ :warning: If you clone the repository directly off GitHub you might end up with a version that is still under development.


Notes 
---

1. :warning: MarkerMAG assumes the id of paired reads in the format of `XXXX.1` and `XXXX.2`. The only difference is the last character.
   You can rename your reads with MarkerMAG's `rename_reads` module ([manual](doc/README_rename_reads.md)). 
   
1. Although you can use your preferred tool to reconstruct 16S rRNA gene sequences from the metagenomic dataset, 
   MarkerMAG does have a supplementary module (`matam_16s`) to reconstruct 16S using Matam. 
   Please refer to the manual [here](doc/README_matam_16s.md) if you want to use it.


How to run:
---

+ Link 16S rRNA gene sequences with MAGs: 

      MarkerMAG link -p Soil -r1 R1.fasta -r2 R2.fasta -marker Soil_16S_uclust_0.999.fasta -mag refined_MAG -x fasta -t 12

+ A detailed explanation for all customizable parameters needs to be added.


Output files:
---

+ #### Summary of identified linkages at genome level

    | MarkerGene | Genome | Linkage | Round |
    |:---:|:---:|:---:|:---:|
    | matam_16S_7   | MAG_6 | 189| Rd1 |
    | matam_16S_12  | MAG_9 | 102| Rd1 |
    | matam_16S_5   | MAG_26| 23 | Rd1 |
    | matam_16S_1   | MAG_30| 307| Rd2 |
    | matam_16S_6   | MAG_59| 55 | Rd2 |
    | matam_16S_21  | MAG_7 | 39 | Rd2 |

+ #### Summary of identified linkages at contig level

    |Marker___Genome(total_number_of_linkages)	|Contig	|Round_1	|Round_2	|
    |:---:|:---:|:---:|:---:|
    |matam_16S_7___MAG_6(189)	    |NODE_1799_length_5513_cov_262.747160	|176	|0|
    |matam_16S_7___MAG_6(189)	    |NODE_1044_length_15209_cov_227.503497	|5	    |0|
    |matam_16S_7___MAG_6(189)	    |NODE_521_length_41010_cov_237.908851	|4	    |0|
    |matam_16S_7___MAG_6(189)	    |NODE_1106_length_13879_cov_211.336082	|4	    |0|
    |matam_16S_12___MAG_9(102)	    |NODE_840_length_21071_cov_25.185811	|102	|0|
    |matam_16S_5___MAG_26(23)	    |NODE_70_length_216864_cov_15.399508	|19	    |0|
    |matam_16S_5___MAG_26(23)	    |NODE_218_length_95089_cov_16.599933	|4	    |0|
    |matam_16S_1___MAG_30(307)	    |NODE_48_length_826_cov_0.666667	    |0	    |307|
    |matam_16S_6___MAG_59(55)	    |NODE_101_length_615_cov_0.377049	    |0	    |36|
    |matam_16S_6___MAG_59(55)	    |NODE_83_length_668_cov_0.214418	    |0	    |19|
    |matam_16S_21___MAG_7(39)	    |NODE_171_length_493_cov_0.295082	    |0	    |39|

    ![linkages](doc/images/linkages_plot.png)

+ #### Visualization of linkages
  
  MarkerMAG supports the visualization of all identified linkages (requires [Tablet](https://ics.hutton.ac.uk/tablet/)). 
  These files ([example](doc/vis_folder)) are in the [Prefix]_linkage_visualization_rd1/2 folder. 
  You can visualize how the linking reads are aligned to the linked MAG contig and 16S rRNA genes by double-clicking the .tablet in each folder. 
  Fifty Ns are added between the linked MAG contig and 16S rRNA gene.
  
  If you see an error from Tablet which says "input files are not in a format that can be understood by tablet", 
  please refer to [https://github.com/cropgeeks/tablet/issues/15](https://github.com/cropgeeks/tablet/issues/15) for the solution.

  ![linkages](doc/images/linking_reads.png)
   