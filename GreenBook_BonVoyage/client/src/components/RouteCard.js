// src/components/RouteCard.js
import React from 'react';
import { Link } from 'react-router-dom';

const RouteCard = ({ route }) => {
  return (
    <div className="route-card">
      <h3>{route.name}</h3>
      <ul>
        {route.places.map(place => (
          <li key={place.id}>{place.name} ({place.city})</li>
        ))}
      </ul>
      <Link to={`/routes/${route.id}`}>View Route Details</Link>
    </div>
  );
};

export default RouteCard;
