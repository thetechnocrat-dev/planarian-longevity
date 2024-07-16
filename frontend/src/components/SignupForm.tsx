import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, TextField, Typography } from '@mui/material';
import { saveUserInfo } from '../utils/auth';
import { User } from '../types';
import api from '../api/axiosConfig';

interface SignupFormProps {
  onLogin: (user: User) => void;
}

const SignupForm: React.FC<SignupFormProps> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');

    try {
      const response = await api.post('/users/signup/', {
        username,
        email,
        password,
      });

      saveUserInfo(response.data.token, response.data.user);
      onLogin(response.data.user);
      navigate('/claim');
    } catch (error) {
      console.error('Error signing up:', error);
      setError('Failed to sign up. Please try again.');
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
    >
      <Typography variant="h5" component="h1" gutterBottom>
        Sign Up
      </Typography>
      <TextField
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        margin="normal"
        required
      />
      <TextField
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        margin="normal"
        required
        type="email"
      />
      <TextField
        label="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        margin="normal"
        required
        type="password"
      />
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Sign Up
      </Button>
      <p>Already have an account? <a href="/login" style={{ cursor: 'pointer' }}>Log in</a></p>
    </Box>
  );
};

export default SignupForm;
