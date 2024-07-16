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

const App: React.FC = () => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
      console.log(`App component isLoggedIn ${isLoggedIn()}`)
      if (isLoggedIn()) {
          const userInfo = getUserInfo();
          console.log(`App component user ${userInfo}`)
          setUser(userInfo);
      }
    }, []);

    const handleLogout = () => {
        setUser(logout());
    };

    return (
        <Router>
            <div>
                <Navbar user={user} onLogout={handleLogout} />
                <Routes>
                    <Route path="/" element={<Navigate replace to={user ? "/devices" : "/signup"} />} />
                    <Route path="/signup" element={<SignupForm onLogin={(newUser) => setUser(newUser)} />} />
                    <Route path="/login" element={<LoginForm onLogin={(newUser) => setUser(newUser)} />} />
                    <Route path="/claim" element={<DeviceClaimForm />} />
                    <Route path="/devices" element={<DeviceList />} />
                    <Route path="/devices/:register_id" element={<DeviceDetail />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
