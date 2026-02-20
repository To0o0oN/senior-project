import axios from 'axios';

const instance = axios.create({
    baseUrl: 'http://localhost:8000', // ปรับเป็น IP เครื่อง Backend
});

// ดึง Token ใส่ Header อัตโนมัติ
instance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default instance;