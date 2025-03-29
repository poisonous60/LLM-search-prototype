from fastapi import Request
from fastapi.responses import JSONResponse
from models.api import APIResponse
from services.langchain_service import process_query

async def webhook(request: Request):
    """
    POST 요청을 처리하는 웹훅 엔드포인트
    """
    try:
        data = await request.json()
        user_input = data.get("query", {}).get("userInput", "")
        
        if not user_input:
            return JSONResponse(
                status_code=400,
                content=APIResponse(
                    success=False,
                    error="사용자 입력이 필요합니다"
                ).model_dump()
            )
        
        # 쿼리 처리
        result = process_query(user_input)
        
        return JSONResponse(
            content=APIResponse(
                success=True,
                data=result
            ).model_dump()
        )
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=APIResponse(
                success=False,
                error=str(e)
            ).model_dump()
        )

async def search(query: str):
    """
    GET 요청을 처리하는 검색 엔드포인트
    """
    try:
        if not query:
            return JSONResponse(
                status_code=400,
                content=APIResponse(
                    success=False,
                    error="검색어를 입력해주세요"
                ).model_dump()
            )
        
        # 쿼리 처리
        result = process_query(query)
        
        return JSONResponse(
            content=APIResponse(
                success=True,
                data=result
            ).model_dump()
        )
    except Exception as e:
        print(f"Error in search: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=APIResponse(
                success=False,
                error=str(e)
            ).model_dump()
        ) 