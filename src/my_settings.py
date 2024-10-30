import os


def settings():

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
    settings["space_label"] = "MNI152NLin2009cAsym"
    settings["sub_labels"] = sub_labels
    settings["run_labels"] = run_labels
    settings["tr"] = 1.5
    settings["confounds_of_interest"] = confounds_of_interest

    return settings
