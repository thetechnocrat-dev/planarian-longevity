import api from './axiosConfig';
import { saveUserInfo, saveAccessToken, getRefreshToken, logout } from '../utils/auth';
import { User } from '../types';

interface SignupData {
    username: string;
    email: string;
    password: string;
}

interface LoginData {
    email: string;
    password: string;
}

export const getPresignedUrl = (filename: string) => {
    return api.get(`/users/get-presigned-url/${filename}/`);
};

export const signup = async (data: SignupData): Promise<User> => {
    try {
        const response = await api.post('/users/signup/', data);
        const { access, refresh, user } = response.data;
        saveUserInfo(access, refresh, user);
        return user;
    } catch (error) {
        console.error('Error signing up:', error);
        throw error;
    }
};

export const login = async (data: LoginData): Promise<User> => {
    try {
        const response = await api.post('/users/login/', data);
        const { access, refresh, user } = response.data;
        saveUserInfo(access, refresh, user);
        return user;
    } catch (error) {
        console.error('Error logging in:', error);
        throw error;
    }
};

export const refreshToken = async (): Promise<string | null> => {
    const refresh = getRefreshToken();
    if (!refresh) {
        logout();
        return null;
    }

    try {
        const response = await api.post('/users/token/refresh/', { refresh });

        if (response.status === 200) {
            const { access } = response.data;
            saveAccessToken(access);
            return access;
        } else {
            logout();
            return null;
        }
    } catch (error) {
        console.error('Failed to refresh token:', error);
        logout();
        return null;
    }
};
