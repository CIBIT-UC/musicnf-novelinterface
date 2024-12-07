# Imports
import os
import glob
import numpy as np
import pandas as pd
from nilearn.glm.first_level import FirstLevelModel
from nilearn.glm.second_level import SecondLevelModel
from nilearn.plotting import plot_design_matrix
from src.my_settings import settings


def firstlevel(
    settings,
    task_label,
    hp_hz,
    contrast_list,
    contrast_renamed_list,
    use_masked_data=False,
):
    """
    Perform first-level GLM analysis on fMRI data for multiple subjects and runs.

    Parameters:
    - settings (dict): Configuration settings containing paths, labels, and other parameters.
    - task_label (str): Label for the task being analyzed.
    - hp_hz (float): High-pass filter cutoff frequency in Hz.
    - contrast_list (list): List of contrasts to be computed.
    - contrast_renamed_list (list): List of renamed contrasts for output filenames.
    - use_masked_data (bool): If True, use masked data for the analysis. Default is False.

    Returns:
    None

    This function performs the following steps:
    1. Iterates over subjects specified in the settings.
    2. For each subject, iterates over runs specified in the settings.
    3. Loads functional images, event files, and confound files for each run.
    3.1. If physio data is available, it is also loaded and added to the confound data.
    4. Preprocesses the event and confound data.
    5. Fits a first-level GLM model to the data.
    6. Plots and saves the design matrix for each run.
    7. Computes and saves contrast maps (z-score and effect size) for each contrast.
    """

    if use_masked_data:
        masked_string = "preprocmasked"
    else:
        masked_string = "preproc"

    # Iterate over subjects
    for sub_label in settings["sub_labels"]:

        print(f"Processing subject {sub_label}")

        # define first level model
        model = FirstLevelModel(
            t_r=settings["tr"],
            noise_model="ar1",
            hrf_model="glover",
            drift_model="cosine",
            slice_time_ref=0.474,  # this value is specific to the acquisition parameters of the dataset. In this case it is the StartTime parameter that can be found in the .json after fmriprep (0.711) divided by the TR (1.5) = 0.474
            high_pass=hp_hz,
            subject_label=sub_label,
            smoothing_fwhm=4,
            n_jobs=2,
            verbose=2,
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
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_space-{settings["space_label"]}_desc-{masked_string}_bold.nii.gz",
            )

            events_tsv = os.path.join(
                settings["bids_path"],
                f"sub-{sub_label}",
                "func",
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_events.tsv",
            )

            # load as pandas dataframe
            events = pd.read_csv(events_tsv, sep="\t")

            # delete Rest and RestFinal rows
            # events = events[events["trial_type"] != "Discard"]
            events = events[events["trial_type"] != "Rest"]
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

            # PHYSIO DATA REGRESSORS
            physio_file = os.path.join(
                settings["bids_path"],
                "derivatives",
                "physio-out",
                f"sub-{sub_label}",
                f"sub-{sub_label}_task-{task_label}_run-{run_label}_desc-physioregressors.txt",
            )

            # if physio file exists, get the regressors
            if os.path.exists(physio_file):
                print(
                    f"Found physio file for sub-{sub_label} task-{task_label} run-{run_label}"
                )

                # read physio_file
                physio = pd.read_csv(physio_file, sep="\t", header=None)

                # rename columns to physio01, physio02, etc.
                physio.columns = [
                    f"physio{i:02}" for i in range(1, physio.shape[1] + 1)
                ]

                # remove columns with only nans
                physio = physio.dropna(axis=1, how="all")

                # join confounds and physio
                confounds = pd.concat([confounds, physio], axis=1)

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

            # repeat the contrast for the number of runs just to avoid the warning
            c_list = [contrast_list[ii]] * len(settings["run_labels"])
            maps = fmri_glm.compute_contrast(c_list, output_type="all")

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


def secondlevel(settings, task_label, contrast_renamed_list):
    """
    Perform second-level GLM analysis on fMRI data for specified contrasts.

    Parameters:
    - settings (dict): Configuration settings containing paths and other parameters.
    - task_label (str): Label for the task being analyzed.
    - contrast_renamed_list (list): List of renamed contrasts for which the second-level analysis is performed.

    Returns:
    None

    This function performs the following steps:
    1. Iterates over the list of renamed contrasts.
    2. For each contrast, lists all first-level z-map files corresponding to the contrast.
    3. Prints the number of z-map files found.
    4. Creates a design matrix for the second-level analysis.
    5. Defines and fits a second-level GLM model using the z-map files and the design matrix.
    6. Computes the contrast (z-score map) for the second-level analysis.
    """
    # Iterate on the contrast list
    for contrast_name in contrast_renamed_list:

        print(f"Running 2nd level for contrast {contrast_name}")

        # List all zmap nii.gz files
        zmap_files = glob.glob(
            os.path.join(
                settings["out_glm_path"],
                f"sub-*_task-{task_label}_stat-z_con-{contrast_name}.nii.gz",
            )
        )
        zmap_files.sort()

        # print number of zmap files
        print(f"Number of zmap files: {len(zmap_files)}")

        # create design matrix for 2nd level
        design_matrix_g = pd.DataFrame(
            [1] * len(zmap_files),
            columns=["intercept"],
        )

        # define 2nd level model
        second_level_model = SecondLevelModel(smoothing_fwhm=8.0, n_jobs=3)

        second_level_model = second_level_model.fit(
            zmap_files,
            design_matrix=design_matrix_g,
        )

        # compute contrast (z score map)
        z_map_g = second_level_model.compute_contrast(
            second_level_contrast="intercept",
            output_type="z_score",
        )

        # save group map
        z_map_g.to_filename(
            os.path.join(
                settings["out_glm_group_path"],
                f"group_task-{task_label}_stat-z_con-{contrast_name}.nii.gz",
            )
        )

        print(f"Finished 2nd level for contrast {contrast_name}")
