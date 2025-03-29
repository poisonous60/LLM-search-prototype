import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import { sendQueryToN8n, sendQueryToPython, getTestResponse } from './services/apiService';
import { formatResponse } from './utils/responseFormatter';

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useTestData, setUseTestData] = useState(false);
  const [selectedServer, setSelectedServer] = useState('python'); // 'n8n'에서 'python'으로 변경

  const handleSearch = async (query) => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      
      if (useTestData) {
        response = getTestResponse(query);
        response = response[0];  // 배열의 첫 번째 항목 추출
      } else {
        if (selectedServer === 'n8n') {
          response = await sendQueryToN8n(query);
          response = response.data[0];
        } else {
          response = await sendQueryToPython(query);
          response = response.data;
        }
      }
      
      console.log('처리된 응답:', response);  // 디버깅용 로그 추가
      const formattedResponse = formatResponse({ data: [response] });
      setResults(prev => [formattedResponse, ...prev]);
    } catch (err) {
      setError(err.message);
      console.error('검색 중 오류 발생:', err);
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
        <div className="server-controls">
          <label>
            <input
              type="checkbox"
              checked={useTestData}
              onChange={(e) => setUseTestData(e.target.checked)}
            />
            테스트 모드
          </label>
          <div className="server-selector">
            <label>
              <input
                type="radio"
                name="server"
                value="n8n"
                checked={selectedServer === 'n8n'}
                onChange={(e) => setSelectedServer(e.target.value)}
              />
              n8n
            </label>
            <label>
              <input
                type="radio"
                name="server"
                value="python"
                checked={selectedServer === 'python'}
                onChange={(e) => setSelectedServer(e.target.value)}
              />
              Python
            </label>
          </div>
        </div>
      </div>
      <SearchBar onSearch={handleSearch} loading={loading} />
      <SearchResults 
        results={results} 
        loading={loading} 
        error={error} 
        onDelete={handleDelete}
      />
    </div>
  );
}

export default App; 