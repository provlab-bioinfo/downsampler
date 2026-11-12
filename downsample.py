#!/usr/bin/python
import subprocess, re, shutil, os, random, argparse, gzip, warnings
from pathlib import Path
from alive_progress import alive_bar

def isGZ(filepath):
    """Check if file is GZIP'd
    :param filepath: File to check
    :return: bool
    """    
    with gzip.open(filepath, 'r') as fh:
        try:
            fh.read(1)
        except gzip.BadGzipFile:
            return False
    return True

def getReads(file):
    """Counts number of reads in a file via zcat
    :param file: File to check
    :return: Number of reads in the file
    """    
    zcat = subprocess.Popen(["zcat",file], stdout=subprocess.PIPE, text=True)
    numseqs = int(subprocess.run(["wc", "-l"], stdin=zcat.stdout, capture_output=True).stdout)
    return int(numseqs / 4)
    
def subsample(file,output,depth):
    """Subsamples a file. Automatically selects tool based on extension.
    :param file: Path to file to subsample
    :param output: The output directory
    :param depth: The depth to sample
    """  
    fileExt = Path(file).suffix.lower()
    if fileExt.lower == ".gz" or ".gzip": fileExt = Path(file).suffixes[-2]

    match (fileExt):
        case ".bam" | ".sam":
            samtools_view(file,output,depth)
        case ".fasta" | ".fa" | ".fastq" | ".fq":
            seqtk_sample(file,output,depth)

def seqtk_sample(file, output, depth):
    """Subsamples a FASTQ/FASTA file via seqtk sample. Can be GZIP'd.
    :param file: Path to file to subsample
    :param output: The output directory
    :param depth: The depth to sample
    """    
    # seqtk sample [file] [depth] > [output]
    with open(output, "w") as outfile:
        if (isGZ(file)):
            seq = subprocess.Popen(["seqtk","sample",str(file),str(depth)], stdout=subprocess.PIPE, text=True)
            subprocess.run(["gzip"], stdin=seq.stdout, stdout=outfile)
        else:
            subprocess.run(["seqtk","sample",str(file),str(depth)], stdout=outfile)

def samtools_view(file, output, depth):
    """Subsamples a SAM/BAM file via samtools view.
    :param file: Path to file to subsample
    :param output: The output directory
    :param depth: The depth to sample
    """    
    #samtools view -s [proportion] -b [file] > [output]
    if (depth < 1): depth = depth + random.randint(1,100000) # For samtools; -s is INT.FRAC, where INT is the seed.
    if (Path(file).suffix != ".bam"): 
        subprocess.run(["samtools","view","-s",depth,"-o",output,file])
    else:
        subprocess.run(["samtools","view","-s",depth,"-b","-o",output,file])

def downsample(files, output, regex, depths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], random = True, includeOriginal = True, verbose = True):
    """Downsample files at specified proportions. 

    :param files: Files to downsample, seperated by a space. E.g., `--files file1.fastq.gz file2.fastq.gz`.
    :param output: Path to the output folder
    :param regex: Regex for modifying the file name to include the downsample proportion. E.g., for `F1_S1_L001_R1_001.fastq.gz` and `0.5` depth, `regex = '(_S\\d*)'` will insert '_0.5' right after '_S1', producing `F1_S1_0.5_L001_R1_001.fastq.gz`.
    :param depths: List of depths for output files. Can be represented as float propotion of the original sample (e.g., [0.1, 0.5, 0.9]), or as a integer number of reads (e.g., [1000, 2000, 3000]. Must be all either floats or integers. Defaults to [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]. 
    :param random: Should the reads be random or sequential? If random, all reads will be randomly subsampled from the original input. If sequential, all reads will be subsampled from the previous subsampled file. E.g., for depths = [0.7,0.8,0.9], the 0.9 depth is subsampled from the input file, the 0.8 depth is subsampled from the 0.9 depth output, and the 0.7 is subsampled from the 0.8 depth file. defaults to True
    :param includeOriginal: Include the original sample? Will be labelled with proportion of 1.0., defaults to True
    :param verbose: Be chatty, defaults to True
    """    
    files = files if isinstance(files, list) else [files]
    depths = depths if isinstance(depths, list) else [depths]

    if not (all(isinstance(x, float) for x in depths) or all(isinstance(x, int) for x in depths)):
        raise Exception(f"Depths must be all floats or all integers: {depths}")
    
    if not random and len(depths) != len(set(depths)):
        raise Exception(f"Cannot have duplicated depths with a non-random subset: {depths}. Remove duplicate depths or set random = True.")

    if not os.path.exists(output): os.makedirs(output)

    depths = sorted(depths, reverse = True)
    recursiveDepths = {depths[0]: depths[0]}
    if not random: 
        for i in reversed(range(1,len(depths))): recursiveDepths.update({depths[i]: depths[i]/depths[i-1]})
    
    with alive_bar(total = len(files)*(len(depths)+int(includeOriginal)), title="Downsampling files....", unknown="dots_waves", disable = not verbose) as bar:         
        for file in files:
            f = Path(file)
            lastout = None
            for depth in depths:
                out = Path(output,re.sub(regex, fr'\1_{depth}', f.stem) + f.suffix)
                if random or lastout is None:
                    subsample(file, out, depth)
                    # print(f"file: {file}\nout: {out}\ndepth: {depth}\n")
                else:
                    subsample(lastout, out, recursiveDepths.get(depth))
                    # print(f"file: {lastout}\nout: {out}\ndepth: {recursiveDepths.get(depth)}\n")
                lastout = out
                if ((nReads := getReads(out)) < depth): warnings.warn(f"Not enough reads in input file. Depth '{depth}' contains only {nReads}.")    
                bar()
            if (includeOriginal):
                f = Path(output,re.sub(regex, fr'\1_1.0', f.stem) + f.suffix)
                shutil.copyfile(file, f)
                bar()            

def int_or_float(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)  # Or use float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{value}' is not a valid integer or float")

def main(args):
    downsample(args.files, args.output, args.regex, args.depths, args.random, args.includeOriginal, args.verbose)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--files', nargs='+', required=True, help='Files to downsample, seperated by a space. E.g., `--files file1.fastq file2.fastq`.')
    parser.add_argument('-o','--output', required=True, help="Path to the output folder")
    parser.add_argument('-r', '--regex', default = '(_S\\d*)', help="Regex for modifying the file name to include the downsample proportion. E.g., for `F1_S1_L001_R1_001.fastq.gz` and `0.5` depth, `--regex '(_S\\d*)'` would produce `F1_S1_0.5_L001_R1_001.fastq.gz`.")
    parser.add_argument('-d', '--depths', type=int_or_float, nargs='+', default = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], help='The proportional depth to sequence, seperated by a space. E.g., `0.5` would retain 50%% of reads, which generally would approximate 50%% depth.\nDefault is: 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9')
    parser.add_argument('-x', '--random', action='store_true', help='Should the reads be random or sequential? If sequential, all reads will be subsampled from the previous subsampled file. E.g., for depths = [0.7,0.8,0.9], the 0.9 depth is subsampled from the input file, the 0.8 depth is subsampled from the 0.9 depth output, and the 0.7 is subsampled from the 0.8 depth file.')
    parser.add_argument('-i', '--includeOriginal', action='store_true', help='Include the original sample? Will be labelled with proportion of 1.0. Default: False')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be chatty?')
    args = parser.parse_args()
    main(args)
