[[ -f ~/.bashrc ]] && source ~/.bashrc
echo in muscle
pwd

mamba activate cap2025_muscle

for i in {20..199};do
echo i 
ls -l group${i}*fasta | wc -l

cat<<EOF>"Muscle${i}.job"
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --qos=standby
#SBATCH --mem=8GB
#SBATCH --export=ALL
#SBATCH -t 72:00:00
#SBATCH --partition=msg,bus,physics,pws,m9pws,pws3,mkt24,m11-1,m11-2,m8,m8n,m9,m8g,m9g,paulbryf,bio,bep8

for file in group${i}*fasta; do muscle -super5 \$file -output \${file%fasta}afa; done;

EOF
sbatch "Muscle${i}.job"
cat "Muscle${i}.job"
rm "Muscle${i}.job"

done