// FollowersPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FollowingPage.css';
import Sidebar from './Sidebar';

const FollowingPage = () => {
  const [following, setFollowing] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFollowing();
  }, []);

  const fetchFollowing = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/following');
      setFollowing(response.data);
    } catch (error) {
      console.error('Error fetching following:', error);
      setError('Failed to fetch following. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="following-page">
         <Sidebar />
      {isLoading && <div>Loading...</div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {following.map(following => (
        <div key={following.id} className="following">
          <img src={following.profilePhoto} alt={following.name} />
          <p>{following.name}</p>
        </div>
      ))}
    </div>
  );
};

export default FollowingPage;
