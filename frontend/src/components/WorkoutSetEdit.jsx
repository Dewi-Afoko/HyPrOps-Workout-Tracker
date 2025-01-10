import React, { useState } from "react";
import axios from "axios";

const SetEdit = ({ workoutId, setOrder, exerciseName, onUpdateSuccess }) => {
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

        if (Object.keys(data).length === 1) {
            alert("Please provide at least one field to update.");
            return;
        }

        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/edit_set`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            onUpdateSuccess(); // Refresh the parent component
        } catch (error) {
            console.error("Error updating set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating set: ${errorMessage}`);
        }
    };

    return (
        <form>
            <div>
                <label htmlFor="exerciseName">Exercise Name</label>
                <input
                    id="exerciseName"
                    type="text"
                    placeholder="Enter exercise name"
                    value={newExerciseName}
                    onChange={(e) => setNewExerciseName(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="setType">Set Type</label>
                <input
                    id="setType"
                    type="text"
                    placeholder="Enter set type"
                    value={setType}
                    onChange={(e) => setSetType(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="reps">Reps</label>
                <input
                    id="reps"
                    type="number"
                    placeholder="Enter reps"
                    value={reps}
                    onChange={(e) => setReps(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="loading">Loading (kg)</label>
                <input
                    id="loading"
                    type="number"
                    step="0.1"
                    placeholder="Enter loading"
                    value={loading}
                    onChange={(e) => setLoading(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="focus">Focus</label>
                <input
                    id="focus"
                    type="text"
                    placeholder="Enter focus"
                    value={focus}
                    onChange={(e) => setFocus(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="rest">Rest (seconds)</label>
                <input
                    id="rest"
                    type="number"
                    step="0.1"
                    placeholder="Enter rest time"
                    value={rest}
                    onChange={(e) => setRest(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="notes">Notes</label>
                <textarea
                    id="notes"
                    placeholder="Enter notes"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </div>
            <button type="button" onClick={handleEdit}>
                Update Set
            </button>
        </form>
    );
};

export default SetEdit;
