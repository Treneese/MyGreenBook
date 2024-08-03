// SettingsPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SettingsPage.css';
import Sidebar from './Sidebar';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    email: '',
    notificationsEnabled: false,
    privacy: 'public',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get('/api/settings');
      setSettings(response.data);
    } catch (error) {
      console.error('Error fetching settings:', error);
      setError('Failed to fetch settings. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSettings(prevSettings => ({
      ...prevSettings,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSaveSettings = async () => {
    try {
      setIsLoading(true);
      await axios.put('/api/settings', settings);
      setMessage('Settings saved successfully.');
    } catch (error) {
      console.error('Error saving settings:', error);
      setError('Failed to save settings. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="settings-page">
         <Sidebar />
      <h1>Settings</h1>
      {isLoading && <div>Loading...</div>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <div className="settings-form">
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={settings.email}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Enable Notifications:
          <input
            type="checkbox"
            name="notificationsEnabled"
            checked={settings.notificationsEnabled}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Privacy:
          <select
            name="privacy"
            value={settings.privacy}
            onChange={handleInputChange}
          >
            <option value="public">Public</option>
            <option value="private">Private</option>
            <option value="friends-only">Friends Only</option>
          </select>
        </label>
        <button onClick={handleSaveSettings}>Save Settings</button>
      </div>
    </div>
  );
};

export default SettingsPage;
