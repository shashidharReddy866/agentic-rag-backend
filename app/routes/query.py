from fastapi import APIRouter, HTTPException
from app.services.retriever import get_retriever
from app.services.agent import agent
import app.routes.upload as upload_route
import traceback

router = APIRouter()

@router.post("/query")
def query_system(query: str):
    if upload_route.VECTOR_DB is None:
        return {"error": "Upload a document first"}

    try:
        import json
        retriever = get_retriever(upload_route.VECTOR_DB)
        response = agent(query, retriever)
        
        try:
            json_response = json.loads(response)
            return json_response
        except:
            return {"answer": response}
    except Exception as e:
        trace_details = traceback.format_exc()
        print("ERROR:", trace_details)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
