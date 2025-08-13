import time
import numpy as np

def calc_signal_var(baseline, value, maxPSC):
    """
    Calculates NF Signal.

    Args:
        baseline: float - baseline value for current time point
        value: float - BOLD value at current time point
        maxPSC: float - maximum variation (percent value)

    Returns:
        float: Normalized signal variance
    """
    #print(f'Baseline: {baseline}, Value: {value}, maxPSC: {maxPSC}')
    signal_var = (value - baseline) * 100 / baseline
    #print(f'Signal Var: {signal_var}')
    signal_var_norm = signal_var / maxPSC
    #print(f'Signal Var Norm: {signal_var_norm}')

    # Limit signal_var_norm to 0-1 range
    signal_var_final = np.clip(signal_var_norm, 0, 1)
    #print(f'Signal Var Final: {signal_var_final}')

    # discretize signal_var_final into a 0-10 integer range
    signal_var_final_d = int(round(signal_var_final * 10))

    #print(f'Signal Var Final (Discretized): {signal_var_final_d}')

    return signal_var_final, signal_var_final_d

def calc_correlation(tbvNetInt, window_size, time_point):
    value = tbvNetInt.get_pearson_correlation_at_time_point(window_size, time_point)[0]

    # Convert the value to -10 to 10 range
    value_d = value * 10

    # Discretize the value
    value_d = int(round(value_d))

    return value, value_d


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
        _, _, ROImeansM1[i] = tbvNetInt.get_mean_of_roi_at_time_point(i, time_point)

    timeM1 = time.time() - start_time

    return ROImeansM1, timeM1

def parse_prt_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    conditions = {}
    current_condition = None
    reading_intervals = False

    for line in lines:
        line = line.strip()
        
        # Skip non-relevant lines
        if any(line.startswith(keyword) for keyword in ['FileVersion', 'ResolutionOfTime', 'Experiment', 
                                                        'BackgroundColor', 'TextColor', 'TimeCourseColor', 
                                                        'TimeCourseThick', 'ReferenceFuncColor', 'ReferenceFuncThick',
                                                        'NrOfConditions', 'ResponseConditions']):
            continue

        if reading_intervals:
            if line.startswith('Color:'):
                # Finished reading intervals for the current condition
                reading_intervals = False
                continue
            elif line:
                # Attempt to read onset and offset
                try:
                    onset, offset = map(int, line.split()[:2])
                    conditions[current_condition] = np.append(conditions[current_condition], [[onset, offset]], axis=0)
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

def wait_for_data(tbvNetInt, wait_time):
    """
    Control function
    Waits for all correct initial parameters to run the thermometer.
    
    Args:
        tbvNetInt: TBVNetworkInterface instance
        wait_time: float - sleep time in seconds

    Returns:
        n_rois: int - number of ROIs in TBV
        currentTime: int - current volume
        expectedTime: int - number of volumes of run
    """
    currentTime = tbvNetInt.get_current_time_point()
    expectedTime = tbvNetInt.get_expected_nr_of_time_points()

    counter = 0
    maxcounter = 100

    # Case 1: Previous data in memory
    # Case 2: First run after starting TBV
    while currentTime == expectedTime or currentTime > 2:
        if counter == 0:
            print('Waiting for new data...')
        elif counter == maxcounter:
            print(f'ERROR: No new data found after {wait_time * maxcounter} seconds.')
            raise RuntimeError('Script Terminated.')

        time.sleep(wait_time)
        counter += 1

        currentTime = tbvNetInt.get_current_time_point()
        expectedTime = tbvNetInt.get_expected_nr_of_time_points()

    counter = 0
    n_rois = tbvNetInt.get_nr_of_rois()
    maxcounter = 1000

    # Case 3: No ROI selected
    while n_rois == 0:
        if counter == 0:
            print('Waiting for ROI load...')
        elif counter == maxcounter:
            print(f'ERROR: ROI was not Pre-Loaded on TBV after {wait_time * maxcounter} seconds.')
            raise RuntimeError('Script Terminated.')

        time.sleep(wait_time)
        counter += 1
        n_rois = tbvNetInt.get_nr_of_rois()

    counter = 0

    # Case 4: After Network plugin restart
    while currentTime < 1:
        if counter == 0:
            print('Waiting for data...')
        elif counter == maxcounter:
            print(f'ERROR: No new data found after {wait_time * maxcounter} seconds.')
            raise RuntimeError('Script Terminated.')

        time.sleep(wait_time)
        currentTime = tbvNetInt.get_current_time_point()
        counter += 1

    return n_rois, currentTime, expectedTime