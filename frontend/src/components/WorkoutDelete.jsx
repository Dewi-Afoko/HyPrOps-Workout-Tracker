import React from "react";
import axios from "axios";

const WorkoutDelete = ({ workoutId, onDeleteSuccess }) => {
    const handleDelete = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        if (!window.confirm("Are you sure you want to delete this workout?")) {
            return; // Exit if the user cancels
        }

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
            onDeleteSuccess(); // Callback to refresh the parent component
        } catch (error) {
            console.error("Error deleting workout:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error deleting workout: ${errorMessage}`);
        }
    };

    return (
        <button
            style={{
                backgroundColor: "red",
                color: "white",
                border: "none",
                padding: "8px 16px",
                borderRadius: "5px",
                cursor: "pointer",
                fontWeight: "bold",
            }}
            onClick={handleDelete}
        >
            Delete Workout
        </button>
    );
};

export default WorkoutDelete;
