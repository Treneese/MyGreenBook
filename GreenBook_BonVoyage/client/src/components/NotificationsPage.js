// NotificationsPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './NotificationsPage.css';
import Sidebar from './Sidebar';

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/notifications');
      setNotifications(response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
      setError('Failed to fetch notifications. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="notifications-page">
      <Sidebar />
      <h1>Notifications</h1>
      {isLoading && <div className="loading-spinner">Loading...</div>} {/* Add spinner here */}
      {error && <p className="error">{error}</p>}
      {notifications.length === 0 && !isLoading && !error && (
        <p>No notifications available.</p> // Empty state message
      )}
      <ul>
        {notifications.map(notification => (
          <li key={notification.id} className="notification-item">
            <p>{notification.message}</p>
            <p>{new Date(notification.date).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotificationsPage;
