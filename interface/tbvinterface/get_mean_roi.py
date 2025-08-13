import time
import numpy as np

def get_mean_roi(n_rois, tbvNetInt, time_point):
    """
    Retrieves Mean ROI Activation for all ROIs.

    Args:
        n_rois: int - number of ROIs
        tbvNetInt: TBVNetworkInterface instance
        time_point: int - time point to retrieve (0-based)

    Returns:
        tuple: ROImeansM1 (np.ndarray), timeM1 (float)
    """
    start_time = time.time()

    ROImeansM1 = np.zeros(n_rois)

    for i in range(n_rois):
        ROImeansM1[i] = tbvNetInt.tGetMeanOfROIAtTimePoint(i, time_point)

    timeM1 = time.time() - start_time

    return ROImeansM1, timeM1