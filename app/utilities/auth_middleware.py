from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != settings.APP_API_KEY:
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API Key"}
            )
        response = await call_next(request)
        return response