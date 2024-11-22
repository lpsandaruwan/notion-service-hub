from typing import Any, Dict, Optional
import httpx


class AsyncHttpClient:
    """
    A HTTP client for asynchronous requests.
    """

    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        """
        Initialize the HTTP client.

        Args:
            client (Optional[httpx.AsyncClient]): Optionally provide a custom AsyncClient instance.
        """
        self._client = client or httpx.AsyncClient()

    async def get(self, url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        Perform a GET request.

        Args:
            url (str): The URL to request.
            headers (Dict[str, str]): The headers for the request.
            params (Optional[Dict[str, Any]]): Query parameters for the request.

        Returns:
            httpx.Response: The response from the server.
        """
        params = params or {}
        try:
            response = await self._client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while making GET request to {url}: {e}")

    async def post(self, url: str, headers: Dict[str, str], request_body: Dict[str, Any],
                   params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        Perform a POST request.
        """
        params = params or {}
        try:
            response = await self._client.post(url, headers=headers, json=request_body, params=params)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while making POST request to {url}: {e}")

    async def put(self, url: str, headers: Dict[str, str], request_body: Dict[str, Any],
                  params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """
        Perform a PUT request.
        """
        params = params or {}
        try:
            response = await self._client.put(url, headers=headers, json=request_body, params=params)
            response.raise_for_status()
            return response
        except httpx.RequestError as e:
            raise RuntimeError(f"An error occurred while making PUT request to {url}: {e}")

    async def close(self) -> None:
        """
        Close the HTTP client.
        """
        await self._client.aclose()

    async def __aenter__(self):
        """
        Support async context management.
        """
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Automatically close the client on exit.
        """
        await self.close()
