import numpy as np


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
