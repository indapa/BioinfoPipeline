#!/usr/bin/env python
import sys
import os
import argparse
from PedPy import Ped, Pedfile

def main():
    """ we generated a tped and binary plink file from a VCF file via vcftools based on this:
        https://gist.github.com/arq5x/2378903
        The VCF doesn't contain family relationships in the header and we should adjust this
        by adjusting the family relations in the plink derived fam file from a master pedfile
        with the correct FIDs,MIDs, PIDs gender and affected status """

    usage = "usage: %prog [options]  "
    parser = argparse.ArgumentParser(description='Program description')
    parser.add_argument('-masterped', dest='masterped', type=str, help="master ped file")
    parser.add_argument('plinkped',  type=str,help='plink generated ped file')

    args=parser.parse_args()

    masterpedobj=Pedfile(args.masterped)
    masterpedobj.parsePedfile()

    plinkpedobj=Pedfile(args.plinkped)
    plinkpedobj.parsePedfile()

    """
    Read the ped informat from the master ped
    Read the individual ped objects in a dictonary, keyed by the individual id

    """
    pedlist=masterpedobj.getPedList()
    masterpeddict={}
    for p in pedlist:
        pheno=p.getpheno()
        if int(pheno) != -9:
            p.setpheno( str(int(pheno)+1))

        masterpeddict[p.getid()]=p

    for p in plinkpedobj.getPedList():
        #print p


        iid=p.getid()
        newpedobj=None
        if iid in masterpeddict.keys():
            newpedobj=masterpeddict[iid]
        else:
            sys.stderr.write(iid + " not in masterped!\n")
            #print p
            newpedobj=p

        print newpedobj
        #print newpedobj





if __name__ == "__main__":
    main()
