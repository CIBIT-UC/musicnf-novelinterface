"""
This script renames physiological data files for a specific subject in a BIDS dataset.

The script performs the following steps:
1. Defines the subject name and input folder path.
2. Lists all files in the input folder.
3. Filters out files that start with a dot (hidden files).
4. Loops through the remaining files and renames them based on their suffix.

File Renaming Rules:
- Files ending with 'AC1.puls' are renamed to '<sub_name>_task-nf_run-1.puls'.
- Files ending with 'AC2.puls' are renamed to '<sub_name>_task-nf_run-2.puls'.
- Files ending with 'SH1.puls' are renamed to '<sub_name>_task-sham_run-1.puls'.
- Files ending with 'SH2.puls' are renamed to '<sub_name>_task-sham_run-2.puls'.
- Files ending with 'LOC.puls' are renamed to '<sub_name>_task-loc_run-1.puls'.

The file names are not always consistent, so this is just a helper function.

Example:
For subject 'sub-15', the file 'AC1.puls' will be renamed to 'sub-15_task-nf_run-1.puls'.

Usage:
Simply run the script to rename the files in the specified input folder.
"""

import os

sub_name = "sub-21"

input_folder = "/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/" + sub_name

# find all files in the input folder
files = os.listdir(input_folder)

# ignore all files that start with a dot
files = [file for file in files if not file.startswith(".")]

# loop through all files
for file in files:
    # check if the file is a .tsv file
    if file.endswith("AC1.puls") or file.endswith("ACT1.puls"):
        # rename to subname_task-nf_run-1.puls
        new_name = sub_name + "_task-nf_run-1.puls"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("AC1.resp") or file.endswith("ACT1.resp"):
        # rename to subname_task-nf_run-1.resp
        new_name = sub_name + "_task-nf_run-1.resp"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("AC2.puls") or file.endswith("ACT2.puls"):
        # rename to subname_task-nf_run-2.puls
        new_name = sub_name + "_task-nf_run-2.puls"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("AC2.resp") or file.endswith("ACT2.resp"):
        # rename to subname_task-nf_run-2.resp
        new_name = sub_name + "_task-nf_run-2.resp"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("SH1.puls"):
        # rename to subname_task-sham_run-1.puls
        new_name = sub_name + "_task-sham_run-1.puls"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("SH1.resp"):
        # rename to subname_task-sham_run-1.resp
        new_name = sub_name + "_task-sham_run-1.resp"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("SH2.puls"):
        # rename to subname_task-sham_run-2.puls
        new_name = sub_name + "_task-sham_run-2.puls"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("SH2.resp"):
        # rename to subname_task-sham_run-2.resp
        new_name = sub_name + "_task-sham_run-2.resp"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("LOC.puls"):
        # rename to subname_task-loc_run-1.puls
        new_name = sub_name + "_task-loc_run-1.puls"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )

    if file.endswith("LOC.resp"):
        # rename to subname_task-loc_run-1.resp
        new_name = sub_name + "_task-loc_run-1.resp"
        os.rename(
            os.path.join(input_folder, file), os.path.join(input_folder, new_name)
        )
