export interface User {
    id: string;
    email: string;
    username: string;
    isLoggedIn: boolean;
    access_token?: string;
    refresh_token?: string;
}

export interface Device {
    uuid: string;
    register_id: string;
    device_type: string;
    device_version: string;
    owner_username: string;
    registered: boolean;
    mac_address: string;
}

export interface Measurement {
    id: number;
    value: string;
    inference_value: string;
    inference_status: string;
    recorded_at: string;
    uploaded_at: string;
    queued_at: string;
}

export interface Message {
    username: string;
    device_type: string;
    created_at: string;
    content: string;
}
