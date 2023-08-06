# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import pytest
from azure.identity import EnvironmentCredential

from msgraph.core import GraphClient


@pytest.fixture
def graph_client():
    scopes = ['https://graph.microsoft.com/.default']
    credential = EnvironmentCredential()
    client = GraphClient(credential=credential, scopes=scopes)
    return client


def test_no_retry_success_response(graph_client):
    """
    Test that a request with valid http header and a success response is not retried
    """
    response = graph_client.get('https://graph.microsoft.com/v1.0/users')

    assert response.status_code == 200
    with pytest.raises(KeyError):
        response.request.headers["retry-attempt"]


def test_valid_retry_429(graph_client):
    """
    Test that a request with valid http header and 503 response is retried
    """
    response = graph_client.get('https://httpbin.org/status/429')

    assert response.status_code == 429
    assert response.request.headers["retry-attempt"] == "3"


def test_valid_retry_503(graph_client):
    """
    Test that a request with valid http header and 503 response is retried
    """
    response = graph_client.get('https://httpbin.org/status/503')

    assert response.status_code == 503
    assert response.request.headers["retry-attempt"] == "3"


def test_valid_retry_504(graph_client):
    """
    Test that a request with valid http header and 503 response is retried
    """
    response = graph_client.get('https://httpbin.org/status/504')

    assert response.status_code == 504
    assert response.request.headers["retry-attempt"] == "3"


def test_request_specific_options_override_default(graph_client):
    """
    Test that retry options passed to the request take precedence over
    the default options.
    """
    response_1 = graph_client.get('https://httpbin.org/status/429')
    response_2 = graph_client.get('https://httpbin.org/status/503', max_retries=2)
    response_3 = graph_client.get('https://httpbin.org/status/504')
    response_4 = graph_client.get('https://httpbin.org/status/429', max_retries=1)

    assert response_1.status_code == 429
    assert response_1.request.headers["Retry-Attempt"] == "3"
    assert response_2.status_code == 503
    assert response_2.request.headers["Retry-Attempt"] == "2"
    assert response_3.status_code == 504
    assert response_3.request.headers["Retry-Attempt"] == "3"
    assert response_4.status_code == 429
    assert response_4.request.headers["Retry-Attempt"] == "1"


def test_retries_time_limit(graph_client):
    """
    Test that the cumulative retry time plus the retry-after values does not exceed the
    provided retries time limit
    """

    response = graph_client.get('https://httpbin.org/status/503', retry_time_limit=0.1)

    assert response.status_code == 503
    headers = response.request.headers
    with pytest.raises(KeyError):
        response.request.headers["retry-attempt"]
