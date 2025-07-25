import uvicorn
from backend.config import settings

if __name__ == "__main__":
    uvicorn.run("backend.api:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
