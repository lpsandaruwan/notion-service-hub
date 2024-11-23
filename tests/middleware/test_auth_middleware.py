from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI()


class MockSettings:
    APP_API_KEY = 'test_api_key'


app.add_middleware(AuthMiddleware)


@app.get('/protected')
async def protected_endpoint():
    return {'message': 'You have access'}


def test_auth_middleware_valid_key(monkeypatch):
    monkeypatch.setattr('app.config.settings', MockSettings())
    client = TestClient(app)
    headers = {'X-API-Key': 'f6473d3e-7074-4769-b69f-32c98827b28c'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 200
    assert response.json() == {'message': 'You have access'}


def test_auth_middleware_invalid_key(monkeypatch):
    monkeypatch.setattr('app.config.settings', MockSettings())
    client = TestClient(app)
    headers = {'X-API-Key': 'wrong_key'}
    response = client.get('/protected', headers=headers)
    assert response.status_code == 403
    assert response.json() == {'detail': 'Invalid API Key'}


def test_auth_middleware_missing_key(monkeypatch):
    monkeypatch.setattr('app.config.settings', MockSettings())
    client = TestClient(app)
    response = client.get('/protected')
    assert response.status_code == 403
    assert response.json() == {'detail': 'Invalid API Key'}
