import React from "react";
import axios from "axios";
import API_BASE_URL from "../config";

const SetToggleComplete = ({ workoutId, setOrder, complete, onToggleSetComplete }) => {
    const handleToggle = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.patch(
                `${API_BASE_URL}/workouts/${workoutId}/${setOrder}/mark_complete`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onToggleSetComplete(); // Callback to refresh or update the parent component
        } catch (error) {
            console.error("Error toggling set status:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error toggling set status: ${errorMessage}`);
        }
    };

    return (
        <button onClick={handleToggle}>
            {complete ? "Mark Incomplete" : "Mark Complete"}
        </button>
    );
};

export default SetToggleComplete;
