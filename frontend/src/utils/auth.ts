import { User } from '../types';

export const saveUserInfo = (access: string, refresh: string, user: User) => {
    const userInfo: User = {
        ...user,
        isLoggedIn: true,
        access_token: access,
        refresh_token: refresh,
    };
    localStorage.setItem('user', JSON.stringify(userInfo));
};

export const getUserInfo = (): User | null => {
    const user = localStorage.getItem('user');
    console.log(`getUserInfo ${user}`);
    return user ? JSON.parse(user) : null;
};

export const isLoggedIn = (): boolean => {
    const user = getUserInfo();
    return user ? user.isLoggedIn : false;
};

export const logout = (): null => {
    localStorage.removeItem('user');
    return null;
};

export const getAccessToken = (): string | null => {
    const user = getUserInfo();
    return user ? user.access_token || null : null;
};

export const getRefreshToken = (): string | null => {
    const user = getUserInfo();
    return user ? user.refresh_token || null : null;
};

export const saveAccessToken = (access: string) => {
    const user = getUserInfo();
    if (user) {
        user.access_token = access;
        localStorage.setItem('user', JSON.stringify(user));
    }
};
