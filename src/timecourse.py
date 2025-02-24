import os

import numpy as np
import pandas as pd
from nilearn.image import resample_to_img
from nilearn.maskers import NiftiMasker, NiftiSpheresMasker
from scipy.stats import pearsonr

from src.my_settings import settings
from src.utils import generate_brainnetome_mask

# Load settings
sett = settings()

pmc_coords = [(-30, -5, 64), (18, -2, 72)]
labels = ["leftPMC", "rightPMC"]


def extract_era_corr_sphere(
    sub_label,
    task_label,
    run_label,
    sphere_radius=6,
    window_size_online=8,
    window_size_offline=4,
):
    masker = NiftiSpheresMasker(
        pmc_coords,
        radius=6,
        detrend=True,
        standardize=True,
        standardize_confounds=True,
        smoothing_fwhm=4,
        high_pass=0.008,
        t_r=sett["tr"],
        memory=os.path.join(sett["git_path"], "data", "nilearn_mem"),
        memory_level=1,
        verbose=2,
    )

    # Paths
    func_img = os.path.join(
        sett["derivatives_path"],
        f"sub-{sub_label}",
        "func",
        f"sub-{sub_label}_task-{task_label}_run-{run_label}{sett['space_label']}_desc-preproc_bold.nii.gz",
    )

    confounds_tsv = os.path.join(
        sett["derivatives_path"],
        f"sub-{sub_label}",
        "func",
        f"sub-{sub_label}_task-{task_label}_run-{run_label}_desc-confounds_timeseries.tsv",
    )

    # load as pandas dataframe
    confounds = pd.read_csv(confounds_tsv, sep="\t")

    # filter
    confounds = confounds[sett["confounds_of_interest"]]

    # fill NaNs with 0
    confounds = confounds.fillna(0)

    # PHYSIO DATA REGRESSORS
    physio_file = os.path.join(
        sett["bids_path"],
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
        physio.columns = [f"physio{i:02}" for i in range(1, physio.shape[1] + 1)]

        # remove columns with only nans
        physio = physio.dropna(axis=1, how="all")

        # join confounds and physio
        confounds = pd.concat([confounds, physio], axis=1)

    time_series = masker.fit_transform(func_img, confounds=confounds)

    # get the events
    events_file = os.path.join(
        sett["bids_path"],
        f"sub-{sub_label}",
        "func",
        f"sub-{sub_label}_task-{task_label}_run-{run_label}_events.tsv",
    )

    events = pd.read_csv(events_file, sep="\t")

    # remove last 'Rest' event
    events = events[:-1]

    # compensate the onsets with a hemodynamic delay of 4 seconds
    events["onset"] = events["onset"] + 3

    # create onsets and durations in volumes, considering the TR, as integers
    events["onset_volume"] = (events["onset"] / sett["tr"]).astype(int)
    events["duration_volume"] = (events["duration"] / sett["tr"]).astype(int)

    # get all the volume indexes for Rest
    rest_volumes = []

    # iterate on the events for which trial type is Rest
    for idx, row in events[events["trial_type"] == "Rest"].iterrows():
        # set the start and end volume indexes for the rest period
        start = row["onset_volume"]
        end = start + row["duration_volume"]

        rest_volumes.append(np.arange(start, end))

    # join all the rest periods
    rest_volumes = np.concatenate(rest_volumes)

    # get the average of the rest period
    rest_mean = time_series[rest_volumes, :].mean(axis=0)

    # get the signal change
    signal_change = time_series - rest_mean

    # get the bilateral signal change
    signal_change_avg = signal_change.mean(axis=1)

    # now let's create the average timecourse of all the imagery periods
    imagery_volumes = []

    # iterate on the events for which trial type is Imagery
    for idx, row in events[events["trial_type"] == "MotorImageryOne"].iterrows():
        # set the start and end volume indexes for the imagery period
        start = row["onset_volume"]
        end = start + 20

        imagery_volumes.append(np.arange(start, end))

        # Iterate on the length of imagery volumes
    imagery_tcs = np.zeros(
        (len(pmc_coords), len(imagery_volumes), len(imagery_volumes[0]))
    )

    for rr in range(len(pmc_coords)):
        for i, volumes in enumerate(imagery_volumes):
            imagery_tcs[rr, i, :] = signal_change[volumes, rr]

    correlations_online = np.zeros((len(imagery_volumes), len(imagery_volumes[0])))
    correlations_offline = np.zeros((len(imagery_volumes), len(imagery_volumes[0])))

    # iterate on the trials
    for i in range(len(imagery_volumes)):
        # iterate on the imagery volumes
        for j in range(len(imagery_volumes[0])):
            # set the window in volumes
            this_window_online = np.arange(
                imagery_volumes[i][j] - window_size_online, imagery_volumes[i][j]
            )
            this_window_offline = np.arange(
                imagery_volumes[i][j] - window_size_offline, imagery_volumes[i][j]
            )

            # calculate correlation
            correlations_online[i, j] = pearsonr(
                signal_change[this_window_online, 0],
                signal_change[this_window_online, 1],
            )[0]
            correlations_offline[i, j] = pearsonr(
                signal_change[this_window_offline, 0],
                signal_change[this_window_offline, 1],
            )[0]

    return (
        time_series,
        signal_change,
        signal_change_avg,
        imagery_tcs,
        correlations_online,
        correlations_offline,
    )


def extract_imagery_time_courses(subject, task, run, roi_string, n_timepoints):
    # Paths
    func_img_path = os.path.join(
        sett["derivatives_path"],
        f"sub-{subject}",
        "func",
        f"sub-{subject}_task-{task}_run-{run}_space-MNI152NLin2009cAsym_desc-preprocmasked_bold.nii.gz",
    )
    confounds_path = os.path.join(
        sett["derivatives_path"],
        f"sub-{subject}",
        "func",
        f"sub-{subject}_task-{task}_run-{run}_desc-confounds_timeseries.tsv",
    )
    events_file = os.path.join(
        sett["bids_path"],
        f"sub-{subject}",
        "func",
        f"sub-{subject}_task-{task}_run-{run}_events.tsv",
    )
    glm_img_path = os.path.join(
        sett["bids_path"],
        "derivatives",
        "nilearn-glm",
        f"sub-{subject}_task-{task}_stat-z_con-MotorImageryMinusRest.nii.gz",
    )

    # Check if all files exist
    if not os.path.exists(func_img_path):
        print(f"File not found: {func_img_path}")
        return np.full((1, n_timepoints), np.nan)
    if not os.path.exists(confounds_path):
        print(f"File not found: {confounds_path}")
        return np.full((1, n_timepoints), np.nan)
    if not os.path.exists(events_file):
        print(f"File not found: {events_file}")
        return np.full((1, n_timepoints), np.nan)
    if not os.path.exists(glm_img_path):
        print(f"File not found: {glm_img_path}")
        return np.full((1, n_timepoints), np.nan)

    # Mask generation and resampling
    mask = generate_brainnetome_mask(
        os.path.join(sett["git_path"], "data", "brainnetome"), roi_string=roi_string
    )
    mask_resampled = resample_to_img(mask, func_img_path, interpolation="nearest")

    # z_map = nib.load(glm_img_path)
    # z_map_resampled = resample_img(
    #     z_map,
    #     target_affine=mask_resampled.affine,
    #     target_shape=mask_resampled.shape,
    #     interpolation="nearest",
    # )
    # thres = 3.1
    # mask_1 = NiftiMasker(mask_img=mask_resampled)
    # z_data_masked = mask_1.fit_transform(z_map_resampled)
    # binary_mask_data = (z_data_masked > thres).astype(np.int32)
    # binary_mask_img = mask_1.inverse_transform(binary_mask_data)

    # check if binary mask is empty - if so, return NaN array
    # if np.sum(binary_mask_data) == 0:
    #     print(f"Empty mask for {subject} {task} {run}")
    #     return np.full((1, 20), np.nan)

    # Load confounds
    confounds = pd.read_csv(confounds_path, sep="\t")
    confounds = confounds[sett["confounds_of_interest"]].fillna(0)
    physio_file = os.path.join(
        sett["bids_path"],
        "derivatives",
        "physio-out",
        f"sub-{subject}",
        f"sub-{subject}_task-{task}_run-{run}_desc-physioregressors.txt",
    )
    if os.path.exists(physio_file):
        physio = pd.read_csv(physio_file, sep="\t", header=None)
        physio.columns = [f"physio{i:02}" for i in range(1, physio.shape[1] + 1)]
        physio = physio.dropna(axis=1, how="all")
        confounds = pd.concat([confounds, physio], axis=1)
    confounds = (confounds - confounds.mean()) / confounds.std()

    # Load events
    events = pd.read_csv(events_file, sep="\t")
    events = events[~events["trial_type"].isin(["Discard", "RestFinal"])]
    events["onset"] += 3  # Hemodynamic delay
    events["onset_volume"] = (events["onset"] / sett["tr"]).astype(int)
    events["duration_volume"] = (events["duration"] / sett["tr"]).astype(int)

    # Get all the rest volumes in a single array
    rest_volumes = np.concatenate(
        [
            np.arange(row["onset_volume"], row["onset_volume"] + row["duration_volume"])
            for _, row in events[events["trial_type"] == "Rest"].iterrows()
        ]
    )

    # Get time course of mask image
    masker = NiftiMasker(
        mask_img=mask_resampled, confounds=confounds, high_pass=0.008, t_r=sett["tr"]
    )
    voxel_tcs = masker.fit_transform(func_img_path)

    # Compute signal change
    rest_mean = voxel_tcs[rest_volumes].mean()
    signal_change = 100 * (voxel_tcs - rest_mean) / rest_mean
    signal_change_avg = signal_change.mean(axis=1)

    # Get imagery volumes
    imagery_one_volumes = [
        np.arange(row["onset_volume"], row["onset_volume"] + row["duration_volume"])
        for _, row in events[events["trial_type"] == "MotorImageryOne"].iterrows()
    ]
    imagery_two_volumes = [
        np.arange(row["onset_volume"], row["onset_volume"] + row["duration_volume"])
        for _, row in events[events["trial_type"] == "MotorImageryTwo"].iterrows()
    ]

    # Compute imagery time courses
    imagery_one_tcs = np.zeros((len(imagery_one_volumes), n_timepoints))
    imagery_two_tcs = np.zeros((len(imagery_two_volumes), n_timepoints))

    for i, volumes in enumerate(imagery_one_volumes):
        imagery_one_tcs[i, : len(volumes)] = signal_change_avg[volumes]

    for i, volumes in enumerate(imagery_two_volumes):
        imagery_two_tcs[i, : len(volumes)] = signal_change_avg[volumes]

    return imagery_one_tcs, imagery_two_tcs
