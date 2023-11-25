import pyaudio
import numpy as np
from scipy.signal import find_peaks
import mido
import time
import keyboard
import math


def check_microphone():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if 'mic' in info['name'].lower():
            return True
    return False

microphone_available = check_microphone()
# initialize pyaudio
p = pyaudio.PyAudio()
score = []

# audio parameters
sample_rate = 44100
buffer_size = 1024
audio_format = pyaudio.paInt16
n_channels = 1

# open audio stream
stream = p.open(format=audio_format, channels=n_channels, rate=sample_rate, input=True,
                frames_per_buffer=buffer_size)

# initialize pitch tracking variables
pitch_list = []
prev_pitch = 0
#check microphone plugged in or not


# get note name from MIDI note number
def note_name(midi_note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note_name = note_names[midi_note % 12]
    octave = (midi_note // 12) - 1
    return '{}{}'.format(note_name, octave)

def main():
    # calculate autocorrelation of audio data
    corr = np.correlate(audio_data, audio_data, mode='full')
    corr = corr[len(corr)//2:]

            # find peaks in the autocorrelation
    peaks, _ = find_peaks(corr, distance=20)

            # calculate pitch as the distance between peaks
    if len(peaks) > 1:
        pitch = sample_rate / (peaks[1] - peaks[0])
        pitch_list.append(pitch)
        prev_pitch = pitch

                # convert pitch to MIDI note number
        midi_note = int(12 * np.log2(pitch / 440) + 69)

                # get note name from MIDI note number
        note = note_name(midi_note)

                # print note name
        print('Note: {}'.format(note))
        score.append(note)
    else:
        pitch_list.append(prev_pitch)




while True:
    
         # read audio data
            audio_data = np.frombuffer(stream.read(buffer_size), dtype=np.int16)


        # normalize audio data
            audio_data = audio_data / np.iinfo(np.int16).max

        # calculate dB level
            rms = math.sqrt(np.mean(np.square(audio_data)))
            db = 20 * np.log10(rms)

        # process pitch if dB level is greater than 20
            if db > -40:
                main()
            time.sleep(0.1)
            if keyboard.is_pressed('s'):
                break


   



   


# stop and close audio stream
stream.stop_stream()
stream.close()
print(score)

# terminate pyaudio
p.terminate()
