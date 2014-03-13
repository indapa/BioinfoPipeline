#!/usr/bin/env python
""" read in a VCF from stdin and count how many SNPs are in the file
    an example use could be tabix foo.vcf.gz 22 | python vcf_snp_count.py"""
import sys
import vcf
vcf_reader=vcf.Reader(fsock=sys.stdin)

db_snp=0
total_pass_snps=0
total_snps=0
for record in vcf_reader:

    if record.is_snp:
        total_snps+=1
        if record.FILTER == None:
            total_pass_snps +=1
            
            if record.ID != None:
                db_snp+=1

print "\t".join(["Total_snps", "PASS_SNPS", "PASS_SNP_DBSNP"])
print "\t".join([str(total_snps), str(total_pass_snps), str(db_snp)])

