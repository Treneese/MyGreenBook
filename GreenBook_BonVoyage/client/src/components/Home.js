// src/components/Home.js
import React, { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import './Home.css';
import Login from './Login';
import Register from './Register';
import Header from './Header';

function Home() {
  const [loggedInUser, setLoggedInUser] = useState(null);

  function logoutUser() {
    setLoggedInUser(null);
  }

  useEffect(() => {
    fetch('/check_session')
      .then((resp) => {
        if (resp.ok) {
          resp.json().then(user => setLoggedInUser(user));
        }
      });
  }, []);

  return (
    <div className="home">
      <Header logoutUser={logoutUser} />
      <h1>Welcome to the Green Book</h1>
      <h2>Bon Voyage</h2>
      <p>Your go-to app for safe route navigation and place finding.</p>
      {
        !!loggedInUser ? 
        <Outlet /> : 
        <Login setUser={setLoggedInUser} />
      }
    </div>
  );
}

export default Home;
