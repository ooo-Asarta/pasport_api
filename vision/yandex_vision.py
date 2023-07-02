import logging
import requests
import io
import json
import base64
from typing import Optional

logger = logging.getLogger(__name__)


from pydantic import BaseModel, validator
from datetime import datetime

class Passport(BaseModel):
    _ISSUE_DATE_FORMAT = "%d.%m.%Y"

    name: str
    middle_name: str
    surname: str
    gender: str
    citizenship: str
    birth_date: str
    birth_place: str
    number: str
    issued_by: str
    issue_date: str
    subdivision: str
    expiration_date: str

    @property
    def formatted_issue_date(self) -> str:
        return self._format_date(self.issue_date)

    @staticmethod
    def _format_date(date_str: str) -> str:
        try:
            date = datetime.strptime(date_str, Passport._ISSUE_DATE_FORMAT)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            return ""

    @validator('birth_date', 'issue_date', pre=True)
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Invalid date format. Expected format: dd.mm.yyyy')
        return value

    def validate(self) -> bool:
        # Дополнительные проверки, если необходимо
        return True

class YandexVision:
    def __init__(self, oauth_token: str, folder_id: str):
        self.oauth_token = oauth_token
        self.folder_id = folder_id

    async def precognize_passport(self, image: io.BytesIO) -> Optional[str]:
        file_content = self._encode_image(image)
        body = self._build_precognize_passport_request_body(file_content)

        try:
            response = self._send_request(body)
            if response.status_code == 200:
                results = self._parse_precognize_passport_response(response)
                pasport = self._create_passport_from_data(results)
                return pasport
            else:
                logger.error(f"Request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {str(e)}")   
            return None 


    def _encode_image(self, image) -> str:
        file_content = image.read()
        encoded_image = base64.b64encode(file_content).decode('utf-8')
        return encoded_image

    def _build_precognize_passport_request_body(self, file_content):
        return {
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
        }

    def _send_request(self, body):
        url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {self.oauth_token}'
        }
        return requests.post(url, headers=headers, data=json.dumps(body))

    def _parse_precognize_passport_response(self, response):
        response_json = response.json()
        results = response_json['results'][0]['results'][0]['textDetection']['pages'][0]['entities']
        return results
    
    def _create_passport_from_data(self, data) -> Optional[Passport]:
        required_fields = [
            'name', 'middle_name', 'surname', 'gender', 'citizenship', 'birth_date',
            'birth_place', 'number', 'issued_by', 'issue_date','subdivision', 'expiration_date'
        ]
    
        passport_data = {}
        for entity in data:
            if entity['name'] in required_fields:
                passport_data[entity['name']] = entity['text']
    
        if len(passport_data) == len(required_fields):
            return Passport(**passport_data)
    
        raise ValueError('Invalid passport data. Missing required fields.')
    