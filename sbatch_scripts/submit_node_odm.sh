#!/bin/bash
#SBATCH -c10 --mem-per-cpu=4000 --time 3:0:0 -A def-svassili
#SBATCH --mail-user=serguei.vassiliev@ace-net.ca
#SBATCH --mail-type=BEGIN

module load apptainer
apptainer overlay create --fakeroot --size 32000 ${SLURM_TMPDIR}/NodeODM.ovl
srun  apptainer run --fakeroot --overlay ${SLURM_TMPDIR}/NodeODM.ovl NodeODM.sif &
wait
