![image](/pics/covflo_logo.png)

## Introduction

Python tool for subsampling/downsampling sequencing data. This was originally built to help determine the minimum sequencing depth necessary for bioinformatic pipelines. It wraps conventiently wraps [seqtk](https://github.com/lh3/seqtk)<sup>[1]</sup> (FASTA/FASTQ) and [samtools](http://www.htslib.org/)<sup>[2]</sup> (SAM/BAM) to generate a set of downsampled sequencing files to input into the desired pipeline.

## Table of Contents

- [Introduction](#introduction)
- [Quick-Start Guide](#quick-start%guide)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Input](#input)
- [Output](#output)
- [Workflow](#workflow)
- [References](#references)

## Quick-Start Guide

<!--
Run covflo pipeline:
```
nextflow run j3551ca/covflo -profile conda --conda_cache /path/to/caches --dir /home/user/sarscov2/input_data -r main
```
For details on available arguments, enter:
```
nextflow run j3551ca/covflo -r main --help
```
-->

## Dependencies

<!--
[Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) is required to build an environment with required workflow dependencies.

This bioinformatic pipeline requires Nextflow:
```
conda install -c bioconda nextflow
```
or download and add the nextflow executable to a location in your user $PATH variable:
```
curl -fsSL get.nextflow.io | bash
mv nextflow ~/bin/
```
Nextflow requires Java v8.0+, so check that it is installed:
```
java -version
```
The OS-independent conda environment activated upon running covflo is specified in the
```environment.yml``` file of the project directory and is built when 
```-profile conda``` is included in the command line. Nextflow will save
the environment to the project directory by default. Alternatively, the 
necessary conda environment can be saved to a different shared location 
accesible to compute nodes by adding ```--conda_cache /path/to/new/location/```.
-->

## Installation

<!--
To copy the program into a directory of your choice, from desired directory run:
```
git clone https://github.com/j3551ca/covflo.git
cd covflo
nextflow run main.nf -profile conda --dir /home/user/sarscov2/input_data/
```
or run directly from Github using:
```
nextflow run j3551ca/covflo -profile conda --dir /home/user/sarscov2/input_data
```
-->

## Input

<!--
The pipeline requires the following files which should be present in the config
and data folders of the directory containing sequences to be analyzed. These
are named the same within different directories - the only thing that needs to be changed
each run is the input directory, which can be specified with the --dir flag on the
command line.

- Multi-fasta file containing consensus sequences of interest [./data/sequences.fasta]
- Reference genome used to align reads to during guided assembly [./config/Ref.gb]
- File containing metadata for sequences under analysis [./data/metadata.csv]
- Excluded strains/ samples [./config/dropped_strains.txt]
- Strains/ samples to ensure are included [./config/included_strains.txt]
- Genomic cluster text files from previous build to be used as input for current [./config/SARS-CoV-2_{0.8,0.9}\_GenomicClusters.txt]
- Pairwise transmission probabilities (>0.8 or 0.9) between samples text files from previous build [./config/SARS-CoV-2_{0.8,0.9}\_TransProbs.txt]
- Colors used in final auspice visualization [./config/colors.csv]
- Sample latitudes and longitudes [./config/lat_longs.csv]
- Specifications for visualization in auspice (ex. title) [./config/auspice_config.json]

## Output

The output directories are 'results', 'auspice', and 'reports'.

results:
- filtered.fasta
- removedpercent.fasta
- replaced.fasta
- informative.fasta (no log)
- names.dedup
- deduped.fasta
- compressed.fasta
- weights
- fasttree.nwk
- resolvedtree.nwk
- blscaled.raxml{\*.startTree, \*.rba, \*.log, \*.bestTreeCollapsed, \*.bestTree, \*.bestModel}
- brlen_round.nwk
- collapse_length.nwk
- repopulate.nwk
- order.nwk
- tree.nwk
- branch_lengths.json
- nt_muts.json
- aa_muts.json
- inferred_traits.json
- SARS-CoV-2_{0.8,0.9}\_TransProbs.tsv (pairwise transmission probabilities used as input for next tree build)
- SARS-CoV-2_{0.8,0.9}\_GenomicClusters.tsv (genomic clusters used as input for next tree build)
- SARS-CoV-2_{0.8,0.9}\_ClustersSummary.tsv
- tree_collapse_snp.nwk
- tc_cluster.tsv
- metadataCluster.tsv

*NOTE: the above files are listed in order of appearance in the 'main.nf' script, where process used to generate them as well as short description of process can be found in 'tag' directive.

auspice:
- ncov_na.json (final tree)
- tip-frequencies.json

reports:
- covflo_usage.html
- covflo_timeline.html
- covflo_dag.html

 -->
 <!--
## Workflow

![image](/pics/covflo_workflow.png)
-->

## References

1. Lh3/SEQTK: Toolkit for processing sequences in FASTA/Q Formats https://github.com/lh3/seqtk (accessed Sep 28, 2023). 

2. Danecek, P.; Bonfield, J. K.; Liddle, J.; Marshall, J.; Ohan, V.; Pollard, M. O.; Whitwham, A.; Keane, T.; McCarthy, S. A.; Davies, R. M.; Li, H. Twelve years of SAMtools and BCFtools. GigaScience 2021, 10. 
