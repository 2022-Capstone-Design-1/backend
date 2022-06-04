import os
import librosa
import numpy as np
import soundfile as sf
import math
from pydub import AudioSegment
import wave

def convertVideo2Audio(file, file_name, file_id):
    # File upload
    mp4_version = AudioSegment.from_file(file, "mp4")
    # Slice audio
    ten_seconds = 10 * 1000
    one_min = ten_seconds * 6
    file_len = math.ceil(len(mp4_version) / ten_seconds)

    # up/down volumn >> 선택사항 +- 숫자
    # beginning = first_5_seconds + 6

    makefolder_path = f"./pybackend/upload/uploadVideo/{file_id}"
    createDirectory(makefolder_path)

    mp4_version.export(f'{makefolder_path}/audio/{file_name}.wav', format('wav'), parameters=['-ar', '16000', '-ac', '1'])
    # Save the result
    # can give parameters-quality, channel, etc
    for i in range(file_len):
        start_idx = ten_seconds * i
        last_idx = ten_seconds * (i + 1)
        if last_idx > len(mp4_version):
            last_idx = len(mp4_version)
        first_10_seconds = mp4_version[start_idx:last_idx]
        # last_5_seconds = mp4_version[-5000:]
        # first_5_seconds.export('result.pcm', format('u16be'), bitrate='16k')
        # 추출 경로
        first_10_seconds.export(f'{makefolder_path}/trimAudio/{file_name}_{i}.wav', format('wav'), bitrate='16k', parameters=['-ar', '16000', '-ac', '1'])

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(directory + f'/audio')
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
    
    for i in range(0, iteration):
        ny = y[sec*sr*i : (sec*i*sr)+(sr*sec)]
        sf.write(save_file + f'_{i}.wav', ny, sr, format='WAV', endian='LITTLE', subtype='PCM_16')   
        
        print(save_file + f'_{i}.wav')
        