import React from 'react';
import './ReviewCard.css';

const ReviewCard = ({ review }) => {
  const { content, rating, user, place } = review;

  // Check if user exists before accessing properties
  if (!user) {
    return null; // or handle the case where user is undefined/null
  }

  return (
    <div className="review-card">
      <div className="user-info">
        {/* Optional chaining to safely access user.image */}
        {<img src={user.image} alt={`${user.username}'s Profile`} /> }
        {/* {profile.image && <img src={profile.image} alt="Profile" style={{ width: '100px', height: '100px' }} />} */}
        <p>{user.username}</p>
      </div>
      <div className="review-content">
        <p>{content}</p>
        <p>Rating: {rating}</p>
        <p>Place: {place.name} ({place.city})</p>
      </div>
      {/* Additional UI components for comments, likes, etc. */}
    </div>
  );
};

export default ReviewCard;
