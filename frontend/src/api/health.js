import http from "./http"

export const checkHealthService = () => 
    http.get('/api/health')