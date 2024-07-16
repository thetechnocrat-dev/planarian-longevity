export interface User {
    username: string;
    isLoggedIn: boolean;
    token?: string;
}

export interface Device {
    uuid: string;
    register_id: string;
    device_type: string;
    device_version: string;
    owner_username: string;
    registered: boolean;
}