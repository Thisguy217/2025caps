if [ ! $2 ]; then
    echo provide the subjectFiles and the number of jobs to run
    exit 0
fi


[[ -f ~/.bashrc ]] && source ~/.bashrc
echo in fast blass
pwd

mamba activate cap2025_blast
subjectFileName=$1
echo $subjectFileName

dirToScripts=/home/cazvash9/2025capsInited/clusteringScripts/blastScripts/

python ${dirToScripts}assignQueries.py $subjectFileName $2


for dir in blastJob*/;
do
cd $dir


 bash runSingleBlast.sh $subjectFileName

cd ..

done
