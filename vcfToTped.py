#!/usr/bin/env python
import sys
import os
import argparse
from common import return_file_basename
from collections import defaultdict
import vcf

""" convert a VCF to PLINK TPED file """

def main():
    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='convert vcf to plink tped format')

    parser.add_argument('vcfile',  type=str,help='*.vcf.gz file')

    args=parser.parse_args()

    vcf_reader = vcf.Reader(open(args.vcfile, 'r'))


    sys.stderr.write("iterating through genotypes in vcf...\n")

    for record in vcf_reader:
        #print record.CHROM, record.ID, '0', record.POS
        if record.is_snp != True:
            continue
        if record.ID == None:
            recordid=":".join([record.CHROM, str(record.POS)])
        else:
            recordid=record.ID
        genotypes=[]
        for sample in record.samples:
            if sample.called == False:
                genotype="0 0"
            else:
                genotype=" ".join(sample.gt_bases.split('/'))
            genotypes.append(genotype)


        genotypestring="\t".join(genotypes)
        outstring=[record.CHROM, recordid, '0', str(record.POS), genotypestring]
        print "\t".join(outstring)


if __name__ == "__main__":
    main()
