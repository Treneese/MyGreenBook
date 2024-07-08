// src/components/PlaceCard.js
import {React, useState} from 'react';
import { Link } from 'react-router-dom';
import './PlaceCard.css'; 
import SafetyMark from './SafetyMark';

const PlaceCard = ({ place }) => {
    const { id, name, image } = place;
    const [isFavorite, setIsFavorite] = useState(false);
  
    const toggleFavorite = () => {
      setIsFavorite(!isFavorite);
    };

  return (

    <div className="place-card">
      <h3>{place.name}</h3>
      <p>City: {place.city}</p>
      <p>Address: {place.address}</p>
      <p>Safety Rating: {place.safety_rating}</p>
      <Link to={`/places/${place.id}`}>View Details</Link>
      {/* <SafetyMark placeId={place.id} /> */}
      <button className={`favorite-button ${isFavorite ? "favorite" : ""}`} onClick={toggleFavorite}>
          {isFavorite ? "Remove Favorite" : "Add to Favorites"}
        </button>
    </div>
  );
};

export default PlaceCard;
