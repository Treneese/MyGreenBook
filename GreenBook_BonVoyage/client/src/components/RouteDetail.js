import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import './RouteDetail.css'

const RouteDetails = () => {
  const { routeId } = useParams();
  const navigate = useNavigate();
  const [route, setRoute] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRoute = async () => {
      try {
        const response = await api.get(`/api/routes/${routeId}`);
        setRoute(response.data);
      } catch (error) {
        setError('Error fetching route details');
        console.error('Error fetching route details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRoute();
  }, [routeId]);

  const handleDelete = async () => {
    const confirmDelete = window.confirm('Are you sure you want to delete this route?');
    if (!confirmDelete) return;

    try {
      await api.delete(`/api/routes/${routeId}`);
      navigate('/routes'); 
    } catch (error) {
      setError('Error deleting route');
      console.error('Error deleting route:', error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="route-details">
      <h1>{route.name}</h1>
      <h3>Places:</h3>
      <ul>
        {route.places.map(place => (
          <li key={place.id}>{place.name} ({place.city})</li>
        ))}
      </ul>
      <button onClick={handleDelete}>Delete Route</button>
    </div>
  );
};

export default RouteDetails;