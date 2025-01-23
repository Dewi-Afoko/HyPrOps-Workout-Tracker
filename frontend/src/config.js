const API_BASE_URL = import.meta.env.VITE_API_URL || "https://your-render-app.onrender.com"; // Default to Render if not set
console.log("VITE_API_URL from import.meta.env:", import.meta.env.VITE_API_URL);
console.log("Final API_BASE_URL:", API_BASE_URL);

export default API_BASE_URL;
