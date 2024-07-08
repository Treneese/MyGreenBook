// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header({  logoutUser }) {
 
  function handleLogout() {
      fetch('/logout', {
          method: 'DELETE'
      }).then( resp => {
          if (resp.ok) {
             
              logoutUser()
          }
      })
  }
  return (
    <header className="header">
      <nav className="nav">
        <ul className="nav-list">
          {/* <li className="nav-item">
            <Link to="/">Home</Link>
          </li> */} 
          <li className="nav-item">
            <Link to="/places">Places</Link>
          </li>
          <li className="nav-item">
            <Link to="/routes"> Route</Link>
          </li>
          <li className="nav-item">
            <Link to="/map">Map</Link>
          </li>
          <li className="nav-item">
            <Link to="/community">OurCommunity</Link>
          </li>
          <li className="nav-item">
            <Link to="/profile">Profile</Link>
          </li>
          <li className="nav-item">
            <Link to="/login">Login</Link>
          </li>
          {/* <li className="nav-item">
            <Link to="/register">Register</Link>
          </li> */}
        </ul>
      </nav>
      <button onClick={handleLogout}>Logout</button>
    </header>
  );
};

export default Header;
