import React from "react";
import axios from "axios";

const SetDeleteButton = ({ workoutId, setOrder, onDeleteSuccess }) => {
    const handleDelete = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/workouts/${workoutId}/delete_set/${setOrder}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onDeleteSuccess(); // Callback to refresh the parent component
        } catch (error) {
            console.error("Error deleting set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error deleting set: ${errorMessage}`);
        }
    };

    return (
        <button onClick={handleDelete}>
            Delete Set
        </button>
    );
};

export default SetDeleteButton;
