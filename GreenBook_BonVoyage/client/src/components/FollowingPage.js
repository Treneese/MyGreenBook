import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FollowingPage.css';
import Sidebar from './Sidebar';

const FollowingPage = ({ userId }) => {
  const [following, setFollowing] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchFollowing = async () => {
      try {
        const response = await axios.get(`/api/following/${userId}`);
        setFollowing(response.data.following);
      } catch (error) {
        console.error('Error fetching following:', error);
        setError('Failed to fetch following. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchFollowing();
  }, [userId]);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="following-page">
         <Sidebar />
      <h1>Following</h1>
      {following.map(user => (
        <div key={user.id} className="following-user">
          <img src={user.profile_picture} alt={user.username} />
          <p>{user.username}</p>
        </div>
      ))}
    </div>
  );
};

export default FollowingPage;

