from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.langchain_service import process_query

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수 확인
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 특정 도메인만 허용하도록 수정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/search")
async def search(query: str):
    """
    검색 쿼리를 처리하고 결과를 반환합니다.
    
    Args:
        query (str): 검색 쿼리
        
    Returns:
        dict: 검색 결과
    """
    try:
        print(f"\n=== 검색 요청 시작 ===")
        print(f"입력 쿼리: {query}")
        
        result = process_query(query)
        print(f"처리 결과: {result}")
        
        return result[0]
    except Exception as e:
        print(f"\n=== 에러 발생 ===")
        print(f"에러 타입: {type(e)}")
        print(f"에러 메시지: {str(e)}")
        import traceback
        print(f"스택 트레이스:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 