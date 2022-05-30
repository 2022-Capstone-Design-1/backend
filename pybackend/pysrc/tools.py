import os
import librosa
import numpy as np
import soundfile as sf
import math
import wave

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(directory + '/audio')
            os.makedirs(directory + '/trimAudio')
    except OSError:
        print("Error: Failed to create the directory.")
        

def trim_audio(audio_file, save_file):
    sr = 16000
    sec = 2
    mono=True

    y, sr = librosa.load(audio_file, sr=sr, mono=mono)

    duration = y.shape[0]/sr
    print(f"Audio Duration: {duration}")
    
    iteration = int((math.ceil(duration)/sec))
    print(f"iteration : {iteration}")
    
    for i in range(0, iteration+1):
        ny = y[sec*sr*i : (sec*i*sr)+(sr*sec)]
        sf.write(save_file + f'_{i}.wav', ny, sr, format='WAV', endian='LITTLE', subtype='PCM_16')   
        
        print(save_file + f'_{i}.wav')
        