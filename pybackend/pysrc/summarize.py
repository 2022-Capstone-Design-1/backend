from flask import Flask, jsonify
from flask_restx import Api, Resource, Namespace, reqparse, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from pathlib import Path
import subprocess, os
from .tools import createDirectory, trim_audio
import json

Summarize = Namespace(
    name='Summarize',
    description='요약에 대한 API'
)

summarize_parser = Summarize.parser()
# parser.add_argument('Device-name', location='headers', required=True)
summarize_parser.add_argument('text', type=str, location='form', required=True)


@Summarize.route('/')
class IndexSummarize(Resource):
    def get(self):
        """요약 index"""
        return {"result": "summarize index"}


@Summarize.route('/summarizeText')
class SummarizeText(Resource):
    
    @Summarize.expect(summarize_parser, validate=True)
    @Summarize.response(200, 'Success')
    @Summarize.response(500, 'Failed')
    def post(self):
        """텍스트를 요약 합니다."""
        try:
            args = summarize_parser.parse_args()
            text = args['text']

            result = ''

            kobart_dir_path = Path.cwd()
            inference_path = Path.joinpath(kobart_dir_path, 'pybackend', 'KoBART-summarization', 'inference.py')

            cmd = f"python {inference_path} --text \"{text}\""
            
            result = os.popen(cmd).read()
            print(result)

            return {"result": result}, 200
        
        except:
            return {"result": "Failed"}, 500