import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchDeviceDetails, fetchDeviceMeasurements } from '../api/deviceApi';
import { getPresignedUrl } from '../api/userApi';
import { Device, Measurement } from '../types';
import { isLoggedIn } from '../utils/auth';
import { Typography, Button, Box, Table, TableBody, TableCell, TableHead, TableRow, TablePagination } from '@mui/material';

const DeviceDetail: React.FC = () => {
    const { register_id } = useParams<{ register_id: string }>();
    const [device, setDevice] = useState<Device | null>(null);
    const [measurements, setMeasurements] = useState<Measurement[]>([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [totalMeasurements, setTotalMeasurements] = useState(0);

    useEffect(() => {
        if (isLoggedIn() && register_id) {
            fetchDeviceDetails(register_id)
                .then(response => setDevice(response.data))
                .catch(error => console.error('Error fetching device details:', error));

            fetchMeasurements(register_id, 1, rowsPerPage);
        }
    }, [register_id, rowsPerPage]);

    const fetchMeasurements = (register_id: string, page: number, rowsPerPage: number) => {
        fetchDeviceMeasurements(register_id, page)
            .then(response => {
                setMeasurements(response.data.results);
                setTotalMeasurements(response.data.count);
            })
            .catch(error => console.error('Error fetching device measurements:', error));
    };

    const handlePageChange = (event: unknown, newPage: number) => {
        setPage(newPage);
        fetchMeasurements(register_id!, newPage + 1, rowsPerPage);
    };

    const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
        fetchMeasurements(register_id!, 1, parseInt(event.target.value, 10));
    };

    const handleDownload = async (filepath: string) => {
        try {
            const encodedFilepath = encodeURIComponent(filepath);
            const response = await getPresignedUrl(encodedFilepath);
            window.location.href = response.data.url;
        } catch (error) {
            console.error('Error fetching presigned URL:', error);
        }
    };

    const extractFilename = (path: string) => {
        return path.split('/').pop();
    };

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

                    <Typography variant="h6" sx={{ mt: 2 }}>Measurements</Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Value</TableCell>
                                <TableCell>Recorded At</TableCell>
                                <TableCell>Uploaded At</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {measurements.map((measurement) => (
                                <TableRow key={measurement.recorded_at}>
                                    <TableCell>
                                        <Button onClick={() => handleDownload(measurement.value)}>
                                            {extractFilename(measurement.value)}
                                        </Button>
                                    </TableCell>
                                    <TableCell>
                                        <Button onClick={() => handleDownload(measurement.inference_value)}>
                                            {extractFilename(measurement.inference_value)}
                                        </Button>
                                    </TableCell>
                                    <TableCell>{new Date(measurement.recorded_at).toLocaleString()}</TableCell>
                                    <TableCell>{new Date(measurement.uploaded_at).toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                    <TablePagination
                        component="div"
                        count={totalMeasurements}
                        page={page}
                        onPageChange={handlePageChange}
                        rowsPerPage={rowsPerPage}
                        onRowsPerPageChange={handleRowsPerPageChange}
                    />
                </>
            ) : (
                <Typography variant="body2">Loading...</Typography>
            )}
        </Box>
    );
};

export default DeviceDetail;
