import json

import pytest
from werkzeug.wrappers import Request, Response

from vercel_python_wsgi import handler


# Test applications

@Request.application
def application(request):
    return Response(json.dumps({
        'args': request.args,
        'query_string': request.query_string.decode('utf-8')
    }))


@Request.application
def multivalue_cookie_application(request):
    response = Response('Check cookies')
    response.set_cookie('cookie_1', 'value_1')
    response.set_cookie('cookie_2', 'value_2')
    return response


# Event helpers

def prep_event(event):
    event['body'] = json.dumps(event['body'])
    return event


def update_body(event, **kwargs):
    body = event['body']
    for key, value in kwargs.items():
        body[key] = value
    event['body'] = body
    return event


# Event fixtures

@pytest.fixture
def get_event():
    return {
        'Action': 'Invoke',
        'body': {
            'headers': {
                'accept': ('text/html,application/xhtml+xml,application/xml;'
                           'q=0.9,image/webp,image/apng,*/*;q=0.8'),
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'connection': 'close',
                'host': 'python-wsgi-test.now.sh',
                'internal-lambda-name': 'insecure-lambda-name',
                'internal-lambda-region': 'iad1',
                'referer': 'https://zeit.co/',
                'upgrade-insecure-requests': '1',
                'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X '
                               '10_14_3) AppleWebKit/537.36 (KHTML, '
                               'like Gecko) Chrome/72.0.3626.119 '
                               'Safari/537.36'),
                'x-forwarded-for': '255.255.255.255',
                'x-forwarded-host': 'python-wsgi-test.now.sh',
                'x-forwarded-proto': 'https',
                'x-now-deployment-url': 'python-wsgi-test.now.sh',
                'x-now-id': 'insecure-now-id',
                'x-now-log-id': 'insecure-now-log-id',
                'x-now-trace': 'iad1',
                'x-real-ip': '255.255.255.255',
                'x-zeit-co-forwarded-for': '255.255.255.255'
            },
            'host': 'python-wsgi-test.now.sh',
            'method': 'GET',
            'path': '/'
        },
    }


# Tests

def test_vercel_handler_get_request(get_event):
    response = handler(application, prep_event(get_event), None)
    assert response['statusCode'] == 200


def test_vercel_handler_querystring(get_event):
    event = update_body(get_event, path='/?param%3Dvalue%26param2%3Dvalue2')
    response = handler(application, prep_event(event), None)
    assert response['statusCode'] == 200

    request_data = json.loads(response['body'])
    assert request_data['args'] == {'param': 'value', 'param2': 'value2'}


def test_vercel_handler_multivalue_cookies(get_event):
    response = handler(multivalue_cookie_application, prep_event(get_event),
                       None)
    assert response['statusCode'] == 200
    assert 'Set-Cookie' in response['headers']
    assert response['headers']['Set-Cookie'] == [
        'cookie_1=value_1; Path=/',
        'cookie_2=value_2; Path=/',
    ]
