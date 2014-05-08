for x in /home/unix/aindap/REU-data/Research/LASERSeq/*.seq
do
fbname=$(basename $x .HGDP_938.seq)
#echo $x
#echo $fbname
#python pileup2seq/pileup2seq.py -m resources/HGDP/HGDP_938.site -o test NA12878.chrom22.pileup
#echo "/broad/software/free/Linux/redhat_5_x86_64/pkgs/python_2.7.1-sqlite3-rtrees/bin/python /home/unix/aindap/software/LASER-1.03/pileup2seq/pileup2seq.py -m /home/unix/aindap/software/LASER-1.03/resources/HGDP/HGDP_938.site -o $fbname $x" > $fbname.pileup_seq.sh

echo "/home/unix/aindap/software/LASER-1.03/laser -p /home/unix/aindap/software/LASER-1.03/laser.conf -s $x -g /home/unix/aindap/software/LASER-1.03/resources/HGDP/HGDP_938.geno -c /home/unix/aindap/software/LASER-1.03/resources/HGDP/HGDP_938.RefPC.coord -o $PWD/$fbname -k 10 -r 5" > $fbname.laser-run.sh

#echo "cp $fbname.* /home/unix/aindap/REU-data/Research/LASERuns/" >> $fbname.laser-run.sh
#echo "var=$(pwd)" >> $fbname.laser-run.sh
#echo "$var" >> $fbname.laser-run.sh
#./laser -s pileup2seq/test.seq  -g resource/HGDP/HGDP_938.geno -c resource/HGDP/HGDP_938.RefPC.coord -o test -k 2

done

