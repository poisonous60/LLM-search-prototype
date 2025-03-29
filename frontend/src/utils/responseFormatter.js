/**
 * API 응답을 화면에 표시할 형식으로 변환
 * @param {Object} response - API 응답 데이터
 * @returns {Object} 포맷팅된 응답 데이터
 */
export const formatResponse = (response) => {
  if (!response || !response.data || !response.data[0]) {
    return {
      response: '응답 데이터가 없습니다.',
      links: []
    };
  }

  const result = response.data[0];
  
  // response가 객체이고 text 필드가 있는 경우 text 필드를 사용
  const responseText = result.response && typeof result.response === 'object' && 'text' in result.response
    ? result.response.text
    : result.response;
  
  return {
    response: responseText || '응답 텍스트가 없습니다.',
    links: result.link || []
  };
};

/**
 * 응답 데이터를 표시하기 위한 스타일 객체
 */
export const responseStyles = {
  whiteSpace: 'pre-wrap', // 줄바꿈과 공백 보존
  fontFamily: 'monospace', // 고정폭 폰트 사용
  textAlign: 'left', // 왼쪽 정렬
  backgroundColor: '#1a1a1a', // 어두운 배경색
  color: '#ffffff', // 흰색 텍스트
  padding: '1rem', // 내부 여백
  borderRadius: '4px', // 모서리 둥글게
  marginTop: '0.5rem', // 상단 여백
  boxShadow: '0 2px 4px rgba(0,0,0,0.2)', // 그림자 효과
  fontSize: '0.9rem', // 폰트 크기
  lineHeight: '1.5', // 줄 간격
}; 