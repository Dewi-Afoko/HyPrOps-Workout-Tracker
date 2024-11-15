import React from "react";
import ReactDOM from "react-dom/client";
import ApiButton from "./components/GetUsers"; // Import the button component
import GetUsers from "./components/GetUsers";

const App = () => {
    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>Welcome to My Landing Page</h1>
            <GetUsers /> {/* Use the button component here */}
        </div>
    );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);