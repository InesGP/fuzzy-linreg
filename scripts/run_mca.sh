#!/bin/bash
#SBATCH --job-name=flirt_mca
#SBATCH --output=flirt_mca_%a.out
#SBATCH --time=1:0:0
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=2G
#SBATCH --account=def-glatard
#SBATCH --array=5
#SBATCH --mail-type=ALL
#SBATCH --mail-user=inesgp99@gmail.com

source /home/ine5/projects/def-glatard/ine5/pytorch/bin/activate

module load apptainer/1.1

#MCA
parallel "bosh exec launch --imagepath /scratch/ine5/fuzzy_fsl_flirt.sif flirt-fuzzy.json ./{1}" ::: invocations/anat-12dofs/mca/${SLURM_ARRAY_TASK_ID}/*
# parallel "bosh exec launch --imagepath container_images/vnmd_fsl_6.0.4-2021-04-22-ac3439c3920c.simg descriptors/flirt.json ./{1}" ::: invocations/ieee/*

