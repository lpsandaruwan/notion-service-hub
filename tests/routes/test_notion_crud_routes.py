from unittest.mock import AsyncMock, patch, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routes.notion_crud_routes import notion_router

app = FastAPI()
app.include_router(notion_router)
client = TestClient(app)


class AsyncContextManagerMock:
    def __init__(self, async_mock):
        self.async_mock = async_mock

    async def __aenter__(self):
        return self.async_mock

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass


@pytest.fixture
def mock_notion_service():
    service_mock = AsyncMock()
    async_context = AsyncContextManagerMock(service_mock)
    factory_mock = MagicMock()
    factory_mock.return_value = async_context

    with patch('app.routes.notion_crud_routes.NotionService', factory_mock):
        yield service_mock


def test_list_databases_success(mock_notion_service):
    mock_database = {
        "object": "database",
        "id": "14563f5f-6fb7-8012-a496-f933e8a0ae69",
        "cover": None,
        "icon": {
            "type": "external",
            "external": {
                "url": "/images/app-packages/task-db-icon.svg"
            }
        },
        "created_time": "2024-11-21T05:50:00.000Z",
        "created_by": {
            "object": "user",
            "id": "145d872b-594c-8130-8c50-0002d233bc00"
        },
        "last_edited_by": {
            "object": "user",
            "id": "145d872b-594c-8130-8c50-0002d233bc00"
        },
        "last_edited_time": "2024-11-22T19:00:00.000Z",
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Tasks",
                    "link": None
                },
                "annotations": {
                    "bold": False,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": False,
                    "color": "default"
                },
                "plain_text": "Tasks",
                "href": None
            }
        ],
        "description": [],
        "is_inline": False,
        "properties": {
            "Task name": {
                "id": "title",
                "name": "Task name",
                "type": "title",
                "title": {}
            }
        },
        "parent": {
            "type": "workspace",
            "workspace": True
        },
        "url": "https://www.notion.so/14563f5f6fb78012a496f933e8a0ae69",
        "archived": False,
        "in_trash": False
    }

    mock_notion_service.list_databases.return_value = [mock_database]
    response = client.get("/databases")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["id"] == "14563f5f-6fb7-8012-a496-f933e8a0ae69"
    assert response_data[0]["object"] == "database"
    assert mock_notion_service.list_databases.call_count == 1


def test_get_database_success(mock_notion_service):
    mock_database = {
        "object": "database",
        "id": "14563f5f-6fb7-8012-a496-f933e8a0ae69",
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Tasks",
                    "link": None
                }
            }
        ],
        "properties": {
            "Task name": {
                "id": "title",
                "name": "Task name",
                "type": "title",
                "title": {}
            }
        }
    }

    mock_notion_service.get_database.return_value = mock_database
    database_id = "14563f5f-6fb7-8012-a496-f933e8a0ae69"
    response = client.get(f"/databases/{database_id}")

    assert response.status_code == 200
    assert response.json()["id"] == database_id
    mock_notion_service.get_database.assert_called_once_with(database_id)


def test_list_pages_success(mock_notion_service):
    mock_pages = [{
        "object": "page",
        "id": "14663f5f-6fb7-8060-8751-e7d52e0116e1",
        "created_time": "2024-11-22T17:05:00.000Z",
        "last_edited_time": "2024-11-22T17:05:00.000Z",
        "created_by": {
            "object": "user",
            "id": "145d872b-594c-8130-8c50-0002d233bc00"
        },
        "last_edited_by": {
            "object": "user",
            "id": "145d872b-594c-8130-8c50-0002d233bc00"
        },
        "cover": None,
        "icon": {
            "type": "external",
            "external": {
                "url": "https://www.notion.so/icons/clipping_lightgray.svg"
            }
        },
        "parent": {
            "type": "database_id",
            "database_id": "14563f5f-6fb7-8012-a496-f933e8a0ae69"
        },
        "archived": False,
        "properties": {
            "Task name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Sample Task",
                            "link": None
                        }
                    }
                ]
            }
        }
    }]
    mock_notion_service.list_pages.return_value = mock_pages
    response = client.get("/pages")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["id"] == "14663f5f-6fb7-8060-8751-e7d52e0116e1"
    assert response_data[0]["object"] == "page"
    assert mock_notion_service.list_pages.call_count == 1
