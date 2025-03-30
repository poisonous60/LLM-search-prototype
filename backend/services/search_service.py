from serpapi.google_search import GoogleSearch
import os
import json
from models.search import SearchResults, SearchResult


def search_google(query: str) -> str:
    """
    Google 검색을 수행하여 관련 URL들을 반환합니다.
    
    Args:
        query (str): 검색어
        
    Returns:
        str: JSON 형식의 검색 결과 목록
    """
    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google",
        "q": query,
        "num": 8
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "organic_results" in results:
        search_results = []
        for result in results["organic_results"][:8]:
            search_results.append(SearchResult(
                title=result.get("title", ""),
                url=result.get("link", "")
            ))
        return SearchResults(results=search_results).model_dump_json()
    return SearchResults(results=[]).model_dump_json() 




# 테스트 데이터
TEST_SEARCH_RESULTS = {
    "results": [
        {"title": "인공지능과 딥러닝", "url": "https://m.yes24.com/goods/detail/23196334"},
        {"title": "인공지능·머신러닝·딥러닝 차이점은?ㅣ개념부터 ...", "url": "https://www.codestates.com/blog/content/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-%EB%94%A5%EB%9F%AC%EB%8B%9D%EA%B0%9C%EB%85%90"},
        {"title": "[AI란 무엇인가] 인공지능 머신러닝 딥러닝 차이점 총정리", "url": "https://hongong.hanbit.co.kr/ai-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5-%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-%EB%94%A5%EB%9F%AC%EB%8B%9D-%EC%B0%A8%EC%9D%B4%EC%A0%90-%EC%B4%9D%EC%A0%95%EB%A6%AC/"},
        {"title": "인공지능, 머신러닝, 딥러닝 개념", "url": "https://brunch.co.kr/@gdhan/10"},
        {"title": "인공지능과 딥러닝 | 마쓰오 유타카 - 국내도서 - 교보문고", "url": "https://product.kyobobook.co.kr/detail/S000001877733"},
        {"title": "[AI 완벽가이드] 인공지능, 머신러닝, 딥러닝 차이점 총정리", "url": "https://blog.naver.com/hanbitstory/223774062701"},
        {"title": "인공지능, 머신러닝, 딥러닝 - 무엇이 다를까?", "url": "https://blog.naver.com/qualcommkr/221123371711"},
        {"title": "딥 러닝이란 무엇인가요? - 딥 러닝 AI 설명", "url": "https://aws.amazon.com/ko/what-is/deep-learning/"}
    ]
}

def test_search_google(query: str) -> str:
    """
    테스트용 구글 검색 함수입니다.
    
    Args:
        query (str): 검색어
        
    Returns:
        str: JSON 형식의 검색 결과 목록
    """
    # 실제 검색어를 사용하여 테스트 데이터 생성
    search_results = []
    for i in range(8):
        search_results.append(SearchResult(
            title=f"{query} 검색결과 {i+1}",
            url=f"https://example.com/search/{query}/{i+1}"
        ))
    return SearchResults(results=search_results).model_dump_json()