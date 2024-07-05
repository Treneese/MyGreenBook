// src/components/CreatePlace.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';  // Adjust the path based on your directory structure

const CreatePlace = () => {
  const [name, setName] = useState('');
  const [city, setCity] = useState('');
  const [address, setAddress] = useState('');
  const [safetyRating, setSafetyRating] = useState('');
  const navigate = useNavigate();

  const handleCreatePlace = async () => {
    try {
      const response = await api.post('/api/places', { 
        name, 
        city, 
        address, 
        safety_rating: parseFloat(safetyRating) 
      });
      if (response.status === 201) {
        navigate.push('/places');  // Navigate to the places list page
      } else {
        console.error('Unexpected response status:', response.status);
      }
    } catch (error) {
      console.error('Error creating place:', error);
    }
  };

  return (
    <div className="create-place">
      <h2>Create New Place</h2>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="City"
        value={city}
        onChange={e => setCity(e.target.value)}
      />
      <input
        type="text"
        placeholder="Address"
        value={address}
        onChange={e => setAddress(e.target.value)}
      />
      <input
        type="number"
        placeholder="Safety Rating"
        value={safetyRating}
        onChange={e => setSafetyRating(e.target.value)}
      />
      <button onClick={handleCreatePlace}>Create Place</button>
    </div>
  );
};

export default CreatePlace;

