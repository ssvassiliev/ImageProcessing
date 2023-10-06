#!/bin/bash
#SBATCH -c1 --mem-per-cpu=4000 --time 3:0:0 -A def-svassili

module load apptainer
apptainer overlay create --fakeroot --size 3000 ${SLURM_TMPDIR}/ClusterODM.ovl
srun apptainer run --fakeroot --overlay ${SLURM_TMPDIR}/ClusterODM.ovl  ClusterODM.sif &
wait

