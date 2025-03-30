from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.output_parsers import PydanticOutputParser
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from services.search_service import search_google, test_search_google
from models.search import SearchResults
import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
from typing import List

# 환경 변수 로드
load_dotenv()

# LangChain 설정
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# 메모리 설정
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# langchain의 WebBaseLoader를 사용하여 웹 페이지 내용 가져오기
# 시간 오래 걸려서 주석 처리리
# def fetch_url_content(urls: List[str]) -> List[str]:
#     """
#     URL들의 내용을 WebBaseLoader를 사용하여 가져옵니다.
    
#     Args:
#         urls (List[str]): URL 주소 목록
        
#     Returns:
#         List[str]: 웹페이지 내용 목록
#     """
#     try:
#         # WebBaseLoader로 웹 페이지 내용 로드
#         loader = WebBaseLoader(urls)
#         docs = loader.load()
        
#         # 문서 분할
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200,
#             length_function=len,
#         )
#         splits = text_splitter.split_documents(docs)
        
#         # 임베딩 생성
#         embeddings = GoogleGenerativeAIEmbeddings(
#             model="models/embedding-001",
#             google_api_key=os.getenv("GOOGLE_API_KEY")
#         )
        
#         # 벡터 저장소 생성
#         vectorstore = FAISS.from_documents(splits, embeddings)
        
#         return [doc.page_content for doc in splits]
#     except Exception as e:
#         print(f"URL 내용 가져오기 실패: {urls}")
#         print(f"에러: {str(e)}")
#         return []

def fetch_url_content(url: str) -> str:
    """
    URL의 내용을 가져옵니다.
    
    Args:
        url (str): URL 주소
        
    Returns:
        str: 웹페이지 내용
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 불필요한 요소 제거
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript', 'meta', 'link', 'aside', 'form', 'button', 'input', 'select', 'textarea']):
            element.decompose()
            
        # 주요 내용 추출
        main_content = ""
        
        # 1. 메인 콘텐츠 영역 찾기
        main_content_candidates = [
            # article 태그
            soup.find('article'),
            # main 태그
            soup.find('main'),
            # content 관련 div
            *[div for div in soup.find_all('div') if any(keyword in div.get('class', []) for keyword in ['content', 'article', 'post', 'entry', 'main', 'detail', 'description'])],
            # body 태그
            soup.body
        ]
        
        # 2. 가장 적절한 콘텐츠 선택
        for candidate in main_content_candidates:
            if candidate:
                text = candidate.get_text(strip=True)
                # 텍스트가 너무 짧거나 너무 길면 건너가기
                if 100 < len(text) < 10000:
                    main_content = text
                    break
        
        # 3. 모든 텍스트를 가져옴
        if not main_content:
            main_content = soup.get_text(strip=True)
        
        # 텍스트 정리
        lines = [line.strip() for line in main_content.split('\n') if line.strip()]
        content = ' '.join(lines)
        
        # 내용이 너무 길 경우 앞부분만 사용
        if len(content) > 4000:
            content = content[:4000] + "..."
            
        return content
    except Exception as e:
        print(f"URL 내용 가져오기 실패: {url}")
        print(f"에러: {str(e)}")
        return ""

def summarize_content(content: str) -> str:
    """
    웹페이지 내용을 요약합니다.
    
    Args:
        content (str): 웹페이지 내용
        
    Returns:
        str: 요약된 내용
    """
    prompt = f"""link에 들어가서 안의 내용을 markdown 형식으로 요약해:

{content}

CONCISE SUMMARY:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"내용 요약 실패: {str(e)}")
        return ""

def summarize_all(summaries: list) -> str:
    """
    모든 요약 내용을 종합하여 하나의 요약문을 생성합니다.
    
    Args:
        summaries (list): 각 링크의 요약 내용 목록
        
    Returns:
        str: 종합된 요약문
    """
    combined_text = "\n\n".join(summaries)
    prompt = f"""link를 요약한 결과를 바탕으로 userInput에 대해 markdown 형식으로 답변해:

{combined_text}

CONCISE SUMMARY:

### 아래 내용을 지켜서 답변해줘:
1. 존댓말로 써
2. 요약', '정리' 같은 단어를 넣지 마
3. 처음에 네가 한 행동을 말하지 말고 userInput에 대한 내용을 바로 설명해
4. 일반적으로 모든 경우에 적용되는 답변은 하지 말고 검색한 내용을 바탕으로 구체적으로 답변해
5. 여러 경우나 사례가 있을 경우 긴 줄글로 답변하지 말고 markdown 형식을 이용해서 나눠서 답변해
6. 마지막에 추가 질문 부탁, 도움이 되었으면 좋겠다 같이 요구나 명령, 희망하는 늬양스의 말 하지 말고 본론만 말하고 끝내"""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"종합 요약 실패: {str(e)}")
        return ""

