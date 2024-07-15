import React, { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';
import api from './axiosConfig';
import { AxiosError } from 'axios';  // Import AxiosError for type checking

const DeviceClaimForm: React.FC = () => {
  const [registerId, setRegisterId] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    setSuccess('');

    try {
      await api.post('/devices/claim/', { register_id: registerId });  // Removed 'response' since it's not used
      setSuccess('Device claimed successfully!');
      setRegisterId('');
    } catch (error: unknown) {  // Type annotation for error
      if (error instanceof AxiosError) {  // Type guard for Axios errors
        console.error('Error claiming device:', error.response?.data.error);
        setError('Failed to claim device. Please try again.');
      } else {
        console.error('An unexpected error occurred:', error);
        setError('An unexpected error occurred. Please try again.');
      }
    }
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
    >
      <Typography variant="h5" component="h1" gutterBottom>
        Claim Device
      </Typography>
      <TextField
        label="Register ID"
        value={registerId}
        onChange={(e) => setRegisterId(e.target.value)}
        margin="normal"
        required
      />
      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          {error}
        </Typography>
      )}
      {success && (
        <Typography color="primary" sx={{ mt: 2 }}>
          {success}
        </Typography>
      )}
      <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
        Claim
      </Button>
    </Box>
  );
};

export default DeviceClaimForm;
