from flask import Flask, jsonify
from flask_restx import Api, Resource, Namespace, reqparse, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pathlib import Path
import subprocess, os
from .tools import createDirectory, trim_audio
import json

Audio = Namespace(
    name='Audio',
    description='음성에 대한 API'
)

post_parser = Audio.parser()
# parser.add_argument('Device-name', location='headers', required=True)
post_parser.add_argument('id', type=str, location='form', required=True)
post_parser.add_argument('file', type=FileStorage, location='files', required=True)

inference_parser = Audio.parser()
inference_parser.add_argument('id', type=str, location='json', required=True)

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
            
            if ext != '.wav':
                return {"result": "Invalid Extension"}, 405
            
            makefolder_path = f"./pybackend/static/upload/uploadAudio/{id}"
            createDirectory(makefolder_path)
            
            f.save(makefolder_path + "/audio/" + secure_filename(id) + ".wav")
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
    @Audio.response(200, 'Success')
    @Audio.response(500, 'Failed')
    def post(self):
        """음성 스크립트를 추론 합니다."""
        try:
            args = inference_parser.parse_args()
            id = args['id']

            result = ''
            data = {}
            backend_dir_path = Path.cwd()
            inference_path = f'{backend_dir_path}/pybackend/hyper/tasks/SpeechRecognition/klecspeech/scripts/inference.sh'

            trim_audio_path = f"./pybackend/static/upload/uploadAudio/{id}/trimAudio"
            audio_path = f"./pybackend/static/upload/uploadAudio/{id}/audio"
            print('path : ' + trim_audio_path)
            trim_audio_list = os.listdir(trim_audio_path)
            trim_audio_list = sorted(trim_audio_list)

            iteration = 0
            sec = 0
            timeTable = {}
            for audio in trim_audio_list:

                path = f'{trim_audio_path}/{audio}'
                print(path)
                cmd = f"{inference_path} \"{path}\""

                out = os.popen(cmd).read()
                out = out.splitlines()[61]
                out = out[14:]
                print(out)
                timeTable[sec] = out
                iteration += 1
                sec += 10
            data['timeTable'] = timeTable
            audio = os.listdir(audio_path)[0]
            print(f"{inference_path} /\"{audio_path}/{audio}\"")
            out = os.popen(f"{inference_path} \"{audio_path}/{audio}\"").read()
            out = out.splitlines()[61]
            out = out[14:]

            out = out.replace('요 ', '요. ')
            out = out.replace('다 ', '다. ')
            data["srcAddress"] = f'https://f9c8-106-101-1-109.jp.ngrok.io/static/upload/uploadAudio/{id}/audio/{id}.wav'
            data['fullScript'] = out

            # summarize
            result = ''

            kobart_dir_path = Path.cwd()
            inference_path = Path.joinpath(kobart_dir_path, 'pybackend', 'KoBART-summarization', 'inference.py')

            cmd = f"python {inference_path} --text \"{out}\""

            result = os.popen(cmd).read()
            print(result)
            data['summary'] = result

            return json.dumps(data, ensure_ascii=False), 200
        except:
            return {"result": "Failed"}, 500
