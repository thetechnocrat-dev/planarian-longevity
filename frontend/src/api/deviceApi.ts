import api from './axiosConfig';

export const fetchDeviceDetails = (register_id: string) => {
    return api.get(`/devices/${register_id}/`);
};

export const fetchDevices = () => {
    return api.get('/devices/list-devices/');
};

export const fetchDeviceMeasurements = (register_id: string, page = 1, inference_status?: string) => {
    let url = `/devices/${register_id}/measurements/?page=${page}`;
    if (inference_status) {
        url += `&inference_status=${inference_status}`;
    }
    return api.get(url);
};

export const updateInferenceStatus = (id: number, inference_status: string) => {
    return api.post('/devices/update_inference_status/', { id, inference_status });
};
