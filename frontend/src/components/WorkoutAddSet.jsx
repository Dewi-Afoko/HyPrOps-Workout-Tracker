import React, { useState } from "react";
import axios from "axios";

const AddSetToWorkout = ({ onSetAdded = () => {}}) => {
    const [showModal, setShowModal] = useState(false);
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
            setShowModal(false); // Close the modal
            onSetAdded(); // Notify parent component to refresh data
        } catch (error) {
            console.error("Error adding set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error adding set: ${errorMessage}`);
        }
    };

    return (
        <div>
            {/* Button to open modal */}
            <button onClick={() => setShowModal(true)}>Add Set</button>

            {/* Modal */}
            {showModal && (
                <div
                    style={{
                        position: "fixed",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        backgroundColor: "rgba(0, 0, 0, 0.5)",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                    }}
                >
                    <div
                        style={{
                            backgroundColor: "white",
                            padding: "20px",
                            borderRadius: "8px",
                            width: "400px",
                        }}
                    >
                        <h2>Add a Set</h2>
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
                            <button
                                type="button"
                                onClick={() => setShowModal(false)}
                                style={{ marginLeft: "10px" }}
                            >
                                Cancel
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AddSetToWorkout;
