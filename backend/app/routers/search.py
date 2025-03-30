from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services.search_service import search_google
from ..services.langchain_service import process_search_results, SearchResults
from ..models.api import APIResponse

router = APIRouter()

class SearchQuery(BaseModel):
    userInput: str
    model: str = "gemini"  # 기본값은 gemini

@router.post("/webhook", response_model=APIResponse)
async def webhook(query: SearchQuery):
    try:
        # 검색 실행
        search_results = search_google(query.userInput)
        
        # 검색 결과 처리
        processed_results = process_search_results(
            query=query.userInput,
            search_results=search_results,
            model_name=query.model
        )
        
        return APIResponse(
            success=True,
            data=processed_results.results[0],  # 첫 번째 결과만 반환
            error=None
        )
    except Exception as e:
        return APIResponse(
            success=False,
            data=None,
            error=str(e)
        ) 