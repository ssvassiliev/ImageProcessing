#!/bin/bash
#SBATCH -c20 --mem-per-cpu=4000 --time 24:0:0 

WORKDIR=`pwd -P`
PROJECT_NAME=Rockland_November_2020

module load apptainer
apptainer run -C -B ${WORKDIR}:/datasets --writable-tmpfs ODM-10b.sif \
--orthophoto-resolution 7.0 \
--primary-band Green \
--dem-resolution 10 \
--skip-3dmodel \
--feature-quality ultra \
--feature-type hahog \
--pc-quality high \
--mesh-octree-depth 12 \
--mesh-size 400000 \
--min-num-features 100000 \
--radiometric-calibration none \
--max-concurrency ${SLURM_CPUS_PER_TASK} \
--project-path /datasets ${PROJECT_NAME} \
--rerun-all