# 도구 정의
tools = [
    Tool(
        name="search",
        func=search_google,  # 테스트 함수 대신 실제 검색 함수 사용
        description="구글 검색을 수행하여 관련 URL들을 반환합니다."
    )
]

# 프롬프트 템플릿
system_prompt = """태그와 검색어를 기반으로 구글 검색을 통해 관련도 순으로 8개의 url을 나열해줘.
검색 결과는 다음 형식의 JSON으로 반환해주세요:
{{
    "results": [
        {{
            "title": "검색 결과 제목",
            "url": "검색 결과 URL"
        }}
    ]
}}
단, 검색은 딱 한번만 해."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 에이전트 생성
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

def process_query(query: str) -> List[dict]:
    """
    사용자 쿼리를 처리하고 검색 결과를 반환합니다.
    
    Args:
        query (str): 사용자 입력 쿼리
        
    Returns:
        List[dict]: 처리된 결과 리스트
    """
    try:
        print(f"\n=== 쿼리 처리 시작 ===")
        print(f"입력 쿼리: {query}")
        
        # 정보 추출 (태그와 검색어)
        extraction_prompt = f"""
        다음 텍스트에서 태그와 검색어를 추출해주세요:
        {query}
        
        태그는 주제나 카테고리를 나타내는 키워드이고,
        검색어는 실제 검색에 사용할 구체적인 키워드입니다.
        """
        
        print("\n=== 태그/검색어 추출 시작 ===")
        extraction_response = llm.invoke(extraction_prompt)
        extracted_info = extraction_response.content
        print(f"추출된 정보: {extracted_info}")
        
        # 추출이 어려운 경우 체크
        if any(phrase in extracted_info for phrase in [
            "추출하기는 어렵습니다",
            "텍스트가 제공되지 않았습니다",
            "텍스트를 제공해 주시면",
            "입력된 텍스트가 없습니다",
            "텍스트가 비어있습니다",
            "검색어가 너무 짧습니다",
            "검색어가 모호합니다"
        ]):
            return [{
                "response": "검색어가 너무 짧거나 모호합니다. 더 구체적인 검색어를 입력해주세요.",
                "link": []
            }]
        
        # 에이전트 실행
        print("\n=== 에이전트 실행 시작 ===")
        agent_input = f"태그: {extracted_info}\n검색어: {query}"
        print(f"에이전트 입력: {agent_input}")
        
        agent_response = agent_executor.invoke({
            "input": agent_input
        })
        print(f"에이전트 출력: {agent_response['output']}")
        
        # 결과 파싱
        print("\n=== 결과 파싱 시작 ===")
        output_parser = PydanticOutputParser(pydantic_object=SearchResults)
        parsed_results = output_parser.parse(agent_response["output"])
        print(f"파싱된 결과: {parsed_results.model_dump()}")
        
        # URL 내용 가져오기
        print("\n=== URL 내용 수집 시작 ===")
        urls = [result.url for result in parsed_results.results]
        all_content = fetch_url_content(urls)
        results_with_refs = [{
            "title": result.title,
            "url": result.url
        } for result in parsed_results.results]
        
        # 모든 내용을 기반으로 하나의 답변 생성
        print("\n=== 답변 생성 시작 ===")
        combined_content = "\n\n".join(all_content)
        prompt = f"""다음 내용을 바탕으로 '{query}'에 대해 답변해주세요:

{combined_content}

### 아래 내용을 지켜서 답변해줘:
1. 존댓말로 써
2. 요약', '정리' 같은 단어를 넣지 마
3. 처음에 네가 한 행동을 말하지 말고 userInput에 대한 내용을 바로 설명해
4. 일반적으로 모든 경우에 적용되는 답변은 하지 말고 검색한 내용을 바탕으로 구체적으로 답변해
5. 여러 경우나 사례가 있을 경우 긴 줄글로 답변하지 말고 markdown 형식을 이용해서 나눠서 답변해
6. 마지막에 추가 질문 부탁, 도움이 되었으면 좋겠다 같이 요구나 명령, 희망하는 늬양스의 말 하지 말고 본론만 말하고 끝내"""

        final_response = llm.invoke(prompt)
        print(f"최종 답변: {final_response.content}")
        
        return [{
            "response": final_response.content,
            "link": results_with_refs
        }]
        
    except Exception as e:
        print(f"처리 중 오류 발생: {str(e)}")
        return [{
            "response": f"죄송합니다. 처리 중 오류가 발생했습니다: {str(e)}",
            "link": []
        }] 