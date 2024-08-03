// CreatePost.js
import React, { useState } from 'react';
import axios from 'axios';
import './CreatePost.css';

const CreatePost = ({ currentUser }) => {
  const [content, setContent] = useState('');
  const [photo, setPhoto] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePost = async () => {
    if (!content && !photo) {
      alert('Please add some content or a photo.');
      return;
    }

    try {
      setIsLoading(true);
      const formData = new FormData();
      formData.append('content', content);
      if (photo) {
        formData.append('photo', photo);
      }
      const response = await axios.post('/api/posts', formData, { withCredentials: true });

      // Assuming response.data contains the new post object
      setContent('');
      setPhoto(null);
      // Add the new post to the feed
    } catch (error) {
      console.error('Error creating post:', error);
      setError('Failed to create post. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="create-post">
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What's on your mind?"
      />
      <input
        type="file"
        onChange={(e) => setPhoto(e.target.files[0])}
      />
      <button onClick={handlePost} disabled={isLoading}>
        {isLoading ? 'Posting...' : 'Post'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default CreatePost;
