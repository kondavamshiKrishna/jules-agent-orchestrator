from fastapi import APIRouter
from app.services.jules_client import get_jules_client
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def list_sources():
    client = get_jules_client()
    try:
        # Wrap the synchronous SDK call in asyncio.to_thread as per memory guidelines
        resp = await asyncio.to_thread(client.list_sources)
        if not resp:
            return []

        sources = []
        # Parse the pydantic model returned by the SDK into dicts
        for s in getattr(resp, 'sources', getattr(resp, 'get', lambda *a: [])('sources', [])):
            sources.append({"id": getattr(s, 'id', getattr(s, 'get', lambda *a: '')('id')),
                            "name": getattr(s, 'name', getattr(s, 'get', lambda *a: '')('name'))})
        return sources
    except Exception as e:
        logger.exception("Failed to list sources: %s", e)
        return []
