import requests


class Downloader():
    def __init__(self, endpoint, headers):
        self.endpoint = endpoint
        self.headers = headers

    def download(self, full_path):
        res = requests.get(self.endpoint, headers=self.headers)

        with open(full_path, 'wb') as f:
            f.write(res.content)