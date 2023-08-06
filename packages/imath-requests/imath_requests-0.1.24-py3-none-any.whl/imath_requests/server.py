"""
server.py
====================================
Mock server for testing REST API.
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse


class ImageMetaDataEndpoint(Resource):
    def get(self):
        image_meta_data = {
            "part_id" : "Part1234",
            "value_id" : "Camera1",
            "source": "Camera_Control_PC_Garret",
            "values" : [
                { 
                    "value": "Part1234_1.1_2.2_1.jpg",
                    "timestamp": "1516193959559",
                    "position": [346.2,2],
                    "dimension" : [5.2,1],
                    "quality" : "1"
                },
                { 
                    "value": "Part1234_1.1_2.2_2.jpg",
                    "timestamp": "1516193959559",
                    "position": [246.2,5],
                    "dimension" : [1.7,4],
                    "quality" : "-1"
                }
            ],
            "qualifying_metadata" : [
                { 
                    "key": "key1",
                    "value": "value1"
                },
                { 
                    "key": "key2",
                    "value": "value2"
                }
            ]
        }
        return {'data': image_meta_data}, 200  # return data and 200 OK code

    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        return {'data': json_data}, 200  # return data with 200 OK


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        @self.app.route('/')
        def index():
            page = """ 
                <h1>Welcome to iMath Requests test server</h1>
                <h3>The following API endpoints are available:</h3>
                <ul>
                    <li>/image_meta_data</li>
                </ul>
            """
            return page

        self.api.add_resource(ImageMetaDataEndpoint, '/image_meta_data')

    def run(self):
        self.app.run()

if __name__ == "__main__":
    server = Server()
    server.run()