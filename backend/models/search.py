from pydantic import BaseModel, Field
from typing import List

class SearchResult(BaseModel):
    title: str = Field(description="검색 결과의 제목")
    url: str = Field(description="검색 결과의 URL")

class SearchResults(BaseModel):
    results: List[SearchResult] = Field(description="검색 결과 목록") 