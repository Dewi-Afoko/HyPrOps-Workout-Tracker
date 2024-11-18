import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form"; 
import "bootstrap/dist/css/bootstrap.min.css"; 

const AddDetailsToExercise = () => {
    const [reps, setReps] = useState(0);
    const [loading, setLoading] = useState(0);
    const [rest, setRest] = useState(0);
    const [notes, setNotes] = useState("");

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem('user_id');
        const workout_id = localStorage.getItem('workout_id');
        const exercise_name = localStorage.getItem('exercise_name');

        if (!exercise_name) {
            alert("No exercise found!");
            return;
        }
        try {
            const response = await axios.patch(`http://127.0.0.1:5000/workouts/${user_id}/${workout_id}/add_details`, 
                {
                    exercise_name: exercise_name, 
                    reps: parseFloat(reps), 
                    loading: parseFloat(loading), 
                    rest: parseFloat(rest), 
                    notes: notes, 
                });
            alert(`API Response: ${JSON.stringify(response.data)}`);
        } catch (error) {
            console.error(error);
            alert(error.response?.data?.error || "An error occurred");
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px", textAlign: "center" }}>
            <Form.Group controlId="formReps" style={{ marginBottom: "20px" }}>
                <Form.Label style={{ color: "black", fontWeight: "bold" }}>Reps</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter reps"
                    value={reps}
                    onChange={(e) => setReps(e.target.value)}
                    style={{
                        borderRadius: "50px",
                        fontSize: "16px",
                        padding: "10px 15px",
                        textAlign: "center",
                    }}
                />
            </Form.Group>
            <Form.Group controlId="formLoading" style={{ marginBottom: "20px" }}>
                <Form.Label style={{ color: "black", fontWeight: "bold" }}>Loading</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter loading (weight)"
                    value={loading}
                    onChange={(e) => setLoading(e.target.value)}
                    style={{
                        borderRadius: "50px",
                        fontSize: "16px",
                        padding: "10px 15px",
                        textAlign: "center",
                    }}
                />
            </Form.Group>
            <Form.Group controlId="formRest" style={{ marginBottom: "20px" }}>
                <Form.Label style={{ color: "black", fontWeight: "bold" }}>Rest</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter rest interval (seconds)"
                    value={rest}
                    onChange={(e) => setRest(e.target.value)}
                    style={{
                        borderRadius: "50px",
                        fontSize: "16px",
                        padding: "10px 15px",
                        textAlign: "center",
                    }}
                />
            </Form.Group>
            <Form.Group controlId="formNotes" style={{ marginBottom: "20px" }}>
                <Form.Label style={{ color: "black", fontWeight: "bold" }}>Notes</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter any additional notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
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
                Add Exercise Details!
            </Button>
        </div>
    );
};

export default AddDetailsToExercise;
