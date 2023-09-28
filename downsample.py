#!/usr/bin/python

import subprocess, re, shutil
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

def downsample(files, output, regex, depths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], verbose = True):
    files = files if isinstance(files, list) else [files]
    depths = depths if isinstance(depths, list) else [depths]
    with alive_bar(total = len(files)*(len(depths)+1), title="Downsampling files....", unknown="dots_waves", disable = not verbose) as bar:
        for file in files:
            f = Path(file)
            for depth in depths:
                    out = Path(output,re.sub(regex, fr'\1_{depth}', f.stem) + f.suffix)
                    seqtk_sample(file, out, depth)
                    bar()
            f = Path(output,re.sub(regex, fr'\1_1.0', f.stem) + f.suffix)
            shutil.copyfile(file, f)
    
files = ["F1_S1_L001_R1_001.fastq.gz","/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/F2_S2_L002_R2_002.fastq.gz"]
output = "/nfs/Genomics_DEV/projects/alindsay/Projects/downsampler/"
regex = '(_S\\d*)'

downsample(files, output, regex)