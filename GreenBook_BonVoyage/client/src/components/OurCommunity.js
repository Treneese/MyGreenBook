

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReviewCard from './ReviewCard';
import './OurCommunity.css';
import Sidebar from './Sidebar';
import StoryReel from './StoryReel';
import CreatePost from './CreatePost';

const OurCommunity = () => {
  const [reviews, setReviews] = useState([]);
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
    setIsLoading(true);
    try {
      const response = await axios.get('/api/reviews');
      setReviews(response.data);
    } catch (error) {
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
      setError('Failed to fetch user profile. Please try again.');
    }
  };

  const fetchPlaces = async () => {
    try {
      const response = await axios.get('/api/places');
      setPlaces(response.data);
    } catch (error) {
      setError('Failed to fetch places. Please try again.');
    }
  };

  const handlePostReview = async () => {
    if (!currentUser) {
      alert('You must be logged in to post a review.');
      return;
    }
    if (!newReview.trim() || newRating < 0 || newRating > 5) {
      alert('Please provide a valid review and rating (0.0 - 5.0).');
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
      setError('Failed to post review. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLikeReview = async (reviewId) => {
    try {
      await axios.post(`/api/reviews/${reviewId}/like`, {}, { withCredentials: true });
      setReviews(reviews.map(review => 
        review.id === reviewId ? { ...review, likes: review.likes + 1 } : review
      ));
    } catch (error) {
      setError('Failed to like review. Please try again.');
    }
  };

  const handleAddComment = async (reviewId, commentContent, userId) => {
    try {
      const response = await axios.post(
        `/api/reviews/${reviewId}/comments`,
        { content: commentContent, user_id: userId },
        { withCredentials: true }
      );
      const newComment = response.data;

      setReviews(reviews.map(review =>
        review.id === reviewId ? { ...review, comments: [...review.comments, newComment] } : review
      ));
    } catch (error) {
      setError('Failed to add comment. Please try again.');
    }
  };

  const handleEditReview = async (reviewId, newContent) => {
    try {
      const response = await axios.put(`/api/reviews/${reviewId}`, { content: newContent }, { withCredentials: true });
      setReviews(reviews.map(review => 
        review.id === reviewId ? { ...review, content: response.data.content } : review
      ));
    } catch (error) {
      setError('Failed to edit review. Please try again.');
    }
  };

  if (isLoading) {
    return <div className="loading-spinner">Loading...</div>; // Update this to a spinner
  }

  return (
    <div className="community-container">
      <Sidebar />
      <div className="main-content">
        <StoryReel />
        <div className="content">
          <h1>Our Community</h1>
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
                placeholder="Rating (0.0-5.0)"
                min="0"
                max="5"
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
            <p className="login-prompt">You must be logged in to post a review.</p>
          )}
          <div className="reviews">
            {error && <p className="error">{error}</p>}
            {reviews.map(review => (
              <ReviewCard 
                key={review.id} 
                review={review} 
                onAddComment={handleAddComment}
                onEditReview={handleEditReview}
                onLikeReview={handleLikeReview}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OurCommunity;





