import React from 'react';
import Navbar from './Navbar';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';

const App: React.FC = () => {
  return (
    <div>
      <Navbar />
      <Container>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome to Openzyme
        </Typography>
        {/* Add more content here */}
      </Container>
    </div>
  );
};

export default App;
