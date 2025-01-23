import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import axios from "axios";
import API_BASE_URL from "../config";

const SetEdit = ({ workoutId, setOrder, exerciseName, onUpdateSuccess, handleClose }) => {
    const [newExerciseName, setNewExerciseName] = useState(exerciseName || "");
    const [setType, setSetType] = useState("");
    const [reps, setReps] = useState("");
    const [loading, setLoading] = useState("");
    const [focus, setFocus] = useState("");
    const [rest, setRest] = useState("");
    const [notes, setNotes] = useState("");

    const handleEdit = async () => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        const data = { set_order: setOrder };
        if (newExerciseName) data.exercise_name = newExerciseName;
        if (setType) data.set_type = setType;
        if (reps) data.reps = parseInt(reps, 10);
        if (loading) data.loading = parseFloat(loading);
        if (focus) data.focus = focus;
        if (rest) data.rest = parseFloat(rest);
        if (notes) data.notes = notes;

        console.log("Sending PATCH request with data:", JSON.stringify(data, null, 2));  // ✅ Debugging output


        if (Object.keys(data).length === 1) {
            alert("Please provide at least one field to update.");
            return;
        }

        try {
            const response = await axios.patch(
                `${API_BASE_URL}/workouts/${workoutId}/edit_set`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onUpdateSuccess(); // Refresh the parent component
            handleClose(); // Close the modal
        } catch (error) {
            console.error("Error updating set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating set: ${errorMessage}`);
        }
    };

    return (
        <Form>
            <Form.Group className="mb-3">
                <Form.Label>Exercise Name</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter exercise name"
                    value={newExerciseName}
                    onChange={(e) => setNewExerciseName(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Set Type</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter set type"
                    value={setType}
                    onChange={(e) => setSetType(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Reps</Form.Label>
                <Form.Control
                    type="number"
                    placeholder="Enter reps"
                    value={reps}
                    onChange={(e) => setReps(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Loading (kg)</Form.Label>
                <Form.Control
                    type="number"
                    step="0.1"
                    placeholder="Enter loading"
                    value={loading}
                    onChange={(e) => setLoading(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Focus</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter focus"
                    value={focus}
                    onChange={(e) => setFocus(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Rest (seconds)</Form.Label>
                <Form.Control
                    type="number"
                    step="0.1"
                    placeholder="Enter rest time"
                    value={rest}
                    onChange={(e) => setRest(e.target.value)}
                />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Notes</Form.Label>
                <Form.Control
                    as="textarea"
                    rows={3}
                    placeholder="Enter notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </Form.Group>
            <div className="d-flex justify-content-end">
                <Button variant="secondary" onClick={handleClose} className="me-2">
                    Cancel
                </Button>
                <Button variant="primary" onClick={handleEdit}>
                    Update Set
                </Button>
            </div>
        </Form>
    );
};

export default SetEdit;
