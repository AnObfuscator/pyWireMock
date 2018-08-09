import mappings


def stub_for(request_mapping):
    return mappings.Stub(request_mapping)


def a_response():
    return mappings.ResponseDefinition()


def url_matching(url):
    return mappings.UrlPattern(url)


def get(url_pattern):
    return mappings.RequestPattern('GET', url_pattern)


def post(url_pattern):
    return mappings.RequestPattern('POST', url_pattern)


def put(url_pattern):
    return mappings.RequestPattern('PUT', url_pattern)


def delete(url_pattern):
    return mappings.RequestPattern('DELETE', url_pattern)


def head(url_pattern):
    return mappings.RequestPattern('HEAD', url_pattern)


def trace(url_pattern):
    return mappings.RequestPattern('TRACE', url_pattern)


def options(url_pattern):
    return mappings.RequestPattern('OPTIONS', url_pattern)


def any(url_pattern):
    return mappings.RequestPattern('ANY', url_pattern)


def matching(body_content):
    return mappings.RequestBodyPattern(body_content, RequestBodyMatchType.MATCHES)


def not_matching(body_content):
    return mappings.RequestBodyPattern(body_content, RequestBodyMatchType.DOES_NOT_MATCH)


def equal_to_xml(body_content):
    return mappings.RequestBodyPattern(body_content, RequestBodyMatchType.EQUAL_TO_XML)


def matches_xpath(body_content):
    return mappings.RequestBodyPattern(body_content, RequestBodyMatchType.MATCHES_XPATH)


def equal_to_json(body_content):
    return mappings.RequestBodyPattern(body_content, RequestBodyMatchType.EQUAL_TO_JSON)


def record_spec():
    return mappings.RecordSpec()


STARTED = 'Started'


class RequestBodyMatchType:
    MATCHES = 'matches'
    DOES_NOT_MATCH = 'doesNotMatch'
    EQUAL_TO_XML = 'equalToXml'
    MATCHES_XPATH = 'matchesXPath'
    EQUAL_TO_JSON = 'equalToJson'
