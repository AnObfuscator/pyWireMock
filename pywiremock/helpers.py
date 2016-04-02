import mappings


class Stub:
    @classmethod
    def create_with(cls, request_mapping, response_mapping):
        return mappings.Stub(request_mapping, response_mapping)


class Request:
    @classmethod
    def where(cls, method, url_match):
        return RequestPatternBuilder(method, url_match)

    # def for_all():
    #     return RequestPatternBuilder()


class Response:
    @classmethod
    def that_is(cls, status, body):
        return mappings.ResponseDefinition(status, body)


class Url:
    @classmethod
    def matches(cls, url):
        return mappings.UrlPattern(url)


class Method:
    @classmethod
    def is_post(cls):
        return 'POST'

    @classmethod
    def is_get(cls):
        return 'GET'

    @classmethod
    def is_put(cls):
        return 'PUT'

    @classmethod
    def is_delete(cls):
        return 'DELETE'


class RequestPatternBuilder:
    def __init__(self, method, url_pattern):
        self.request_pattern = mappings.RequestPattern()
        self.request_pattern.set_method(method)
        self.request_pattern.set_url_pattern(url_pattern)

    def with_header(self):
        return self

    def without_header(self):
        return self

    def with_query_param(self):
        return self

    def with_request_body(self, body):
        self.request_pattern.set_body(body)
        return self

    def build(self):
        return self.request_pattern