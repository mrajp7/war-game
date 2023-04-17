import requests
from time import sleep

class RequestMethod:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class APIRequest:
    """_summary_
    API Request with inbuilt builder 
    """
    def __init__(self, builder):
        self.url = builder.url
        self.headers = builder.headers
        self.params = builder.params
        self.data = builder.data
        self.json = builder.json
        self.files = builder.files
        self.response = None

    def send_request(self, method, endpoint):
        sleep(0.5) # ! Assumption: Deck API is very slow
        url = self.url + endpoint
        if method == RequestMethod.GET:
            self.response = requests.get(url, headers=self.headers, params=self.params)
        elif method == RequestMethod.POST:
            if self.json is not None:
                self.response = requests.post(url, headers=self.headers, json=self.json)
            else:
                self.response = requests.post(url, headers=self.headers, data=self.data)
        elif method == RequestMethod.PUT:
            if self.json is not None:
                self.response = requests.put(url, headers=self.headers, json=self.json)
            else:
                self.response = requests.put(url, headers=self.headers, data=self.data)
        elif method == RequestMethod.DELETE:
            self.response = requests.delete(url, headers=self.headers, params=self.params)
        else:
            raise ValueError("Invalid method")

        return self

    def get_response_status_code(self):
        return self.response.status_code

    def get_response_content_type(self):
        return self.response.headers['content-type']

    def get_response_body(self):
        return self.response.text

    def get_response_json(self):
        return self.response.json()

    class APIRequestBuilder:
        def __init__(self, url):
            self.url = url
            self.headers = {}
            self.params = {}
            self.data = {}
            self.json = None
            self.files = {}

        def add_header(self, key, value):
            self.headers[key] = value
            return self

        def add_param(self, key, value):
            self.params[key] = value
            return self

        def add_data(self, key, value):
            self.data[key] = value
            return self

        def set_json(self, json_data):
            self.json = json_data
            return self

        def add_file(self, key, filepath):
            with open(filepath, 'rb') as f:
                self.files[key] = f.read()
            return self

        def build(self):
            return APIRequest(self)
