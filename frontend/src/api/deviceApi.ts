import api from './axiosConfig';

export const fetchDeviceDetails = (register_id: string) => {
    return api.get(`/devices/${register_id}/`);
};

export const fetchDevices = () => {
    return api.get('/devices/list-devices/');
};
