#!/bin/bash

eval "$(conda shell.bash hook)"

module load slurm
conda activate fusion

python3 exp.py $1