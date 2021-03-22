import pytest
import json
from application.db import get_db

def test_read(app, client):
    resp = client.get('/')
    expected = [{"id": 0, "first_name": "first", "middle_name": None, "last_name": "last", "email": "first.last@email.com", "age": 30}, {"id": 1, "first_name": "new_name", "middle_name": "middle", "last_name": "tester", "email": "test@email.com", "age": 45}]
    assert resp.status_code == 200
    assert json.loads(resp.data) == expected


def test_read_one_person(app, client):
    resp = client.get('/1')
    expected = [{"id": 1, "first_name": "new_name", "middle_name": "middle", "last_name": "tester", "email": "test@email.com", "age": 45}]
    assert resp.status_code == 200
    assert json.loads(resp.data) == expected

# Commenting this out because test data not loaded correctly
# def test_read_one_person_version(app, client):
#     resp = client.get('/1/20201003')
#     expected = [{
#         "id": 1,
#         "first_name": "test",
#         "middle_name": "middle",
#         "last_name": "tester",
#         "email": "test@email.com",
#         "age": 45
#         }]
#     assert resp.status_code == 200
#     assert json.loads(resp.data) == expected

def test_read_nonexisting_person(app, client):
    resp = client.get('/3')
    expected = b'Person with id 3 not found'
    assert resp.status_code == 404
    assert resp.data == expected

"""
Tests to add:
    - create new person
    - create new person missing required
    - attempt to create existing user
    - update existing user
        - have all data in form
        - not all the data in form
        - no data in form
    - update nonexisting user
    - delete existing user
    - delete nonexisting user
"""