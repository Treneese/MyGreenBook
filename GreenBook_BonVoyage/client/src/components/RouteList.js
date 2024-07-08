// src/components/RouteList.js
import React, { useEffect, useState } from 'react';
import RouteCard from './RouteCard';
import { Link } from 'react-router-dom';
import api from '../api';

function RouteList ({ search }) {
  const [routes, setRoutes] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRoutes = async () => {
      try {
        const response = await fetch("/api/routes");
        if (!response.ok) {
          throw new Error("Failed to fetch routes");
        }
        const data = await response.json();
        setRoutes(data);
      } catch (error) {
        console.error('Error fetching routes:', error);
        setError(error.message);
      }
    };

    fetchRoutes();
  }, []);

  const removeRoute = (routeId) => {
    const filteredRoutes = routes.filter((route) => route.id !== routeId);
    setRoutes(filteredRoutes);
  };

  const filteredRoutes = routes.filter((route) => {
    const lowercaseSearch = search ? search.toLowerCase() : '';
    const lowercaseName = route.name ? route.name.toLowerCase() : '';
    return lowercaseName.includes(lowercaseSearch);
  });

  const routeCards = filteredRoutes.map((route) => (
    <RouteCard key={route.id} route={route} removeRoute={removeRoute} />
  ));

  return (
    <div className="route-list">
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


