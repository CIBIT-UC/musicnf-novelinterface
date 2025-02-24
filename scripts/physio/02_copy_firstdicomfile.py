"""
This script copies the first DICOM file from a specified subject's DICOM folder to an output folder.

The script performs the following steps:
1. Defines the subject ID and name.
2. Constructs the path to the subject's DICOM folder.
3. Lists all folders in the DICOM folder.
4. If there is only one folder, updates the DICOM folder path to include this folder.
5. Sets the output folder path.
6. Lists all folders in the updated DICOM folder path.
7. Defines a list of protocol tasks.

Example:
For subject '22', the script will look for DICOM files in '/Volumes/T7/BIDS-MUSICNF/sourcedata/22' and copy the first DICOM file found to '/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/sub-22'.

Usage:
Simply run the script to copy the first DICOM file for the specified subject.
"""

import os

sub_id = "21"
sub_name = "sub-" + sub_id

dicom_folder = "/Volumes/T7/BIDS-MUSICNF/sourcedata/" + sub_id

# find all folders in dicom folder
folders = os.listdir(dicom_folder)

if len(folders) == 1:
    dicom_folder = os.path.join(dicom_folder, folders[0])

# set output folder
output_folder = "/Volumes/T7/BIDS-MUSICNF/derivatives/physio-raw/" + sub_name

# find all folders in dicom folder
folders = os.listdir(dicom_folder)

protocol_task_list = [
    "Active_NF_Run1_AP",
    "Active_NF_Run2_AP",
    "Loc_Run1_AP",
    "Sham_NF_Run1_AP",
    "Sham_NF_Run2_AP",
]

task_list = [
    "task-nf_run-1",
    "task-nf_run-2",
    "task-loc_run-1",
    "task-sham_run-1",
    "task-sham_run-2",
]

# copy the first file in the folder dicom_folder/task to output_folder with the name subname_task-taskname_run-1_firstvol.dcm
for task in protocol_task_list:
    # find the correct folder
    task_folder = [folder for folder in folders if task in folder]

    if len(task_folder) == 1:
        task_folder = os.path.join(dicom_folder, task_folder[0])
    else:
        continue

    # find all files in the task folder
    files = os.listdir(task_folder)

    # ignore all files that start with a dot
    files = [file for file in files if not file.startswith(".")]

    # sort the files
    files.sort()

    # find the first file
    first_file = files[0]

    # copy the first file to the output folder
    new_name = (
        sub_name + "_" + task_list[protocol_task_list.index(task)] + "_firstvol.dcm"
    )
    os.system(
        "cp "
        + os.path.join(task_folder, first_file)
        + " "
        + os.path.join(output_folder, new_name)
    )
