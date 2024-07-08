// src/components/CreateRoute.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import PlaceList from './PlaceList';

const CreateRoute = () => {
  const [name, setName] = useState('');
  const [placeIds, setPlaceIds] = useState([]);
  const [places, setPlaces] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await api.get('/api/places');
        setPlaces(response.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };

    fetchPlaces();
  }, []);

  const handleCheckboxChange = (placeId) => {
    setPlaceIds((prevPlaceIds) => {
      if (prevPlaceIds.includes(placeId)) {
        return prevPlaceIds.filter((id) => id !== placeId);
      } else {
        return [...prevPlaceIds, placeId];
      }
    });
  };

  const handleCreateRoute = async () => {
    try {
      await api.post('/api/routes', { name, place_ids: placeIds });
      navigate('/routes');
    } catch (error) {
      console.error('Error creating route:', error);
    }
  };

  return (
    <div className="create-route">
      <h2>Create New Route</h2>
      <input
        type="text"
        placeholder="Route Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <div>
        <h3>Select Places</h3>
        {places.map((place) => (
          <div key={place.id}>
            <label>
              <input
                type="checkbox"
                value={place.id}
                checked={placeIds.includes(place.id)}
                onChange={() => handleCheckboxChange(place.id)}
              />
              {place.name} ({place.city})
            </label>
          </div>
        ))}
      </div>
      <button onClick={handleCreateRoute}>Create Route</button>
    </div>
  );
};

export default CreateRoute;
