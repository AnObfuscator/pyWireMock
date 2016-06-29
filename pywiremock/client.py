import json
import requests


class WireMock:
    def __init__(self, port, host=None, url_prefix=None):
        self._host = host if host else 'localhost'
        self._port = port
        self._url_prefix = url_prefix if url_prefix else ''

    def save_mappings(self):
        raise NotImplementedError

    def reset_mappings(self):
        """
        reset all mappings, including defaults
        """
        url = 'http://{}:{}/__admin/reset'.format(self._host, self._port)
        requests.post(url)

    def reset_to_default_mappings(self):
        """
        reset mappings to defaults loaded from json
        """
        url = 'http://{}:{}/__admin/mappings/reset'.format(self._host, self._port)
        requests.post(url)

    def reset_requests(self):
        raise NotImplementedError

    def reset_all_requests(self):
        url = 'http://{}:{}/__admin/requests/reset'.format(self._host, self._port)
        requests.post(url)

    def reset_scenarios(self):
        raise NotImplementedError

    def register(self, stub_mapping):
        url = 'http://{}:{}/__admin/mappings/new'.format(self._host, self._port)
        result = requests.post(url, stub_mapping.to_json())
        # print(stub_mapping.to_json())
        # print(result)

    def list_all_stub_mappings(self):
        raise NotImplementedError

    def set_global_fixed_delay(self, milliseconds):
        raise NotImplementedError

    def add_delay_before_processing_requests(self, milliseconds):
        raise NotImplementedError

    def verify(self, count, request_pattern):
        url = 'http://{}:{}/__admin/requests/count'.format(self._host, self._port)
        request_body = request_pattern.to_json()
        response = requests.post(url, request_body)
        # print(response.content)
        response_content = json.loads(response.content)
        response_count = int(response_content['count'])
        if count != response_count:
            raise AssertionError('Assertion failed. Expected count: {} Actual count: {}'.format(count, response_count))