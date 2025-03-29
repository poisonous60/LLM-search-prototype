import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';

function SearchResults({ results, loading, error, onDelete }) {
  const [activeTab, setActiveTab] = useState('answer'); // 'answer' 또는 'sources'

  // URL에서 도메인 추출 함수
  const getDomain = (url) => {
    try {
      const domain = new URL(url).hostname;
      return domain.replace('www.', '');
    } catch (e) {
      return '';
    }
  };

  // 파비콘 URL 생성 함수
  const getFaviconUrl = (url) => {
    const domain = getDomain(url);
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`;
  };

  if (loading) {
    return <div className="loading">검색 중...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="search-results">
      {results.map((result, index) => (
        <div key={index} className="result-item">
          <button 
            className="delete-button"
            onClick={() => onDelete(index)}
            aria-label="답변 삭제"
          >
            ×
          </button>
          
          <div className="tabs">
            <button 
              className={`tab-button ${activeTab === 'answer' ? 'active' : ''}`}
              onClick={() => setActiveTab('answer')}
            >
              답변
            </button>
            <button 
              className={`tab-button ${activeTab === 'sources' ? 'active' : ''}`}
              onClick={() => setActiveTab('sources')}
            >
              출처
            </button>
          </div>

          <div className="tab-content">
            {activeTab === 'answer' && (
              <div className="response">
                <ReactMarkdown>{result.response}</ReactMarkdown>
              </div>
            )}
            {activeTab === 'sources' && result.links?.length > 0 && (
              <div className="links">
                <ul>
                  {result.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <img 
                        src={getFaviconUrl(link.url)} 
                        alt={`${getDomain(link.url)} favicon`}
                        className="favicon"
                        onError={(e) => {
                          e.target.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=';
                        }}
                      />
                      <a href={link.url} target="_blank" rel="noopener noreferrer">
                        {link.title}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default SearchResults; 