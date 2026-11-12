## Downsampler

 [![Lifecycle:Stable](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](https://lifecycle.r-lib.org/articles/stages.html#stable) [![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/CompEpigen/scMethrix/issues) [![License: GPL3](https://img.shields.io/badge/license-GPL3-lightgrey.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html) [![minimal Python version: 3.11](https://img.shields.io/badge/Python-3.11-6666ff.svg)](https://www.python.org/) [![Package Version = 1.0.0](<https://img.shields.io/badge/Package%20version-1.0.0-orange.svg?style=flat-square>)](https://github.com/provlab-bioinfo/downsampler/blob/main/NEWS) [![Last-changedate](<https://img.shields.io/badge/last%20change-2026--11--12-yellowgreen.svg>)](https://github.com/provlab-bioinfo/downsampler/blob/main/NEWS)

Python tool for subsampling/downsampling sequencing data. This was originally built to help determine the minimum sequencing depth necessary for bioinformatic pipelines. It wraps conventiently wraps [seqtk](https://github.com/lh3/seqtk)<sup></sup> (FASTA/FASTQ) and [samtools](http://www.htslib.org/)<sup></sup> (SAM/BAM) to generate a set of downsampled sequencing files to input into the desired pipeline.

## Table of Contents

- [Quick-Start Guide](#quick-start%guide)
- [Dependencies](#dependencies)
- [Inputs](#inputs)
- [Notes](#notes)
- [References](#references)

## Quick-Start Guide

```
conda activate downsampler
python downsample.py \
  --files <Input FA/FQ/SAM/BAM files> \
  --output <Output directory> \ 
  --regex <Regex for renaming downsamples> \
  --depths <Depth of downsamples> \
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

## Inputs

**`--files`**: Files to downsample, seperated by a space. E.g., `--files file1.fastq file2.fastq`.

**`--output`**: Path to the output folder

**`--regex`**: Regex for modifying the file name to include the downsample proportion. E.g., for `F1_S1_L001_R1_001.fastq.gz` and `0.5` depth, `regex = '(_S\\d*)'` will insert '_0.5' right after '_S1', producing `F1_S1_0.5_L001_R1_001.fastq.gz`.

**`--depths`**:  List of depths for output files. Can be represented as float propotion of the original sample (e.g., `[0.1, 0.5, 0.9]`), or as a integer number of reads (e.g., `[1000, 2000, 3000]`). Must be all either floats or integers.List of depths as represented as propotion of the original sample. Defaults to `[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]`.

**`--random`**: Should the reads be random or sequential? If sequential, all reads will be subsampled from the previous subsampled file. E.g., for `depths = [0.7,0.8,0.9]`, the `0.9` depth is subsampled from the input file, the `0.8` depth is subsampled from the `0.9` depth output, and the `0.7` is subsampled from the `0.8` depth file. Defaults to `True`

**`--includeOriginal`**: Include the original sample? Will be labelled with proportion of `1.0`. Defaults to `True`

**`--verbose`**: Be chatty. Defaults to `True`

## Notes

No QC is done on downsamples. It's possible that a low enough downsample has < 1x coverage, resulting in an incomplete genome.

## References

1. Lh3/SEQTK: Toolkit for processing sequences in FASTA/Q Formats https://github.com/lh3/seqtk (accessed Sep 28, 2023).
2. Danecek, P.; Bonfield, J. K.; Liddle, J.; Marshall, J.; Ohan, V.; Pollard, M. O.; Whitwham, A.; Keane, T.; McCarthy, S. A.; Davies, R. M.; Li, H. Twelve years of SAMtools and BCFtools. GigaScience 2021, 10.
