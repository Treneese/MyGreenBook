// MessagesPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Conversation from './Conversation';
import UserSearchModal from './UserSearchModal';
import './MessagesPage.css';

const MessagesPage = () => {
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newConversationUser, setNewConversationUser] = useState(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      setIsLoading(true);
      const userId = 1; // Replace with the actual user ID from authentication or context
      const response = await axios.get('/conversations', {
        params: { user_id: userId }
      });
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations:', error);
      setError('Failed to fetch conversations. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchMessages = async (conversation) => {
    try {
      setIsLoading(true);
      const response = await axios.get(`/api/messages/${conversation.id}`);
      setMessages(response.data.messages);
    } catch (error) {
      console.error('Error fetching messages:', error);
      setError('Failed to fetch messages. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectConversation = (conversation) => {
    setSelectedConversation(conversation);
    fetchMessages(conversation);
  };

  const handleStartConversation = async (user) => {
    try {
      setIsLoading(true);
      const userId = 1; // Replace with the actual user ID from authentication or context
      await axios.post('/api/messages', {
        sender_id: userId,
        content: 'Hello!',
        recipients: [user.id]
      });
      setNewConversationUser(null);
      fetchConversations(); // Refresh the conversations list
      alert('Conversation started successfully!'); // User feedback
    } catch (error) {
      console.error('Error starting conversation:', error);
      setError('Failed to start a new conversation. Please try again.');
    } finally {
      setIsLoading(false);
      setIsModalOpen(false); // Close the modal after starting the conversation
    }
  };

  return (
    <div className="messages-page">
      <div className="sidebar">
        <Conversation 
          conversations={conversations} 
          onSelectConversation={handleSelectConversation} 
        />
        <button className="add-button" onClick={() => setIsModalOpen(true)}>+</button>
      </div>
      <div className="messages-content">
        <h1>Messages</h1>
        {isLoading && <div className="loading-spinner">Loading...</div>} {/* Add spinner here */}
        {error && <p className="error">{error}</p>}
        {!selectedConversation && !isLoading && <p>Select a conversation to view messages.</p>}
        {selectedConversation && messages.length === 0 && !isLoading && <p>No messages found in this conversation.</p>}
        {messages.map((message, idx) => (
          <div key={idx} className="message">
            <p><strong>{message.sender}:</strong> {message.content}</p>
            <p>{new Date(message.timestamp).toLocaleString()}</p>
          </div>
        ))}
      </div>
      <UserSearchModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onStartConversation={handleStartConversation} 
      />
    </div>
  );
};

export default MessagesPage;

