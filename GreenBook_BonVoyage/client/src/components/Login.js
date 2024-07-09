import React, { useState } from 'react';
import { useNavigate, Link  } from 'react-router-dom';
import * as yup from 'yup';

const Login = ({ setUser }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [login, setLogin] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const loginSchema = yup.object().shape({
    username: yup.string().required('Username is required'),
    password: yup.string().required('Password is required'),
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'username') {
      setUsername(value);
    } else if (name === 'password') {
      setPassword(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await loginSchema.validate({ username, password });

      const endpoint = login ? '/api/login' : '/api/register';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      if (response.ok) {
        const user = await response.json();
        setUser(user);
        navigate('/places');
      } else {
        const errorResponse = await response.json();
        setError(errorResponse.message || 'Login failed. Please try again.');
      }
    } catch (validationError) {
      setError(validationError.errors ? validationError.errors[0] : 'Validation failed. Please try again.');
    }
  };

  return (
    <div className="login">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={username}
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





