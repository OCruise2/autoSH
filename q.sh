#Running in current environment and current directory
#$ -V -cwd

#Runtime - min 15 min, max 48 h
#$ -l h_rt=12:00:00

#Number of processors - MUST MATCH INPUT FILE
#$ -pe smp 2

#Requesting memory per core - 3GB is typically safe for normal sized basis sets
#$ -l h_vmem=3G

#Get email at start and end of job
#$ -m be

#Running the job itself
module load openmpi/3.1.4

export orcadir=/apps/applications/orca/5.0.4/1/default/bin/

$orcadir/orca B3LYP_OPT_2-4-dichloropyridine.inp > B3LYP_OPT_2-4-dichloropyridine.out