import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import ReactMapGL, { Marker, Popup } from 'react-map-gl';
import mapboxgl from 'mapbox-gl';
import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh3aWR6M3Eyc280MmxvZHFlaHR2MnhqIn0.pZ_BsbK0D_2RrErWEX28HA' ;
function Map() {
//   const [places, setPlaces] = useState([]);
//   const [selectedPlace, setSelectedPlace] = useState(null);
//   const [viewport, setViewport] = useState({
//     width: '100vw',
//     height: '100vh',
//     latitude: -3.745,
//     longitude: -38.523,
//     zoom: 10
//   });

//   useEffect(() => {
//     const fetchPlaces = async () => {
//       try {
//         const response = await axios.get('http://localhost:5555/api/places');
//         setPlaces(response.data);
//       } catch (error) {
//         console.error('Error fetching places:', error);
//       }
//     };
//     fetchPlaces();
//   }, []);

//   useEffect(() => {
//     const handleResize = () => {
//       setViewport(prev => ({
//         ...prev,
//         width: '100%',
//         height: '400px'
//       }));
//     };
//     window.addEventListener('resize', handleResize);
//     handleResize(); // Call handleResize once initially

//     return () => window.removeEventListener('resize', handleResize);
//   }, []);

//   return (
//     <div>
//       <ReactMapGL
//         {...viewport}
//         mapboxAccessToken={
//           'pk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh3aWR6M3Eyc280MmxvZHFlaHR2MnhqIn0.pZ_BsbK0D_2RrErWEX28HA'
//         }
//         onViewportChange={nextViewport => setViewport(nextViewport)}
//         mapStyle="mapbox://styles/mapbox/streets-v11"
//       >
//         {places.map(place => (
//           <Marker
//             key={place.id}
//             latitude={place.latitude}
//             longitude={place.longitude}
//           >
//             <div
//               style={{ cursor: 'pointer' }}
//               onClick={() => setSelectedPlace(place)}
//             >
//               📍
//             </div>
//           </Marker>
//         ))}
//         {selectedPlace && (
//           <Popup
//             latitude={selectedPlace.latitude}
//             longitude={selectedPlace.longitude}
//             onClose={() => setSelectedPlace(null)}
//             closeOnClick={true}
//           >
//             <div>
//               <h4>{selectedPlace.name}</h4>
//               <p>{selectedPlace.city}</p>
//             </div>
//           </Popup>
//         )}
//       </ReactMapGL>
//     </div>
//   );
// }


  useEffect(() => {
    navigator.geolocation.getCurrentPosition(successLocation, errorLocation, {
      enableHighAccuracy: true,
    });

    function successLocation(position) {
      setupMap([position.coords.longitude, position.coords.latitude]);
    }

    function errorLocation() {
      setupMap([-2.24, 53.48]);
    }

    function setupMap(center) {
      const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: center,
        zoom: 15,
      });

      const nav = new mapboxgl.NavigationControl();
      map.addControl(nav);

      // Example of adding a marker to the map
      new mapboxgl.Marker()
        .setLngLat(center)
        .addTo(map);

      // Function to add route
      function addRoute(start, end) {
        const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&access_token=${mapboxgl.accessToken}`;
        
        fetch(url)
          .then(response => response.json())
          .then(data => {
            const route = data.routes[0].geometry.coordinates;
            const geojson = {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: route,
              },
            };

            if (map.getSource('route')) {
              map.getSource('route').setData(geojson);
            } else {
              map.addLayer({
                id: 'route',
                type: 'line',
                source: {
                  type: 'geojson',
                  data: geojson,
                },
                layout: {
                  'line-join': 'round',
                  'line-cap': 'round',
                },
                paint: {
                  'line-color': '#3887be',
                  'line-width': 5,
                  'line-opacity': 0.75,
                },
              });
            }
          })
          .catch(err => {
            console.error('Error fetching directions:', err);
          });
      }

      // Example usage of addRoute function
      addRoute(center, [-2.24, 53.48]); // Replace with desired coordinates
    }
  }, []);

  return <div id="map" style={{ height: '100vh', width: '100vw' }}></div>;
};


export default Map;
