#$/bin/bash
#$ -V -cwd
#$ -l h_rt=48:00:00
#$ -pe smp 16
#$ -l h_vmem=3G
#$ -m be

module load openmpi/3.1.4
export ORIG=$PWD
export SCR=$TMPDIR #Provided by the system but not /scratch or /tmp. Assigned on a per job basis
cp hydride_transfer_scan.inp $SCR
cd $SCR
/apps/applications/orca/5.0.4/1/default/bin/orca hydride_transfer_scan.inp > hydride_transfer_scan,out
rm -f *.tmp
cp *.xyz *.hess *.out $ORIG
