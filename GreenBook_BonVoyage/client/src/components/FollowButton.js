import React, { useState } from 'react';
import axios from 'axios';

const FollowButton = ({ userId, isFollowing }) => {
  const [following, setFollowing] = useState(isFollowing);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFollow = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`/api/follow/${userId}`);
      setFollowing(true);
      console.log('Followed:', response.data);
    } catch (error) {
      console.error('Error following user:', error);
      setError('Failed to follow. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUnfollow = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.delete(`/api/unfollow/${userId}`);
      setFollowing(false);
      console.log('Unfollowed:', response.data);
    } catch (error) {
      console.error('Error unfollowing user:', error);
      setError('Failed to unfollow. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button 
        onClick={following ? handleUnfollow : handleFollow} 
        disabled={loading}
        aria-pressed={following}
      >
        {loading ? 'Processing...' : (following ? 'Unfollow' : 'Follow')}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
};


export default FollowButton;
