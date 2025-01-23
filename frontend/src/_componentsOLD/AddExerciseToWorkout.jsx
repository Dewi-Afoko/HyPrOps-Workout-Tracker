import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import "bootstrap/dist/css/bootstrap.min.css";

const AddExerciseToWorkout = ({ onNewExercise }) => {
    const [exerciseName, setExerciseName] = useState("");

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token || !workout_id) {
            alert("User ID, token or workout_id not found in localStorage.");
            return;
        }
        try {
            const response = await axios.post(
                `${API_BASE_URL}/workouts/${user_id}/${workout_id}/add_exercise`,
                { exercise_name: exerciseName },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`API Response: ${JSON.stringify(response.data)}`);
            localStorage.setItem("exercise_name", exerciseName);

            // Trigger the callback to refresh the workout details
            if (onNewExercise) onNewExercise();
        } catch (error) {
            console.error(error);
            const errorMessage = error.response?.data?.error || "An unknown error occurred";
            alert(errorMessage);
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px", textAlign: "center" }}>
            <Form.Group controlId="formExercise" style={{ marginBottom: "20px" }}>
                <Form.Label style={{ color: "black", fontWeight: "bold" }}>Exercise</Form.Label>
                <Form.Control
                    type="string"
                    placeholder="Enter exercise"
                    value={exerciseName}
                    onChange={(e) => setExerciseName(e.target.value)}
                    style={{
                        borderRadius: "50px",
                        fontSize: "16px",
                        padding: "10px 15px",
                        textAlign: "center",
                    }}
                />
            </Form.Group>
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
                Add a new exercise!
            </Button>
        </div>
    );
};

export default AddExerciseToWorkout;
