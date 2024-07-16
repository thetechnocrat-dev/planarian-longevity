import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchDeviceDetails } from '../api/deviceApi';
import { Device } from '../types';
import { isLoggedIn } from '../utils/auth';
import { Typography, Box } from '@mui/material';

const DeviceDetail: React.FC = () => {
    const { register_id } = useParams<{ register_id: string }>();
    const [device, setDevice] = useState<Device | null>(null);

    useEffect(() => {
        if (isLoggedIn() && register_id) {
            fetchDeviceDetails(register_id)
                .then(response => setDevice(response.data))
                .catch(error => console.error('Error fetching device details:', error));
        }
    }, [register_id]);

    return (
        <Box sx={{ p: 2 }}>
            {device ? (
                <>
                    <Typography variant="h5">Device Detail</Typography>
                    <Typography variant="body1">Register ID: {device.register_id}</Typography>
                    <Typography variant="body1">Type: {device.device_type}</Typography>
                    <Typography variant="body1">Version: {device.device_version}</Typography>
                    <Typography variant="body1">Owner: {device.owner_username}</Typography>
                    <Typography variant="body1">Registered: {device.registered ? 'Yes' : 'No'}</Typography>
                </>
            ) : (
                <Typography variant="body2">Loading...</Typography>
            )}
        </Box>
    );
};

export default DeviceDetail;
