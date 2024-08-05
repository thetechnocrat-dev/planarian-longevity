import React, { useEffect, useState } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { fetchDeviceDetails, fetchDeviceMeasurements, updateInferenceStatus } from '../api/deviceApi';
import { getPresignedUrl } from '../api/userApi';
import { Device, Measurement } from '../types';
import { isLoggedIn, getUserInfo } from '../utils/auth';
import { Typography, Button, Box, Table, TableBody, TableCell, TableHead, TableRow, TablePagination, Select, MenuItem, SelectChangeEvent, FormControl, Breadcrumbs, Link } from '@mui/material';

const DeviceDetail: React.FC = () => {
    const { register_id } = useParams<{ register_id: string }>();
    const [device, setDevice] = useState<Device | null>(null);
    const [measurements, setMeasurements] = useState<Measurement[]>([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage] = useState(10); // Fixed rows per page to 10
    const [totalMeasurements, setTotalMeasurements] = useState(0);
    const [filter, setFilter] = useState<string>(''); // State for the inference status filter
    const userInfo = getUserInfo();

    useEffect(() => {
        if (isLoggedIn() && register_id) {
            fetchDeviceDetails(register_id)
                .then(response => setDevice(response.data))
                .catch(error => console.error('Error fetching device details:', error));

            setPage(0);
            setMeasurements([]); // Clear measurements before fetching new data
            fetchMeasurements(register_id, 1, filter);
        }
    }, [register_id, filter]);

    useEffect(() => {
        const interval = setInterval(() => {
            if (isLoggedIn() && register_id) {
                fetchMeasurements(register_id, page + 1, filter);
            }
        }, 10000);

        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, [register_id, page, filter]);

    const fetchMeasurements = (register_id: string, page: number, filter: string) => {
        fetchDeviceMeasurements(register_id, page, filter)
            .then(response => {
                setMeasurements(response.data.results);
                setTotalMeasurements(response.data.count);
            })
            .catch(error => console.error('Error fetching device measurements:', error));
    };

    const handlePageChange = (event: unknown, newPage: number) => {
        setPage(newPage);
        fetchMeasurements(register_id!, newPage + 1, filter);
    };

    const handleFilterChange = (event: SelectChangeEvent<string>) => {
        setFilter(event.target.value as string);
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

    const handleAnalyze = async (id: number) => {
        try {
            await updateInferenceStatus(id, 'selected');
            fetchMeasurements(register_id!, page + 1, filter);
        } catch (error) {
            console.error('Error updating inference status:', error);
        }
    };

    const extractFilename = (path: string) => {
        return path.split('/').pop();
    };

    const isDeviceOwner = device?.owner_username === userInfo?.username;

    return (
        <Box sx={{ p: 2 }}>
            <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
                <Link component={RouterLink} to="/devices" color="inherit">
                    Devices
                </Link>
                <Typography color="textPrimary">{register_id}</Typography>
            </Breadcrumbs>
            {device ? (
                <>
                    <Typography variant="h5">Device Detail</Typography>
                    <Typography variant="body1">Register ID: {device.register_id}</Typography>
                    <Typography variant="body1">Type: {device.device_type}</Typography>
                    <Typography variant="body1">Version: {device.device_version}</Typography>
                    <Typography variant="body1">Owner: {device.owner_username}</Typography>
                    <Typography variant="body1">Registered: {device.registered ? 'Yes' : 'No'}</Typography>

                    <Typography variant="h6" sx={{ mt: 2 }}>Measurements</Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Typography variant="body1" sx={{ mr: 2 }}>Inference Status</Typography>
                        <FormControl sx={{ minWidth: 200 }}>
                            <Select value={filter} onChange={handleFilterChange} displayEmpty>
                                <MenuItem value="">All</MenuItem>
                                <MenuItem value="not_selected">Not Selected</MenuItem>
                                <MenuItem value="selected">Selected</MenuItem>
                                <MenuItem value="processing">Processing</MenuItem>
                                <MenuItem value="failed">Failed</MenuItem>
                                <MenuItem value="succeeded">Succeeded</MenuItem>
                            </Select>
                        </FormControl>
                    </Box>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Video</TableCell>
                                <TableCell>Tracked Video</TableCell>
                                <TableCell>Recorded At</TableCell>
                                <TableCell>Inference Status</TableCell>
                                <TableCell>Action</TableCell>
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
                                        {measurement.inference_value ? (
                                            <Button onClick={() => handleDownload(measurement.inference_value)}>
                                                {extractFilename(measurement.inference_value)}
                                            </Button>
                                        ) : (
                                            <span>Null</span>
                                        )}
                                    </TableCell>
                                    <TableCell>{new Date(measurement.recorded_at).toLocaleString()}</TableCell>
                                    <TableCell>{measurement.inference_status}</TableCell>
                                    <TableCell>
                                        <Button
                                            onClick={() => handleAnalyze(measurement.id)}
                                            disabled={!isDeviceOwner || measurement.inference_status !== 'not_selected'}
                                        >
                                            Analyze
                                        </Button>
                                    </TableCell>
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
                        rowsPerPageOptions={[]} // Disable rows per page selection
                        onRowsPerPageChange={() => {}} // No-op to satisfy the prop requirement
                    />
                </>
            ) : (
                <Typography variant="body2">Loading...</Typography>
            )}
        </Box>
    );
};

export default DeviceDetail;
