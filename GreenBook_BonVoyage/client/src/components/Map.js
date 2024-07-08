import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapboxDirections from '@mapbox/mapbox-gl-directions/dist/mapbox-gl-directions';
import mapboxgl from 'mapbox-gl';
import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh3aWR6M3Eyc280MmxvZHFlaHR2MnhqIn0.pZ_BsbK0D_2RrErWEX28HA' ;

function Map() {
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

     
      new mapboxgl.Marker()
        .setLngLat(center)
        .addTo(map);

        const directions = new MapboxDirections({
          accessToken: mapboxgl.accessToken,
        });
     
        map.addControl(directions, 'top-left');

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

      
      addRoute(center, [-2.24, 53.48]);
    }
  }, []);

  return <div id="map" style={{ height: '100vh', width: '100vw' }}></div>;
};


export default Map;
