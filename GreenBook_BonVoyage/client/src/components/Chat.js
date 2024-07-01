// src/components/Chat.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
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

  const sendMessage = (e) => {
    e.preventDefault();
    socket.send(message);
    setMessage('');
  };

  return (
    <div className="App">
      <h1>Chat Application</h1>
      <div className="chat-window">
        <div className="chat-messages">
          {chat.map((msg, index) => (
            <div key={index} className="message">
              {msg}
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

