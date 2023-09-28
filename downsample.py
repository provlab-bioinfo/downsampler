#!/usr/bin/python
import subprocess, re, shutil, os
from pathlib import Path
from alive_progress import alive_bar

def isGZ(filepath):
    with open(filepath, 'rb') as f:
        return f.read(2) == b'\x1f\x8b'

def getReads(file):
    zcat = subprocess.Popen(["zcat",file], stdout=subprocess.PIPE, text=True)
    numseqs = int(subprocess.run(["wc", "-l"], stdin=zcat.stdout, capture_output=True).stdout)
    return int(numseqs / 4)
    
def seqtk_sample(file, output, depth):
    # seqtk sample [file] [depth] > [output]
    with open(output, "w") as outfile:
        if (isGZ(file)):
            seq = subprocess.Popen(["seqtk","sample",str(file),str(depth)], stdout=subprocess.PIPE, text=True)
            subprocess.run(["gzip"], stdin=seq.stdout, stdout=outfile)
        else:
            subprocess.run(["seqtk","sample",str(file),str(depth)], stdout=outfile)

# def samtools_view(file, output, depth):
#     #samtools view -s [proportion] -b [file] > [output]

def downsample(files, output, regex, depths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], random = True, verbose = True):
    files = files if isinstance(files, list) else [files]
    depths = depths if isinstance(depths, list) else [depths]
    
    if not random and len(depths) != len(set(depths)):
        raise("Cannot have duplicated depths with a non-random subset. Remove duplicate depths or set random = True.")

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

file1 = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/F1_S1_L001_R1_001.fastq.gz"
file2 = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/F2_S2_L002_R2_002.fastq.gz"
output = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/"
regex = '(_S\\d*)'

downsample(file1, output, regex, random = True)
downsample(file2, output, regex, random = False)