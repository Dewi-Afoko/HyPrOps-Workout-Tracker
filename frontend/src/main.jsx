import React from 'react';
import ReactDOM from 'react-dom/client'; // Updated to "react-dom/client"
import App from './App'; // Adjust the path if necessary
import './index.css'; // Optional: if you have a global CSS file

ReactDOM.createRoot(document.getElementById('root')).render(
<React.StrictMode>
    <App />
</React.StrictMode>
);