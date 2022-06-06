<p align="center"><img width="484" alt="image" src="https://user-images.githubusercontent.com/34434155/172136178-35ae8277-a573-4a6b-864f-510685e806d3.png">

## Introduction  
- 영상/음성 파일에 대한 스크립트를 생성하기 위한 서버
- 서버 : Python Flask restx
- 모델 : kospeech에서 제공하는 Acoustic Model 중 deepspeech2(ds2) model 사용
- 현재 Repository에 서버 API에 해당하는 코드와 학습된 deepspeech2 model 모두 포함

## Model
- Aihub 한국어 음성 1000시간 중 200시간 데이터로 학습 완료
- Aihub 한국어 강의 음성 4000시간 (약 570만개) 학습 예정
- 현재 학습은 32 batch size, 20 epoch로 진행

## API
- /audio/audioPost : 음성 파일(.wav)을 서버에 업로드  
- /audio/inferenceAudio : 서버에 업로드된 음성 파일을 추론  
- /video/postVideo : 동영상 파일(.mp4)를 서버에 업로드  
- /video/inferenceAudio : 서버에 업로드된 음성 파일을 추론  

  http://localhost:5000 로 접속하여 Swagger API 상세 스펙 확인 가능  
 

## Installation
- Python 3.9 가상환경 사용

### Virtual Environment
```
conda create -n project_name python==3.9
```

### Prerequisites  
- Numpy : `pip install numpy`  
- Pandas : `pip install pandas`
- Matplotlib : `pip install matplotlib`
- librosa : `conda install -c conda-forge librosa`
- torchaudio : `pip install torchaudio==0.8.0`
- tqdm : `pip install tqdm`
- hydra : `pip install hydra-core --upgrade`
- flask : `pip install flask`
- flask_restx : `pip install flask_restx`
- python-docx : `pip install python-docx`

### Install from source
```
pip install -r requirements_backend.txt
```

### Start Server
```
python start_server.py
```
