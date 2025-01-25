# dcm2bids
Some useful commands for converting DICOM files to BIDS format.

# Initialize folder structure with dcm2bids_scaffold before copying raw DICOM files
    mkdir /Volumes/T7/BIDS-MUSICNF
    cd /Volumes/T7/BIDS-MUSICNF
    dcm2bids_scaffold

# Copy raw DICOM files to sourcedata folder

bidsroot
    |-- sourcedata
        |-- 01
            |-- 01 (optional)
                |-- 01.dcm
                |-- 02.dcm
                |-- ...

# Run this bash command for each subject

    export subID=22

    dcm2bids \
    -d /Volumes/T7/BIDS-MUSICNF/sourcedata/$subID \
    -p $subID \
    -c /Volumes/T7/BIDS-MUSICNF/code/dcm2bids_config.json \
    -o /Volumes/T7/BIDS-MUSICNF

# Edit .jsons of the fmap files due to fmriprep legacy format for bids relative paths


# Clear dot files

    dot_clean -m /Volumes/T7/BIDS-MUSICNF