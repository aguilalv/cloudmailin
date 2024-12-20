import pytest

from flask import jsonify

def test_new(client):

    email_data = {'envelope':{'from':'test'},
                  'headers' :{'subject': 'test'}
                 }

    response = client.post('/generic/new',
                           json=email_data)

    assert response.json == {'sender':'test','subject':'test'}
