import React, { useState, useEffect } from "react";
import { Form, Button, ListGroup } from "react-bootstrap";
import axios from "axios";

const WorkoutEditDetails = ({ workoutId, onUpdateSuccess, handleClose }) => {
    const [name, setName] = useState("");
    const [date, setDate] = useState("");
    const [userWeight, setUserWeight] = useState("");
    const [sleepScore, setSleepScore] = useState("");
    const [sleepQuality, setSleepQuality] = useState("");
    const [notes, setNotes] = useState([]);
    const [newNote, setNewNote] = useState("");

    useEffect(() => {
        fetchWorkoutDetails();
    }, []);

    const fetchWorkoutDetails = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts/${workoutId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });

            const workout = response.data.workout;
            setName(workout.workout_name || "");
            setDate(workout.date ? workout.date.split("T")[0] : "");
            setUserWeight(workout.user_weight || "");
            setSleepScore(workout.sleep_score || "");
            setSleepQuality(workout.sleep_quality || "");
            setNotes(workout.notes || []);
        } catch (error) {
            console.error("Error fetching workout details:", error);
            alert("Failed to load workout details.");
        }
    };

    const handleSubmitDetails = async () => {
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
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            alert(response.data.message);
            onUpdateSuccess();
        } catch (error) {
            console.error("Error updating workout details:", error);
            alert("Failed to update workout details.");
        }
    };

    const handleAddNote = async () => {
        if (!newNote.trim()) {
            alert("Please enter a note.");
            return;
        }

        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/add_notes`,
                { notes: newNote },
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            alert(response.data.message);
            setNotes([...notes, newNote]); // Append new note to the list
            setNewNote(""); // Clear input field
            onUpdateSuccess();
        } catch (error) {
            console.error("Error adding notes:", error);
            alert("Failed to add notes.");
        }
    };

    const handleDeleteNote = async (index) => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        if (!window.confirm("Are you sure you want to delete this note?")) return;

        try {
            await axios.delete(
                `http://127.0.0.1:5000/workouts/${workoutId}/delete_note/${index}`,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            setNotes(notes.filter((_, i) => i !== index)); // Remove note from local state
            alert("Note deleted successfully.");
            fetchWorkoutDetails(); // Refresh without closing modal
        } catch (error) {
            console.error("Error deleting note:", error);
            alert("Failed to delete note.");
        }
    };

    const handleSubmit = () => {
        handleSubmitDetails();
        if (newNote) {
            handleAddNote();
        }
        handleClose();
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

            {/* Notes Section */}
            <Form.Group className="mb-3">
                <Form.Label>Existing Notes</Form.Label>
                <ListGroup>
                    {notes.length > 0 ? (
                        notes.map((note, index) => (
                            <ListGroup.Item key={index} className="d-flex justify-content-between align-items-center">
                                {note}
                                <Button variant="danger" size="sm" onClick={() => handleDeleteNote(index)}>
                                    ❌
                                </Button>
                            </ListGroup.Item>
                        ))
                    ) : (
                        <p>No notes available.</p>
                    )}
                </ListGroup>
            </Form.Group>

            {/* Add New Note Section */}
            <Form.Group className="mb-3">
                <Form.Label>Add New Note</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter a new note"
                    value={newNote}
                    onChange={(e) => setNewNote(e.target.value)}
                />
                <Button variant="success" className="mt-2" onClick={handleAddNote}>
                    Add Note
                </Button>
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
