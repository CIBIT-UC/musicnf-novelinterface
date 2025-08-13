import time

import mido
import numpy as np
from midi_functions import clear_all_notes, create_chord_from_number, send_chord_off, send_chord_on
from tbv_functions import calc_correlation, calc_signal_var, get_mean_roi, parse_prt_file, wait_for_data
from TBVClient import TBVClient
from TBVNetworkInterface import TBVNetworkInterface

# CHECKLIST
# * TBV Network Plugin v1.73 or greater
# * Pre-Load two ROIs

# Select IP
TBV_IP = "192.168.238.189"  # MRI TBV PC
# TBV_IP = '192.168.6.72'      # CELSIUS
TBV_PORT = 55555

# Select TR and wait time
TR = 1.5  # in seconds
wait_time = 0.05  # in seconds

# Select PRT path
prtPath = "./prt_creator/prt/MusicNF_Main_v0.3_PostDiscard.prt"
# prtName = 'MusicNF_Main_v0.3_PostDiscard.prt'

# Select NF parameters
selected_roi = 1
maxPSC = 2.5
# ignore = 8 # Ignore the first 8 data points (discard condition)
updateThreshold = 3  # Only updates after having this number of points after shiftBegin
baseline_name = "Rest"
upregulation_name = "MotorImagery"

# Turn On/Off Real Feedback
FEEDBACK = True

# Correlation Window Size
window_size = 8  # in volumes

# MIDI Output
midi_music_out = mido.open_output("IAC Driver Music Port")
midi_noise_out = mido.open_output("IAC Driver Noise Port")
midi_beep_out = mido.open_output("IAC Driver Beep Port")

# Open TBV Connection
tbvNetInt = TBVNetworkInterface(TBVClient(TBV_IP, TBV_PORT))
tbvNetInt.create_connection()

# WAIT FOR DATA
n_rois, currentTime, expectedTime = wait_for_data(tbvNetInt, wait_time)

# INITIALIZE Variables and NF Parameters
shiftBegin = int(6 / TR)
shiftEnd = int(shiftBegin / 3)

last = 0  # zero based

time_counter = 0  # volume counter

counter = 0  # time out counter
maxcounter = 100  # max time out counter

chord = [60 - 12, 60, 60 + 7]  # initial chord

# Initialize Variables
ROImeans = np.zeros((expectedTime, n_rois))  # ROI means over time
PearsonCorr = np.zeros((expectedTime, 1))  # Pearson Correlation over time
PearsonCorrDiscrete = np.zeros((expectedTime, 1))  # Discrete Pearson Correlation over time
PearsonCorrSham = np.zeros((expectedTime, 1))  # Sham Pearson Correlation over time
PearsonCorrDiscreteSham = np.zeros((expectedTime, 1))  # Discrete Sham Pearson Correlation over time

SignalVar = np.zeros(expectedTime)  # Signal PSC Variation to baseline over time
SignalVarDiscrete = np.zeros(expectedTime)  # Discrete Signal PSC Variation to baseline over time
Baseline = np.zeros(expectedTime)  # Baseline value over time

BaselineIndexes = np.zeros(expectedTime)  # Baseline Indexes
BaselineIndexesUpdate = np.zeros(expectedTime)  # Baseline Update Indexes

# Read PRT file
conditions, cond_names = parse_prt_file(prtPath)

# Find the index of the baseline condition in conditions
baseline_index = cond_names.index(baseline_name)
print(f"Baseline Index: {baseline_index}")

# Find the index of the last baseline condition in conditions
last_baseline_index = cond_names.index("RestFinal")

# Find the index of the increased condition in conditions
upregulation_index = cond_names.index(upregulation_name)
print(f"Upregulation Index: {upregulation_index}")

# Initalize NOISE_ON - a flag for the white noise sound
NOISE_ON = False

# Imagery volume counter - to keep feedback steady during the first 3 volumes
imagery_counter = 0

# Iterate on the baseline trials to define the baseline indexes and the baseline update indexes
for ii in range(len(conditions[baseline_name])):
    start_volume = int(conditions[baseline_name][ii, 0] + shiftBegin)
    end_volume = int(conditions[baseline_name][ii, 1] + shiftEnd)

    BaselineIndexes[start_volume - 1 : end_volume] = 1
    BaselineIndexesUpdate[start_volume - 1 + shiftEnd + updateThreshold : end_volume] = 1

# BaselineIndexes[:ignore] = 0
BaselineIndexesUpdate[: shiftBegin + updateThreshold] = 0

# Fetch the duration of the increased condition in volumes
blockDur = conditions[upregulation_name][0, 1] - conditions[upregulation_name][0, 0] + 1

# Fetch the intermediate volume indexes of all the trials of the 'Increased' condition
BeepIndexes = np.zeros(expectedTime)
for ii in range(len(conditions[upregulation_name])):
    # find the intermediate volume index
    start_volume = int(conditions[upregulation_name][ii, 0])
    end_volume = int(conditions[upregulation_name][ii, 1])

    intermediate_volume = int((start_volume + end_volume) / 2)
    BeepIndexes[intermediate_volume] = 1  # on
    BeepIndexes[intermediate_volume + 1] = 2  # off

