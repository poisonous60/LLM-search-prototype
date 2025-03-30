from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Link(BaseModel):
    title: str = Field(description="링크의 제목")
    url: str = Field(description="링크의 URL")

class SearchResult(BaseModel):
    response: str = Field(description="검색 결과 텍스트")
    link: List[Link] = Field(description="참조 링크 목록")

class SearchResults(BaseModel):
    results: List[SearchResult] = Field(description="검색 결과 목록")

def get_llm(model_name: str = "gemini"):
    """선택된 모델에 따라 LLM을 반환합니다."""
    if model_name == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
    elif model_name == "gpt-4o-mini":
        return ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    else:
        raise ValueError(f"지원하지 않는 모델입니다: {model_name}")

def process_search_results(query: str, search_results: List[dict], model_name: str = "gemini") -> SearchResults:
    """검색 결과를 처리하고 요약합니다."""
    llm = get_llm(model_name)
    
    # 검색 결과를 텍스트로 변환
    search_text = "\n".join([
        f"제목: {result['title']}\nURL: {result['link']}\n내용: {result['snippet']}"
        for result in search_results
    ])
    
    # 검색 결과를 청크로 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.create_documents([search_text])
    
    # 요약 프롬프트 설정
    prompt_template = """다음 검색 결과를 바탕으로 사용자의 질문에 대한 답변을 작성해주세요.
    답변은 markdown 형식으로 작성해주세요.

    사용자 질문: {query}

    검색 결과:
    {text}

    답변:"""
    
    prompt = PromptTemplate.from_template(prompt_template)
    
    # 요약 체인 구성
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    
    # 요약 실행
    summary = stuff_chain.invoke({
        "query": query,
        "input_documents": docs
    })
    
    # 링크 추출
    links = [
        Link(
            title=result["title"],
            url=result["link"]
        )
        for result in search_results
    ]
    
    return SearchResults(
        results=[
            SearchResult(
                response=summary["output_text"],
                link=links
            )
        ]
    ) 