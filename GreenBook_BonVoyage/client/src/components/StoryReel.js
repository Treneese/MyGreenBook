// StoryReel.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StoryReel.css';

const StoryReel = () => {
  const [stories, setStories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/stories');
      setStories(response.data);
    } catch (error) {
      console.error('Error fetching stories:', error);
      setError('Failed to fetch stories. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="story-reel">
      {isLoading && <div>Loading...</div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {stories.map(story => (
        <div key={story.id} className="story">
          <img src={story.photo} alt={story.user.name} />
          <p>{story.user.name}</p>
        </div>
      ))}
    </div>
  );
};

export default StoryReel;
