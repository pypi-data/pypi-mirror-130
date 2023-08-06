"""
server.py
====================================
Mock server for testing REST API.
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse


class PartDataEndpoint(Resource):
    def get(self):
        part_data = {
            "timestamp": 1516193959559,
            "part_id": "Part1234",
            "source": "Camera_Control_PC_Garret",
            "part_data": [
                {
                    "key": "steel_grade",
                    "value": "Grade01"
                },
                {
                    "key": "heat_number",
                    "value": "C1234566"
                },
                {
                    "key": "rolling_schedule",
                    "value": "Schedule1"
                },
                {
                    "key": "analysis",
                    "value": [
                        {
                            "key": "C",
                            "value": "0.2"
                        },
                        {
                            "key": "Mn",
                            "value": "0.02"
                        }
                    ]
                }
            ]
        }
        return {'data': part_data}, 200  # return data and 200 OK code

    def post(self):
        json_data = request.get_json(force=True)
        print(json_data)
        return {'data': json_data}, 200  # return data with 200 OK


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
                    "position": [346.2, 2.0, 0.0],
                    "dimension" : [5.2, 1.0, 0.0],
                    "quality" : "1"
                },
                { 
                    "value": "Part1234_1.1_2.2_2.jpg",
                    "timestamp": "1516193959559",
                    "position": [246.2, 5.0, 0.0],
                    "dimension" : [1.7, 4.0, 0.0],
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


class ImageAnalysisDataEndpoint(Resource):
    def get(self):
        image_analysis_data = {
            "part_id": "Part1234",
            "source": "Analysis System",
            "value": "Part1234_1.1_2.2_1.jpg",
            "timestamp": "1516193959559",
            "failures": [
                {
                    "id": 124355435321576,
                    "failure": "4711",
                    "position": [
                        44.2,
                        17.4,
                        0.0
                    ],
                    "dimension": [
                        5.2,
                        1.0,
                        0.0
                    ],
                    "qualifying_metadata": [
                        {
                            "key": "xxx",
                            "value": "1"
                        },
                        {
                            "key": "yyy",
                            "value": "2"
                        }
                    ]
                },
                {
                    "id": 124355435321578,
                    "failure": "4712",
                    "position": [
                        33.2,
                        3.0,
                        0.0
                    ],
                    "dimension": [
                        2.3,
                        1.1,
                        0.0,
                    ],
                    "qualifying_metadata": [
                        {
                            "key": "xxx",
                            "value": "1"
                        },
                        {
                            "key": "yyy",
                            "value": "2"
                        }
                    ]
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
                    <li>/part_data</li>
                    <li>/image_meta_data</li>
                    <li>/image_analysis_data</li>
                </ul>
            """
            return page

        self.api.add_resource(PartDataEndpoint, '/part_data')
        self.api.add_resource(ImageMetaDataEndpoint, '/image_meta_data')
        self.api.add_resource(ImageAnalysisDataEndpoint, '/image_analysis_data')

    def run(self):
        self.app.run()

if __name__ == "__main__":
    server = Server()
    server.run()
