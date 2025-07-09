import axios, { AxiosRequestConfig } from "axios";

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:5000/api/v1',
});

export const axiosClient = <T = unknown>(config: AxiosRequestConfig): Promise<T> => {
    return axiosInstance(config).then((response) => response.data);
};