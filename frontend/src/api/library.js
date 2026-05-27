import http from "./http";

export const getCategoriesService = () => 
    http.get('/api/library/categories')

export const getDetailImageService = (params) => 
    http.get('/api/library/images', params)

export const getImageMetricsService = (params) => 
    http.post('/api/analysis/metrics', params)
