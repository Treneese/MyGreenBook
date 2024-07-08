// src/components/Chat.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import axios from 'axios';
import './App.css';

const socket = io('http://localhost:5555');

const Chat = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);

  useEffect(() => {
    socket.on('message', msg => {
      setChat(prevChat => [...prevChat, msg]);
    });
  }, []);

  const sendMessage = async (e) => {
    e.preventDefault();
    socket.send(message);
    setMessage('');
  
    if (message.startsWith('/review')) {
      const [_, content, rating, placeId] = message.split(' ');
      try {
        const response = await axios.post('http://localhost:5000/api/reviews', {
          content,
          rating: parseInt(rating),
          place_id: parseInt(placeId)
        }, { withCredentials: true });
        console.log('Review created:', response.data);
      } catch (error) {
        console.error('Error creating review:', error);
      }
    }
  };

  const deleteReview = async (reviewId) => {
    try {
      await axios.delete(`http://localhost:5000/api/reviews/${reviewId}`, { withCredentials: true });
      console.log('Review deleted');
    } catch (error) {
      console.error('Error deleting review:', error);
    }
  };

  return (
    <div className="App">
    <h1>Chat Application</h1>
    <div className="chat-window">
      <div className="chat-messages">
        {chat.map((msg, index) => (
          <div key={index} className="message">
            {msg}
            {/* Assuming a special message format to delete a review */}
            {msg.startsWith('/deleteReview') && (
              <button onClick={() => deleteReview(msg.split(' ')[1])}>Delete Review</button>
            )}
          </div>
        ))}
      </div>
    </div>
    <form onSubmit={sendMessage}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message..."
      />
      <button type="submit">Send</button>
    </form>
  </div>
);
}

export default Chat;

