// src/components/Login.js
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import api from '../api';
import { Link } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const handleLogin = async () => {
    try {
      const response = await api.post('http://localhost:5555/login', { email, password });
      localStorage.setItem('token', response.data.token);
      history.push('http://localhost:5555/places');
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="login">
      <h2>Login</h2>
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
      <button onClick={handleLogin}>Login</button>
      <p>Or Register Here</p>
      <Link className="Register" to="/register">Register</Link>
    </div>
  );
};

export default Login;

