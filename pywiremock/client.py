import json
import requests


class WireMock:
    def __init__(self, port, host=None, url_prefix=None):
        self._host = host if host else 'localhost'
        self._port = port
        self._url_prefix = url_prefix if url_prefix else ''
        self._base_url = 'http://{}:{}/__admin'.format(self._host, self._port)

    def list_all_stub_mappings(self, limit=None, offset=None):
        url = '{}/mappings'.format(self._base_url)
        response = requests.get(url) # TODO support limit & offset
        return response.json()

    def add_stub_mapping(self, stub_mapping):
        url = '{}/mappings'.format(self._base_url)
        response = requests.post(url, stub_mapping.to_json())
        return response.json()

    def reset_mappings(self):
        """
        reset all mappings, including defaults
        """
        url = '{}/mappings'.format(self._base_url)
        requests.delete(url)

    def reset_to_default_mappings(self):
        """
        reset mappings to defaults loaded from json
        """
        url = '{}/mappings/reset'.format(self._base_url)
        requests.post(url)

    def get_stub_mapping(self, mapping_id):
        url = '{}/mappings/{}'.format(self._base_url, mapping_id)
        response = requests.get(url)
        return response.json()

    def edit_stub_mapping(self, mapping_id, stub_mapping):
        url = '{}/mappings/{}'.format(self._base_url, mapping_id)
        response = requests.put(url, stub_mapping.to_json())

    def remove_stub_mapping(self, mapping_id):
        url = '{}/mappings/{}'.format(self._base_url, mapping_id)
        requests.delete(url)

    def save_mappings(self):
        url = '{}/mappings/save'.format(self._base_url)
        requests.post(url)

    def get_all_requests(self, limit=None, since_date=None):
        """
        Get received requests
        """
        url = '{}/requests'.format(self._base_url)
        response = requests.get(url)  # TODO support query params
        return response.json()

    def reset_requests(self):
        """
        Delete all received requests
        """
        url = '{}/requests'.format(self._base_url)
        requests.delete(url)

    def get_request(self, request_id):
        """
        Single logged request
        """
        url = '{}/requests/{}'.format(self._base_url, request_id)
        response = requests.get(url)
        return response.json()

    def reset_all_requests(self):
        """
        Empty the request journal
        """
        url = '{}/requests/reset'.format(self._base_url)
        requests.post(url)

    def count_requests_matching(self, request_pattern):
        """
        Count requests logged in the journal matching the specified criteria
        """
        url = '{}/requests/count'.format(self._base_url)
        response = requests.post(url, request_pattern.to_json())
        return response.json()

    def find_requests_matching(self, request_pattern):
        """
        Retrieve details of requests logged in the journal matching the specified criteria
        """
        url = '{}/requests/find'.format(self._base_url)
        response = requests.post(url, request_pattern.to_json())
        return response.json()

    def find_unmatched_requests(self):
        """
        Get details of logged requests that weren't matched by any stub mapping
        """
        url = '{}/requests/unmatched'.format(self._base_url)
        response = requests.get(url)
        return response.json()

    def find_near_misses_for_unmatched_results(self):
        """
        Retrieve near-misses for all unmatched requests
        """
        url = '{}/requests/unmatched/near-misses'.format(self._base_url)
        response = requests.get(url)
        return response.json()

    def start_recording(self, record_spec):
        """
        Start recording stub mappings
        """
        url = '{}/recordings/start'.format(self._base_url)
        requests.post(url, record_spec.to_json())

    def stop_recording(self):
        """
        Stop recording stub mappings
        """
        url = '{}/recordings/stop'.format(self._base_url)
        response = requests.post(url)
        return response.json()

    def get_recording_status(self):
        """
        Get the recording status (started or stopped)
        """
        url = '{}/recordings/status'.format(self._base_url)
        response = requests.get(url)
        return response.json()

    def snapshot_record(self, record_spec):
        """
        Take a snapshot recording
        """
        url = '{}/recordings/snapshot'.format(self._base_url)
        response = requests.post(url, record_spec.to_json())
        return response.json()

    def get_scenarios(self):
        """
        Get all scenarios
        """
        url = '{}/scenarios'.format(self._base_url)
        response = requests.get(url)
        return response.json()

    def reset_scenarios(self):
        """
        Reset the state of all scenarios
        """
        url = '{}/scenarios/reset'.format(self._base_url)
        requests.post(url)

    def find_top_near_misses_for(self, logged_request=None, request_pattern=None):
        """
        Find at most 3 near misses for closest stub mappings to the specified request or request pattern
        """
        response = None
        if logged_request:
            url = '{}/near-misses/request'.format(self._base_url)
            response = requests.post(url, logged_request.to_json())

        elif request_pattern:
            url = '{}/near-misses/request-pattern'.format(self._base_url)
            response = requests.post(url, request_pattern.to_json())
        else:
            raise NotImplementedError
        return response.json()

    def register(self, stub_mapping):
        url = 'http://{}:{}/__admin/mappings/new'.format(self._host, self._port)
        result = requests.post(url, stub_mapping.to_json())
        # print(stub_mapping.to_json())
        # print(result)

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

    def shutdown(self):
        url = '{}/shutdown'.format(self._base_url)
        requests.post(url)
