from fastapi import FastAPI

from app.config import settings
from app.routes.notion_crud_routes import notion_router
from app.utilities.auth_middleware import AuthMiddleware


app = FastAPI()

# Add the API key validation middleware
app.add_middleware(AuthMiddleware)

# Include your notion router
app.include_router(notion_router, prefix=settings.APP_BASE_PATH)
