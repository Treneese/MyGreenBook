import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMapGL, { Marker, Popup } from 'react-map-gl';

function Map() {
  const [places, setPlaces] = useState([]);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [viewport, setViewport] = useState({
    width: '100%',
    height: '400px',
    latitude: -3.745,
    longitude: -38.523,
    zoom: 10
  });

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const response = await axios.get('http://localhost:5555/places');
        setPlaces(response.data);
      } catch (error) {
        console.error('Error fetching places:', error);
      }
    };
    fetchPlaces();
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setViewport(prev => ({
        ...prev,
        width: '100%',
        height: '400px'
      }));
    };
    window.addEventListener('resize', handleResize);
    handleResize(); // Call handleResize once initially

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return (
    <div>
      <ReactMapGL
        {...viewport}
        mapboxApiAccessToken={
          'sk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh4dnFsN2ExZDJhMmtwdmtkbDl4dG45In0.vCYN3WxxmO06CZpe_pqHVQ'
        }
        onViewportChange={nextViewport => setViewport(nextViewport)}
        mapStyle="mapbox://styles/mapbox/streets-v11"
      >
        {places.map(place => (
          <Marker
            key={place.id}
            latitude={place.latitude}
            longitude={place.longitude}
          >
            <div
              style={{ cursor: 'pointer' }}
              onClick={() => setSelectedPlace(place)}
            >
              📍
            </div>
          </Marker>
        ))}
        {selectedPlace && (
          <Popup
            latitude={selectedPlace.latitude}
            longitude={selectedPlace.longitude}
            onClose={() => setSelectedPlace(null)}
            closeOnClick={true}
          >
            <div>
              <h4>{selectedPlace.name}</h4>
              <p>{selectedPlace.city}</p>
            </div>
          </Popup>
        )}
      </ReactMapGL>
    </div>
  );
}

export default Map;
