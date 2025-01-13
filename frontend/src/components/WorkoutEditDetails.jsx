import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";

const WorkoutEditDetails = ({ workoutId, onUpdateSuccess, handleClose }) => {
    const [name, setName] = useState("");
    const [date, setDate] = useState("");
    const [userWeight, setUserWeight] = useState("");
    const [sleepScore, setSleepScore] = useState("");
    const [sleepQuality, setSleepQuality] = useState("");

    const handleSubmit = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        const data = {};
        if (name) data.name = name;
        if (date) data.date = date;
        if (userWeight) data.user_weight = userWeight;
        if (sleepScore) data.sleep_score = sleepScore;
        if (sleepQuality) data.sleep_quality = sleepQuality;

        if (Object.keys(data).length === 0) {
            alert("Please provide at least one detail to update.");
            return;
        }

        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/edit_details`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onUpdateSuccess(); // Notify the parent to refresh data
            handleClose(); // Close the modal
        } catch (error) {
            console.error("Error updating workout details:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating workout details: ${errorMessage}`);
        }
    };

    return (
        <Form>
            <Form.Group className="mb-3">
                <Form.Label>Workout Name</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter workout name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Workout Date</Form.Label>
                <Form.Control
                    type="date"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>User Weight (kg)</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter user weight"
                    value={userWeight}
                    onChange={(e) => setUserWeight(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Sleep Score</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter sleep score"
                    value={sleepScore}
                    onChange={(e) => setSleepScore(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Sleep Quality</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter sleep quality"
                    value={sleepQuality}
                    onChange={(e) => setSleepQuality(e.target.value)}
                />
            </Form.Group>
            <div className="d-flex justify-content-end">
                <Button variant="secondary" onClick={handleClose} className="me-2">
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleSubmit}>
                    Update Details
                </Button>
            </div>
        </Form>
    );
};

export default WorkoutEditDetails;
