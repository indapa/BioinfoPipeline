#!/usr/bin/env python
import sys
import os
import argparse
import vcf

def main():
    
    """ write  PASS SNPs  to a bed4 format to STDOUT  """
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='Program description')
    parser.add_argument('vcf',  type=str,help='file.vcf')
    parser.add_argument('--compressed',dest='compress',action='store_true')
    args = parser.parse_args()
    print args
    if args.compress == True:
        vcf_reader=vcf.Reader(open(args.vcf,'r'), compressed=True)
    else:
         vcf_reader=vcf.Reader(open(args.vcf,'r'))
    for record in vcf_reader:
        if record.ID == None: 
            record.ID='.'
        if record.is_snp and record.FILTER == None:
            outstring="\t".join([record.CHROM, str(record.start), str(record.end), record.ID])
            print outstring

if __name__ == "__main__":
    main()
