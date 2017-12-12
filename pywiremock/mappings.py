import json


class Mapping:
    def to_json(self):
        as_dict = self.serialize()
        return json.dumps(as_dict)

    def serialize(self):
        return self.__dict__


class Stub(Mapping):
    def __init__(self, request_pattern):
        assert isinstance(request_pattern, RequestPattern)
        self._request_pattern = request_pattern
        self._response_definition = None
        self._scenario_name = None
        self._required_scenario_state = None
        self._new_scenario_state = None

    def will_return(self, response_definition):
        assert isinstance(response_definition, ResponseDefinition)
        self._response_definition = response_definition
        return self

    def in_scenario(self, scenario_name):
        self._scenario_name = scenario_name
        return self

    def when_scenario_state_is(self, scenario_state):
        self._required_scenario_state = scenario_state
        return self

    def will_set_state_to(self, scenario_state):
        self._new_scenario_state = scenario_state
        return self

    def serialize(self):
        as_dict = {'request': self._request_pattern.serialize(), 'response': self._response_definition.serialize()}
        if self._scenario_name:
            as_dict['scenarioName'] = self._scenario_name
        if self._required_scenario_state:
            as_dict['requiredScenarioState'] = self._required_scenario_state
        if self._new_scenario_state:
            as_dict['newScenarioState'] = self._new_scenario_state
        return as_dict

    @classmethod
    def deserialize(cls, mapping, response_body=None):
        request_method = mapping['request']['method']
        request_url = mapping['request']['url']
        request_body_patterns = mapping['request'].get('bodyPatterns', [])
        request_headers = mapping['request'].get('headers', {})
        request = RequestPattern(request_method, UrlPattern(request_url))
        request.set_headers(request_headers)
        for body_pattern in request_body_patterns:
            new_pattern = RequestBodyPattern(None, None)
            new_pattern._pattern = body_pattern
            request.with_request_body(new_pattern)

        response_status = mapping['response']['status']
        response_headers = mapping['response'].get('headers', {})
        stringified_response_body = response_body
        response = ResponseDefinition(response_status, stringified_response_body, response_headers)

        stub = Stub(request).will_return(response)

        return stub


class RequestPattern(Mapping):
    def __init__(self, method, url_pattern):
        assert isinstance(url_pattern, UrlPattern)
        self._pattern = {'method': method, 'url': url_pattern.serialize()}
        self._headers = {}

    def set_headers(self, headers):
        self._headers = headers

    def with_header(self, name, value):
        self._headers[name] = {'equalTo': value}

    def without_header(self, name):
        self._headers[name] = {'absent': True}

    def with_query_param(self):
        raise NotImplementedError

    def with_request_body(self, request_body_pattern):
        assert isinstance(request_body_pattern, RequestBodyPattern)
        body_patterns = self._pattern.get('bodyPatterns', [])
        body_patterns.append(request_body_pattern.serialize())
        self._pattern['bodyPatterns'] = body_patterns
        return self

    def serialize(self):
        self._pattern['headers'] = self._headers
        return self._pattern


class RequestBodyPattern(Mapping):
    def __init__(self, body_content, matches):
        pattern_type = 'matches' if matches else 'doesNotMatch'
        self._pattern = {pattern_type: body_content}

    def serialize(self):
        return self._pattern


class ResponseDefinition(Mapping):
    def __init__(self, status_code=None, body=None, headers=None):
        self._status_code = status_code
        self._body = body
        self._headers = headers if headers else {}

    def with_status(self, status_code):
        self._status_code = status_code
        return self

    def with_body(self, body):
        self._body = body
        return self

    def with_header(self, key, value):
        self._headers[key] = value

    def with_body_file(self, body_file_path):
        raise NotImplementedError

    def serialize(self):
        as_dict = {'status': self._status_code}
        as_dict['headers'] = self._headers
        if self._body:
            as_dict['body'] = self._body

        return as_dict


class Scenario(Mapping):
    def __init__(self):
        pass


class UrlPattern(Mapping):
    def __init__(self, url):
        self._url = url

    def serialize(self):
        return self._url


class RecordSpec(Mapping):
    def __init__(self, url=None):
        self._url = url

    def serialize(self):
        as_dict = {"targetBaseUrl": self._url}
        return as_dict

    def for_target(self, url):
        self._url = url
        return self

    # TODO
    # startRecording(
    #     recordSpec()
    #         .forTarget("http://example.mocklab.io")
    #         .onlyRequestsMatching(getRequestedFor(urlPathMatching("/api/.*")))
    #         .captureHeader("Accept")
    #         .captureHeader("Content-Type", true)
    #         .extractBinaryBodiesOver(10240)
    #         .extractTextBodiesOver(2048)
    #         .makeStubsPersistent(false)
    #         .ignoreRepeatRequests()
    #         .transformers("modify-response-header")
    #         .transformerParameters(Parameters.one("headerValue", "123"))
    #         .matchRequestBodyWithEqualToJson(false, true)
    # );
