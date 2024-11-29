import os
import numpy as np
import pandas as pd
from nilearn.image import math_img


def apply_mask(image_path, mask_path):
    """
    Apply a binary mask to a NIfTI image using FSL's fslmaths tool.

    Parameters:
    - image_path (str): Path to the input NIfTI image file.
    - mask_path (str): Path to the binary mask NIfTI image file.

    Returns:
    - out_path (str): Path to the output masked NIfTI image file.

    This function performs the following steps:
    1. Constructs the output file path by appending '_masked' to the input image file name.
    2. Constructs the fslmaths command to apply the mask to the input image.
    3. Executes the fslmaths command using the os.system function.
    4. Returns the path to the output masked image file.

    Example:
    >>> masked_image = apply_mask("subject01.nii.gz", "mask.nii.gz")
    >>> print(masked_image)
    "subject01_masked.nii.gz"
    """
    out_path = image_path.replace("_bold.nii.gz", "masked_bold.nii.gz")
    cmd = f"fslmaths {image_path} -mas {mask_path} {out_path}"
    os.system(cmd)
    return out_path


def generate_brainnetome_mask(
    bn_path, roi_string, export_flag=False, output_name="brainnetome_mask"
):
    """
    Generates a brain mask from the Brainnetome Atlas based on a region of interest (ROI) string.

    Parameters:
    bn_path (str): The file path to the Brainnetome Atlas directory.
    roi_string (str): The string to search for in the atlas labels to identify regions of interest.
    export_flag (bool, optional): If True, the generated mask will be saved to a file. Default is False.
    output_name (str, optional): The name of the output file if export_flag is True. Default is "brainnetome_mask".

    Returns:
    nibabel.Nifti1Image: The generated brain mask as a Nifti image.
    """

    atlas = os.path.join(bn_path, "BN_Atlas_246_1mm.nii.gz")
    atlas_labels = os.path.join(bn_path, "BN_Atlas_Labels_cleaned.tsv")

    df = pd.read_csv(atlas_labels, sep="\t")

    # get label_id for all that contain the roi_string
    labels = df[df["Description_Short"].str.contains(roi_string, case=True)][
        "Label_ID"
    ].tolist()

    print(f"Found labels for {roi_string}: {labels}")

    # create a mask for each label and combine them
    mask = None
    for label in labels:
        if mask is None:
            mask = math_img(f"img == {label}", img=atlas)
        else:
            mask = math_img(
                "img1 + img2", img1=mask, img2=math_img(f"img == {label}", img=atlas)
            )

    if export_flag:
        mask.to_filename(f"{output_name}.nii.gz")

    return mask


def parse_prt_file(file_path):
    """
    Parse a PRT (Protocol) file and extract condition intervals.

    Parameters:
    - file_path (str): Path to the PRT file to be parsed.

    Returns:
    - conditions (dict): A dictionary where keys are condition names (str) and values are numpy arrays of intervals.
      Each interval is represented as a 2D array with onset and offset times.

    This function performs the following steps:
    1. Opens and reads the PRT file line by line.
    2. Skips non-relevant lines based on predefined keywords.
    3. Identifies condition names and reads their corresponding onset and offset intervals.
    4. Stores the intervals in a dictionary with condition names as keys.

    Example:
    >>> conditions = parse_prt_file("path/to/file.prt")
    >>> print(conditions)
    {'Condition1': array([[0, 10], [20, 30]]), 'Condition2': array([[40, 50]])}
    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    conditions = {}
    current_condition = None
    reading_intervals = False

    for line in lines:
        line = line.strip()

        # Skip non-relevant lines
        if any(
            line.startswith(keyword)
            for keyword in [
                "FileVersion",
                "ResolutionOfTime",
                "Experiment",
                "BackgroundColor",
                "TextColor",
                "TimeCourseColor",
                "TimeCourseThick",
                "ReferenceFuncColor",
                "ReferenceFuncThick",
                "NrOfConditions",
                "ResponseConditions",
            ]
        ):
            continue

        if reading_intervals:
            if line.startswith("Color:"):
                # Finished reading intervals for the current condition
                reading_intervals = False
                continue
            elif line:
                # Attempt to read onset and offset
                try:
                    onset, offset = map(int, line.split()[:2])
                    conditions[current_condition] = np.append(
                        conditions[current_condition], [[onset, offset]], axis=0
                    )
                except ValueError:
                    # If line does not contain two integer values, skip it
                    continue
            continue

        if line.isdigit():
            # Number of intervals, not used directly here
            continue

        if line:
            # Condition name
            current_condition = line
            conditions[current_condition] = np.empty((0, 2), int)
            reading_intervals = True

    conditions_list = list(conditions.keys())

    return conditions, conditions_list


## Define function to get the sequence, conditions, and durations and export the events TSV file
def seq2tsv(sequence, conditions, duration_percondition, output_file_path):

    # initialize
    onsets = []
    durations = []
    trial_type = []

    # build onsets, durations, and trial_type lists
    currentTime = 0
    for ii in range(len(sequence)):
        onsets.append(currentTime)
        durations.append(duration_percondition[sequence[ii]])
        trial_type.append(conditions[sequence[ii]])
        currentTime += durations[sequence[ii]]

    # create events dataframe
    events = pd.DataFrame(
        {
            "onset": onsets,
            "duration": durations,
            "trial_type": trial_type,
        }
    )

    # save events dataframe to file
    events.to_csv(output_file_path, sep="\t", index=False)
