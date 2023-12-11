#!/bin/bash
#SBATCH --job-name=flirt_mca
#SBATCH --output=flirt_mca.out
#SBATCH --time=2:0:0
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=2G
#SBATCH --account=def-glatard
#SBATCH --mail-type=ALL
#SBATCH --mail-user=inesgp99@gmail.com
#SBATCH --array=1-10

source /home/ine5/projects/def-glatard/ine5/pytorch/bin/activate

module load apptainer/1.1

#MCA
parallel "time bosh exec launch --imagepath container_images/glatard_fsl_6.0.4_fuzzy-2023-12-08-a22e376466e7.simg descriptors/flirt-fuzzy.json ./{1}" ::: invocations/mca/${SLURM_ARRAY_TASK_ID}/*


