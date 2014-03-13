#!/usr/bin/env python
""" read in a VCF from stdin and count how many INDELs are in the file
    an example use could be tabix foo.vcf.gz 22 | python vcf_indel_count.py"""
import sys
import vcf
vcf_reader=vcf.Reader(fsock=sys.stdin)

db_indel=0
total_pass_indels=0
total_indels=0
for record in vcf_reader:

    if record.is_indel:
        total_indels+=1
        if record.FILTER == None:
            total_pass_indels +=1
            
            if record.ID != None:
                db_indel+=1

print "\t".join(["Total_indels", "PASS_INDELS", "PASS_INDEL_DBSNP"])
print "\t".join([str(total_indels), str(total_pass_indels), str(db_indel)])

