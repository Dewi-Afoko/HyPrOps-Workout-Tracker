import React from "react";
import ReactDOM from "react-dom/client";
import GetUsers from "./components/GetUsers";
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>HyPrOps Fullstack Workout App</h1>
            <GetUsers />
        </div>
    );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);