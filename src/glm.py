# Imports
import os
import numpy as np
import pandas as pd
from nilearn.glm.first_level import FirstLevelModel
from nilearn.plotting import plot_design_matrix
from src.my_settings import settings

# Load settings
settings = settings()


def firstlevel(settings, task_label, hp_hz, contrast_list, contrast_renamed_list):
    """
    Perform first-level GLM analysis on fMRI data for multiple subjects and runs.

    Parameters:
    - settings (dict): Configuration settings containing paths, labels, and other parameters.
    - task_label (str): Label for the task being analyzed.
    - hp_hz (float): High-pass filter cutoff frequency in Hz.
    - contrast_list (list): List of contrasts to be computed.
    - contrast_renamed_list (list): List of renamed contrasts for output filenames.

    Returns:
    None

    This function performs the following steps:
    1. Iterates over subjects specified in the settings.
    2. For each subject, iterates over runs specified in the settings.
    3. Loads functional images, event files, and confound files for each run.
    4. Preprocesses the event and confound data.
    5. Fits a first-level GLM model to the data.
    6. Plots and saves the design matrix for each run.
    7. Computes and saves contrast maps (z-score and effect size) for each contrast.
    """

    # Iterate over subjects
    for sub_label in settings["sub_labels"]:

        print(f"Processing subject {sub_label}")

        # define first level model
        model = FirstLevelModel(
            t_r=settings["tr"],
            noise_model="ar2",
            standardize=False,
            hrf_model="spm",
            drift_model="cosine",
            slice_time_ref=0.474,  # this value is specific to the acquisition parameters of the dataset
            high_pass=hp_hz,
        )

        func_img_list = []
        events_list = []
        confounds_list = []

        # Iterate on the runs
        for run_label in settings["run_labels"]:

            func_img = os.path.join(
                settings["derivatives_path"],
                f"sub-{sub_label}",
                "func",
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_space-{settings["space_label"]}_desc-preproc_bold.nii.gz",
            )

            events_tsv = os.path.join(
                settings["bids_path"],
                f"sub-{sub_label}",
                "func",
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_events.tsv",
            )

            # load as pandas dataframe
            events = pd.read_csv(events_tsv, sep="\t")

            # delete Discard and RestFinal rows
            events = events[events["trial_type"] != "Discard"]
            events = events[events["trial_type"] != "RestFinal"]

            confounds_tsv = os.path.join(
                settings["derivatives_path"],
                f"sub-{sub_label}",
                "func",
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_desc-confounds_timeseries.tsv",
            )

            # load as pandas dataframe
            confounds = pd.read_csv(confounds_tsv, sep="\t")

            # filter
            confounds = confounds[settings["confounds_of_interest"]]

            # fill NaNs with 0
            confounds = confounds.fillna(0)

            # normalize all confounds to have mean 0 and std 1
            confounds = (confounds - confounds.mean()) / confounds.std()

            # append to lists
            func_img_list.append(func_img)
            events_list.append(events)
            confounds_list.append(confounds)

        # fit model
        fmri_glm = model.fit(func_img_list, events_list, confounds_list)

        # plot and save design matrix
        for rr, run_label in enumerate(settings["run_labels"]):
            X1 = plot_design_matrix(
                fmri_glm.design_matrices_[rr],
                output_file=os.path.join(
                    settings["out_glm_path"],
                    f"sub-{sub_label}_task-{task_label}_run-{run_label}_design-matrix.png",
                ),
            )

        # estimate contrast maps
        for ii in range(len(contrast_list)):
            maps = fmri_glm.compute_contrast(contrast_list[ii], output_type="all")

            maps["z_score"].to_filename(
                os.path.join(
                    settings["out_glm_path"],
                    f"sub-{sub_label}_task-{task_label}_stat-z_con-{contrast_renamed_list[ii]}.nii.gz",
                )
            )
            maps["effect_size"].to_filename(
                os.path.join(
                    settings["out_glm_path"],
                    f"sub-{sub_label}_task-{task_label}_stat-beta_con-{contrast_renamed_list[ii]}.nii.gz",
                )
            )
