import mido
import time

ascending_chord_map = {
    0: [36, 48, 52, 55, 59], # C Major 7
    1: [38, 50, 53, 57, 60], # D Minor 7
    2: [40, 52, 55, 59, 62], # E Minor 7
    3: [41, 53, 57, 60, 64], # F Major 7
    4: [43, 55, 59, 62, 66], # G Major 7
    5: [45, 57, 60, 64, 67], # A Minor 7
    6: [47, 59, 62, 66, 69], # B Minor 7
    7: [48, 60, 64, 67, 71], # C Major 7
    8: [50, 62, 66, 69, 72], # D Minor 7
    9: [52, 64, 67, 71, 74], # E Minor 7
    10: [53, 65, 69, 72, 76] # F Major 7
}

descending_chord_map = {
    0: [36, 48, 51, 54, 57], # C dim 7
    1: [38, 50, 53, 56, 59], # D dim 7
    2: [40, 52, 55, 58, 61], # E dim 7
    3: [41, 53, 56, 59, 62], # F dim 7
    4: [43, 55, 58, 61, 64], # G dim 7
    5: [45, 57, 60, 63, 66], # A dim 7
    6: [47, 59, 62, 65, 68], # B dim 7
    7: [48, 60, 63, 66, 69], # C dim 7
    8: [50, 62, 65, 68, 71], # D dim 7
    9: [52, 64, 67, 70, 73], # E dim 7
    10: [53, 65, 68, 71, 74] # F dim 7
}

# Function to create chords based on a number and its relation to the previous number
def create_chord_from_number(number, previous_number, previous_chord, imagery_counter):

    CHANGE_CHORD = True

    # Set to zero all negative correlations
    if number < 0:
        number = 0
    if previous_number < 0:
        previous_number = 0

    # if imagery_counter is less than 3, set the number to 0
    if imagery_counter == 0:
        number = 0
        previous_number = -1
    elif imagery_counter < 3:
        number = 0
        previous_number = 0

    # Set the base note
    base_note = 48

    # if the number is 0, create a power chord (no 3rd)
    if number == 0:
        chord = [base_note - 12, base_note, base_note + 7]
    else:
        # if the number is greater than the previous number, create a major 7th chord
        if number > previous_number:
            chord = ascending_chord_map[number]
        # if the number is smaller than the previous number, create a minor 7th chord
        elif number < previous_number:
            chord = descending_chord_map[number]

    # if the number is the same as the previous number, keep the same chord
    if number == previous_number:
        CHANGE_CHORD = False
        chord = previous_chord

    return chord, previous_chord, CHANGE_CHORD

# Function to send a chord as MIDI messages
def send_chord_on(midi_out, chord):
    for note in chord:
        midi_out.send(mido.Message('note_on', note=note, velocity=64))

    return chord

def send_chord_off(midi_out, chord):
    for note in chord:
        midi_out.send(mido.Message('note_off', note=note, velocity=64))

def clear_all_notes(midi_out):
    for note in range(30,80):
        midi_out.send(mido.Message('note_off', note=note, velocity=64))
        time.sleep(0.01)        