import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import API_BASE_URL from "../config";

const AddSetToWorkout = ({ workoutId, onSetAdded }) => {
    const [exerciseName, setExerciseName] = useState("");
    const [setType, setSetType] = useState("");
    const [reps, setReps] = useState("");
    const [loading, setLoading] = useState("");
    const [focus, setFocus] = useState("");
    const [rest, setRest] = useState("");
    const [notes, setNotes] = useState("");

    const handleSubmit = async () => {
        if (!exerciseName) {
            alert("Please specify an exercise name.");
            return;
        }

        const token = localStorage.getItem("token");
        if (!workoutId || !token) {
            alert("Workout ID or token not found in localStorage.");
            return;
        }

        const data = {
            exercise_name: exerciseName,
            set_type: setType || null,
            reps: reps || null,
            loading: loading || null,
            focus: focus || null,
            rest: rest || null,
            notes: notes || null,
        };

        try {
            const response = await axios.post(
                `${API_BASE_URL}/workouts/${workoutId}/add_set`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onSetAdded(); // Notify parent component to refresh data
        } catch (error) {
            console.error("Error adding set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error adding set: ${errorMessage}`);
        }
    };

    return (
        <Form>
            <Form.Group className="mb-3">
                <Form.Label>Exercise Name</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter exercise name"
                    value={exerciseName}
                    onChange={(e) => setExerciseName(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Set Type</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter set type (optional)"
                    value={setType}
                    onChange={(e) => setSetType(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Reps</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter number of reps (optional)"
                    value={reps}
                    onChange={(e) => setReps(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Loading (kg)</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter loading (optional)"
                    value={loading}
                    onChange={(e) => setLoading(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Focus</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter focus (optional)"
                    value={focus}
                    onChange={(e) => setFocus(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Rest (seconds)</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter rest time (optional)"
                    value={rest}
                    onChange={(e) => setRest(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Notes</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Add any notes (optional)"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </Form.Group>
            <Button variant="primary" onClick={handleSubmit}>
                Add Set
            </Button>
        </Form>
    );
};

export default AddSetToWorkout;
