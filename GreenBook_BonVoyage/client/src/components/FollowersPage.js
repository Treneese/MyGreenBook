import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FollowersPage.css';
import Sidebar from './Sidebar';

const FollowersPage = ({ userId }) => {
  const [followers, setFollowers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchFollowers = async () => {
      try {
        const response = await axios.get(`/api/followers/${userId}`);
        setFollowers(response.data.followers);
      } catch (error) {
        console.error('Error fetching followers:', error);
        setError('Failed to fetch followers. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchFollowers();
  }, [userId]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="followers-page">
         <Sidebar />
      <h1>Followers</h1>
      {followers.map(follower => (
        <div key={follower.id} className="follower">
          <img src={follower.profile_picture} alt={follower.username} />
          <p>{follower.username}</p>
        </div>
      ))}
    </div>
  );
};

export default FollowersPage;
