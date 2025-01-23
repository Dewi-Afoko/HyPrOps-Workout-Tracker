import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";

const CompleteSet = ({ exerciseName, currentComplete, onCompleteStatusChange }) => {
    const [isComplete, setIsComplete] = useState(currentComplete);

    const handleButtonClick = async () => {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");
        if (!user_id || !token || !workout_id || !exerciseName) {
            alert("Missing required data in localStorage or props.");
            return;
        }

        const newCompleteStatus = !isComplete;

        try {
            const response = await axios.patch(
                `${API_BASE_URL}/workouts/${user_id}/${workout_id}/${exerciseName}`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`Exercise status updated to: ${newCompleteStatus}`);
            setIsComplete(newCompleteStatus);

            // Notify parent component of the status change
            if (onCompleteStatusChange) {
                onCompleteStatusChange(exerciseName, newCompleteStatus);
            }
        } catch (error) {
            console.error("Error updating complete status:", error);
            alert("Failed to update complete status.");
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

export default CompleteSet;