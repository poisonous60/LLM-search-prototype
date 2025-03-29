from pydantic import BaseModel, Field
from typing import Optional

class APIResponse(BaseModel):
    success: bool = Field(description="요청 성공 여부")
    data: Optional[dict] = Field(description="응답 데이터", default=None)
    error: Optional[str] = Field(description="에러 메시지", default=None) 