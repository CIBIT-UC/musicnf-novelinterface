import mido
import time
from midi_functions import create_chord_from_number, send_chord_on, clear_all_notes, send_chord_off

TR = 1.5  # in seconds
chord = [60 - 12, 60, 60 + 7]

# MIDI output
midi_music_out = mido.open_output('IAC Driver Music Port')

CHANGE_CHORD = True
#base_note_prog = [1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 0]
base_note_prog = [1, 0, 1, 2, 6, 8, 10, 9, 7, 5, 3, 1, 0, 0]

for ii in range(1, len(base_note_prog)):
    chord, previous_chord, CHANGE_CHORD = create_chord_from_number(base_note_prog[ii], base_note_prog[ii - 1], chord, 4)

    send_chord_on(midi_music_out, chord)
    time.sleep(2)
    send_chord_off(midi_music_out, chord)
    time.sleep(0.5)

clear_all_notes(midi_music_out)