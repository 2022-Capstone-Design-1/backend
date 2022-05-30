from flask import Flask, jsonify
from flask_restx import Api, Resource, Namespace, reqparse, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import subprocess, os
from .tools import createDirectory, trim_audio

Audio = Namespace(
    name='Audio',
    description='음성에 대한 API'
)

post_parser = Audio.parser()
# parser.add_argument('Device-name', location='headers', required=True)
post_parser.add_argument('id', type=str, location='form', required=True)
post_parser.add_argument('file', type=FileStorage, location='files', required=True)

inference_parser = Audio.parser()
inference_parser.add_argument('id', type=str, location='form', required=True)

@Audio.route('/')
class IndexAudio(Resource):
    def get(self):
        """음성 index"""
        return {"result": "video index"}


@Audio.route('/postAudio')
class PostAudio(Resource):
    
    @Audio.expect(post_parser, validate=True)
    @Audio.response(200, 'Success')
    @Audio.response(404, 'None File')
    @Audio.response(405, 'Invalide Extension')
    @Audio.response(500, 'Failed')
    def post(self):
        """음성을 서버에 업로드 합니다."""
        try:
            args = post_parser.parse_args()
            
            id = args['id']
            f = args['file']
            
            if f.filename == None:
                return {"result": "None File"}, 404
            
            name, ext = os.path.splitext(f.filename)
            
#             convertName = name + '.wav'
#             if ext == '.pcm':
#                 convertFile = pcm2wav(f.filename, convertName, 1, 16, 16000)
            
            makefolder_path = f"./pybackend/upload/{id}"
            createDirectory(makefolder_path)
            
            f.save(makefolder_path + "/audio/" + secure_filename(f.filename))
            
#             오디오 일정 시간으로 나눠서 저장
            audio_path = makefolder_path + '/audio'
            save_path = makefolder_path + '/trimAudio'

            audio_list = os.listdir(audio_path)

            for audio_name in audio_list:
                if audio_name.find('wav') != -1:
                    audio_file = audio_path + '/' + audio_name
                    save_file = save_path + '/' + audio_name[:-4]
                    trim_audio(audio_file, save_file)
                    
                    
            return {"result": "Success"}, 200
        
        except:
            return {"result": "Failed"}, 500


@Audio.route('/inferenceAudio')
class InferenceAudio(Resource):
    
    @Audio.expect(inference_parser, validate=True)
    def post(self):
        """음성 스크립트를 추론 합니다."""
        args = inference_parser.parse_args()
        
        id = args['id']
        
        result = ''
        
        trim_audio_path = f"./pybackend/upload/{id}/trimAudio"
        trim_audio_list = os.listdir(trim_audio_path)
        
#         for audio in trim_audio_list:
#             path = trim_audio_path + '/' + audio
            
#             cmd = "python ./pybackend/kospeech2/bin/inference.py " \
#                       "--model_path \"C:/Users/hooni/Desktop/DL_service/pybackend/kospeech2/outputs/2022-05-29/18-55-43/model.pt\" " \
#                       f"--audio_path \"{path}\" --device \"cpu\""
        cmd = "python ./pybackend/kospeech2/bin/inference.py " \
                      "--model_path \"C:/Users/hooni/Desktop/DL_service/pybackend/kospeech2/outputs/2022-05-29/18-55-43/model.pt\" " \
                      f"--audio_path \"C:/Users/hooni/Desktop/DL_service/pybackend/upload/{id}/audio/000005.wav\" --device \"cpu\""
            
#         C:/Users/hooni/Desktop/DL_service/pybackend/upload/{id}/audio/000005.wav
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.decode('cp949')
        result += result.join(out.splitlines())
            
        return {"result": result}