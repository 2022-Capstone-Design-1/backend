from flask import Flask, jsonify
from flask_restx import Resource, Namespace
from werkzeug.datastructures import FileStorage

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
