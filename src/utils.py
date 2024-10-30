import numpy as np


def parse_prt_file(file_path):
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
