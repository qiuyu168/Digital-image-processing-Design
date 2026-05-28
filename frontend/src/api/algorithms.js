import http from "./http";

export const getAlgorithmService = () => 
    http.get('/api/algorithms')