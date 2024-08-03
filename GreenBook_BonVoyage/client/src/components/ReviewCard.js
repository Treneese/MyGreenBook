import React, { useState } from 'react';
import './ReviewCard.css';

const ReviewCard = ({ review, onLike, onAddComment }) => {
  const { content, rating, user, place, likes, comments = [] } = review; // Default comments to an empty array
  const [newComment, setNewComment] = useState('');

  if (!user) {
    return null;
  }

  const handleAddComment = () => {
    if (newComment.trim()) {
      onAddComment(newComment);
      setNewComment('');
    }
  };
  console.log(user)
  return (
    <div className="review-card">
      <div className="user-info">
        <img src={user.profile_image} alt={`${user.username}'s Profile`} />
        <p>{user.username}</p>
      </div>
      <div className="review-content">
        <p>{content}</p>
        <p>Rating: {rating}</p>
        <p>Place: {place.name} ({place.city})</p>
      </div>
      <div className="review-actions">
        <button onClick={onLike}>Like ({likes})</button>
        <div className="comments-section">
          <h4>Comments:</h4>
          {comments.map((comment, index) => (
            <p key={index}>{comment}</p>
          ))}
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add a comment..."
          />
          <button onClick={handleAddComment}>Post Comment</button>
        </div> 
     </div>
    </div>
  );
};

export default ReviewCard;