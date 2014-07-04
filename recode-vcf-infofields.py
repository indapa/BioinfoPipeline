#!/usr/bin/env python
import sys
import os
import argparse
import vcf
import numpy as np


""" given a VCF file update the AC AN AF fields """
def main():

    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='update the AC AN AF fields of a VCF file')
    parser.add_argument('vcfile',  type=str,help='*.vcf.gz file')
    args=parser.parse_args()


    vcf_reader = vcf.Reader(open(args.vcfile, 'r'))
    vcf_writer = vcf.Writer(open('/dev/stdout', 'w'), vcf_reader)
    for record in vcf_reader:
        #print record.INFO
        #print "num called " + str(record.num_called)
        #print "num het: " + str(record.num_het)
        #print "num hom_alt " + str(record.num_hom_alt)
        #print "num hom_ref " + str(record.num_hom_ref)
        #print "aaf " + str(record.aaf)
        new_an = (2*record.num_called)
        new_ac = (2*record.num_hom_alt) + record.num_het



        record.INFO['AC']=new_ac
        record.INFO['AN']=new_an
        record.INFO['AF']=record.aaf
        record.INFO['CCC']=new_an

        #print record.INFO


        new_site_dp =sum ( [ call.data.DP for call in record.samples if call.called ==True and call.data.DP  ] )
        new_site_gq_mean= round(np.mean([ call.data.GQ for call in record.samples if call.called ==True ]),2)
        new_site_gq_stdev= round(np.std([ call.data.GQ for call in record.samples if call.called ==True ]),2)

        total_samples=len([call.sample for call in record.samples])
        new_ncc=total_samples - new_an

        #print total_samples
        record.INFO['NCC']= new_ncc
        record.INFO['DP']= new_site_dp
        record.INFO['GQ_MEAN']=new_site_gq_mean
        record.INFO['GQ_STDDEV'] = new_site_gq_stdev

        vcf_writer.write_record(record)
        #break


if __name__ == "__main__":
    main()
