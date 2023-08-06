
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


MarkerMAG modules
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

+ You need to either add the dependencies to your system path or specify the path to their executable files with the corresponding arguments.
  
+ Dependencies for supplementary modules can be found from their own manual page.
 

How to install
---

+ BioSAK has been tested on Linux/Mac, but NOT on Windows.
+ MarkerMAG is implemented in [python3](https://www.python.org), you can install it with pip3:

      # install with 
      pip3 install MarkerMAG
        
      # upgrade with 
      pip3 install --upgrade MarkerMAG

+ :warning: If you clone the repository directly off GitHub you might end up with a version that is still under development.


How to run
---

+ :warning: MarkerMAG assumes the id of paired reads in the format of `XXXX.1` and `XXXX.2`. The only difference is the last character.
   You can rename your reads with MarkerMAG's `rename_reads` module ([manual](doc/README_rename_reads.md)). 
 

+ Although you can use your preferred tool to reconstruct 16S rRNA gene sequences from the metagenomic dataset, 
   MarkerMAG does have a supplementary module (`matam_16s`) to reconstruct 16S using Matam. 
   Please refer to the manual [here](doc/README_matam_16s.md) if you want to use it.


+ Link 16S rRNA gene sequences with MAGs: 

      MarkerMAG link -p Soil -r1 R1.fasta -r2 R2.fasta -marker Soil_16S_uclust_0.999.fasta -mag refined_MAG -x fasta -t 12

+ A detailed explanation for all customizable parameters needs to be added.


Output files
---

1. Summary of identified linkages at genome level

    | Marker | MAG | Linkage | Round |
    |:---:|:---:|:---:|:---:|
    | matam_16S_7   | MAG_6 | 181| Rd1 |
    | matam_16S_12  | MAG_9 | 102| Rd1 |
    | matam_16S_6   | MAG_59| 55 | Rd2 |

1. Summary of identified linkages at contig level

    |Marker___MAG(total number of linkages)	|Contig	        |Round_1	|Round_2	|
    |:---:|:---:|:---:|:---:|
    |matam_16S_7___MAG_6(181)	            |Contig_1799	|176	    |0          |
    |matam_16S_7___MAG_6(181)	            |Contig_1044	|5	        |0          |
    |matam_16S_12___MAG_9(102)	            |Contig_840	    |102	    |0          |
    |matam_16S_6___MAG_59(39)	            |Contig_171	    |0	        |55         |

1. Visualization of summary of identified linkages
   
    ![linkages](doc/images/linkages_plot.png)

1. Visualization of individual linkages
  
   MarkerMAG supports the visualization of all identified linkages (requires [Tablet](https://ics.hutton.ac.uk/tablet/)). 
   These files ([example](doc/vis_folder)) are in the [Prefix]_linkage_visualization_rd1/2 folder. 
   You can visualize how the linking reads are aligned to the linked MAG contig and 16S rRNA genes by double-clicking the .tablet in each folder. 
   Fifty Ns are added between the linked MAG contig and 16S rRNA gene.
  
   ![linkages](doc/images/linking_reads.png)
  
   *If you see an error from Tablet that says "input files are not in a format that can be understood by tablet", 
   please refer to [https://github.com/cropgeeks/tablet/issues/15](https://github.com/cropgeeks/tablet/issues/15) for the solution.
   