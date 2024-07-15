import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Navbar';
import SignupForm from './SignupForm';
import LoginForm from './LoginForm';
import DeviceClaimForm from './DeviceClaimForm';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <div>
        <Navbar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
        <Container>
          <Routes>
            <Route path="/" element={<Typography variant="h4" component="h1" gutterBottom>Welcome to Openzyme</Typography>} />
            <Route path="/signup" element={<SignupForm onLogin={handleLogin} />} />
            <Route path="/login" element={<LoginForm onLogin={handleLogin} />} />
            <Route path="/claim" element={<DeviceClaimForm />} />  {/* Add this line */}
          </Routes>
        </Container>
      </div>
    </Router>
  );
};

export default App;
