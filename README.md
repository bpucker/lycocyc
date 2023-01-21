# LycoCyc
Collection of scripts for lycopene cyclase analysis.


## Grouping cyclase sequences into clades

A phylogenetic tree of all cyclase sequences was used to identify cyclase clades. Sequences of the different clades were extracted into individual FASTA files. This script processes these classification results and generates a mapping file of cyclase sequence IDs to clades.


```
Usage:
  python fastaClades2info.py --fasta <DIR> --out <FILE>
  
  --fasta  STR   FASTA file input folder
  --out    STR   Output file
```

`--fasta` specifies a FASTA file containing folder. The IDs in these FASTA files need to match the IDs in other analyses. The clade name is inferred from the filename.

`--out` specifies the output file (mapping file) that assigns cyclase sequence IDs to phylogenetic clades. Sequence IDs are given in column1, clade names are given in column2.


## DeepTMHMM result mapper

Script for mapping of DeepTMHMM results to a phylogenetic tree. This script allows the integration of information about phylogenetic clades of the sequences.

```
Usage:
  python DeepTMHMM2tree.py --tmr <FILE> --out <DIR>
  
  --tmr    STR   GFF3 input file
  --out    STR   Output folder
  
  optional:
  --info   STR   Info file (clade mapping)
	--name   STR   File name prefix
```

`--tmr` specifies the output file of DeepTMHMM which is a GFF3 file.

`--out` specifies the output folder where the result files of this mapping will be placed. Result files can be imported into iTOL as annotation files.

`--info` specifies the clade mapping file to include phylogenetic information in the annotation file.

`--name` specifies a file name prefix.



## References

This repository.
