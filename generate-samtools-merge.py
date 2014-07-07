#!/usr/bin/env python
import sys
import os
import argparse
import csv
from collections import defaultdict
from common import return_file_basename
import datetime



def main():

    """ generate jobs for samtools merge on Broad cluster """
    today=datetime.datetime.today()

    datestr=today.strftime("20%y%m%d %X")



    CWD=os.getcwd()


    REF="/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta"
    SAMTOOLS="/broad/software/free/Linux/redhat_5_x86_64/pkgs/samtools/samtools_0.1.19/bin/samtools"
    #bsub -q hour -o aindap.$fbname.out $PWD/$x; done

    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='generate jobs for samtools merge on Broad cluster')

    #parser.add_argument("--ti", type=str, dest='ti', help="target interval file (full path)")


    parser.add_argument('indexfile',  type=str,help='REU index file')

    #parser.add_argument("--queue", type=str, dest='queue', default="week")
    args=parser.parse_args()

    #command="java -Xmx2g -jar " + BIN+"/"+args.picardtool



    #TARGETS= args.ti


    #sys.stderr.write("using "  + TARGETS +"\n")

    #ReuIndexRecord = namedtuple('ReuIndexRecord', 'PDO, SeqProject, Title, BI, PDOSample, ExternalID, BAMPath')

    #java -Xmx8g -jar  /seq/software/picard/current/bin/CalculateHsMetrics.jar BAIT_INTERVALS=$TARGETS TARGET_INTERVALS=$TARGETS INPUT=$BAM OUTPUT=00428C.hsmetrics.txt REFERENCE_SEQUENCE=$REF PER_TARGET_COVERAGE=00428C.pertarget.txt


    indexfh=open(args.indexfile, 'r')

    d = defaultdict(list)

    for line in indexfh:

        fields=line.strip().split('\t')
        (reuid, status, phenotype, consent, dnaquality, samplesource, amountsent, concentration, yaleid, bamfile, checksum)=fields

        d[yaleid].append(bamfile)

    for sample in d.keys():
        files=" ".join( d[sample] )

        commandline =  SAMTOOLS + " merge " + "".join([CWD+"/", sample, ".bam"]) + " " + files
        #print commandline






        scriptfile=".".join([sample, 'samtoolsmerge', 'sh'])
        outfh=open(scriptfile, 'w')
        outfh.write("#"+datestr+"\n")
        outfh.write(commandline+"\n")


if __name__ == "__main__":
    main()
