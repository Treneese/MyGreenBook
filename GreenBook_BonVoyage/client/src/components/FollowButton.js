import React, { useState } from 'react';
import axios from 'axios';

const FollowButton = ({ userId, isFollowing }) => {
  const [following, setFollowing] = useState(isFollowing);

  const handleFollow = async () => {
    try {
      const response = await axios.post(`/follow/${userId}`);
      setFollowing(true);
      console.log('Followed:', response.data);
    } catch (error) {
      console.error('Error following user:', error);
    }
  };

  const handleUnfollow = async () => {
    try {
      const response = await axios.delete(`/unfollow/${userId}`);
      setFollowing(false);
      console.log('Unfollowed:', response.data);
    } catch (error) {
      console.error('Error unfollowing user:', error);
    }
  };

  return (
    <button onClick={following ? handleUnfollow : handleFollow}>
      {following ? 'Unfollow' : 'Follow'}
    </button>
  );
};

export default FollowButton;
