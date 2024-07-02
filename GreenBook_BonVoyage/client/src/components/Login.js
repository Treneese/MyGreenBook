// src/components/Login.js
import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { Link } from 'react-router-dom';
import * as yup from 'yup';

const Login = ({ setUser }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [login, setLogin] = useState(true);
  const history = useHistory();

  const loginSchema = yup.object().shape({
    email: yup.string().email('Invalid email format').required('Email is required'),
    password: yup.string().required('Password is required'),
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'email') {
      setEmail(value);
    } else if (name === 'password') {
      setPassword(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const isValid = await loginSchema.validate({ email, password });
      if (isValid) {
        const endpoint = login ? '/login' : '/register';
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
          const user = await response.json();
          setUser(user);
          history.push('/places');
        } else {
          console.error('Login failed:', response.statusText);
        }
      }
    } catch (error) {
      console.error('Validation failed:', error.errors);
    }
  };

  return (
    <div className="login">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
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
        <button type="submit">Login</button>
      </form>
      <p>Or Register Here</p>
      <Link className="Register" to="/register">Register</Link>
    </div>
  );
};

export default Login;


