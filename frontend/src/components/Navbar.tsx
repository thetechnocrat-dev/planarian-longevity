import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { User } from '../types';
import { useTheme, useMediaQuery } from '@mui/material';

interface NavbarProps {
  user: User | null;
  onLogout: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  return (
    <AppBar position="sticky">
      <Toolbar>
        <Typography
          component={Link}
          to="/"
          variant="h6"
          sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}
        >
          Openzyme
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          {user ? (
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
