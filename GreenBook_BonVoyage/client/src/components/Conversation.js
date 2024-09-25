// Conversation.js
import React from 'react';
import './MessagesPage.css';

const Conversation = ({ conversations, onSelectConversation }) => {
  return (
    <div className="conversation-sidebar">
      <h2>Conversations</h2>
      <ul>
        {conversations.map((conversation, index) => (
          <li key={index} onClick={() => onSelectConversation(conversation)}>
            <div className="conversation-participant">
              {conversation.participants.map((participant, idx) => (
                <div key={idx}>
                  <img src={participant.profile_picture} alt={participant.username} />
                  <span>{participant.username}</span>
                </div>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Conversation;
