// src/components/Register.js
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import api from '../api';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const handleRegister = async () => {
    try {
      await api.post('http://localhost:5555/register', { username, email, password });
      history.push('http://localhost:5555/login');
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  return (
    <div className="register">
      <h2>Register</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default Register;
