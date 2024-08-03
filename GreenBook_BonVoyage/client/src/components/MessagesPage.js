// FollowersPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MessagesPage.css';

const MessagesPage = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/messages');
      setMessages(response.data);
    } catch (error) {
      console.error('Error fetching messages:', error);
      setError('Failed to fetch messages. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="messages-page">
      {isLoading && <div>Loading...</div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {messages.map(messages=> (
        <div key={messages.id} className="messages">
          <img src={messages.profilePhoto} alt={messages.name} />
          <p>{messages.name}</p>
        </div>
      ))}
    </div>
  );
};

export default MessagesPage;
