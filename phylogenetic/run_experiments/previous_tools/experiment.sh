#!/bin/bash

## Before running, must see the following parameters:
# maximum value for k, parameter from k centers and k medoids 
MAX_K=4

# Full path of each python file with script
#SCRIPTS=("../cluster/FromNewick.py" "../cluster/FromNewick_random.py" "../cluster/k_centers.py")
PYTHON_PATH="../cluster/k_centers.py"


# Names for each type of run, must match element by element with Scripts 
# For the naming of the output directory, leave underscore at the end 
#DESCRIPTIONS=("kmedoids_pointcollect_" "kmedoids_random_" "kcenters_")
TYPE="kcenters_"

START_LOC=$(pwd)
INPUT_FILES=("$(echo ../TreeLifeData_small/*.newick)")


#for index in ${!SCRIPTS[*]}
#do

#PYTHON_PATH=${SCRIPTS[$index]}
#TYPE=${DESCRIPTIONS[$index]}
echo "Running: $TYPE"
echo "For file: $PYTHON_PATH"
	
# Create output directory for files 
NOW=$(date +%Y-%m-%d:%H:%M:%S)
OUTPUT_PATH="../newickData/$TYPE$NOW"
mkdir $OUTPUT_PATH

# Setup for run
PYTHON_FILE=$(basename $PYTHON_PATH)
RUN_DIR=$(dirname $PYTHON_PATH)

# Run specified method on each file for the tree of life data
cd $RUN_DIR
for INPUT in $INPUT_FILES
do
    BASE_FILE=$(basename $INPUT)
    echo "Currently working on file: $BASE_FILE"
    python $PYTHON_FILE $INPUT $MAX_K > "$OUTPUT_PATH/$BASE_FILE.out"
done

cd $START_LOC

#done 
