/**
 * API 응답을 화면에 표시할 형식으로 변환
 * @param {Object} response - API 응답 데이터
 * @returns {Object} 포맷팅된 응답 데이터
 */
export const formatResponse = (response) => {
  console.log('원본 응답:', response);
  
  // axios 응답에서 data 필드의 내용만 추출
  let data = response.data || response;
  // data 타입이 array인 경우 첫 번째 요소를 사용
  if (Array.isArray(data)) {
    data = data[0];
  }

  console.log('data 필드:', data);
  
  if (!data || !data.response) {
    console.log('데이터 없음');
    return {
      response: '응답 데이터가 없습니다.',
      link: []
    };
  }
  
  // response가 객체이고 text 필드가 있는 경우 text 필드를 사용
  const responseText = data.response && typeof data.response === 'object' && 'text' in data.response
    ? data.response.text
    : data.response;
  
  const result = {
    response: responseText || '응답 텍스트가 없습니다.',
    link: data.link || []
  };
  
  console.log('처리된 결과:', result);
  return result;
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