import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import SignupForm from './components/SignupForm';
import LoginForm from './components/LoginForm';
import DeviceClaimForm from './components/DeviceClaimForm';
import DeviceList from './components/DeviceList';
import DeviceDetail from './components/DeviceDetail';
import { isLoggedIn, getUserInfo, logout } from './utils/auth';
import { User } from './types';
import { Box } from '@mui/material';

const App: React.FC = () => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (isLoggedIn()) {
            const userInfo = getUserInfo();
            console.log('User is logged in:', userInfo);
            setUser(userInfo);
        } else {
            console.log('User is not logged in');
        }
        setLoading(false);
    }, []);

    const handleLogout = () => {
        setUser(logout());
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <Router>
            <Box display="flex" flexDirection="column" minHeight="100vh">
                <Navbar user={user} onLogout={handleLogout} />
                <Box component="main" flexGrow={1} p={3}>
                    <Routes>
                        <Route path="/" element={user ? <DeviceList /> : <Navigate replace to="/login" />} />
                        <Route path="/signup" element={<SignupForm onLogin={(newUser) => setUser(newUser)} />} />
                        <Route path="/login" element={<LoginForm onLogin={(newUser) => setUser(newUser)} />} />
                        <Route path="/claim" element={user ? <DeviceClaimForm /> : <Navigate replace to="/login" />} />
                        <Route path="/devices" element={user ? <DeviceList /> : <Navigate replace to="/login" />} />
                        <Route path="/devices/:register_id" element={user ? <DeviceDetail /> : <Navigate replace to="/login" />} />
                    </Routes>
                </Box>
                <Box component="footer" p={2} textAlign="center">
                    © {new Date().getFullYear()} Openzyme
                </Box>
            </Box>
        </Router>
    );
};

export default App;
