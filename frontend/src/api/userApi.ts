import api from './axiosConfig';

export const getPresignedUrl = (filename: string) => {
    return api.get(`/users/get-presigned-url/${filename}/`);
};
