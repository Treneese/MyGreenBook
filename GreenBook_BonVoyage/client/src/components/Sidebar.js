// Sidebar.js
import React from 'react';
import './Sidebar.css';
import { Link } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <ul>
          <li className="sidebar-item">
            <Link to="/community">Home</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/profile">Profile</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/notifications">Notifications</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/settings">Settings</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/followers">Followers</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/following">Following</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/messages">Messages</Link>
          </li>
          <li className="sidebar-item">
            <Link to="/community/history">History</Link>
          </li>
      </ul>
    </div>
  );
};

export default Sidebar;