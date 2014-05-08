for x in /home/unix/aindap/REU-data/Research/LASERPileups/*.pileup
do
fbname=$(basename $x .pileup)
#echo $fbname
#python pileup2seq/pileup2seq.py -m resources/HGDP/HGDP_938.site -o test NA12878.chrom22.pileup
echo "/broad/software/free/Linux/redhat_5_x86_64/pkgs/python_2.7.1-sqlite3-rtrees/bin/python /home/unix/aindap/software/LASER-1.03/pileup2seq/pileup2seq.py -m /home/unix/aindap/software/LASER-1.03/resources/HGDP/HGDP_938.site -o $fbname $x" > $fbname.pileup_seq.sh



done

