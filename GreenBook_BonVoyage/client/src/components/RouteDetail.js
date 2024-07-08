import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

const RouteDetails = () => {
    const { routeId } = useParams();
    const navigate = useNavigate();
    const [route, setRoute] = useState(null);

    useEffect(() => {
        const fetchRoute= async () => {
          try {
            const response = await api.get(`http://localhost:5555/api/routes/${routeId}`);
            setPlace(response.data);
          } catch (error) {
            console.error('Error fetching route details:', error);
          }
        };
    
        fetchRoute();
      }, [routeId]);

      const handleDelete = async () => {
        try {
          await api.delete(`http://localhost:5555/api/places/${placeId}`);
          navigate('/places'); // Redirect to the list of places after deletion
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

export default RouteDetail;