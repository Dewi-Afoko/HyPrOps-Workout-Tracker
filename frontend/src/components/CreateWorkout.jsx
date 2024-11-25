import React from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS
import { useNavigate } from "react-router-dom";

const CreateWorkout = () => {
    const navigate = useNavigate();

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem('user_id');
        const token = localStorage.getItem('token'); // Retrieve token from localStorage
        if (!user_id || !token) {
            alert("User ID or token not found in localStorage.");
            return;
        }
        try {
            // Make the POST request with token in headers
            const response = await axios.post(
                `http://127.0.0.1:5000/workouts/${user_id}`, 
                {}, // Assuming no body is required, otherwise replace with the request payload
                {
                    headers: {
                        Authorization: `Bearer ${token}` // Add token to Authorization header
                    }
                }
            );
            alert(`API Response: ${JSON.stringify(response.data)}`);
            localStorage.setItem('workout_id', response.data.workout_id); // Set workout's ID in localStorage
            navigate(0);
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
            Create Workout
        </Button>
    );
};

export default CreateWorkout;
