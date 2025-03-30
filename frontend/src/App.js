import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import { sendQueryToN8n, sendQueryToPython, getTestResponse } from './services/apiService';
import { formatResponse } from './utils/responseFormatter';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useTestData, setUseTestData] = useState(false);
  const [selectedServer, setSelectedServer] = useState('python');
  const [selectedModel, setSelectedModel] = useState('gemini');

  const handleSearch = async (query) => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      let response;
      if (useTestData) {
        response = await getTestResponse(query);
        response = response[0];  // 배열의 첫 번째 항목 추출
      } else {
        response = selectedServer === 'python' 
          ? await sendQueryToPython(query, selectedModel)
          : await sendQueryToN8n(query);
      }
      
      console.log('처리된 응답:', response);  // 디버깅용 로그 추가
      const formattedResponse = formatResponse(response);  // response.data를 전달하지 않고 response만 전달
      setResults(prev => [formattedResponse, ...prev]);
    } catch (error) {
      console.error('검색 에러:', error);
      setError('검색 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (index) => {
    setResults(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="App">
      <div className="header">
        <h1>AI 검색</h1>
        <div className="server-controls">
          <div className="server-selector">
            <label>
              <input
                type="radio"
                value="python"
                checked={selectedServer === 'python'}
                onChange={(e) => setSelectedServer(e.target.value)}
              />
              Python 백엔드
            </label>
            <label>
              <input
                type="radio"
                value="n8n"
                checked={selectedServer === 'n8n'}
                onChange={(e) => setSelectedServer(e.target.value)}
              />
              n8n
            </label>
          </div>
          {selectedServer === 'python' && (
            <div className="model-selector">
              <label>
                <input
                  type="radio"
                  value="gemini"
                  checked={selectedModel === 'gemini'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                Gemini
              </label>
              <label>
                <input
                  type="radio"
                  value="gpt-4o-mini"
                  checked={selectedModel === 'gpt-4o-mini'}
                  onChange={(e) => setSelectedModel(e.target.value)}
                />
                GPT-4o-mini
              </label>
            </div>
          )}
          <label>
            <input
              type="checkbox"
              checked={useTestData}
              onChange={(e) => setUseTestData(e.target.checked)}
            />
            테스트 모드
          </label>
        </div>
      </div>
      <SearchBar onSearch={handleSearch} loading={loading} />
      {error && <div className="error">{error}</div>}
      <SearchResults results={results} onDelete={handleDelete} />
    </div>
  );
}

export default App; 