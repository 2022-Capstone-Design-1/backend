import os
import librosa
import soundfile as sf
import math
from pydub import AudioSegment

def convertVideo2Audio(file, file_name, file_id):
    makefolder_path = f"./pybackend/static/upload/uploadVideo/{file_id}"
    createDirectory(makefolder_path)
    os.makedirs(f"{makefolder_path}/video")
    file.save(f'./pybackend/static/upload/uploadVideo/{file_id}/video/{file_id}.mp4')

    # File upload
    mp4_version = AudioSegment.from_file(f'./pybackend/static/upload/uploadVideo/{file_id}/video/{file_id}.mp4', "mp4")
    # Slice audio
    seconds = 10 * 1000
    one_min = seconds * 6
    #seconds = one_min
    file_len = math.ceil(len(mp4_version) / seconds)

    # up/down volumn >> 선택사항 +- 숫자
    # beginning = first_5_seconds + 6

    mp4_version.export(f'{makefolder_path}/audio/{file_id}.wav', format('wav'), parameters=['-ar', '16000', '-ac', '1'])
    # Save the result
    # can give parameters-quality, channel, etc
    for i in range(file_len):
        start_idx = seconds * i
        last_idx = seconds * (i + 1)
        if last_idx > len(mp4_version):
            last_idx = len(mp4_version)
        first_10_seconds = mp4_version[start_idx:last_idx]
        # 추출 경로
        first_10_seconds.export(f'{makefolder_path}/trimAudio/{file_id}_{i}.wav', format('wav'), parameters=['-ar', '16000', '-ac', '1'])

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
    sec = 10
    mono=True

    y, sr = librosa.load(audio_file, sr=sr, mono=mono)

    duration = y.shape[0]/sr
    print(f"Audio Duration: {duration}")
    
    iteration = int((math.ceil(duration)/sec))
    print(f"iteration : {iteration}")
    
    for i in range(0, iteration+1):
        last = (sec*i*sr)+(sr*sec)
        if last - sec*sr*i < 1 : break
        if last > len(y):
            ny = y[sec*sr*i : ]
        else:
            ny = y[sec*sr*i : last]
        sf.write(save_file + f'_{i}.wav', ny, sr, format='WAV')
        
        print(save_file + f'_{i}.wav')
        