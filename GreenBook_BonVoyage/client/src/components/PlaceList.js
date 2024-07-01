// src/components/PlaceList.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

const PlaceList = () => {
  const [places, setPlaces] = useState([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await api.get('http://localhost:5555/places');
        setPlaces(response.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };

    fetchPlaces();
  }, []);

  return (
    <div className="place-list">
      <h2>Places</h2>
      <Link className='Places' to="/places/new">Add New Place</Link>
      <ul>
        {places.map(place => (
          <li key={place.id}>
            <Link className='Places' to={`/places/${place.id}`}>{place.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PlaceList;
