import React from 'react';
import { useNavigate } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { useTheme, useMediaQuery } from '@mui/material';

interface NavbarProps {
  isLoggedIn: boolean;
  onLogout: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ isLoggedIn, onLogout }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Openzyme
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {isLoggedIn ? (
            <Button color="inherit" onClick={onLogout}>Logout</Button>
          ) : (
            <>
              {!isMobile && (
                <>
                  <Button color="inherit" onClick={() => navigate('/login')}>Login</Button>
                  <Button color="inherit" onClick={() => navigate('/signup')}>Signup</Button>
                </>
              )}
              {isMobile && (
                <Button color="inherit" onClick={() => navigate('/login')}>Login/Signup</Button>
              )}
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
