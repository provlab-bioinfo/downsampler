#!/usr/bin/python
import subprocess, re, shutil, os, random
from pathlib import Path
from alive_progress import alive_bar

def isGZ(filepath):
    """Check if file is GZIP'd
    :param filepath: File to check
    :return: bool
    """    
    with open(filepath, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'

def getReads(file):
    """Counts number of reads in a file via zcat
    :param file: File to check
    :return: Number of reads in the file
    """    
    zcat = subprocess.Popen(["zcat",file], stdout=subprocess.PIPE, text=True)
    numseqs = int(subprocess.run(["wc", "-l"], stdin=zcat.stdout, capture_output=True).stdout)
    return int(numseqs / 4)
    
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

def downsample(files, output, regex, depths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], random = True, verbose = True):
    """Downsample files at specified proportions. 

    :param files: _description_
    :param output: _description_
    :param regex: _description_
    :param depths: _description_, defaults to [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    :param random: Should the reads be random or sequential. If sequential, all reads will be subsampled from the previous subsampled file. E.g., for depths = [0.7,0.8,0.9], the 0.9 depth is subsampled from the input file, the 0.8 depth is subsampled from the 0.9 depth output, and the 0.7 is subsampled from the 0.8 depth file. defaults to True
    :param verbose: _description_, defaults to True
    """    
    files = files if isinstance(files, list) else [files]
    depths = depths if isinstance(depths, list) else [depths]
    
    if not random and len(depths) != len(set(depths)):
        raise("Cannot have duplicated depths with a non-random subset. Remove duplicate depths or set random = True.")

    if not os.path.exists(output): os.makedirs(output)

    depths = sorted(depths, reverse = True)
    recursiveDepths = {depths[0]: depths[0]}
    if not random: 
        for i in reversed(range(1,len(depths))): recursiveDepths.update({depths[i]: depths[i]/depths[i-1]})
    
    with alive_bar(total = len(files)*(len(depths)+1), title="Downsampling files....", unknown="dots_waves", disable = not verbose) as bar:         
        for file in files:
            f = Path(file)
            lastout = None
            for depth in depths:
                out = Path(output,re.sub(regex, fr'\1_{depth}', f.stem) + f.suffix)
                if random or lastout is None:
                    seqtk_sample(file, out, depth)
                    print(f"file: {file}\nout: {out}\ndepth: {depth}\n")
                else:
                    seqtk_sample(lastout, out, recursiveDepths.get(depth))
                    print(f"file: {lastout}\nout: {out}\ndepth: {recursiveDepths.get(depth)}\n")
                lastout = out
                bar()
            f = Path(output,re.sub(regex, fr'\1_1.0', f.stem) + f.suffix)
            shutil.copyfile(file, f)
            bar()

# file1 = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/F1_S1_L001_R1_001.fastq.gz"
# file2 = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/F2_S2_L002_R2_002.fastq.gz"
# output = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/"
regex = '(_S\\d*)'
depths = [0.5,0.1,0.05,0.01,0.005,0.001]
# downsample(file1, output, regex, random = True)
# downsample(file2, output, regex, random = False)


files = "/nfs/APL_Genomics/scratch/230927_N_I_008_WW/230927_MN01658_0129_A000H5NFKW/Alignment_1/20230928_065543/Fastq/"
files = [os.path.abspath(os.path.join(files, p)) for p in os.listdir(files)]
downsample(files, "/nfs/APL_Genomics/scratch/230927_N_I_008_WW/230927_MN01658_0129_A000H5NFKW/Alignment_1/20230928_065543/Fastq_rand/", regex, depths = depths, random = True)
downsample(files, "/nfs/APL_Genomics/scratch/230927_N_I_008_WW/230927_MN01658_0129_A000H5NFKW/Alignment_1/20230928_065543/Fastq_seq/", regex, depths = depths, random = False)