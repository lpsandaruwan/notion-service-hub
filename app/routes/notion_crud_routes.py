from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.services.notion_service import NotionService
from app.utilities import LOG

notion_router = APIRouter()


@notion_router.get('/databases', response_model=List[Dict[str, Any]])
async def list_databases():
    """
    Fetch all databases in the Notion workspace, limited by API key's scope.
    """
    LOG.info('Request received to fetch databases list')
    async with NotionService() as service:
        try:
            databases = await service.list_databases()
            return databases
        except Exception as e:
            LOG.error('Error occurred while listing databases')
            raise HTTPException(status_code=500, detail=str(e))


@notion_router.get('/databases/{database_id}', response_model=Dict[str, Any])
async def get_database(database_id: str):
    """
    Retrieve database in the Notion workspace.
    """
    LOG.info(f'Request received to fetch database, {database_id}')
    async with NotionService() as service:
        try:
            database = await service.get_database(database_id)
            return database
        except Exception as e:
            LOG.error(f'Error occurred while retrieving database, {database_id}')
            raise HTTPException(status_code=500, detail=str(e))


@notion_router.get('/pages', response_model=List[Dict[str, Any]])
async def list_pages():
    """
    Fetch all pages in the Notion workspace, limited by API key's scope.
    """
    LOG.info(f'Request received to list all pages')
    async with NotionService() as service:
        try:
            pages = await service.list_pages()
            return pages
        except Exception as e:
            LOG.error(f'Error occurred while listing pages')
            raise HTTPException(status_code=500, detail=str(e))


@notion_router.post('/databases/{database_id}/pages', response_model=Dict[str, Any])
async def create_page(database_id: str, properties: Dict[str, Any]):
    """
    Create a new page (page) in a specific Notion database.

    Args:
        database_id: The ID of the database.
        properties: The properties of the page to create.

    Returns:
        The created page object.
    """
    LOG.info(f'Request received to create a page in {database_id}')
    async with NotionService() as service:
        try:
            page = await service.create_page(database_id, properties)
            return page
        except Exception as e:
            LOG.error(f'Error occurred while creating page in {database_id}')
            raise HTTPException(status_code=500, detail=str(e))
