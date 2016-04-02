import json
import requests


class WireMock:
    def __init__(self, port, host=None, url_prefix=None):
        self._host = host if host else 'localhost'
        self._port = port
        self._url_prefix = url_prefix if url_prefix else ''

    def save_mappings(self):
        pass

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
        pass

    def reset_all_requests(self):
        url = 'http://{}:{}/__admin/requests/reset'.format(self._host, self._port)
        requests.post(url)

    def reset_scenarios(self):
        pass

    def register(self, stub_mapping):
        url = 'http://{}:{}/__admin/mappings/new'.format(self._host, self._port)
        requests.post(url, stub_mapping.to_json())

    def list_all_stub_mappings(self):
        pass

    def set_global_fixed_delay(self, milliseconds):
        pass

    def add_delay_before_processing_requests(self, milliseconds):
        pass

    def verify(self, count, request_builder):
        url = 'http://{}:{}/__admin/requests/count'.format(self._host, self._port)
        request_body = request_builder.build().to_json()
        response = requests.post(url, request_body)
        # print(response.content)
        response_content = json.loads(response.content)
        response_count = int(response_content['count'])
        # return count == response_count
        if count != response_count:
            raise AssertionError('Assertion failed. Expected count: {} Actual count: {}'.format(count, response_count))