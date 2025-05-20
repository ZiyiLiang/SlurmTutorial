#!/bin/bash

# Parameters
SEED_LIST=$(seq 1 10)  # Run for seeds 1 to 10

# Slurm parameters
MEMO=100M                           # Memory required (100 MB)
TIME=00-00:10:00                    # Time required (10 minutes)
CORE=1                              # Cores required (1)

# Assemble order
ORDP="sbatch --mem=$MEMO --nodes=1 --ntasks=1 --cpus-per-task=$CORE --time=$TIME --partition=biodatascience.p"

# Create directory for log files
LOGS="logs/classification"
OUT_DIR="results/classification"

mkdir -p $LOGS
mkdir -p $OUT_DIR

comp=0
incomp=0

for SEED in $SEED_LIST; do
    JOBN="classification_seed$SEED"
    OUT_FILE="$OUT_DIR/classification_results_seed$SEED.txt"
    COMPLETE=0
    
    if [[ -f $OUT_FILE ]]; then
        COMPLETE=1
        ((comp++))
    fi

    if [[ $COMPLETE -eq 0 ]]; then
        ((incomp++))
        # Script to be run
        SCRIPT="exp.sh $SEED"
        # Define job name
        OUTF="$LOGS/$JOBN.out"
        ERRF="$LOGS/$JOBN.err"
        # Assemble slurm order for this job
        ORD="$ORDP -J $JOBN -o $OUTF -e $ERRF $SCRIPT"
        # Print order
        echo $ORD
        # Submit order
        $ORD
    fi
done

echo "Jobs already completed: $comp, submitted unfinished jobs: $incomp"