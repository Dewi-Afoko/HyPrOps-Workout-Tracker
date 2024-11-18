import React from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS

const GetUsers = () => {

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
        <Button 
            onClick={handleButtonClick} 
            variant="dark" 
            style={{
                backgroundColor: "black",
                color: "red",
                borderRadius: "50px",
                fontSize: "16px",
                padding: "10px 20px",
            }}
        >
            Click Me to Call GET Users
        </Button>
    );
};

export default GetUsers;