#!/bin/bash

## Before running, must see the following parameters:
# maximum value for k, parameter from k centers and k medoids 
MAX_K=1

# Full path of each python file with script
SCRIPTS=("../cluster/FromNewick.py" "../cluster/FromNewick_random.py")

# Names for each type of run, must match element by element with Scripts 
# For the naming of the output directory, leave underscore at the end 
DESCRIPTIONS=("kmedoids_pointcollect_" "kmedoids_random_")

index=0
START_LOC=$(pwd)

for PYTHON_PATH in $SCRIPTS
do
	
	TYPE=${DESCRIPTIONS[$index]}
	index=$(( $index + 1 ))
	
	# Create output directory for files 
	NOW=$(date +%Y-%m-%d:%H:%M:%S)
	OUTPUT_PATH="../newickData/$TYPE$NOW"
	mkdir $OUTPUT_PATH

	# Setup for run 
	PYTHON_FILE=$(basename $PYTHON_PATH)
	RUN_DIR=$(dirname $PYTHON_PATH)


	# Run specified method on each file for the tree of life data 
	INPUT_FILES=("$(echo ../TreeLifeData/*.newick)")
	cd $RUN_DIR
	for INPUT in $INPUT_FILES
	do
		BASE_FILE=$(basename $INPUT)
		echo "Currently working on file: $BASE_FILE"
		python $PYTHON_FILE $INPUT $MAX_K > "$OUTPUT_PATH/$BASE_FILE.out"
	done

	cd $START_LOC
done 