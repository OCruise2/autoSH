#Running in current environment and current directory
#$ -V -cwd

#Runtime - min 15 min, max 48 h
#$ -l h_rt=00:15:00

#Number of processors - MUST MATCH INPUT FILE - defaults to 1

#Requesting memory per core - 2GB is typically safe for normal sized basis sets
#$ -l h_vmem=1G

#Get email at start and end of job
#$ -m be

#Running the job itself
module load python/native

python test.py