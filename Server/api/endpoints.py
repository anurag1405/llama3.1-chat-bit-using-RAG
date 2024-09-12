from fastapi import APIRouter,HTTPException
from models.query import Query
from models.file import TextPayload
from services.agent_service import handle_agent_query
from utils.vector_store import add_file_to_vector_store



router = APIRouter()

@router.post("/query")
async def query_endpoint(query: Query):
    result = await handle_agent_query(query)
    return result

@router.post("/uploadfile")
async def upload_file_endpoint(payload: TextPayload):
    text = payload.text
    if text:
        result = add_file_to_vector_store(text)
        return {"message": f"File content added and retriever updated: {result}"}
    else:
        raise HTTPException(status_code=400, detail="No text provided.")
