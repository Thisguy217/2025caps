# creates mamba environments

scriptRelativeDir=/slurmScripts/

bashProfilePath=~/.bash_profile
bashRCPath=~/.bashrc


force=false
if [[ $* == *-f* ]]; then
   echo forced
   force=true
else
   echo not forced
fi



#add mamba import
if ( ! cat $bashRCPath | grep -q "conda\|mamba" ) || ( $force == true ) ; 
then
    echo added mamba import to bashrc
    
    cat >> $bashRCPath << end

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="\$('/apps/miniconda3/latest/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ \$? -eq 0 ]; then
    eval "\$__conda_setup"
else
    if [ -f "/apps/miniconda3/latest/etc/profile.d/conda.sh" ]; then
        . "/apps/miniconda3/latest/etc/profile.d/conda.sh"
    else
        export PATH="/apps/miniconda3/latest/bin:\$PATH"
    fi
fi
unset __conda_setup

if [ -f "/apps/miniconda3/latest/etc/profile.d/mamba.sh" ]; then
    . "/apps/miniconda3/latest/etc/profile.d/mamba.sh"
fi
# <<< conda initialize <<<
end

else
    echo not added mamba import to bashrc
fi

exportCall="export PATH=\$PATH:$(pwd)$scriptRelativeDir"
if ( ! cat $bashProfilePath| grep -q "$exportCall" ) || ( $force == true ) ; 
then
    echo "\n$exportCall" >> $bashProfilePath
    echo updated path to bashprofile
else
    echo not updated path to bashprofile
fi


# TODO: check if necessary
# add a manual bashrc call to bash profile; I don't know why this isn't already called
bashRCCall="[[ -f ~/.bashrc ]] && source ~/.bashrc"
if ( ! cat $bashProfilePath| grep -q "$bashRCCall" ) || ( $force == true ) ; 
then
    echo "\n$bashRCCall" >> $bashProfilePath
    echo added bash call to bashprofile
else
    echo not added bashrc call to bashprofile
fi

chmod a+x .${scriptRelativeDir}* # make executable

source "$bashProfilePath"

mamba create -n cap2025_blast pandas bioconda::blast
mamba create -n cap2025_muscle bioconda::muscle