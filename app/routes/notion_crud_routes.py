from fastapi import APIRouter, HTTPException
from app.services.notion_service import NotionService
from typing import Any, Dict, List

from app.utilities import LOG


notion_router = APIRouter()

@notion_router.get('/databases', response_model=List[Dict[str, Any]])
async def list_databases():
    """
    Fetch all databases in the Notion workspace.
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

@notion_router.get('/databases/{database_id}/tasks', response_model=List[Dict[str, Any]])
async def list_tasks(database_id: str):
    """
    Fetch all tasks (pages) in a specific database.
    """
    LOG.info(f'Request received to fetch pages list in {database_id}')
    async with NotionService() as service:
        try:
            tasks = await service.list_tasks(database_id)
            return tasks
        except Exception as e:
            LOG.error(f'Error occurred while listing pages in {database_id}')
            raise HTTPException(status_code=500, detail=str(e))

@notion_router.post('/databases/{database_id}/tasks', response_model=Dict[str, Any])
async def create_task(database_id: str, properties: Dict[str, Any]):
    """
    Create a new task (page) in a specific Notion database.

    Args:
        database_id: The ID of the database.
        properties: The properties of the task to create.

    Returns:
        The created task object.
    """
    LOG.info(f'Request received to create a page in {database_id}')
    async with NotionService() as service:
        try:
            task = await service.create_task(database_id, properties)
            return task
        except Exception as e:
            LOG.error(f'Error occurred while creating task in {database_id}')
            raise HTTPException(status_code=500, detail=str(e))
