import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header({ isLoggedIn, logoutUser }) {
  function handleLogout() {
    fetch('/logout', {
      method: 'DELETE'
    }).then(resp => {
      if (resp.ok) {
        logoutUser();
      }
    });
  }

  return (
    <header className="header">
      <div className="logo">
      <img src="/BonVoyageLogo.png" alt="Logo" className="Bon-Voyage-Logo" />
      </div>
      <nav className="nav">
        <ul className="nav-list">
          {/* <li className="nav-item">
            <Link to="/">Home</Link>
          </li> */}
          <li className="nav-item">
            <Link to="/places">Places</Link>
          </li>
          <li className="nav-item">
            <Link to="/routes">Route</Link>
          </li>
          <li className="nav-item">
            <Link to="/map">Map</Link>
          </li>
          <li className="nav-item">
            <Link to="/community">Our Community</Link>
          </li>
        </ul>
      </nav>
      {isLoggedIn ? (
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      ) : (
        <Link to="/login" className="login-button">Login</Link>
      )}
    </header>
  );
}

export default Header;

