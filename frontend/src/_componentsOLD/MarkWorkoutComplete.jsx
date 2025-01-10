import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css";

const CompleteWorkout = ({ workoutId, initialComplete, onStatusChange }) => {
    const [isComplete, setIsComplete] = useState(initialComplete);

    const handleButtonClick = async () => {
        const newCompleteStatus = !isComplete;

        const user_id = localStorage.getItem("user_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token || !workoutId) {
            alert("User ID, Workout ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${user_id}/${workoutId}`,
                { complete: newCompleteStatus },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`Workout status updated: ${JSON.stringify(response.data)}`);
            setIsComplete(newCompleteStatus);

            // Notify parent component of the status change
            if (onStatusChange) {
                onStatusChange(workoutId, newCompleteStatus);
            }
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to update workout status. Check console for details.");
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
            {isComplete ? "Mark as Incomplete" : "Mark as Complete"}
        </Button>
    );
};

export default CompleteWorkout;
