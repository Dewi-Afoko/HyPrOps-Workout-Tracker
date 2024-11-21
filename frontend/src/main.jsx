import React from "react";
import ReactDOM from "react-dom/client";
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomePage } from "./pages/Homepage/LandingPage";
import { RegisterUser } from "./pages/Register/Register";


const App = () => {
    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
                        <h1>HyPrOps Fullstack Workout App</h1>
                <BrowserRouter>
        <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<RegisterUser/>} />
        </Routes>
    </BrowserRouter>
</div>
    );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);