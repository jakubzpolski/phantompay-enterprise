import axios from 'axios'
const API = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000' })
export const createRequest = (amount, description) => API.post('/api/create-request', { amount, description })
export const getCheckoutUrl = (hash) => API.post(`/api/checkout/${hash}`)
export const getStatus = (hash) => API.get(`/api/status/${hash}`)  // implemented via polling page or extend backend later
