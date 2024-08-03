// FollowersPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FollowersPage.css';
import Sidebar from './Sidebar';

const FollowersPage = () => {
  const [followers, setFollowers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFollowers();
  }, []);

  const fetchFollowers = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/followers');
      setFollowers(response.data);
    } catch (error) {
      console.error('Error fetching followers:', error);
      setError('Failed to fetch followers. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="followers-page">
         <Sidebar />
      {isLoading && <div>Loading...</div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {followers.map(follower => (
        <div key={follower.id} className="follower">
          <img src={follower.profilePhoto} alt={follower.name} />
          <p>{follower.name}</p>
        </div>
      ))}
    </div>
  );
};

export default FollowersPage;
