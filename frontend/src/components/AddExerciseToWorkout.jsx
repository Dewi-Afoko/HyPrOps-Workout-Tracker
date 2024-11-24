import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form"; 
import "bootstrap/dist/css/bootstrap.min.css"; 

const AddExerciseToWorkout = () => {
    const [exerciseName, setExerciseName] = useState(""); // State for exercise being added, currently name as a string
    const handleButtonClick = async () => {
        const user_id = localStorage.getItem('user_id');
        const workout_id = localStorage.getItem('workout_id');
        const token = localStorage.getItem('token'); // Retrieve token from localStorage
        if (!user_id || !token || !workout_id) {
            alert("User ID, token or workout_id not found in localStorage.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/workouts/${user_id}/${workout_id}/add_exercise`, { exercise_name: exerciseName }, {
                headers: {
                Authorization: `Bearer ${token}`, // Add token to Authorization header
                },
            });
            alert(`API Response: ${JSON.stringify(response.data)}`);
            localStorage.setItem("exercise_name", exerciseName);
        } catch (error) {
            console.error(error);
            const errorMessage = error.response?.data?.error || "An unknown error occurred";
            alert(errorMessage);
        }}
    

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
                    Add Exercise!
                </Button>
        </div>
    );
};

export default AddExerciseToWorkout;
