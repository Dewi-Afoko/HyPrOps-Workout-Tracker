import React, { useState, useEffect } from "react";
import axios from "axios";

const WorkoutToggleComplete = ({ workoutId, initialComplete, onToggleComplete }) => {
    const [complete, setComplete] = useState(initialComplete);

    useEffect(() => {
        setComplete(initialComplete); // Sync state with parent when props change
    }, [initialComplete]);

    const handleToggle = async () => {
        localStorage.setItem("workout_id", workoutId); 
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/mark_complete`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            setComplete(!complete); // Toggle the state locally
            onToggleComplete(); // Notify parent to refresh the workout list
        } catch (error) {
            console.error("Error toggling workout status:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error toggling workout status: ${errorMessage}`);
        }
    };

    return (
        <button onClick={handleToggle}>
            {complete ? "Mark Incomplete" : "Mark Complete"}
        </button>
    );
};

export default WorkoutToggleComplete;
