import api from './axiosConfig';

export const fetchMessages = (deviceType: string) => {
    return api.get('/messaging/list/', {
        params: {
            device_type: deviceType
        }
    });
};

export const createMessage = (deviceType: string, content: string) => {
    return api.post('/messaging/create/', {
        device_type: deviceType,
        content: content
    });
};
