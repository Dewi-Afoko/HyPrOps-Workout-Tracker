import React from "react";
import axios from "axios";

const WorkoutDelete = ({ workoutId, onDeleteSuccess }) => {
    const handleDelete = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        const confirmDelete = window.confirm(
            "Are you sure you want to delete this workout? This action cannot be undone."
        );
        if (!confirmDelete) return;

        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/workouts/${workoutId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onDeleteSuccess(); // Call parent callback to refresh the list or navigate
        } catch (error) {
            console.error("Error deleting workout:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Failed to delete workout: ${errorMessage}`);
        }
    };

    return (
        <button

            onClick={handleDelete}
        >
            Delete Workout
        </button>
    );
};

export default WorkoutDelete;
