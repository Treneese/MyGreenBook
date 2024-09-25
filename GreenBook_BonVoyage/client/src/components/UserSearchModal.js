// UserSearchModal.js
import React, { useState } from 'react';
import axios from 'axios';
import './UserSearchModal.css'; // Create this CSS file for modal styles

const UserSearchModal = ({ isOpen, onClose, onStartConversation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/users/search', { params: { query: searchQuery } });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Error searching users:', error);
      setError('Failed to search users. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Find Users</h2>
        <input 
          type="text" 
          placeholder="Search users..." 
          value={searchQuery} 
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyUp={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
        />
        <button onClick={handleSearch}>Search</button>
        {isLoading && <div>Loading...</div>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div className="search-results">
          {searchResults.map((user) => (
            <div key={user.id} className="search-result-item">
              <img src={user.profile_picture} alt={user.username} />
              <span>{user.username}</span>
              <button onClick={() => onStartConversation(user)}>Start Conversation</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default UserSearchModal;
