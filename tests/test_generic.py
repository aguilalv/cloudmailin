import pytest

def test_new(client):
    response = client.post('/generic/new',
                           json={'envelope':
                                  {'from':'test'},
                                 'headers':
                                  {'subject': 'test'}
                                 })
    assert response.data == b'Message from test about test'
