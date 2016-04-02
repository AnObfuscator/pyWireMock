import json


class Mapping:
    def to_json(self):
        as_dict = self.serialize()
        return json.dumps(as_dict)

    def serialize(self):
        return self.__dict__


class Stub(Mapping):
    def __init__(self, request_pattern, response_definition, priority=None, scenario_name=None, required_scenario_state=None, scenario=None):
        self._request_pattern = request_pattern
        self._response_definition = response_definition

    def serialize(self):
        return {'request': self._request_pattern.build().serialize(), 'response': self._response_definition.serialize()}


class RequestPattern(Mapping):
    def __init__(self):
        self._pattern = {}

    def set_method(self, method):
        self._pattern['method'] = method

    def set_url_pattern(self, url_pattern):
        self._pattern['url'] = url_pattern.to_json()

    def set_body(self, body, matches=True):
        this_pattern = {}
        pattern_type = 'matches' if matches else 'doesNotMatch'
        this_pattern[pattern_type] = body
        body_patterns = self._pattern.get('bodyPatterns', [])
        body_patterns.append(this_pattern)
        self._pattern['bodyPatterns'] = body_patterns

    def serialize(self):
        return self._pattern


class ResponseDefinition(Mapping):
    def __init__(self, status_code, body):
        self._status_code = status_code
        self._body = body

    def serialize(self):
        return {'status': self._status_code, 'body': self._body}


class Scenario(Mapping):
    def __init__(self):
        pass


class UrlPattern(Mapping):
    def __init__(self, url):
        self._url = url

    def to_json(self):
        return self._url
