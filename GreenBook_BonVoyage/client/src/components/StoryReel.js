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

  return (
    <div className="story-reel">
      {isLoading && <div className="loading">Loading...</div>}
      {error && <p className="error">{error}</p>}
      {stories.length === 0 && !isLoading && !error && <p>No stories available.</p>}
      {stories.map(story => (
        <div key={story.id} className="story">
          <img src={story.media} alt={`Story ${story.id}`} />
          {/* Displaying user information; assumes user info is included in story data */}
          {/* If not, you would need to modify the backend or fetch user info separately */}
          {story.user && (
            <div className="story-user">
              <p>{story.user.name}</p>
              <img src={story.user.image} alt={`User ${story.user.name}`} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default StoryReel;
