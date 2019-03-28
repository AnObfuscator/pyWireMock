import unittest
from pywiremock.client import WireMock
from pywiremock.helpers import *
import requests

# Note: this assumes that there is a WireMock instance running locally on 7890, with the mappings defined in 'sample'

class StandaloneExample(unittest.TestCase):

    def setUp(self):
        self._sample_server = WireMock(7890, 'localhost')

    def tearDown(self):
        self._sample_server.reset_all_requests()
        self._sample_server.reset_to_default_mappings()

    def test_attach_to_standalone_and_get_predefined_method(self):
        # Act
        result = requests.get('http://localhost:7890/api/default/get')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'More content\n')

        expected_request = get(url_matching('/api/default/get'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_post_predefined_method(self):
        # Act
        result = requests.post('http://localhost:7890/api/default/post', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'More content\n')

        expected_request = post(url_matching('/api/default/post')).with_request_body(matching('some content'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_put_predefined_method(self):
        # Act
        result = requests.put('http://localhost:7890/api/default/put', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'More content\n')

        expected_request = put(url_matching('/api/default/put')).with_request_body(matching('some content'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_delete_predefined_method(self):
        # Act
        result = requests.delete('http://localhost:7890/api/default/delete')

        # Verify
        self.assertEqual(result.status_code, 204)

        expected_request = delete(url_matching('/api/default/delete'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_define_method_then_get(self):
        # Setup
        new_request = get(url_matching('/api/defined/get'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)
        self._sample_server.register(new_stub)

        # Act
        result = requests.get('http://localhost:7890/api/defined/get')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, 'defined content')

        self._sample_server.verify(1, new_request)

    def test_attach_to_standalone_and_define_method_then_post(self):
        # Setup
        new_request = post(url_matching('/api/defined/post')).with_request_body(matching('some content'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)
        self._sample_server.register(new_stub)

        # Act
        result = requests.post('http://localhost:7890/api/defined/post', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, 'defined content')

        self._sample_server.verify(1, new_request)

    def test_attach_to_standalone_and_define_method_then_put(self):
        # Setup
        new_request = put(url_matching('/api/defined/put')).with_request_body(matching('some content'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)
        self._sample_server.register(new_stub)

        # Act
        result = requests.put('http://localhost:7890/api/defined/put', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.text, 'defined content')

        self._sample_server.verify(1, new_request)

    def test_attach_to_standalone_and_define_method_then_delete(self):
        # Setup
        new_request = delete(url_matching('/api/defined/delete'))
        new_response = a_response().with_status(204)
        new_stub = stub_for(new_request).will_return(new_response)
        self._sample_server.register(new_stub)

        # Act
        result = requests.delete('http://localhost:7890/api/defined/delete')

        # Verify
        self.assertEqual(result.status_code, 204)

        self._sample_server.verify(1, new_request)
