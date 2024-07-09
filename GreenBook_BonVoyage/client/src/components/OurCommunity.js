import React, { useState, useEffect } from 'react';
import axios from 'axios';

const OurCommunity = () => {
  const [reviews, setReviews] = useState([]);
  const [user, setUser] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [newReview, setNewReview] = useState('');
  const [newRating, setNewRating] = useState(0);
  const [newPlaceId, setNewPlaceId] = useState(null);
  const [places, setPlaces] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchReviews();
    fetchCurrentUserProfile();
    fetchPlaces();
  }, []);

  const fetchReviews = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/reviews');
      setReviews(response.data);
    } catch (error) {
      console.error('Error fetching reviews:', error);
      setError('Failed to fetch reviews. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchCurrentUserProfile = async () => {
    try {
      const response = await axios.get('/api/profile');
      setCurrentUser(response.data);
    } catch (error) {
      console.error('Error fetching current user profile:', error);
      setError('Failed to fetch current user profile. Please try again.');
    }
  };

  const fetchPlaces = async () => {
    try {
      const response = await axios.get('/api/places');
      setPlaces(response.data);
    } catch (error) {
      console.error('Error fetching places:', error);
      setError('Failed to fetch places. Please try again.');
    }
  };

  const handlePostReview = async () => {
    if (!currentUser) {
      alert('You must be logged in to post a review.');
      return;
    }

    try {
      setIsLoading(true);
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
      setError('Failed to post review. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="community-container">
      <h1>Our Community</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {reviews.map(review => (
        <div key={review.id} className="review-card">
          <img src={user.image} alt="Profile" />
          <h3>{user.username}</h3>
          <p>{review.content}</p>
          <p>Rating: {review.rating}</p>
          <p>Place: {place.name}</p>
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
          <select
            value={newPlaceId}
            onChange={(e) => setNewPlaceId(Number(e.target.value))}
          >
            <option value="" disabled>Select a place</option>
            {places.map(place => (
              <option key={place.id} value={place.id}>
                {place.name}
              </option>
            ))}
          </select>
          <button onClick={handlePostReview}>Post Review</button>
        </div>
      ) : (
        <p>You must be logged in to post a review.</p>
      )}
    </div>
  );
};

export default OurCommunity;





