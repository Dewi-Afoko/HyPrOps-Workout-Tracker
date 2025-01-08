import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AddSetToWorkout = () => {
    const [exerciseName, setExerciseName] = useState("");
    const [setType, setSetType] = useState("");
    const [reps, setReps] = useState("");
    const [loading, setLoading] = useState("");
    const [focus, setFocus] = useState("");
    const [rest, setRest] = useState("");
    const [notes, setNotes] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!exerciseName) {
            alert("Please specify an exercise name.");
            return;
        }

        const workoutId = localStorage.getItem("workout_id");
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
                `http://127.0.0.1:5000/workouts/${workoutId}/add_set`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            navigate(0); // Refresh the page or navigate as needed
        } catch (error) {
            console.error("Error adding set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error adding set: ${errorMessage}`);
        }
    };

    return (
        <div>
            <h1>Add a Set to Workout</h1>
            <form>
                <div>
                    <label htmlFor="exerciseName">Exercise Name</label>
                    <input
                        id="exerciseName"
                        type="text"
                        placeholder="Enter exercise name"
                        value={exerciseName}
                        onChange={(e) => setExerciseName(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="setType">Set Type</label>
                    <input
                        id="setType"
                        type="text"
                        placeholder="Enter set type (optional)"
                        value={setType}
                        onChange={(e) => setSetType(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="reps">Reps</label>
                    <input
                        id="reps"
                        type="number"
                        placeholder="Enter number of reps (optional)"
                        value={reps}
                        onChange={(e) => setReps(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="loading">Loading (Weight)</label>
                    <input
                        id="loading"
                        type="number"
                        placeholder="Enter loading in kg (optional)"
                        value={loading}
                        onChange={(e) => setLoading(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="focus">Focus</label>
                    <input
                        id="focus"
                        type="text"
                        placeholder="Enter focus (optional)"
                        value={focus}
                        onChange={(e) => setFocus(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="rest">Rest (Seconds)</label>
                    <input
                        id="rest"
                        type="number"
                        placeholder="Enter rest time in seconds (optional)"
                        value={rest}
                        onChange={(e) => setRest(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="notes">Notes</label>
                    <textarea
                        id="notes"
                        placeholder="Add any notes (optional)"
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                    />
                </div>
                <button type="button" onClick={handleSubmit}>
                    Add Set
                </button>
            </form>
        </div>
    );
};

export default AddSetToWorkout;
