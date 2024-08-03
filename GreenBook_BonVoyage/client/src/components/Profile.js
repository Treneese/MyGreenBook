import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Profile.css';
import Sidebar from './Sidebar';

const Profile = () => {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    bio: '',
    image: ''
  });

  const [initialProfile, setInitialProfile] = useState({
    username: '',
    email: '',
    bio: '',
    image: ''
  });

  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/profile');
        setProfile(response.data);
        setInitialProfile(response.data); // Store initial profile for comparison
      } catch (error) {
        console.error('Error fetching profile:', error);
        setError('Failed to fetch profile data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfile((prevProfile) => ({
      ...prevProfile,
      [name]: value
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setProfile((prevProfile) => ({
          ...prevProfile,
          image: reader.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put('/api/profile', profile);
      setIsEditing(false);
      alert('Profile updated successfully');
    } catch (error) {
      console.error('Error updating profile:', error);
      setError('Failed to update profile. Please try again.');
    }
  };

  const handleCancel = () => {
    // Reset profile to initial state and exit edit mode
    setProfile(initialProfile);
    setIsEditing(false);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
       <Sidebar />
      <h2>Profile</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            name="username"
            value={profile.username}
            onChange={handleInputChange}
            disabled={!isEditing}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={profile.email}
            onChange={handleInputChange}
            disabled={!isEditing}
          />
        </div>
        <div>
          <label>Bio:</label>
          <textarea
            name="bio"
            value={profile.bio}
            onChange={handleInputChange}
            disabled={!isEditing}
          />
        </div>
        <div>
          <label>Profile Image:</label>
          {profile.image && <img src={profile.image} alt="Profile" style={{ width: '100px', height: '100px' }} />}
          {isEditing && <input type="file" onChange={handleImageChange} />}
        </div>
        <div>
          {isEditing ? (
            <>
              <button type="button" onClick={handleCancel}>Cancel</button>
              <button type="submit">Save</button>
            </>
          ) : (
            <button type="button" onClick={() => setIsEditing(true)}>
              Edit
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default Profile;



