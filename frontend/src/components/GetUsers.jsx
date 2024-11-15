import React from "react";
import axios from "axios";

const GetUsers = () => {
    // Function to handle button click
    const handleButtonClick = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/users");
            alert(`API Response: ${JSON.stringify(response.data)}`);
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    return (
        <button onClick={handleButtonClick} style={{ fontSize: "16px", padding: "10px 20px" }}>
            Click Me to Call GET Users
        </button>
    );
};

export default GetUsers