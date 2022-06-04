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
inference_parser.add_argument('id', type=str, location='form', required=True)

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

            result = ''
            data = {}

            backend_dir_path = Path.cwd()
            inference_path = Path.joinpath(backend_dir_path, 'pybackend', 'kospeech2', 'bin', 'inference.py')
            model_path = Path.joinpath(backend_dir_path, 'pybackend', 'kospeech2', 'outputs', '2022-05-29', '18-55-43',
                                       'model.pt')

            # trim_audio_path = f"./pybackend/upload/{id}/trimAudio"
            trim_audio_path = Path.joinpath(backend_dir_path, 'pybackend', 'upload/uploadVideo', f'{id}', 'trimAudio')
            trim_audio_list = os.listdir(trim_audio_path)

            iteration = 0
            sec = 0
            for audio in trim_audio_list:
                # path = trim_audio_path + '/' + audio
                path = Path.joinpath(trim_audio_path, audio)

                cmd = f"python {inference_path} " \
                      f"--model_path \"{model_path}\" " \
                      f"--audio_path \"{path}\" --device \"cpu\""

                # proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                # out, err = proc.communicate()
                # out = out.decode('cp949')

                out = os.popen(cmd).read()
                print(out)
                data[iteration] = [f'{sec}-{sec + 2}', out.splitlines()[0]]
                iteration += 1
                sec += 2

            return json.dumps(data, ensure_ascii=False), 200

        except:
            return {"result": "Failed"}, 500