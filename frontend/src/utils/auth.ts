export const saveUserInfo = (token: string, user: any) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
};

export const getUserInfo = () => {
    const user = localStorage.getItem('user');
    console.log(`getUserInfo ${user}`)
    return user ? JSON.parse(user) : null;
};

export const isLoggedIn = () => {
    return !!localStorage.getItem('token');
};

export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return null;
}
