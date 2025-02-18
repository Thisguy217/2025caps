
jobName=FIXMEblast.job
subjectFileName=$1
cat<<EOF>$jobName
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4GB
#SBATCH --qos=standby
#SBATCH --export=ALL
#SBATCH -t 48:00:00
#SBATCH --partition=msg,bus,physics,pws,m9pws,pws3,mkt24,m11-1,m11-2,m8,m8n,m9,m8g,m9g,paulbryf,bio,bep8

echo current dir
pwd

trap "echo trap triggered; runSingleBlast.sh; exit" 15
python /home/cazvash9/scripts/blastScripts/blastWithRestart.py queries.fasta ../$subjectFileName &
wait

EOF
sbatch $jobName
