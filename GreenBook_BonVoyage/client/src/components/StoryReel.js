import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StoryReel.css';

const StoryReel = () => {
  const [stories, setStories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      const response = await axios.get('/api/stories');
      setStories(response.data);
    } catch (error) {
      console.error('Error fetching stories:', error);
      setError('Failed to fetch stories. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    setError('');
    setIsLoading(true);
    fetchStories();
  };

  return (
    <div className="story-reel">
      {isLoading && <div className="loading">Loading...</div>}
      {error && (
        <div className="error">
          <p>{error}</p>
          <button onClick={handleRetry}>Retry</button>
        </div>
      )}
      {stories.length === 0 && !isLoading && !error && 
      <p>No stories available.</p>}
      {stories.map(story => (
        <div key={story.id} className="story">
          <img 
            src={story.media} 
            alt={`Story ${story.id}`} 
            // onError={(e) => { e.target.onerror = null; e.target.src='/public/travelstory.png'; }} 
          />
          {story.user && (
            <div className="story-user">
              <p>{story.user.name}</p>
              <img 
                src={story.user.image} 
                alt={`User ${story.user.name}`} 
                // onError={(e) => { e.target.onerror = null; e.target.src='/public/travelstory.png'; }} 
              />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StoryReel;
