#!/bin/bash

set -e

echo $PWD
ls 

if [ ! -d "${INPUT_ARTIFACTS}" ]; then
    printf "${INPUT_ARTIFACTS} does not exist\n"
    exit
fi

# Repository name
repository_name=$(basename ${PWD})
printf "Repository name is ${repository_name}\n"

if [ -z "${INPUT_REPO}" ]; then
    INPUT_REPO=${INPUT_REPOSITORY}
fi

# If we don't have the docs directory yet, copy it there
if [ ! -d "${INPUT_DOCS}" ]; then
    printf "Output directory ${INPUT_DOCS} does not exist yet, copying...\n"
    cp -R ${ACTION_PATH}/docs ${INPUT_DOCS}

   # Ensure repository and baseurl at top of _config
   sed -i "1irepository: ${INPUT_REPO}" ${INPUT_DOCS}/_config.yml
   sed -i "1ibaseurl: /${repository_name}" ${INPUT_DOCS}/_config.yml
   cat ${INPUT_DOCS}/_config.yml

fi

if [ -z "${INPUT_EXPERIMENT}" ]; then 
    printf "Experiment directory is not set, will look over all directories under ${INPUT_ARTIFACTS}\n"
    for dirname in $(ls ${INPUT_ARTIFACTS}); do
        printf "python visualize-predictions.py artifacts/$dirname\n"
        python ${ACTION_PATH}/scripts/visualize-predictions.py ${INPUT_ARTIFACTS}/$dirname
    done   
else 

    # Make sure experiment directory exists first
    dirname=${INPUT_ARTIFACTS}/${INPUT_EXPERIMENT}
    printf "Looking for directory ${dirname}\n"
    if [ ! -d "{dirname}" ]; then
        printf "${dirname} does not exist\n"
        exit
    fi

    printf "python visualize-predictions.py ${INPUT_ARTIFACTS}/${INPUT_EXPERIMENT}\n"
    python ${ACTION_PATH}/scripts/visualize-predictions.py ${INPUT_ARTIFACTS}/${INPUT_EXPERIMENT}
fi
