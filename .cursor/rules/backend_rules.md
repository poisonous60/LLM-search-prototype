# 백엔드 개발 규칙

## 1. API 엔드포인트 규칙
- 모든 API 엔드포인트는 `/api/v1/` 접두사를 사용합니다
- HTTP 메서드는 RESTful 규칙을 따릅니다 (GET, POST, PUT, DELETE)
- 현재 구현된 `/api/v1/webhook` 엔드포인트는 POST 메서드를 사용하여 데이터를 받습니다

## 2. API 응답 형식
- 모든 응답은 `APIResponse` Pydantic 모델을 따릅니다:
  ```python
  {
    "success": bool,      # 요청 성공 여부
    "data": dict,         # 성공 시 응답 데이터
    "error": str          # 실패 시 에러 메시지
  }
  ```

- 검색 API (`/api/v1/search`) 응답 형식:
  ```python
  {
    "data": {
      "response": str,    # 검색 결과 텍스트
      "link": [          # 참조 링크 목록
        {
          "title": str,  # 링크 제목
          "url": str     # 링크 URL
        }
      ]
    }
  }
  ```

- HTTP 상태 코드:
  - 200: 성공
  - 400: 잘못된 요청 (예: 필수 파라미터 누락)
  - 500: 서버 내부 오류

## 3. 에러 처리
- 모든 API 엔드포인트는 try-except 블록으로 감싸져 있어 예외 처리가 되어 있습니다
- 예외 발생 시 적절한 에러 메시지와 함께 500 상태 코드를 반환합니다
- 입력값 검증이 필요한 경우 400 상태 코드를 반환합니다

## 4. 환경 변수
- 모든 민감한 정보(API 키 등)는 `.env` 파일에서 관리됩니다
- `load_dotenv()`를 통해 환경 변수를 로드합니다

## 5. CORS 설정
- 개발 환경에서는 모든 출처를 허용합니다
- 프로덕션 환경에서는 필요한 출처만 허용하도록 설정해야 합니다

## 6. 코드 구조
- FastAPI를 사용하여 API 서버를 구현합니다
- Pydantic 모델을 사용하여 데이터 검증을 수행합니다
- LangChain을 사용하여 AI 기능을 구현합니다
- 모든 외부 API 호출은 try-except 블록으로 감싸서 에러 처리를 합니다 