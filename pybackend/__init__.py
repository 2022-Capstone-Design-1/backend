from flask import Flask, request
from flask_restx import Api, Resource
from .pysrc.audio import Audio

app = Flask(__name__)
app.debug = True
api = Api(
    app,
    title='2022-CNU-Capstone-Design-1 API Server',
    description='음성/동영상에 대한 스크립트 생성을 위한 API Server',
    terms_url='/',
    contact="https://github.com/2022-CNU-Capstone-Design-1/backend"
)

api.add_namespace(Audio, '/audio')