#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40
#SBATCH --exclusive
#SBATCH --mem=0
#SBATCH --job-name=job
#SBATCH --account=rrg-najmanov
#SBATCH --time=7-00:00:00




source ~/env/bin/activate

sh ./cmd.sh


