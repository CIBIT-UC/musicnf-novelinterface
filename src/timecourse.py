import os
import pandas as pd
import numpy as np
from nilearn.image import resample_to_img
from nilearn.maskers import NiftiMasker
from nilearn.image import resample_img
from src.my_settings import settings
from src.utils import generate_brainnetome_mask
import nibabel as nib


def extract_imagery_time_courses(subject, task, run, roi_string):
    # Load settings
    sett = settings()

    # Paths
    func_img_path = os.path.join(
        sett["derivatives_path"],
        f"sub-{subject}",
        "func",
        f"sub-{subject}_task-{task}_run-{run}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz",
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

    # Mask generation and resampling
    mask = generate_brainnetome_mask(
        os.path.join(sett["git_path"], "data", "brainnetome"), roi_string=roi_string
    )
    mask_resampled = resample_to_img(mask, func_img_path, interpolation="nearest")
    z_map = nib.load(glm_img_path)
    z_map_resampled = resample_img(
        z_map,
        target_affine=mask_resampled.affine,
        target_shape=mask_resampled.shape,
        interpolation="nearest",
    )
    thres = 3.1
    mask_1 = NiftiMasker(mask_img=mask_resampled)
    z_data_masked = mask_1.fit_transform(z_map_resampled)
    binary_mask_data = (z_data_masked > thres).astype(int)
    binary_mask_img = mask_1.inverse_transform(binary_mask_data)

    # check if binary mask is empty - if so, return NaN array
    if np.sum(binary_mask_data) == 0:
        print(f"Empty mask for {subject} {task} {run}")
        return np.full((1, 20), np.nan)

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

    # Get rest volumes
    rest_volumes = np.concatenate(
        [
            np.arange(
                row["onset_volume"] + 3, row["onset_volume"] + row["duration_volume"]
            )
            for _, row in events[events["trial_type"] == "Rest"].iterrows()
        ]
    )

    # Get time course of mask image
    masker = NiftiMasker(
        mask_img=binary_mask_img, confounds=confounds, high_pass=0.008, t_r=sett["tr"]
    )
    voxel_tcs = masker.fit_transform(func_img_path)

    # Compute signal change
    rest_mean = voxel_tcs[rest_volumes].mean()
    signal_change = 100 * (voxel_tcs - rest_mean) / rest_mean
    signal_change_avg = signal_change.mean(axis=1)

    # Get imagery volumes
    imagery_volumes = [
        np.arange(row["onset_volume"], row["onset_volume"] + row["duration_volume"])
        for _, row in events[events["trial_type"] == "MotorImagery"].iterrows()
    ]

    # Compute imagery time courses
    imagery_tcs = np.zeros((len(imagery_volumes), 20))
    for i, volumes in enumerate(imagery_volumes):
        imagery_tcs[i, : len(volumes)] = signal_change_avg[volumes]

    return imagery_tcs
