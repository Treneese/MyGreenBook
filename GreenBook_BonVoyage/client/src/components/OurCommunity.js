import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OurCommunity = () => {
  const [reviews, setReviews] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [newReview, setNewReview] = useState('');
  const [newRating, setNewRating] = useState(0);
  const [newPlaceId, setNewPlaceId] = useState(null);

  useEffect(() => {
    fetchReviews();
    fetchCurrentUserProfile();
  }, []);

  const fetchReviews = async () => {
    try {
      const response = await axios.get('/api/reviews');
      setReviews(response.data);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };

  const fetchCurrentUserProfile = async () => {
    try {
      const response = await axios.get('/api/profile');
      setCurrentUser(response.data);
    } catch (error) {
      console.error('Error fetching current user profile:', error);
    }
  };

  const handlePostReview = async () => {
    if (!currentUser) {
      alert('You must be logged in to post a review.');
      return;
    }

    try {
      const response = await axios.post('/api/reviews', {
        content: newReview,
        rating: newRating,
        place_id: newPlaceId
      }, { withCredentials: true });

      setReviews([...reviews, response.data]);
      setNewReview('');
      setNewRating(0);
      setNewPlaceId(null);
    } catch (error) {
      console.error('Error posting review:', error);
    }
  };

  return (
    <div className="community-container">
      <h1>Our Community</h1>
      {reviews.map(review => (
        <div key={review.id} className="review-card">
          <img src={review.user_image} alt="Profile Picture" />
          <h3>{review.user_username}</h3>
          <p>{review.content}</p>
          <p>Rating: {review.rating}</p>
          {/* Additional UI components for comments, likes, etc. */}
        </div>
      ))}

      {currentUser ? (
        <div className="post-review">
          <h2>Post a Review</h2>
          <textarea
            value={newReview}
            onChange={(e) => setNewReview(e.target.value)}
            placeholder="Write your review..."
          />
          <input
            type="number"
            value={newRating}
            onChange={(e) => setNewRating(Number(e.target.value))}
            placeholder="Rating (0-5)"
          />
          <input
            type="number"
            value={newPlaceId}
            onChange={(e) => setNewPlaceId(Number(e.target.value))}
            placeholder="Place ID"
          />
          <button onClick={handlePostReview}>Post Review</button>
        </div>
      ) : (
        <p>You must be logged in to post a review.</p>
      )}
    </div>
  );
};

export default OurCommunity;





