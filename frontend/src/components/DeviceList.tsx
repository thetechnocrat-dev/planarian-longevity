import React, { useEffect, useState } from 'react';
import { Grid, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box, Typography, Tabs, Tab, useMediaQuery, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { fetchDevices } from '../api/deviceApi';
import { Device } from '../types';  
import MessageList from './MessageList';

interface DevicesResponse {
    your_devices: Device[];
    other_devices: Device[];
}

const DeviceList: React.FC = () => {
    const [yourDevices, setYourDevices] = useState<Device[]>([]);
    const [otherDevices, setOtherDevices] = useState<Device[]>([]);
    const [tabIndex, setTabIndex] = useState(0);
    const navigate = useNavigate();
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

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

    const handleTabChange = (event: React.ChangeEvent<{}>, newValue: number) => {
        setTabIndex(newValue);
    };

    const renderDeviceTables = () => (
        <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
                <TableContainer component={Paper}>
                    <Box my={2} mx={2}>
                        <Typography variant="h5">Your Devices</Typography>
                    </Box>
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
                    <Box m={2}>
                        <Button onClick={() => navigate('/claim')} variant="contained">Claim Device</Button>
                    </Box>
                </TableContainer>
                <TableContainer component={Paper} sx={{ mt: 3 }}>
                    <Box my={2} mx={2}>
                        <Typography variant="h5">Other Devices</Typography>
                    </Box>
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
            </Grid>
            {!isMobile && (
                <Grid item xs={12} md={6}>
                    <MessageList deviceType="flatworm_watcher" />
                </Grid>
            )}
        </Grid>
    );

    const renderTabs = () => (
        <Box>
            <Tabs value={tabIndex} onChange={handleTabChange} centered>
                <Tab label="Devices" />
                <Tab label="Messages" />
            </Tabs>
            {tabIndex === 0 && (
                <Box p={3}>
                    {renderDeviceTables()}
                </Box>
            )}
            {tabIndex === 1 && (
                <Box p={3}>
                    <MessageList deviceType="flatworm_watcher" />
                </Box>
            )}
        </Box>
    );

    return (
        <Box p={3}>
            {isMobile ? renderTabs() : renderDeviceTables()}
        </Box>
    );
};

export default DeviceList;
