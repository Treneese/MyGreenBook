// src/components/RouteList.js
import React, { useEffect, useState } from 'react';
import RouteCard from './RouteCard';
import { Link } from 'react-router-dom';
import api from '../api';

const RouteList = () => {
  const [routes, setRoutes] = useState([]);

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

  return (
    <div className="route-list">
      <h2>Routes</h2>
      <Link className='Routes'to="/Route/new">Add New Route</Link>
      <ul>
      {routes.map(route => (
        <li key={route.id}>
        <Link className='Routes' to={`/routes/${route.id}`}>{route.name}</Link>
      </li>
    ))}
  </ul>
    </div>
  );
};

export default RouteList;
