#$/bin/bash
#$ -V -cwd
#$ -l h_rt=48:00:00
#$ -pe smp 16
#$ -l h_vmem=6G
#$ -m be

module load openmpi/3.1.4
export ORIG=$PWD
export SCR=$TMPDIR #Provided by the system but not /scratch or /tmp. Assigned on a per job basis
cp GeometryOpt_parallel_HCoCO3CH2CH2.inp $SCR
cd $SCR
/apps/applications/orca/5.0.4/1/default/bin/orca GeometryOpt_parallel_HCoCO3CH2CH2.inp > GeometryOpt_parallel_HCoCO3CH2CH2,out
rm -f *.tmp
cp *.xyz *.hess *.out $ORIG
