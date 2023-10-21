#!/bin/bash
#SBATCH --mem 4000 --time 6:0:0 

BASE_DIR=/project/def-mbarbeau/gnorris
PROJECT_DIR=${BASE_DIR}/Rockland_November_2020 

cd ${BASE_DIR}/ImageProcessing 
source setvars.sh

python preprocess.py -n773 -d${PROJECT_DIR}  -e772 \
-a 0.5326 0.5311 0.5291 0.5259 0.5282 0.5332 0.5316 0.5294 0.5284 0.5278 

