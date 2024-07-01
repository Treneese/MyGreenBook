// src/components/PlaceDetails.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import SafetyMark from './SafetyMark';

const PlaceDetails = () => {
  const { placeId } = useParams();
  const [place, setPlace] = useState(null);

  useEffect(() => {
    const fetchPlace = async () => {
      try {
        const response = await api.get(`http://localhost:5555/places/${placeId}`);
        setPlace(response.data);
      } catch (error) {
        console.error('Error fetching place details:', error);
      }
    };

    fetchPlace();
  }, [placeId]);

  if (!place) return <div>Loading...</div>;

  return (
    <div className="place-details">
      <h1>{place.name}</h1>
      <p>{place.city}</p>
      <p>{place.address}</p>
      <p>Safety Rating: {place.safety_rating}</p>
      <SafetyMark placeId={placeId} />
    </div>
  );
};

export default PlaceDetails;

