# LycoCyc
Collection of scripts for lycopene cyclase analysis.


## Grouping cyclase sequences into clades

A phylogenetic tree of all cyclase sequences was used to identify cyclase clades. Sequences of the different clades were extracted into individual FASTA files. This script processes these classification results and generates a mapping file of cyclase sequence IDs to clades.


```
Usage:
  python fastaClades2info.py --baits <FILE> --out <DIR> [--subject <FILE>|--subjectdir <DIR>]

Mandatory (option1):
  --baits      STR         A multiple FASTA file. 
  --out        STR         Directory for temporary and output files.
  --subject    STR         Subject sequence file.

Mandatory (option2):
  --baits      STR         A multiple FASTA file. 
  --out        STR         Directory for temporary and output files.
  --subjectdir STR         Folder containing subject sequence files.

Optional:
    --number STR        Number of BLAST hits to consider.[10]
```

`--baits` FASTA file containing the bait sequences.


## DeepTMHMM result mapper


## References
