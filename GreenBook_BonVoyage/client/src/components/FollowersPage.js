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

  if (isLoading) return <div className="loading-spinner">Loading...</div>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="followers-page">
      <Sidebar />
      <h1>Followers</h1>
      {followers.length === 0 ? (
        <p>No followers yet.</p>
      ) : (
        followers.map(follower => (
          <div key={follower.id} className="follower">
            <img src={follower.profile_picture} alt={follower.username} />
            <p>
              <a href={`/profile/${follower.id}`}>{follower.username}</a>
            </p>
          </div>
        ))
      )}
    </div>
  );
};


export default FollowersPage;
