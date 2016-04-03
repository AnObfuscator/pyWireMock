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


def matching(body_content):
    return mappings.RequestBodyPattern(body_content, True)


def not_matching(body_content):
    return mappings.RequestBodyPattern(body_content, False)