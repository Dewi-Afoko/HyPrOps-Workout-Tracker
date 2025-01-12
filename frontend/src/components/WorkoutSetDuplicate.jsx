import React from "react";
import axios from "axios";
import { Button } from "react-bootstrap";

const SetDuplicate = ({ workoutId, setOrder, onDuplicateSuccess }) => {
    const handleDuplicateSet = async () => {
        if (!setOrder) {
            alert("Invalid set order.");
            return;
        }

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            console.log(`Attempting to duplicate set. Workout ID: ${workoutId}, Set Order: ${setOrder}`);
            const response = await axios.post(
                `http://127.0.0.1:5000/workouts/${workoutId}/${setOrder}/duplicate_set`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onDuplicateSuccess?.();
        } catch (error) {
            console.error("Error duplicating set:", error);
            const errorMessage = error.response?.data?.error || "Network error occurred.";
            alert(`Failed to duplicate set: ${errorMessage}`);
        }
    };

    return (
        <Button variant="secondary" onClick={handleDuplicateSet}>
            Duplicate Set
        </Button>
    );
};

export default SetDuplicate;
