// src/components/RouteCard.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const RouteCard = ({ route }) => {
  const { id, name, places } = route;
  const [isFavorite, setIsFavorite] = useState(false);

  const toggleFavorite = () => {
    setIsFavorite(!isFavorite);
  };

  return (
    <div className="route-card">
      <h3>{name}</h3>
      <ul>
      {places && places.map(place => (
  <li key={place.id}>{place.name} ({place.city})</li>
))}
      </ul>
      <Link to={`/routes/${id}`}>View Route Details</Link>
      <button onClick={toggleFavorite}>
        {isFavorite ? 'Unfavorite' : 'Favorite'}
      </button>
    </div>
  );
};

export default RouteCard;

