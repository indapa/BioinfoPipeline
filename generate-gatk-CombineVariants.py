#!/usr/bin/env python

import sys
import os
import string

import time
from optparse import OptionParser
from datetime import datetime
import time
from common import return_file_basename

def printFailFunction(fh, filename):
    cwd = os.getcwd()
    fh.write("function Terminate_Script() {" + "\n")
    fh.write("FAILED_TOOL=$1" + "\n")
    fh.write("ERROR=$2" + "\n")
    failname=filename+".fail"
    fh.write("FAIL_FILE=\""+ failname +"\"\n")
    fh.write("FAILBIN=\""+cwd+"\"\n")
    fh.write("echo \"$FAILED_TOOL failed.\" > $FAIL_FILE\n")
    fh.write("cat $ERROR >> $FAIL_FILE\n")
    fh.write("echo `hostname` >> $FAIL_FILE\n")
    fh.write("echo $PBS_NODEFILE >> $FAIL_FILE\n")
    fh.write("if [ ! -d $FAILBIN ]; then mkdir -p $FAILBIN; fi\n")

    fh.write("cp $NODE_DIR/$FAIL_FILE $FAILBIN\n")
    fh.write("rm -fr $NODE_DIR\n")
    fh.write("exit\n")
    fh.write("}\n")

def printTransferFunction(fh):
    fh.write( "function TransferFiles() { " + "\n")
    fh.write ( "SOURCE=$1" + "\n" )
    fh.write ( "DESTINATION=$2" + "\n")
    fh.write("INPUT_FILE=$3" + "\n")
    fh.write("OUTPUT_FILE=$4" + "\n")
    fh.write( "if [ \"$OUTPUT_FILE\" == \"\" ]; then OUTPUT_FILE=$INPUT_FILE; fi" + "\n")
    fh.write( "if [ ! -d $DESTINATION ]; then mkdir -p $DESTINATION; fi" + "\n")
    fh.write( "rsync $SOURCE/$INPUT_FILE $DESTINATION/$OUTPUT_FILE" + "\n")
    
    fh.write ("}" + "\n")

""" generic script to call CombineVariants from the GATK - prepares to run on cluster or on localhost """

def main():
    datestring = str(datetime.now()).split( ' ' )[0]
    datestring=datestring.replace('-','')
    localtime = time.asctime( time.localtime(time.time()) )
    cwd = os.getcwd()

    usage = "usage: %prog [options] vcf.files.list.txt"

    parser = OptionParser(usage)
    parser.add_option("--bin", type="string", dest="binpath", default="/share/home/indapa/software/GenomeAnalysisTK-1.6-5-g557da77/dist", help="GATK path default: /share/home/indapa/software/GenomeAnalysisTK-1.6-5-g557da77/dist")
   
    parser.add_option("--R", type="string", dest='ref', default='/d1/data/pipeline_resources/references/human_reference.b37.including_decoys/human_reference_v37_decoys.fa',
                      help="  reference fasta (default is /d1/data/pipeline_resources/references/human_reference.b37.including_decoys/human_reference_v37_decoys.fa")

    parser.add_option("--scriptname", type="string", dest="scriptname", default="combineVariants.sh", help="name of shell script (combineVariants.sh default)")
    

    parser.add_option("--mergeoption", type="string", dest="mergeoption", default="UNIQUIFY", help="default UNIQUIFY")
    parser.add_option("--runlocal", action="store_true", dest="runlocal", help="run local and not as cluster job", default=False)

    parser.add_option("--mem", type="string", dest="mem", default="mem8", help="memory of node, default mem8")
    parser.add_option("--ppn", type="int", dest="ppn", default=1, help="processes per node default 1")


    (options, args)=parser.parse_args()

    argsfile=args[0]
    fh=open(argsfile, 'r')

    """ file with variant1.vcf variant2.vcf to merge """
    for line in fh:
        (variant1, variant2)=line.strip().split('\t')
        vcf1=return_file_basename(variant1)
        vcf2=return_file_basename(variant2)
        outputfile=".".join([os.path.splitext(file)[0],os.path.splitext(file2)[0], 'combineVariants', 'vcf'])
       
        outdir=outputfile
        outdir=string.replace(outdir,'.vcf', '')

        scriptname=outputfile
        scriptname=string.replace(scriptname,'.vcf', '.sh')
        outfh=open(scriptname,'w')

        localtime = time.asctime( time.localtime(time.time()) )
        outfh.write("#" + localtime +"\n")


        if options.runlocal == False:
            outfh.write("#PBS -l nodes=1:"+options.mem+":ppn="+str(options.ppn)+'\n')
            outfh.write("#PBS -m abe"+'\n')
            outfh.write("\n")
        
            outfh.write("NODE_DIR=/scratch/indapa/"+outdir+"\n")
            outfh.write("INPUT_DIR=$NODE_DIR\n")
            outfh.write("if [ -d $NODE_DIR ]\nthen\nrm -rf $NODE_DIR\n fi"+'\n')
            outfh.write("mkdir -p  $NODE_DIR \n cd $NODE_DIR\n")
            outfh.write("\n")
            printTransferFunction(outfh)
            outfh.write("\n")
            printFailFunction(outfh, scriptname)
            outfh.write("\n")

    

        jarcommand = "java -jar " + options.binpath+"/GenomeAnalysisTK.jar"
        commandtype="-T CombineVariants"
        referencefile= " -R " + options.ref
        variantone= "-V:"+name1 + " " +variant1
        variantwo= "-V:"+name2 + " " +variant2
        output = " -o " + outputfile
        mergestring="-genotypeMergeOptions " + options.mergeoption
        prioritystring="-priority " + priority
    
    
    
        stdout = " > " + scriptname + ".stdout"
        stderr = "2> " + scriptname + ".stderr"
    
    
        commandline = " ".join( [ jarcommand, commandtype,referencefile, variantone, variantwo, output, mergestring, prioritystring, stdout, stderr  ] )
        outfh.write(commandline + "\n")
        outfh.write("\n")
        outfh.write( " if [ $? -ne 0  ]; then \n")
        outfh.write("Terminate_Script \"CombineVariants\" "  + scriptname+".stderr"  +  " \n")
        outfh.write("fi\n")
        if options.runlocal == False:
    #cp back to homedir
            outfh.write("cp " + outputfile + " " + cwd + "\n")
            outfh.write("echo \" " + scriptname + "\" > " + cwd + "/" +scriptname+".complete\n")
            outfh.write("rm -fr $NODE_DIR\n")
        
if __name__ == "__main__":
    main()
