from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .errors import AuthenticationError
from .config import settings
from loguru import logger

security = HTTPBearer()

async def verify_api_key(credentials: HTTPAuthorizationCredentials = None):
    """Verify the API key from the Authorization header"""
    if not credentials:
        raise AuthenticationError("No API key provided")
    
    try:
        api_key = credentials.credentials
        if api_key != settings.OPENAI_API_KEY:
            raise AuthenticationError("Invalid API key")
        return api_key
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise AuthenticationError()

class APIKeyMiddleware:
    """Middleware to verify API key for protected routes"""
    def __init__(self, protected_paths: list[str] = None):
        self.protected_paths = protected_paths or ["/api/v1/rag/query"]

    async def __call__(self, request: Request, call_next):
        path = request.url.path
        
        if path in self.protected_paths:
            try:
                auth = request.headers.get("Authorization")
                if not auth or not auth.startswith("Bearer "):
                    raise AuthenticationError("No API key provided")
                
                api_key = auth.split(" ")[1]
                if api_key != settings.OPENAI_API_KEY:
                    raise AuthenticationError()
                    
            except Exception as e:
                logger.error(f"Authentication error: {str(e)}")
                raise AuthenticationError()
        
        response = await call_next(request)
        return response 