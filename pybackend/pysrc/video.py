import json

from flask import Flask, jsonify
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage
from pathlib import Path

import os
from .tools import convertVideo2Audio

Video = Namespace(
    name='Video',
    description='영상에 대한 API'
)

post_parser = Video.parser()
# parser.add_argument('Device-name', location='headers', required=True)
post_parser.add_argument('id', type=str, location='form', required=True)
post_parser.add_argument('file', type=FileStorage, location='files', required=True)

inference_parser = Video.parser()
inference_parser.add_argument('id', type=str, location='json', required=True)

@Video.route('/postVideo')
class PostVideo(Resource):

    @Video.expect(post_parser, validate=True)
    @Video.response(200, 'Success')
    @Video.response(404, 'None File')
    @Video.response(405, 'Invalide Extension')
    @Video.response(500, 'Failed')
    def post(self):
        """영상을 서버에 업로드 합니다."""
        try:
            args = post_parser.parse_args()

            id = args['id']
            f = args['file']
            if f.filename == None:
                return {"result": "None File"}, 404

            name, ext = os.path.splitext(f.filename)

            if ext != '.mp4':
                return {"result": "Invalid Extension"}, 405
            convertVideo2Audio(f, name, id)
            return {"result": "Success"}, 200

        except:
            return {"result": "Failed"}, 500


@Video.route('/inferenceAudio')
class InferenceAudio(Resource):

    @Video.expect(inference_parser, validate=True)
    @Video.response(200, 'Success')
    @Video.response(500, 'Failed')
    def post(self):
        """음성 스크립트를 추론 합니다."""
        try:
            args = inference_parser.parse_args()
            id = args['id']
            print(inference_parser)
            result = ''
            data = {}

            backend_dir_path = Path.cwd()
            inference_path = f'{backend_dir_path}/pybackend/hyper/tasks/SpeechRecognition/klecspeech/scripts/inference.sh'

            trim_audio_path = f"./pybackend/static/upload/uploadVideo/{id}/trimAudio"
            audio_path = f"./pybackend/static/upload/uploadVideo/{id}/audio"
            print('path : ' + trim_audio_path)
            trim_audio_list = os.listdir(trim_audio_path)
            trim_audio_list = sorted(trim_audio_list)

            iteration = 0
            sec = 0
            timeTable={}
            for audio in trim_audio_list:
                # path = trim_audio_path + '/' + audio
                path = f'{trim_audio_path}/{audio}'
                print(path)
                cmd = f"{inference_path} \"{path}\""

                out = os.popen(cmd).read()
                out = out.splitlines()[61]
                out = out[14:]
                print(out)
                timeTable[sec]=out
                iteration += 1
                sec += 10
            data["srcAddress"] = f'https://f9c8-106-101-1-109.jp.ngrok.io/static/upload/uploadVideo/{id}/video/{id}.mp4'
            data['timeTable'] = timeTable
            audio = os.listdir(audio_path)[0]
            print(f"{inference_path} /\"{audio_path}/{audio}\"")
            out = os.popen(f"{inference_path} \"{audio_path}/{audio}\"").read()
            out = out.splitlines()[61]
            out = out[14:]

            out = out.replace('요 ', '요. ')
            out = out.replace('다 ', '다. ')

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