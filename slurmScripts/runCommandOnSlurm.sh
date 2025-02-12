command=$1
JobSub=$command
if [[ $2 ]]; then
    numTasks=$2
else
    numTasks=1
fi

if [[ $3 ]]; then
    mem=$3
else
    mem=4
fi
cat<<EOF>"$command runcommand.job"
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=$numTasks
#SBATCH --qos=standby
#SBATCH --mem=${mem}GB
#SBATCH --export=ALL
#SBATCH -t 72:00:00
#SBATCH --partition=msg,bus,physics,pws,m9pws,pws3,mkt24,m11-1,m11-2,m8,m8n,m9,m8g,m9g,paulbryf,bio,bep8

eval "$command"

EOF
sbatch "$command runcommand.job"
cat "$command runcommand.job"
rm "$command runcommand.job"

