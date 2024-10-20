// Conversation.js
import React from 'react';
import './MessagesPage.css';

const Conversation = ({ conversations, onSelectConversation, selectedConversationId }) => {
  return (
    <div className="conversation-sidebar">
      <h2>Conversations</h2>
      {conversations.length === 0 ? (
        <p>No conversations available.</p>
      ) : (
        <ul>
          {conversations.map((conversation) => (
            <li 
              key={conversation.id} 
              onClick={() => onSelectConversation(conversation)} 
              className={selectedConversationId === conversation.id ? 'active' : ''}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  onSelectConversation(conversation);
                }
              }}
            >
              <div className="conversation-participant">
                {conversation.participants.map((participant) => (
                  <div key={participant.id}>
                    <img src={participant.profile_picture} alt={participant.username} />
                    <span>{participant.username}</span>
                  </div>
                ))}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Conversation;
