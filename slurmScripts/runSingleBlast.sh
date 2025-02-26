
jobName=${1%.*}blastJob.job
subjectFileName=$1
cat<<EOF>$jobName
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=32GB
#SBATCH --qos=standby
#SBATCH --export=ALL
#SBATCH -t 48:00:00
#SBATCH --partition=msg,bus,physics,pws,m9pws,pws3,mkt24,m11-1,m11-2,m8,m8n,m9,m8g,m9g,paulbryf,bio,bep8


[[ -f ~/.bashrc ]] && source ~/.bashrc

pwd

mamba activate cap2025_blast

trap "echo trap triggered; runSingleBlast.sh $subjectFileName; exit" 15
python /home/cazvash9/scripts/blastScripts/blastWithRestart.py queries.fasta ../$subjectFileName &
wait

EOF
sbatch $jobName