# TIME Iteration
while time_counter < expectedTime:
    if time_counter == currentTime:
        if counter == maxcounter:
            print(f"ERROR: No new point received after {wait_time * maxcounter} seconds.")
            break

        time.sleep(wait_time)
        counter += 1
    else:  # the real deal
        # --- GET CURRENT CONDITION ---
        current_condition = tbvNetInt.get_current_protocol_condition()
        print(f"Current Condition: {current_condition} ({cond_names[current_condition]}) ")

        # --- Fetch ROI activity and Pearson's correlation data ---
        ROImeans[time_counter, :], _ = get_mean_roi(n_rois, tbvNetInt, time_counter)
        PearsonCorr[time_counter, 0], PearsonCorrDiscrete[time_counter, 0] = calc_correlation(tbvNetInt, window_size, time_counter)

        # --- Generate random number between 0 and 1 for SHAM correlation
        PearsonCorrSham[time_counter, 0] = np.random.rand()
        PearsonCorrDiscreteSham[time_counter, 0] = int(round(PearsonCorrSham[time_counter, 0] * 10))

        # --- Calculate Signal Variation to Baseline ---
        # if time_counter >= ignore:  # Ignore first data points

        # Check if the baseline value should be updated
        if BaselineIndexesUpdate[time_counter] == 1:  # if yes, update the baseline value
            Baseline[time_counter] = np.mean(ROImeans[last - shiftBegin : time_counter + 1, selected_roi])
        else:  # if not, keep the previous baseline value
            last = time_counter

            if time_counter == 0:
                Baseline[time_counter] = ROImeans[time_counter, selected_roi]  # the first baseline value
            else:
                Baseline[time_counter] = Baseline[time_counter - 1]  # fetch the previous baseline value

        # calculate the signal variation to the baseline for the selected ROI
        SignalVar[time_counter], SignalVarDiscrete[time_counter] = calc_signal_var(
            Baseline[time_counter], ROImeans[time_counter, selected_roi], maxPSC
        )

        # --- LOGIC BASED ON CURRENT CONDITION ---

        # Play some white noise during the baseline condition
        if (current_condition == baseline_index or current_condition == last_baseline_index) and NOISE_ON == False:  # baseline
            clear_all_notes(midi_music_out)  # stop music
            send_chord_on(midi_noise_out, [60])  # play noise
            NOISE_ON = True

        # Stop playing noise when the baseline condition ends
        if (current_condition == upregulation_index) and NOISE_ON == True:
            clear_all_notes(midi_noise_out)
            imagery_counter = 0  # reset imagery counter
            NOISE_ON = False

        # Play music during the increased condition
        if current_condition == upregulation_index:
            # Get Chord
            if FEEDBACK:
                chord, previous_chord, CHANGE_CHORD = create_chord_from_number(
                    PearsonCorrDiscrete[time_counter, 0], PearsonCorrDiscrete[time_counter - 1, 0], chord, imagery_counter
                )
            else:
                chord, previous_chord, CHANGE_CHORD = create_chord_from_number(
                    PearsonCorrDiscreteSham[time_counter, 0], PearsonCorrDiscreteSham[time_counter - 1, 0], chord, imagery_counter
                )

            # Send MIDI Signal
            if CHANGE_CHORD:
                send_chord_off(midi_music_out, previous_chord)  # stop music - previous chord
                send_chord_on(midi_music_out, chord)  # play music - new chord

            # Prints
            print(f"Imagery Counter: {imagery_counter}")
            print(f"Signal Var ROI1: {SignalVar[time_counter]}")
            print(f"Signal Var ROI1 Discrete: {SignalVarDiscrete[time_counter]}")
            print(f"Pearson Correlation ROI1-ROI2: {PearsonCorr[time_counter, 0]}")
            print(f"Pearson Correlation ROI1-ROI2 Discrete: {PearsonCorrDiscrete[time_counter, 0]}")
            if not FEEDBACK:
                print("-----------------------------------")
                print(f"Pearson Correlation ROI1-ROI2 Sham: {PearsonCorrSham[time_counter, 0]}")
                print(f"Pearson Correlation ROI1-ROI2 Discrete Sham: {PearsonCorrDiscreteSham[time_counter, 0]}")
            print("===================================")

            # Increase the imagery counter
            imagery_counter += 1

        # --- Play a beep sound during the increased condition at the intermediate volume ---
        if BeepIndexes[time_counter] == 1:
            send_chord_on(midi_beep_out, [60])  # play beep
        elif BeepIndexes[time_counter] == 2:
            send_chord_off(midi_beep_out, [60])  # stop beep

        # --- Update Time Counter ---
        print(f"Time {time_counter}")

        time_counter += 1
        counter = 0

    currentTime = tbvNetInt.get_current_time_point()

# Clear all notes
clear_all_notes(midi_noise_out)  # stop noise
clear_all_notes(midi_music_out)  # stop music

# Export ROImeans, PearsonCorr, PearsonCorrDiscrete, SignalVar, SignalVarDiscrete in a single file and timestamp it
timestamp = time.strftime("%Y%m%d-%H%M%S")

if FEEDBACK:
    f_name = "Active"

    np.savez(
        f"MusicNF_{f_name}_{timestamp}.npz",
        ROImeans=ROImeans,
        PearsonCorr=PearsonCorr,
        PearsonCorrDiscrete=PearsonCorrDiscrete,
        SignalVar=SignalVar,
        SignalVarDiscrete=SignalVarDiscrete,
    )
else:
    f_name = "Sham"

    np.savez(
        f"MusicNF_{f_name}_{timestamp}.npz",
        ROImeans=ROImeans,
        PearsonCorr=PearsonCorr,
        PearsonCorrDiscrete=PearsonCorrDiscrete,
        SignalVar=SignalVar,
        SignalVarDiscrete=SignalVarDiscrete,
        PearsonCorrSham=PearsonCorrSham,
        PearsonCorrDiscreteSham=PearsonCorrDiscreteSham,
    )
