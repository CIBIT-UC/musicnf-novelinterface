import os
import pandas as pd
import matplotlib.pyplot as plt


def settings():
    """
    Initialize and return a dictionary containing configuration settings for the project.

    Returns:
    - settings (dict): A dictionary with the following keys and values:
        - "bids_path" (str): Path to the BIDS dataset.
        - "derivatives_path" (str): Path to the derivatives folder.
        - "out_glm_path" (str): Path to the output folder for GLM results.
        - "out_glm_group_path" (str): Path to the output folder for group-level GLM results.
        - "git_path" (str): Path to the GitHub repository.
        - "space_label" (str): Label for the space used in the analysis.
        - "sub_labels" (list): List of subject labels.
        - "run_labels" (list): List of run labels.
        - "confounds_of_interest" (list): List of confound variables of interest.

    This function performs the following steps:
    1. Initializes an empty dictionary.
    2. Defines subject labels as a list of strings formatted as two-digit numbers from 01 to 22.
    3. Defines run labels as a list of strings ["1", "2"].
    4. Defines a list of confound variables of interest.
    5. Adds paths, labels, and confound variables to the dictionary.
    6. Returns the dictionary.
    """

    # inialize dictionary
    settings = {}

    sub_labels = [f"{i:02}" for i in range(1, 23)]

    run_labels = ["1", "2"]

    confounds_of_interest = [
        "csf",
        "white_matter",
        "trans_x",
        "trans_x_derivative1",
        "trans_x_power2",
        "trans_x_derivative1_power2",
        "trans_y",
        "trans_y_derivative1",
        "trans_y_power2",
        "trans_y_derivative1_power2",
        "trans_z",
        "trans_z_derivative1",
        "trans_z_derivative1_power2",
        "trans_z_power2",
        "rot_x",
        "rot_x_derivative1",
        "rot_x_power2",
        "rot_x_derivative1_power2",
        "rot_y",
        "rot_y_derivative1",
        "rot_y_power2",
        "rot_y_derivative1_power2",
        "rot_z",
        "rot_z_derivative1",
        "rot_z_power2",
        "rot_z_derivative1_power2",
    ]

    # add to dictionary
    settings["bids_path"] = "/Volumes/T7/BIDS-MUSICNF"
    settings["derivatives_path"] = "/Volumes/T7/BIDS-MUSICNF/derivatives/fmriprep24"
    settings["out_glm_path"] = "/Volumes/T7/BIDS-MUSICNF/derivatives/nilearn-glm"
    settings["out_glm_group_path"] = (
        "/Volumes/T7/BIDS-MUSICNF/derivatives/nilearn-glm-group"
    )
    settings["git_path"] = "/Users/alexandresayal/GitHub/musicnf-novelinterface"
    settings["space_label"] = "MNI152NLin2009cAsym"
    settings["sub_labels"] = sub_labels
    settings["run_labels"] = run_labels
    settings["tr"] = 1.5
    settings["confounds_of_interest"] = confounds_of_interest

    # set pandas settings
    # increase pandas column number display
    pd.set_option("display.max_columns", 500)
    pd.set_option("display.max_rows", 500)

    # set text font to Cabin
    plt.rcParams["font.family"] = "Cabin"

    return settings
