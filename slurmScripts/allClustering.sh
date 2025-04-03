# TODO ask payne if a slurm script works or if it should be more consolidated

if [ ! $2 ]; then
    echo provide the subjectFiles and the number of jobs to run
    exit 0
fi

#fastBlast.sh $1 $2
#sleep 50 # TODO: sleep 1000 for big jobs or sleep wc -l 
jobIDs=$(ls */*out | grep -oP "slurm.+t" | grep -oP "\d+")
jobIDs=$(echo $jobIDs | sed "s/ /,/g")

jobName=${1%.*}allClustering.job
cat<<EOF>$jobName
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=32GB
#SBATCH --export=ALL
#SBATCH -t 72:00:00
#SBATCH --partition=msg,bus,physics,pws,m9pws,pws3,mkt24,m11-1,m11-2,m8,m8n,m9,m8g,m9g,paulbryf,bio,bep8

[[ -f ~/.bashrc ]] && source ~/.bashrc
mamba activate cap2025_blast

# wait for fastBlast to finish this is because some jobs could have been preempted and still be running
while  squeue -u whoami -o "%.180j" | grep -q "\${1%.*}blastJob.job"; do
        sleep 10
done

concat from each output 
head -n 1 blastJob0/blastOut.tsv > cattedBlastOut.tsv
for dir in blastJob*/; do
	tail -n +2 \$dir/blastOut.tsv >> cattedBlastOut.tsv
done

# making blast groups and alignment
python TEMP_INSTALL_LOCATION/clusteringScripts/makeMuscleInputFiles.py $1 blastMSA 

cd blastMSA

runMuscle.sh

cd ..

# complete-linkage clustering and alignment
python TEMP_INSTALL_LOCATION/clusteringScripts/completeLinkageClustering.py cattedBlastOut.tsv

python TEMP_INSTALL_LOCATION/clusteringScripts/makeMuscleInputFiles.py $1 completeLinkageMSA 

cd completeLinkageMSA

runMuscle.sh

cd ..

# single-linkage clustering and alignment
python TEMP_INSTALL_LOCATION/clusteringScripts/singleLinkageClustering.py cattedBlastOut.tsv

python TEMP_INSTALL_LOCATION/clusteringScripts/makeMuscleInputFiles.py $1 singleLinkageMSA 

cd singleLinkageMSA

runMuscle.sh

cd ..

EOF
#sbatch $jobName
sbatch --dependency afterany:$jobIDs $jobName

