import requests


class FaceData:
    def __init__(self):
        pass

    def uploadFile(self, url, key="d45fd466-51e2-4701-8da8-04351c872236"):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        data = '{ "api_key": "' + key + '", "file_uri": "' + url + '", "detection_flags": "basicpoints,propoints,classifiers,content"}'
        response = requests.post('https://www.betafaceapi.com/api/v2/media', headers=headers, data=data).json()

        return response

    def getData(self, uuid, key="d45fd466-51e2-4701-8da8-04351c872236"):

        headers = {
            'accept': 'application/json',
        }

        params = (
            ('api_key', key),
            ('media_uuid', uuid),
        )

        response = requests.get('https://www.betafaceapi.com/api/v2/media', headers=headers, params=params).json()

        return response

