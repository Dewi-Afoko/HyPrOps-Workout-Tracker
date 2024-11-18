import React from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS

const CreateWorkout = () => {

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem('user_id')
        if (!user_id) {
            alert("User ID not found in localStorage.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/workouts/${user_id}`);
            alert(`API Response: ${JSON.stringify(response.data)}`);
            localStorage.setItem('workout_id', response.workout_id); // Set workout's ID in localStorage
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