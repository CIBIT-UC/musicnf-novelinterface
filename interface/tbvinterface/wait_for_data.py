import time

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
    maxcounter = 500

    # Case 1: Previous data in memory
    # Case 2: First run after starting TBV
    while currentTime == expectedTime or currentTime > 3:
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
    maxcounter = 100

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