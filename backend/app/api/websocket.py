from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, status
from app.core.dependencies import get_rag_service
from app.services.rag_service import RAGService
from app.core.security import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    rag_service: RAGService = Depends(get_rag_service)
):
    try:
        await get_current_user(token)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received query: {data}")
            
            # Streaming response
            async for message in rag_service.query_stream(data):
                await websocket.send_json(message)
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"type": "error", "payload": str(e)})
        except:
            pass
