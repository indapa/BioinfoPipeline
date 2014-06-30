#!/usr/bin/env python
import sys
import os
import argparse
import csv
from collections import namedtuple
from common import return_file_basename
import datetime



def main():
    
    today=datetime.datetime.today()
    
    datestr=today.strftime("20%y%m%d %X")
    
    
    
    CWD=os.getcwd() 
    
    BROAD_STD_AGILENT_TARGETS="/humgen/gsa-pipeline/resources/b37/v5/whole_exome_agilent_1.1_refseq_plus_3_boosters.Homo_sapiens_assembly19.targets.interval_list"
    BROAD_STD_AGILENT_GENCODE="/humgen/gsa-pipeline/resources/b37/v5/gencode.v12_broad.agilent_merged.interval_list"
    REF="/seq/references/Homo_sapiens_assembly19/v1/Homo_sapiens_assembly19.fasta"
    BIN="/seq/software/picard/current/bin"
    #bsub -q hour -o aindap.$fbname.out $PWD/$x; done

    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='Program description')
    
    parser.add_argument("--ti", type=str, dest='ti', help="target interval file (full path)")


    parser.add_argument('indexfile',  type=str,help='REU index file')
    parser.add_argument("--picardtool", type=str, dest='picardtool', default="CalculateHsMetrics.jar")
    parser.add_argument("--queue", type=str, dest='queue', default="week")
    args=parser.parse_args()
    
    command="java -Xmx2g -jar " + BIN+"/"+args.picardtool
    
    

    TARGETS= args.ti

        
    sys.stderr.write("using "  + TARGETS +"\n")
    
    ReuIndexRecord = namedtuple('ReuIndexRecord', 'PDO, SeqProject, Title, BI, PDOSample, ExternalID, BAMPath')
    
    #java -Xmx8g -jar  /seq/software/picard/current/bin/CalculateHsMetrics.jar BAIT_INTERVALS=$TARGETS TARGET_INTERVALS=$TARGETS INPUT=$BAM OUTPUT=00428C.hsmetrics.txt REFERENCE_SEQUENCE=$REF PER_TARGET_COVERAGE=00428C.pertarget.txt

    
    for rec in map(ReuIndexRecord._make, csv.reader(open(args.indexfile, "rb"), delimiter='\t')):
        if rec.PDO == 'PDO': continue
        samplename= return_file_basename( rec.BAMPath)
        samplemetrics = ".".join([samplename, 'hsmetrics', 'txt'])
        pertargetmetrics=".".join([samplename, 'hsmetrics', 'pertarget', 'txt'])
        commandline = [ command , "BAIT_INTERVALS="+TARGETS, "TARGET_INTERVALS="+TARGETS, "INPUT="+rec.BAMPath, "OUTPUT="+CWD+"/"+samplemetrics,
                       "REFERENCE_SEQUENCE="+REF, "PER_TARGET_COVERAGE="+CWD+"/"+pertargetmetrics]
        outstring=" ".join(commandline)
        output=".".join(["aindap", samplename, 'hsmetrics', 'txt'])
        scriptfile=".".join([samplename,rec.SeqProject, 'hsmetrics', 'sh'])
        outfh=open(scriptfile, 'w')
        outfh.write("#"+datestr+"\n")
        outfh.write(outstring+"\n")
        
    
if __name__ == "__main__":
    main()
