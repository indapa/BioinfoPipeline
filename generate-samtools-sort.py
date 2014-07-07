#!/usr/bin/env python
import sys
import os
import argparse
import csv
from collections import defaultdict
from common import return_file_basename
import datetime



def main():

    """ generate jobs for samtools sort on Broad cluster """
    today=datetime.datetime.today()

    datestr=today.strftime("20%y%m%d %X")



    CWD=os.getcwd()


    REF="/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta"
    SAMTOOLS="/broad/software/free/Linux/redhat_5_x86_64/pkgs/samtools/samtools_0.1.19/bin/samtools"
    #bsub -q hour -o aindap.$fbname.out $PWD/$x; done

    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='generate jobs for samtools sort on Broad cluster')




    parser.add_argument('indexfile',  type=str,help='REU index file')

    #parser.add_argument("--queue", type=str, dest='queue', default="week")
    args=parser.parse_args()

    indexfh=open(args.indexfile, 'r')

    d = defaultdict(list)

    for line in indexfh:

        fields=line.strip().split('\t')
        (reuid, status, phenotype, consent, dnaquality, samplesource, amountsent, concentration, yaleid, bamfile, checksum)=fields

        d[yaleid].append(bamfile)

    for sample in d.keys():
        files=" ".join( d[sample] )

        if os.path.isfile(CWD+"/"+sample+".bam") == False:
            sys.sterr.write("merged bam for sample " + sample + " doesn't exist!")
            continue

        commandline =  SAMTOOLS + " sort " +  CWD + "/"+sample+".bam"+  sample+".sorted" +
        #print commandline

        #scriptfile=".".join([sample, 'samtoolsmerge', 'sh'])
        outfh=open(scriptfile, 'w')
        outfh.write("#"+datestr+"\n")
        outfh.write(commandline+"\n")


if __name__ == "__main__":
    main()
