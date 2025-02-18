[[ -f ~/.bashrc ]] && source ~/.bashrc
echo in fast blass
pwd

mamba activate cap2025_blast
subjectFileName=$1
echo $subjectFileName

dirToScripts=TEMP_INSTALL_LOCATION/clusteringScripts/blastScripts/

python ${dirToScripts}assignQueries.py $subjectFileName $2


for dir in blastJob*/;
do
cd $dir


 bash runSingleBlast.sh $subjectFileName

cd ..

done
