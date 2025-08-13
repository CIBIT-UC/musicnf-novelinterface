import mido
from midi_functions import clear_all_notes

# MIDI Output
midi_music_out = mido.open_output('IAC Driver Music Port')
midi_noise_out = mido.open_output('IAC Driver Noise Port')

clear_all_notes(midi_music_out)
clear_all_notes(midi_noise_out)
