from typing import Any, Dict, List
from app.config import settings
from app.utilities.async_http_client import AsyncHttpClient


class NotionService:
    """
    Service class for interacting with the Notion API.
    """

    def __init__(self):
        """
        Initialize the NotionService with base URL, headers, and HTTP client.
        """
        self.__base_url = settings.NOTION_BASE_URL
        self.__headers = {
            'Authorization': f'Bearer {settings.NOTION_API_KEY}',
            'Notion-Version': settings.NOTION_VERSION,
            'Content-Type': 'application/json',
        }
        self.__http_client = AsyncHttpClient()

    async def list_databases(self) -> List[Dict[str, Any]]:
        """
        List all databases in the Notion workspace.

        Returns:
            List[Dict[str, Any]]: A list of databases.
        """
        url = f'{self.__base_url}/search'
        response = await self.__http_client.post(url, headers=self.__headers, request_body={
            'filter': {
                'value': 'database',
                'property': 'object'
            }
        })
        return response.json().get('results', [])

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """
        Get Notion database by it's id.

        Returns:
            [Dict[str, Any]: A database object.
        """
        url = f'{self.__base_url}/databases/{database_id}'
        response = await self.__http_client.get(url, headers=self.__headers)
        return response.json().get('results', [])

    async def list_tasks(self, database_id: str) -> List[Dict[str, Any]]:
        """
        List all tasks (pages) in a specific Notion database.

        Args:
            database_id (str): The ID of the Notion database.

        Returns:
            List[Dict[str, Any]]: A list of tasks (pages) in the database.
        """
        url = f'{self.__base_url}/databases/{database_id}/query'
        response = await self.__http_client.post(url, headers=self.__headers, request_body={
            'filter': {
                'value': 'page',
                'property': 'object'
            }
        })
        return response.json().get('results', [])

    async def create_task(self, database_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new task (page) in a Notion database.

        Args:
            database_id (str): The ID of the Notion database.
            properties (Dict[str, Any]): The properties of the new task.

        Returns:
            Dict[str, Any]: The created task object.
        """
        url = f'{self.__base_url}/pages'
        request_body = {
            'parent': {'database_id': database_id},
            'properties': properties,
        }
        response = await self.__http_client.post(url, headers=self.__headers, request_body=request_body)
        return response.json()

    async def close(self) -> None:
        """
        Close the underlying HTTP client.
        """
        await self.__http_client.close()

    async def __aenter__(self):
        """
        Support async context management.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Automatically close the HTTP client on exit.
        """
        await self.close()
