import unittest
from pywiremock.client import WireMock
from pywiremock.helpers import Method, Request, Response, Stub, Url
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

        expected_request = Request.where(Method.is_get(), Url.matches('/api/default/get'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_post_predefined_method(self):
        # Act
        result = requests.post('http://localhost:7890/api/default/post', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'More content\n')

        expected_request = Request.where(Method.is_post(), Url.matches('/api/default/post')).with_request_body('some content')
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_put_predefined_method(self):
        # Act
        result = requests.put('http://localhost:7890/api/default/put', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'More content\n')

        expected_request = Request.where(Method.is_put(), Url.matches('/api/default/put')).with_request_body('some content')
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_delete_predefined_method(self):
        # Act
        result = requests.delete('http://localhost:7890/api/default/delete')

        # Verify
        self.assertEqual(result.status_code, 204)

        expected_request = Request.where(Method.is_delete(), Url.matches('/api/default/delete'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_define_method_then_get(self):
        # Setup
        new_request_definition = Request.where(Method.is_get(), Url.matches('/api/defined/get'))
        new_response_definition = Response.that_is(200, 'defined content')
        stub_mapping = Stub.create_with(new_request_definition, new_response_definition)
        self._sample_server.register(stub_mapping)

        # Act
        result = requests.get('http://localhost:7890/api/defined/get')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'defined content')

        expected_request = Request.where(Method.is_get(), Url.matches('/api/defined/get'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_define_method_then_post(self):
        # Setup
        new_request_definition = Request.where(Method.is_post(), Url.matches('/api/defined/post')).with_request_body('some content')
        new_response_definition = Response.that_is(200, 'defined content')
        stub_mapping = Stub.create_with(new_request_definition, new_response_definition)
        self._sample_server.register(stub_mapping)

        # Act
        result = requests.post('http://localhost:7890/api/defined/post', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'defined content')

        expected_request = Request.where(Method.is_post(), Url.matches('/api/defined/post')).with_request_body('some content')
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_define_method_then_put(self):
        # Setup
        new_request_definition = Request.where(Method.is_put(), Url.matches('/api/defined/put')).with_request_body('some content')
        new_response_definition = Response.that_is(200, 'defined content')
        stub_mapping = Stub.create_with(new_request_definition, new_response_definition)
        self._sample_server.register(stub_mapping)

        # Act
        result = requests.put('http://localhost:7890/api/defined/put', 'some content')

        # Verify
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.content, 'defined content')

        expected_request = Request.where(Method.is_put(), Url.matches('/api/defined/put'))
        self._sample_server.verify(1, expected_request)

    def test_attach_to_standalone_and_define_method_then_delete(self):
        # Setup
        new_request_definition = Request.where(Method.is_delete(), Url.matches('/api/defined/delete'))
        new_response_definition = Response.that_is(204)
        stub_mapping = Stub.create_with(new_request_definition, new_response_definition)
        self._sample_server.register(stub_mapping)

        # Act
        result = requests.delete('http://localhost:7890/api/defined/delete')

        # Verify
        self.assertEqual(result.status_code, 204)

        expected_request = Request.where(Method.is_put(), Url.matches('/api/defined/delete'))
        self._sample_server.verify(1, expected_request)
