import React, { useState } from 'react';

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="무엇이든 질문하기..."
        className="search-input"
        disabled={loading}
      />
      <button 
        type="submit" 
        className="search-button"
        disabled={loading}
      >
        {loading ? '검색 중...' : '검색'}
      </button>
    </form>
  );
}

export default SearchBar; 