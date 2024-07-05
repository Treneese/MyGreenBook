import React, { useEffect, useState } from "react";
import PlaceCard from "./PlaceCard";
import './PlaceList.css';
import { Link } from 'react-router-dom';

function PlaceList({ search }) {
  const [places, setPlaces] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5555/api/places")
      .then((resp) => {
        if (!resp.ok) {
          throw new Error("Failed to fetch places");
        }
        return resp.json();
      })
      .then((data) => setPlaces(data))
      .catch((error) => setError(error.message));
  }, []);

  function removePlace(placeId) {
    const filteredPlaces = places.filter((place) => place.id !== placeId);
    setPlaces(filteredPlaces);
  }

  const filteredPlaces = places.filter((place) => {
    const lowercaseSearch = search ? search.toLowerCase() : '';
    const lowercaseName = place.name ? place.name.toLowerCase() : '';
    return lowercaseName.includes(lowercaseSearch);
  });

  const placeCards = filteredPlaces.map((place) => (
    <PlaceCard key={place.id} place={place} removePlace={removePlace} />
  ));

  return (
    <div>
      <h1>Places</h1>
      <Link className='Places' to="/places/new">Add New Place</Link>
      {error && <p>Error: {error}</p>}
      {placeCards.length === 0 ? (
        <p>No Places found.</p>
      ) : (
        <ul className="cards">
          {placeCards}
        </ul>
      )}
    </div>
  );
}


export default PlaceList;
