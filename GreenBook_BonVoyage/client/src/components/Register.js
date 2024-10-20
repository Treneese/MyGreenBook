// src/components/Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import * as yup from 'yup';
import './Register.css';

const Register = ({ setUser }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const navigate = useNavigate();

  const registerSchema = yup.object().shape({
    username: yup.string().min(5, 'Username too Short!').max(15, 'Username too Long!').required('Username is required'),
    email: yup.string().email('Invalid email format').required('Email is required'),
    password: yup.string().min(5, 'Password too Short!').max(15, 'Password too Long!').required('Password is required'),
    passwordConfirmation: yup.string().oneOf([yup.ref('password')], 'Passwords must match').required('Password confirmation is required')
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'username') {
      setUsername(value);
    } else if (name === 'email') {
      setEmail(value);
    } else if (name === 'password') {
      setPassword(value);
    } else if (name === 'passwordConfirmation') {
      setPasswordConfirmation(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await registerSchema.validate({ username, email, password, passwordConfirmation });
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
        credentials: 'include', 
      });

        if (response.ok) {
        const user = await response.json();
        setUser(user);
        navigate('/login');
      } else {
        console.error('Registration failed:', response.statusText);
      }
    } catch (error) {
      console.error('Validation failed:', error.errors);
    }
  };

  return (
    <div className="register">
       <h1>Welcome to the Green Book</h1>
      <h2>Bon Voyage</h2>
      <p>Your go-to app for safe route navigation and place finding.</p>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={username}
          onChange={handleChange}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={email}
          onChange={handleChange}
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={password}
          onChange={handleChange}
        />
        <input
          type="password"
          name="passwordConfirmation"
          placeholder="Confirm Password"
          value={passwordConfirmation}
          onChange={handleChange}
        />
        <button type="submit">Register</button>
      </form>
      {/* <p>Or Login Here</p>
      <Link className="Login" to="/login">Login</Link> */}
    </div>
  );
};

export default Register;

