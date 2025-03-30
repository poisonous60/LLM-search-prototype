

### 백엔드
- Python
- FastAPI
- LangChain
- OpenAI API

### 프론트엔드
- React
- React Markdown
- CSS

## 설치 및 실행

### 백엔드 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 필요한 API 키 설정

# 서버 실행
uvicorn main:app --reload
```

### 프론트엔드 설정
```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env
# .env 파일에 필요한 환경 변수 설정

# 개발 서버 실행
npm start
```

## 환경 변수

### 백엔드 (.env)
```
OPENAI_API_KEY=your_openai_api_key
```

### 프론트엔드 (.env)
```
REACT_APP_PYTHON_BACKEND_URL=http://localhost:8000
REACT_APP_USE_TEST_DATA=false
```

## 라이선스

MIT License 