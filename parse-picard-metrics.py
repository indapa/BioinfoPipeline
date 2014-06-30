#!/usr/bin/python
import sys
import os
import string
import re
from optparse import OptionParser
import itertools

""" parse a picard HsMetrics *.metrics output to something more human readable """
def main():
    usage = "usage: %prog [options] file.metrics\n\nparse a picard *.metrics output to something more human readable\n\n"

    parser = OptionParser(usage)
    #parser.add_option("--name", type="string|int|boolean", dest="name", help="help string")
    (options, args)=parser.parse_args()

    metricsfile=args[0]
    #assumping the metrics file is <samplename>.metrics.txt
    #just grab the sample name

    samplename=metricsfile.split('.')[0]


    fh=open(metricsfile, 'r')

    lines=fh.readlines()
    #filter out lines that start with # or are just new lines
    datalines=filter(lambda x: '#' not in x, lines)
    datalines=filter(lambda x: x!='\n' , datalines)
    #then strip newlines from the lines that contain data
    datalines=map(lambda x: x.strip() , datalines)

    #then a simplelines of code to make a dictionary and then print
    keys=datalines[0].split('\t')
    #print datalines[0]
    #print keys

    values=datalines[1].split('\t')
    #metrics_dict=dict(zip(keys,values))

    metrics_dict = dict(itertools.izip_longest(keys,values, fillvalue='NA'))

#print metrics_dict

    for k in keys:
        if k  == 'BAIT_SET': continue
        #if k == 'GENOME_SIZE': continue
        if metrics_dict[k] == 'NA': continue
        print "\t".join( [ k, metrics_dict[k], samplename ])


if __name__ == "__main__":
    main()
