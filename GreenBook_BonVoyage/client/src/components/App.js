import React, { useState, useEffect } from 'react';
import { Link, Outlet } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Header from './Header';
import './App.css';

const App = () => {
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false); // New state variable
  // const [search, setSearch] = useState("");

  // function handleSearch(searchValue) {
  //   setSearch(searchValue);
  // }

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
      {loggedInUser ? (
        <Outlet />
      ) : (
        <>
          {showRegister ? (
            <Register setUser={setLoggedInUser} />
          ) : (
            <Login setUser={setLoggedInUser} />
          )}
          <button onClick={() => setShowRegister(!showRegister)}>
            {showRegister ? 'Already have an account? Log in' : 'Don’t have an account? Register'}
          </button>
        </>
      )}
    </div>
  );
}

export default App;
