// HistoryPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HistoryPage.css';
import Sidebar from './Sidebar';

const HistoryPage = () => {
  const [activities, setActivities] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchActivityHistory();
  }, []);

  const fetchActivityHistory = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/activity-history');
      setActivities(response.data);
    } catch (error) {
      console.error('Error fetching activity history:', error);
      setError('Failed to fetch activity history. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="history-page">
      <Sidebar />
      <h1>Activity History</h1>
      {isLoading && <div className="loading-spinner">Loading...</div>} {/* Add spinner here */}
      {error && <p className="error">{error}</p>}
      {activities.length === 0 && !isLoading && <p>No activities found.</p>}
      <ul>
        {activities.map(activity => (
          <li key={activity.id} className="activity-item">
            <p><strong>{activity.type}</strong> - {activity.content}</p>
            <p>{new Date(activity.date).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPage;
