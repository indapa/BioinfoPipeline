#!/usr/bin/env python
import sys
import os
import argparse
from common import return_file_basename
import vcf

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='extract SNPs or INDELs from a vcf.gz file and write to stdout')
    parser.add_argument('-type', dest='vtype', type=str, help="SNP|INDEL")
    parser.add_argument('vcfile',  type=str,help='*.vcf.gz file')

    args=parser.parse_args()




    vcfroot, ext = os.path.splitext(args.vcfile)
    if ext == '.gz':
        vcf_basename = return_file_basename(return_file_basename(args.vcfile))
    else:
        vcf_basename = return_file_basename(args.vcfile)

    new_vcfname=".".join([vcf_basename, args.vtype, 'vcf'])


    vcf_reader = vcf.Reader(open(args.vcfile, 'r'))
    vcf_writer = vcf.Writer(open('/dev/stdout', 'w'), vcf_reader)

    #sys.stderr.write("writing "+ args.vtype + " to " + new_vcfname +"\n")
    for record in vcf_reader:
        if args.vtype=='SNP' and record.is_snp==True:
            vcf_writer.write_record(record)

        if args.vtype=='INDEL' and record.is_indel==True:
            vcf_writer.write_record(record)





if __name__ == "__main__":
    main()
