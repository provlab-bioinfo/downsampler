## Downsampler

[![Lifecycle: WIP](https://img.shields.io/badge/lifecycle-WIP-yellow.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental) [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/CompEpigen/scMethrix/issues) [![License: GPL3](https://img.shields.io/badge/license-GPL3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![minimal Python version: 3.11](https://img.shields.io/badge/Python-3.11-6666ff.svg)](https://www.python.org/) [![Package Version = 0.0.1](https://img.shields.io/badge/Package%20version-0.0.1-orange.svg?style=flat-square)](https://github.com/provlab-bioinfo/downsampler/blob/main/NEWS) [![Last-changedate](https://img.shields.io/badge/last%20change-2023--10--12-yellowgreen.svg)](https://github.com/provlab-bioinfo/downsampler/blob/main/NEWS)

Python tool for subsampling/downsampling sequencing data. This was originally built to help determine the minimum sequencing depth necessary for bioinformatic pipelines. It wraps conventiently wraps [seqtk](https://github.com/lh3/seqtk)<sup>[1](#references)</sup> (FASTA/FASTQ) and [samtools](http://www.htslib.org/)<sup>[2](#references)</sup> (SAM/BAM) to generate a set of downsampled sequencing files to input into the desired pipeline.

## Table of Contents

- [Quick-Start Guide](#quick-start%guide)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Notes](#notes)
- [References](#references)

## Quick-Start Guide

```
conda activate downsampler
python downsample.py \
  --files <Input FA/FQ/SAM/BAM files> \
  --output <Output directory> \ 
  --regex <Regex for renaming downsamples> \
  --depths <Proportional depth of downsamples> \
  --random <Should reads be random in each downsample?> \
  --includeOriginal <Include the original FASTQ?> \
  --verbose <Be chatty?>
```

## Dependencies

[Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) is required to build the [downsampler](/environments/environment.yml) environment with the necessary workflow dependencies. To create the environment:
```
conda env create -f ./environments/environment.yml
```
<!--
## Installation

## Input

## Output
-->

## Notes
No QC is done on downsamples. It's possible that a low enough downsample has < 1x coverage, resulting in an incomplete genome. 

## References

1. Lh3/SEQTK: Toolkit for processing sequences in FASTA/Q Formats https://github.com/lh3/seqtk (accessed Sep 28, 2023). 

2. Danecek, P.; Bonfield, J. K.; Liddle, J.; Marshall, J.; Ohan, V.; Pollard, M. O.; Whitwham, A.; Keane, T.; McCarthy, S. A.; Davies, R. M.; Li, H. Twelve years of SAMtools and BCFtools. GigaScience 2021, 10. 
