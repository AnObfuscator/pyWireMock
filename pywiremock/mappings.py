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

    def will_return(self, response_definition):
        assert isinstance(response_definition, ResponseDefinition)
        self._response_definition = response_definition
        return self

    def serialize(self):
        return {'request': self._request_pattern.serialize(), 'response': self._response_definition.serialize()}

    @classmethod
    def deserialize(cls, mapping, response_body=None):
        request_method = mapping['request']['method']
        request_url = mapping['request']['url']
        request_body_patterns = mapping['request'].get('bodyPatterns', [])
        request = RequestPattern(request_method, UrlPattern(request_url))
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

    def with_header(self):
        raise NotImplementedError

    def without_header(self):
        raise NotImplementedError

    def with_query_param(self):
        raise NotImplementedError

    def with_request_body(self, request_body_pattern):
        assert isinstance(request_body_pattern, RequestBodyPattern)
        body_patterns = self._pattern.get('bodyPatterns', [])
        body_patterns.append(request_body_pattern.serialize())
        self._pattern['bodyPatterns'] = body_patterns
        return self

    def serialize(self):
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
