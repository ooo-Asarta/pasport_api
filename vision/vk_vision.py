import requests
import io
import json
from models import Passport
from typing import Dict, List


class VkDecoder:
    @classmethod
    def expand_it_into_a_passport_model(cls, response: requests.Response):
        if response.status_code == 200:
            recognized_passport_data: Dict[str, List[str]] = cls._get_the_recognized_passport_data(response)
            return cls._create_paspport(recognized_passport_data)
        else:
            logger.error(
                f"Request failed with status code: {response.status_code}")
            raise ValueError(
                f"Request failed with status code: {response.status_code}")

    @classmethod
    def _create_paspport(cls, recognized_passport_data: Dict[str, List[str]]):
        if not cls._validate_passport_dict(recognized_passport_data):
            raise ValueError("Invalid passport data structure")
        passport_data: Dict[str, str] = cls._merge_lists(
            recognized_passport_data)
        return cls._create_paspport_object(passport_data)

    @classmethod
    def _create_paspport_object(cls, passport_data: Dict[str, str]) -> Passport:
        passport = Passport(name=passport_data['first_name'],
                            middle_name=passport_data['middle_name'],
                            surname=passport_data['last_name'],
                            gender=passport_data['sex'],
                            birth_date=passport_data['birthday'],
                            birth_place=passport_data['birthplace'],
                            number=passport_data['series_number'] +
                            passport_data['number'],
                            issued_by=passport_data['place_of_issue'],
                            issue_date=passport_data['date_of_issue'],
                            subdivision=passport_data['code_of_issue'],
                            )
        return passport

    @classmethod
    def _validate_passport_dict(cls, dictionary: Dict[str, List[str]]) -> bool:
        required_keys = [
            'birthday',
            'birthplace',
            'code_of_issue',
            'date_of_issue',
            'first_name',
            'last_name',
            'middle_name',
            'number',
            'place_of_issue',
            'series_number',
            'sex',
        ]

        for key in required_keys:
            if key not in dictionary:
                return False
            if not isinstance(dictionary[key], list):
                return False

        return True

    @classmethod
    def _get_the_recognized_passport_data(cls, response: requests.Response):
        response_json = response.json()
        results = response_json['body']['objects'][0]['labels']
        return results

    @classmethod
    def _merge_lists(cls, dictionary: Dict[str, List[str]]) -> Dict[str, str]:

        if not isinstance(dictionary, dict):
            raise TypeError("The argument must be a dictionary")

        result = {}
        for key, value in dictionary.items():
            if not isinstance(value, list):
                raise TypeError(f"The values for key '{key}' must be a list")

            unique_values = set(value)
            if len(unique_values) == 1:
                result[key] = value[0].lower()
            else:
                result[key] = ' '.join(unique_values).lower()

        return result


class VkVision:
    def __init__(self, oauth_token: str):
        self.oauth_token = oauth_token

    def recognize_the_passport(self, image: io.BytesIO) -> requests.Response:
        url, meta, files = self._create_passport_recognition_request_settings(
            image)

        try:
            response: requests.Response = self._send_request(
                url=url, files=files, meta=meta)
            return response
        except Exception as e:
            logger.error(f"Response error: {str(e)}")
            raise Exception(f"Response error: {str(e)}")

    def _create_passport_recognition_request_settings(self, image: io.BytesIO):
        url = 'https://smarty.mail.ru/api/v1/docs/recognize'
        file_name = 'file.jpg'
        meta = {
            "images": [
                {
                    "name": "file"
                }
            ]
        }

        image.seek(0)
        files = {
            'file': (file_name, image, 'image/jpeg')
        }
        return url, meta, files

    def _send_request(self, url: str, files, meta: str):
        params = {
            'oauth_token': self.oauth_token,
            'oauth_provider': 'mcs'
        }
        headers = {
            'Accept': 'application/json'
        }
        return requests.post(url,
                             files=files,
                             data={'meta': json.dumps(meta)},
                             headers=headers,
                             params=params)
