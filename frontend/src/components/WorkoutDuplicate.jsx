import React from "react";
import axios from "axios";
import API_BASE_URL from "../config";

const WorkoutDuplicate = ({ workoutId, onDuplicateSuccess }) => {
    const handleDuplicateWorkout = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found. Please log in again.");
            return;
        }

        try {
            const response = await axios.post(
                `${API_BASE_URL}/workouts/${workoutId}/duplicate`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            if (onDuplicateSuccess) onDuplicateSuccess(); // Trigger refresh or any parent action
        } catch (error) {
            console.error("Error duplicating workout:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error duplicating workout: ${errorMessage}`);
        }
    };

    return (
        <button
            onClick={handleDuplicateWorkout}
            style={{
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                padding: "8px 12px",
                cursor: "pointer",
                fontSize: "14px",
            }}
        >
            Duplicate Workout
        </button>
    );
};

export default WorkoutDuplicate;
