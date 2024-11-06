import pytest


def test_home_route(web_client):
    response = web_client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to HyPrOps backend... We finna be cooking!!"}

def test_creating_user(web_client):
    data = {"username": "TestOnev",
            "password": "1234"}
    
    response = web_client.post('/users', json=data)
    assert response.status_code == 201
