#!/bin/bash
#SBATCH --job-name=mcflirt_ieee
#SBATCH --output=mcflirt_ieee.out
#SBATCH --time=1:0:0
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=2G
#SBATCH --account=def-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mina.alizadeh94@gmail.com

module load apptainer/1.1

source /home/mina94/projects/def-glatard/mina94/ENV/bin/activate
parallel "bosh exec launch --imagepath container_images/vnmd_fsl_6.0.4-2021-04-22-ac3439c3920c.simg zenodo.2602109 ./{1}" ::: invocations_mc/ieee/*


