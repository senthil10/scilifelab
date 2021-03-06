import sys
from bcbio.pipeline.config_loader import load_config
if len(sys.argv) < 6:
    print """
Usage:

make_complexity_plots.py  <sample_name> <mail> <config_file> <path> <order_num> <single_end>

        sample_name		This name: /tophat_out_<sample name>
        mail            eg: jun.wang@scilifelab.se
        config_file     post_process.yaml assumes that you have specified samtools
                        version under 'custom_algorithms'/'RNA-seq analysis'
        path            Path to analysis dir containing the tophat_out_ directories
        order_num       Millions of ordered number of reads
    	single_end		For single end runs (-e)
        """
    sys.exit()

name            = sys.argv[1]
mail            = sys.argv[2]
config_file     = sys.argv[3]
path            = sys.argv[4]
order_num       = sys.argv[5]
extrap          = int(2*1000000*float(order_num))

try:
    config  = load_config(config_file)
    extra_arg = config['sbatch']['extra_arg']
    tools   = config['custom_algorithms']['RNA-seq analysis']
    bam     = tools['bamtools']+'/'+tools['bamtools_version']
    bed     = tools['BEDTools']+'/'+tools['BEDTools_version']
    preseq  = tools['Preseq']+'/'+tools['Preseq_version']
except:
    print 'ERROR: problem loading tools version from config file'


f=open("complexity_"+name+".sh",'wa')

##### {0}: sample name, {1}: email address, {2}: preseq, {3}: bamtools  #####
##### {4}: full path to analysis dir., {5}: --qos=seqver, {6}: BEDTools #####
print >>f, """#!/bin/bash -l
#SBATCH -A a2012043
#SBATCH -p core -n 3
#SBATCH -t 40:00:00
#SBATCH -e complexity_{0}.err
#SBATCH -o complexity_{0}.out
#SBATCH -J complexity_{0}
#SBATCH --mail-type=ALL
#SBATCH --mail-user={1}
#SBATCH {5}

module load bioinfo-tools
module load {6}
module load {3}
module load {2}
cd {4}
""".format(name, mail, preseq, bam, path, extra_arg, bed)

if len(sys.argv)==6 or sys.argv[6]!='-e':
	print >>f, """bedtools bamtobed -i tophat_out_{0}/accepted_hits_sorted_{0}.bam | sort -k 1,1 -k 2,2n -k 6,6 >tophat_out_{0}/accepted_hits_sorted_preseq_{0}.bed
preseq lc_extrap -e {1} -P -v -o tophat_out_{0}/{0}.ccurve.txt tophat_out_{0}/accepted_hits_sorted_preseq_{0}.bed
	""".format(name, extrap)
elif len(sys.argv)>6 and sys.argv[6]=='-e':
	print >>f, """preseq lc_extrap -e {1} -v -B tophat_out_{0}/accepted_hits_sorted_{0}.bam -o tophat_out_{0}/{0}.ccurve.txt
	""".format(name, extrap)

f.close()
