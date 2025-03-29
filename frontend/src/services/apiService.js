import axios from 'axios';
import { testResponse } from '../data/testData';

// 환경 변수
const N8N_WEBHOOK_URL = process.env.REACT_APP_N8N_WEBHOOK_URL;
const PYTHON_BACKEND_URL = process.env.REACT_APP_PYTHON_BACKEND_URL;
const USE_TEST_DATA = process.env.REACT_APP_USE_TEST_DATA === 'true';

// 환경 변수 확인을 위한 로그
console.log('Environment Variables:', {
  N8N_WEBHOOK_URL,
  PYTHON_BACKEND_URL,
  USE_TEST_DATA
});

/**
 * n8n 웹훅으로 GET 요청을 보내는 함수
 * @param {string} query - 사용자 입력 검색어
 * @returns {Promise} API 응답
 */
export const sendQueryToN8n = async (query) => {
  if (!N8N_WEBHOOK_URL || N8N_WEBHOOK_URL === 'undefined' || N8N_WEBHOOK_URL === '') {
    console.error('Webhook URL is missing:', N8N_WEBHOOK_URL);
    throw new Error('웹훅 URL이 설정되지 않았습니다. .env 파일을 확인해주세요.');
  }
  
  const params = {
    userInput: query,
    timestamp: new Date().toISOString()
  };
  
  console.log('Request URL:', N8N_WEBHOOK_URL);
  console.log('Request params:', params);
  
  try {
    const response = await axios.get(N8N_WEBHOOK_URL, { 
      params,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.error('API 요청 실패:', error);
    throw error;
  }
};

/**
 * Python 백엔드 서버로 GET 요청을 보내는 함수
 * @param {string} query - 사용자 입력 검색어
 * @returns {Promise} API 응답
 */
export const sendQueryToPython = async (query) => {
  if (!PYTHON_BACKEND_URL || PYTHON_BACKEND_URL === 'undefined' || PYTHON_BACKEND_URL === '') {
    console.error('Python Backend URL is missing:', PYTHON_BACKEND_URL);
    throw new Error('Python 백엔드 URL이 설정되지 않았습니다. .env 파일을 확인해주세요.');
  }
  
  console.log('Request URL:', PYTHON_BACKEND_URL);
  console.log('Query:', query);
  
  try {
    const response = await axios.get(PYTHON_BACKEND_URL, { 
      params: { query },
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Response:', response);
    return response;
  } catch (error) {
    console.error('API 요청 실패:', error);
    throw error;
  }
};

/**
 * 테스트 모드에서 사용할 더미 응답 생성 함수
 * @param {string} query - 사용자 입력 검색어
 * @returns {Object} 테스트 응답
 */
export const getTestResponse = (query) => {
  console.log('=== 테스트 모드 응답 ===');
  console.log('입력 쿼리:', query);
  console.log('테스트 데이터:', testResponse);
  return testResponse;  // data 필드로 감싸지 않고 직접 반환
}; 