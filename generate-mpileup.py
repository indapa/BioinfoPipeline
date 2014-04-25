#!/usr/bin/env python
import sys
import os
import argparse
from datetime import datetime
import time
from common import return_file_basename
import csv
from collections import namedtuple, defaultdict

def main():
    
    
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='generate jobs for mplielup')
    
    parser.add_argument("-Q", help="mapping quality",dest='mq', default='30')
    parser.add_argument("-q", help="base quality", dest='bq', default='20')
    parser.add_argument("-bin", help="path to samtools", dest='bin', default="/broad/software/free/Linux/redhat_5_x86_64/pkgs/samtools/samtools_0.1.19/bin/samtools")
    parser.add_argument("-bed", dest='bed', help="bedfile")
    parser.add_argument("-ref", dest='ref', default='/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta', help="bedfile")
    
    parser.add_argument('seqindex',  type=str,help='file.index')
    
    args = parser.parse_args()
    
    cwd = os.getcwd()
    fh=open(args.seqindex, 'r')
    
    SeqIndexRecord = namedtuple('SeqIndexRecord', 'PDO, SeqProject, Title, SeqCenter, PDOSample, ExternalID, BAMPath, FID, QC')
    bedfile_base=return_file_basename(args.bed)
    
    for rec  in map(SeqIndexRecord._make, csv.reader(fh, delimiter='\t')): 
        if rec.QC != 'PASS':
            continue
        bamfile_base = return_file_basename(rec.BAMPath)
        pileupout=".".join([bamfile_base, bedfile_base, 'pileup'])
        
        commandline=" ".join([ args.bin, 'mpileup', '-q', args.bq, '-Q', args.mq, '-f', args.ref, '-l', args.bed, rec.BAMPath, '>', cwd+pileupout])        
 
        outfh=open("pileupjob."+bamfile_base+"."+bedfile_base+".sh", 'w')
 
        outfh.write(commandline+"\n")
        
        #samtools mpileup -q 30 -Q 20 -f /Users/indapa/Research/Genomes/hg19/Homo_sapiens_assembly19.fasta -l resources/HGDP/HGDP_938.bed pileup2seq/exampleBAM/NA12878.chrom22.recal.bam > NA12878.chrom22.pileup
        
        
        
        
        
                         

if __name__ == "__main__":
    main()
