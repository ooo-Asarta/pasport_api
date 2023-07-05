import requests
import io
import json
import base64
from typing import Optional
from models import Passport
from logger import logger

class YandexDecoder:

    @staticmethod
    def expand_it_into_a_passport_model(response: requests.Response) -> Optional[Passport]:
        if response.status_code == 200:
            results = YandexDecoder._parse_precognize_passport_response(
                response)
            passport_data = YandexDecoder._create_passport_data(results)
            passport = YandexDecoder._create_passport(passport_data)
            return passport
        else:
            logger.error(
                f"Request failed with status code: {response.status_code}")
            raise ValueError(
                f"Request failed with status code: {response.status_code}")

    @staticmethod
    def _parse_precognize_passport_response(response) -> dict:
        response_json = response.json()
        results = response_json['results'][0]['results'][0]['textDetection']['pages'][0]['entities']
        return results

    @staticmethod
    def _create_passport_data(data) -> Optional[Passport]:
        required_fields = [
            'name', 'middle_name', 'surname', 'gender', 'birth_date',
            'birth_place', 'number', 'issued_by', 'issue_date', 'subdivision'
        ]

        passport_data = {}
        for entity in data:
            if entity['name'] in required_fields:
                passport_data[entity['name']] = entity['text']
        return passport_data
    def _create_passport(data):
        passport_series = data['number'][:4]  # Первые 4 цифры номера - это серия паспорта
        passport_number = data['number'][4:]  # Остальные цифры номера - это номер паспорта
    
        full_name = f"{data['surname']} {data['name']} {data['middle_name']}"
    
        passport_data = {
            'passport_series': passport_series,
            'passport_number': passport_number,
            'passport_issued_by': data['issued_by'],
            'passport_issued_on': data['issue_date'],
            'full_name': full_name,
            'date_of_birth': data['birth_date']
        }
    
        passport = Passport(**passport_data)
        return passport
    


class YandexVision:
    def __init__(self, oauth_token: str, folder_id: str):
        self.oauth_token = oauth_token
        self.folder_id = folder_id

    def recognize_the_passport(self, image: io.BytesIO) -> requests.Response:
        file_content = self._encode_image(image)
        body = self._build_recognize_passport_request_body(file_content)
        try:
            response = self._send_request(body)
            return response
        except Exception as e:
            logger.error(f"Response error: {str(e)}")
            raise Exception(f"Response error: {str(e)}")

    @staticmethod
    def _encode_image(image: io.BytesIO) -> str:
        try:
            file_content = image.read()
            encoded_image = base64.b64encode(file_content).decode('utf-8')
            return encoded_image
        except Exception as e:
            logger.error(f"Error encoding the image: {str(e)}")
            raise Exception(f"Error encoding the image: {str(e)}")

    def _build_recognize_passport_request_body(self, file_content: str) -> str:
        return json.dumps({
            "folderId": self.folder_id,
            "analyze_specs": [
                {
                    "content": file_content,
                    "features": [
                        {
                            "type": "TEXT_DETECTION",
                            "text_detection_config": {
                                "language_codes": ["ru"],
                                "model": "passport"
                            }
                        }
                    ]
                }
            ]
        })

    def _send_request(self, body: str) -> requests.Response:
        url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {self.oauth_token}'
        }
        return requests.post(url, headers=headers, data=body)
