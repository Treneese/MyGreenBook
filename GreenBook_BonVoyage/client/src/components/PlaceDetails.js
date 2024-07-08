// src/components/PlaceDetails.js
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import SafetyMark from './SafetyMark';
import ReviewList from "./ReviewList";
//add /api/reviews/<int:review_id> and routes safetymark add deleteboton that connects to back end
const PlaceDetails = () => {
  const { placeId } = useParams();
  const navigate = useNavigate();
  const [place, setPlace] = useState(null);
  const [showReviews, setShowReviews] = useState(false);
  
  useEffect(() => {
    const fetchPlace = async () => {
      try {
        const response = await api.get(`http://localhost:5555/api/places/${placeId}`);
        setPlace(response.data);
      } catch (error) {
        console.error('Error fetching place details:', error);
      }
    };

    fetchPlace();
  }, [placeId]);

  
  const handleDelete = async () => {
    try {
      await api.delete(`http://localhost:5555/api/places/${placeId}`);
      navigate('/places'); // Redirect to the list of places after deletion
    } catch (error) {
      console.error('Error deleting place:', error);
    }
  };

  if (!place) return <div>Loading...</div>;

  return (
    <div className="place-details">
      <h1>{place.name}</h1>
      <p>{place.city}</p>
      <p>{place.address}</p>
      <p>Safety Rating: {place.safety_rating}</p>
      <SafetyMark placeId={placeId} />
      <button onClick={handleDelete}>Delete Place</button>
      <button onClick={() => setShowReviews(!showReviews)}>
        {showReviews ? "Hide Reviews" : "Show Reviews"}
      </button>
      {showReviews && <ReviewList placeId={place.id} />}
    </div>
  );
};

export default PlaceDetails;

