import http from "./http";

export const uploadImageService = (formData) => 
    http.post('/api/upload/image', formData)