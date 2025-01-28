
# Setup udocker container at INCD
    udocker pull nipreps/fmriprep:24.1.1
    srun -p hpc --job-name "my_interactive" --pty bash -i
    udocker create --name=fmriprep2411 nipreps/fmriprep:24.1.1
    udocker setup --execmode=S1 fmriprep2411

# Run fmriprep

    sbatch code/fmriprep.sh
