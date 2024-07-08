// src/components/RouteList.js
import React, { useEffect, useState } from 'react';
import RouteCard from './RouteCard';
import { Link } from 'react-router-dom';
import api from '../api';

const RouteList = () => {
  const [routes, setRoutes] = useState([]);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        const response = await api.get('http://localhost:5555/api/routes');
        setRoutes(response.data);
      } catch (error) {
        console.error('Error fetching routes:', error);
      }
    };

    fetchRoutes();
  }, []);

  function removePlace(placeId) {
    const filteredPlaces = places.filter((place) => place.id !== placeId);
    setPlaces(filteredPlaces);
  }

  const placeCards = filteredPlaces.map((place) => (
    <PlaceCard key={place.id} place={place} removePlace={removePlace} />
  ));
  return (
    <div className="route-list">
      {/* <h2>Routes</h2>
      <Link className='Routes'to="/routes/new">Add New Route</Link>
      <ul> */}
      {/* {routes.map(route => (
        <li key={route.id}>
        <Link className='Routes' to={`/routes/${route.id}`}>{route.name}</Link>
      </li>
    ))}
  </ul> */}


<h1>Routes</h1>
      <Link className='Routes' to="/routes/new">Add New Route</Link>
      {error && <p>Error: {error}</p>}
      {routeCards.length === 0 ? (
        <p>No Routes found.</p>
      ) : (
        <ul className="cards">
          {routeCards}
        </ul>
      )}
    </div>
  );
};
export default RouteList;
