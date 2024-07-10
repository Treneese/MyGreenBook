import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import './RouteDetail.css';
const RouteDetails = () => {
    const { routeId } = useParams();
    const navigate = useNavigate();
    const [route, setRoute] = useState(null);

    useEffect(() => {
        const fetchRoute= async () => {
          try {
            const response = await api.get(`/api/routes/${routeId}`);
            setRoute(response.data);
          } catch (error) {
            console.error('Error fetching route details:', error);
          }
        };
    
        fetchRoute();
      }, [routeId]);

      const handleDelete = async () => {
        try {
          await api.delete(`/api/routes/${routeId}`);
          navigate('/routes'); 
        } catch (error) {
          console.error('Error deleting place:', error);
        }
      };

      if (!route) return <div>Loading...</div>;

      return (
        <div className="route-details">
        <h1>{route.name}</h1>

        <button onClick={handleDelete}>Delete Place</button>
        </div>
  );
};

export default RouteDetails;