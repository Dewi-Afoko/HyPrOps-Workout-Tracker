const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000"; // Default for local dev
console.log("VITE_API_URL from import.meta.env:", import.meta.env.VITE_API_URL);
console.log("Final API_BASE_URL:", API_BASE_URL);

export default API_BASE_URL;
