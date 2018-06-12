import unittest
from pywiremock.client import WireMock
from pywiremock.helpers import *
import requests


# Note: this assumes that there is a WireMock instance running locally on 7890, with the mappings defined in 'sample'
class ClientTest(unittest.TestCase):
    def setUp(self):
        self._sample_server = WireMock(7890, 'localhost')

    def tearDown(self):
        self._sample_server.reset_all_requests()
        self._sample_server.reset_to_default_mappings()

    def test_list_all_stub_mappings(self):
        mappings = self._sample_server.list_all_stub_mappings()

        self.assertEqual(5, mappings['meta']['total'])
        self.assertIsNotNone(mappings['mappings'])

    def test_add_stub_mapping(self):
        new_stubs = self._create_stubs()
        created_stubs = {}
        for k, v in new_stubs.items():
            created_stubs[k] = self._sample_server.add_stub_mapping(v)

        all_stubs = self._sample_server.list_all_stub_mappings()
        self.assertEqual(5+len(new_stubs), all_stubs['meta']['total'])

    def test_reset_mappings(self):
        pass
    #     self._sample_server.reset_mappings()
    #     mappings = self._sample_server.list_all_stub_mappings()
    #
    #     self.assertEqual(0, mappings['meta']['total'])

    def test_reset_to_default_mappings(self):
        new_stubs = self._create_stubs()
        created_stubs = {}
        for k, v in new_stubs.items():
            created_stubs[k] = self._sample_server.add_stub_mapping(v)

        self._sample_server.reset_to_default_mappings()

        mappings = self._sample_server.list_all_stub_mappings()
        self.assertEqual(5, mappings['meta']['total'])

    def test_get_stub_mapping(self):
        new_request = get(url_matching('/api/defined/test'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)

        expected_mapping = self._sample_server.add_stub_mapping(new_stub)
        uuid = expected_mapping['uuid']

        actual_mapping = self._sample_server.get_stub_mapping(uuid)

        self.assertDictEqual(actual_mapping, expected_mapping)

    def test_edit_stub_mapping(self):
        new_request = get(url_matching('/api/defined/test'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)

        original_mapping = self._sample_server.add_stub_mapping(new_stub)
        uuid = original_mapping['uuid']

        new_request = post(url_matching('/api/defined/test/updated'))
        new_response = a_response().with_status(200).with_body('defined content updated')
        new_stub = stub_for(new_request).will_return(new_response)

        updated_mapping = self._sample_server.edit_stub_mapping(uuid, new_stub)

        actual_mapping = self._sample_server.get_stub_mapping(uuid)

        self.assertDictEqual(actual_mapping, updated_mapping)

    def test_remove_stub_mapping(self):
        new_request = get(url_matching('/api/defined/test'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)

        original_mapping = self._sample_server.add_stub_mapping(new_stub)
        uuid = original_mapping['uuid']

        self._sample_server.remove_stub_mapping(uuid)

        mappings = self._sample_server.list_all_stub_mappings()
        self.assertEqual(5, mappings['meta']['total'])

    def test_save_mappings(self):
        pass

    def test_get_all_requests(self):
        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")

        wm_reqs = self._sample_server.get_all_requests()
        self.assertEqual(2, wm_reqs['meta']['total'])

    def test_reset_requests(self):
        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")

        wm_reqs = self._sample_server.get_all_requests()
        self.assertEqual(2, wm_reqs['meta']['total'])

        self._sample_server.reset_requests()

        wm_reqs = self._sample_server.get_all_requests()
        self.assertEqual(0, wm_reqs['meta']['total'])

    def test_get_request(self):
        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")

        wm_reqs = self._sample_server.get_all_requests()
        expected_request = wm_reqs['requests'][0]
        request_id = expected_request['id']

        actual_request = self._sample_server.get_request(request_id)

        self.assertDictEqual(expected_request, actual_request)

    def test_rest_all_requests(self):
        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")

        wm_reqs = self._sample_server.get_all_requests()
        self.assertEqual(2, wm_reqs['meta']['total'])

        self._sample_server.reset_requests()

        wm_reqs = self._sample_server.get_all_requests()
        self.assertEqual(0, wm_reqs['meta']['total'])

    def test_count_requests_matching(self):
        expected_get_request = get(url_matching('/api/default/get'))
        expected_delete_request = delete(url_matching('/api/default/delete'))

        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")
        requests.get("http://localhost:7890/api/default/get")

        matching_requests = self._sample_server.count_requests_matching(expected_get_request)

        self.assertEqual(2, matching_requests['count'])

    def test_find_requests_matching(self):
        expected_get_request = get(url_matching('/api/default/get'))
        expected_delete_request = delete(url_matching('/api/default/delete'))

        requests.get("http://localhost:7890/api/default/get")
        requests.delete("http://localhost:7890/api/default/delete")
        requests.get("http://localhost:7890/api/default/get")

        matching_requests = self._sample_server.find_requests_matching(expected_get_request)

        self.assertEqual(2, len(matching_requests['requests']))

    def test_find_unmatched_requests(self):
        requests.get("http://localhost:7890/api/default/missing")

        unmatched_requests = self._sample_server.find_unmatched_requests()

        self.assertEqual(1, len(unmatched_requests['requests']))

    def test_find_near_misses_for_unmatched_results(self):
        requests.get("http://localhost:7890/api/default/gte")

        unmatched_requests = self._sample_server.find_unmatched_requests()

        self.assertEqual(1, len(unmatched_requests['requests']))

    def test_start_recording_stop_recording_get_recording_status(self):
        recording_status = self._sample_server.get_recording_status()
        self.assertEqual('Stopped', recording_status['status'])

        recording = record_spec().for_target('http://example.mocklab.io')
        self._sample_server.start_recording(recording)
        recording_status = self._sample_server.get_recording_status()
        self.assertEqual('Recording', recording_status['status'])

        self._sample_server.stop_recording()
        recording_status = self._sample_server.get_recording_status()
        self.assertEqual('Stopped', recording_status['status'])

    def test_get_scenarios_reset_scenarios(self):
        expected_scenarios = self._create_scenario()
        created_stubs = {}
        for k, v in expected_scenarios.items():
            created_stubs[k] = self._sample_server.add_stub_mapping(v)

        actual_scenarios = self._sample_server.get_scenarios()
        self.assertEqual(1, len(actual_scenarios['scenarios']))
        scenario_start = actual_scenarios['scenarios'][0]
        # self._verify_scenario(scenario_start, 'Started')

        requests.post('http://localhost:7890/todo/items', data='Cancel newspaper subscription')

        actual_scenarios = self._sample_server.get_scenarios()
        self.assertEqual(1, len(actual_scenarios['scenarios']))
        scenario_start = actual_scenarios['scenarios'][0]
        self._verify_scenario(scenario_start, 'Cancel newspaper item added')

        self._sample_server.reset_scenarios()
        self.assertEqual(1, len(actual_scenarios['scenarios']))
        scenario_start = actual_scenarios['scenarios'][0]
        # self._verify_scenario(scenario_start, 'Started')

    def test_find_top_near_misses_for_request_pattern(self):
        new_request = get(url_matching('/api/defined/test-asdf'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stub = stub_for(new_request).will_return(new_response)
        self._sample_server.add_stub_mapping(new_stub)

        requests.get("http://localhost:7890/api/defined/test-asd")
        requests.get("http://localhost:7890/api/defined/test-adsf")
        requests.get("http://localhost:7890/api/defined/test-asf")
        requests.get("http://localhost:7890/api/defined/test-sdf")

        near_misses = self._sample_server.find_top_near_misses_for(request_pattern=new_request)
        print(near_misses)
        self.assertEqual(3, len(near_misses['nearMisses']))

    def test_find_top_near_misses_for_logged_request(self):
        pass

    def test_update_global_settings(self):
        pass

    def test_shutdown(self):
        pass

    def _create_stubs(self):
        new_stubs = {}

        new_request = get(url_matching('/api/defined/get'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stubs['get'] = stub_for(new_request).will_return(new_response)

        new_request = post(url_matching('/api/defined/post'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stubs['post'] = stub_for(new_request).will_return(new_response)

        new_request = put(url_matching('/api/defined/put'))
        new_response = a_response().with_status(200).with_body('defined content')
        new_stubs['put'] = stub_for(new_request).will_return(new_response)

        new_request = delete(url_matching('/api/defined/delete'))
        new_response = a_response().with_status(204)
        new_stubs['delete'] = stub_for(new_request).will_return(new_response)

        new_request = head(url_matching('/api/defined/head'))
        new_response = a_response().with_status(204)
        new_stubs['head'] = stub_for(new_request).will_return(new_response)

        new_request = trace(url_matching('/api/defined/trace'))
        new_response = a_response().with_status(204)
        new_stubs['trace'] = stub_for(new_request).will_return(new_response)

        new_request = options(url_matching('/api/defined/options'))
        new_response = a_response().with_status(204)
        new_stubs['options'] = stub_for(new_request).will_return(new_response)

        new_request = any(url_matching('/api/defined/any'))
        new_response = a_response().with_status(204)
        new_stubs['any'] = stub_for(new_request).will_return(new_response)

        return new_stubs

    def _create_scenario(self):
        stubs = {}

        new_request = get(url_matching('/todo/items'))
        new_response = a_response().with_body("Buy Milk")
        stubs['default'] = stub_for(new_request).in_scenario("To do list").when_scenario_state_is(STARTED)\
            .will_return(new_response)

        new_request = post(url_matching('/todo/items')).with_request_body(matching('Cancel newspaper subscription'))
        new_response = a_response().with_status(201)
        stubs['cancel'] = stub_for(new_request).in_scenario('To do list').when_scenario_state_is(STARTED)\
            .will_return(new_response).will_set_state_to('Cancel newspaper item added')

        new_request = get(url_matching('/todo/items'))
        new_response = a_response().with_body('Buy Milk, Cancel newspaper subscription')
        stubs['list'] = stub_for(new_request).in_scenario('To do list').when_scenario_state_is('Cancel newspaper item added').will_return(new_response)

        return stubs

    def _verify_scenario(self, scenario, expected_state):
        self.assertEqual(['Started', 'Cancel newspaper item added'], scenario['possibleStates'])
        self.assertEqual(expected_state, scenario['state'])
        self.assertEqual('To do list', scenario['name'])
