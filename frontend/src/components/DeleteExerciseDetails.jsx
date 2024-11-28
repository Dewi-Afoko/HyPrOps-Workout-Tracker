import React from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";

const DeleteDetails = ({ exerciseName, onDeleteSuccess }) => {
    const handleButtonClick = async () => {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");
        const payload = JSON.parse(localStorage.getItem(`payload_${exerciseName}`));

        if (!user_id || !token || !workout_id || !exerciseName) {
            alert("Missing required data in localStorage or props.");
            return;
        }

        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/workouts/${user_id}/${workout_id}/delete_details`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    data: {
                        exercise_name: exerciseName,
                        ...payload, // Include indices like performance_notes_index
                    },
                }
            );

            alert("Deleted successfully!");
            console.log("Response:", response.data);

            // Remove the localStorage entry for this exercise
            localStorage.removeItem(`payload_${exerciseName}`);

            // Call the onDeleteSuccess callback to refresh the parent component's state
            if (onDeleteSuccess) {
                onDeleteSuccess();
            }
        } catch (error) {
            console.error("Error deleting record:", error);
            console.log("Payload sent:", payload);
            alert("Failed to delete record. Check console for details.");
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
            Delete Selected Entries
        </Button>
    );
};

export default DeleteDetails;
