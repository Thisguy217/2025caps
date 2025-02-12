# this file runs a distributed blast on a user determined number of slurm jobs

subjectFileName=$1
echo $subjectFileName
python /home/cazvash9/scripts/blastScripts/assignQueries.py $subjectFileName $2


for dir in blastJob*/;
do
cd $dir


runSingleBlast.sh $subjectFileName

cd ..

done
