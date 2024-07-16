import React, { useEffect, useState } from 'react';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { fetchDevices } from '../api/deviceApi';
import { Device } from '../types';  // Ensure Device type is defined in your types

interface DevicesResponse {
    your_devices: Device[];
    other_devices: Device[];
}

const DeviceList: React.FC = () => {
  const [yourDevices, setYourDevices] = useState<Device[]>([]);
  const [otherDevices, setOtherDevices] = useState<Device[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDevices()
      .then(response => {
        const data: DevicesResponse = response.data;
        setYourDevices(data.your_devices);
        setOtherDevices(data.other_devices);
      })
      .catch(error => console.error('Error fetching devices:', error));
  }, []);

  const handleRowClick = (register_id: string) => {
    navigate(`/devices/${register_id}`);
  };

  return (
    <div>
      <TableContainer component={Paper}>
        <h2>Your Devices</h2>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Register ID</TableCell>
              <TableCell align="right">Type</TableCell>
              <TableCell align="right">Version</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {yourDevices.map((device) => (
              <TableRow key={device.uuid} onClick={() => handleRowClick(device.register_id)} style={{ cursor: 'pointer' }}>
                <TableCell component="th" scope="row">{device.register_id}</TableCell>
                <TableCell align="right">{device.device_type}</TableCell>
                <TableCell align="right">{device.device_version}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Button onClick={() => navigate('/claim')} style={{ margin: '20px' }}>Claim Device</Button>
      </TableContainer>

      <TableContainer component={Paper} style={{ marginTop: '20px' }}>
        <h2>Other Devices</h2>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Register ID</TableCell>
              <TableCell align="right">Type</TableCell>
              <TableCell align="right">Version</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {otherDevices.map((device) => (
              <TableRow key={device.uuid} onClick={() => handleRowClick(device.register_id)} style={{ cursor: 'pointer' }}>
                <TableCell component="th" scope="row">{device.register_id}</TableCell>
                <TableCell align="right">{device.device_type}</TableCell>
                <TableCell align="right">{device.device_version}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default DeviceList;
