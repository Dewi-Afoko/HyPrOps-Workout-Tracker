import React from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";

const DeleteExercise = ({ exerciseName, onDeleteSuccess }) => {
    const handleButtonClick = async () => {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");

        if (!user_id || !token || !workout_id || !exerciseName) {
            alert("Missing required data in localStorage or props.");
            return;
        }

        try {
            const response = await axios.delete(
                `${API_BASE_URL}/workouts/${user_id}/${workout_id}/delete_exercise`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "application/json",
                    },
                    data: {
                        exercise_name: exerciseName,
                    },
                }
            );

            alert("Deleted successfully!");
            console.log("Response:", response.data);


            // Call the onDeleteSuccess callback to refresh the parent component's state
            if (onDeleteSuccess) {
                onDeleteSuccess();
            }
        } catch (error) {
            console.error("Error deleting exercise", error);
            console.log("Payload sent:", payload);
            alert("Failed to delete exercise. Check console for details.");
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
            Delete Exercise From Workout
        </Button>
    );
};

export default DeleteExercise;
