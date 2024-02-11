#!/bin/bash
#SBATCH --job-name=flirt_ieee
#SBATCH --output=flirt_ieee.out
#SBATCH --time=1:0:0
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=2G
#SBATCH --account=def-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=inesgp99@gmail.com

source /home/ine5/projects/def-glatard/ine5/pytorch/bin/activate

module load apptainer/1.1

#IEEE
parallel "bosh exec launch --imagepath container_images/vnmd_fsl_6.0.4-2021-04-22-ac3439c3920c.simg descriptors/flirt.json ./{1}" ::: invocations/ieee/*


