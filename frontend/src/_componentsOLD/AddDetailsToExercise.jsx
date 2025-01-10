import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "bootstrap/dist/css/bootstrap.min.css";

const AddDetailsToExercise = ({ exerciseName, onUpdate }) => {
    const [reps, setReps] = useState(0);
    const [loading, setLoading] = useState(0);
    const [rest, setRest] = useState(0);
    const [notes, setNotes] = useState("");

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token || !workout_id || !exerciseName) {
            alert("User ID, token, workout_id or exercise_name not found in localStorage.");
            return;
        }
        if (reps <= 0 && loading <= 0 && rest <= 0 && notes.trim() === "") {
            alert("Please fill out SOME fields with valid values!");
            return;
        }
        try {
            await axios.patch(
                `http://127.0.0.1:5000/workouts/${user_id}/${workout_id}/add_details`,
                {
                    exercise_name: exerciseName,
                    reps: parseFloat(reps),
                    loading: parseFloat(loading),
                    rest: parseFloat(rest),
                    notes: notes,
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert("Details added successfully!");

            // Trigger the parent component's update function
            if (onUpdate) onUpdate();
        } catch (error) {
            console.error(error);
            alert(error.response?.data?.error || "An error occurred");
        }
    };

    return (
        <div style={{ maxWidth: "800px", margin: "auto", padding: "20px" }}>
            <Form>
                <Row className="align-items-center mb-3">
                    <Col>
                        <Form.Group controlId="formReps">
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
                    </Col>
                    <Col>
                        <Form.Group controlId="formLoading">
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
                    </Col>
                    <Col>
                        <Form.Group controlId="formRest">
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
                    </Col>
                    <Col>
                        <Form.Group controlId="formNotes">
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
                    </Col>
                </Row>
                <div style={{ textAlign: "center" }}>
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
                        Add set performance details!
                    </Button>
                </div>
            </Form>
        </div>
    );
};

export default AddDetailsToExercise;
