import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import API_BASE_URL from "../config";

const CreateWorkout = () => {
    const navigate = useNavigate();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [workoutName, setWorkoutName] = useState("");
    const [userWeight, setUserWeight] = useState("");
    const [sleepScore, setSleepScore] = useState("");
    const [sleepQuality, setSleepQuality] = useState("");
    const [notes, setNotes] = useState("");

    const toggleModal = () => setIsModalOpen(!isModalOpen);

    const handleSubmit = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Auth token not found. Please log in again.");
            return;
        }

        const data = {
            workout_name: workoutName,
        };
        if (userWeight) data.user_weight = userWeight;
        if (sleepScore) data.sleep_score = sleepScore;
        if (sleepQuality) data.sleep_quality = sleepQuality;
        if (notes) data.notes = notes;

        try {
            const response = await axios.post(
                `${API_BASE_URL}/workouts`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`Workout created: ${response.data.message}`);
            localStorage.setItem("workout_id", response.data.workout.id);
            navigate("/thisworkout");
            toggleModal(); // Close modal on success
        } catch (error) {
            console.error("Error creating workout:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error creating workout: ${errorMessage}`);
        }
    };

    return (
        <div>
            {/* Button to open the modal */}
            <button
                style={{
                    backgroundColor: "#007bff",
                    color: "white",
                    border: "none",
                    padding: "10px 20px",
                    borderRadius: "5px",
                    cursor: "pointer",
                    fontSize: "16px",
                }}
                onClick={toggleModal}
            >
                Create Workout
            </button>

            {/* Modal */}
            {isModalOpen && (
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
                        zIndex: 1000,
                    }}
                >
                    <div
                        style={{
                            backgroundColor: "white",
                            padding: "20px",
                            borderRadius: "10px",
                            width: "400px",
                            boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
                        }}
                    >
                        <h2>Create New Workout</h2>
                        <form>
                            <div style={{ marginBottom: "10px" }}>
                                <label htmlFor="workoutName">Workout Name</label>
                                <input
                                    id="workoutName"
                                    type="text"
                                    value={workoutName}
                                    onChange={(e) => setWorkoutName(e.target.value)}
                                    placeholder="Enter workout name"
                                    style={{ width: "100%", padding: "8px" }}
                                />
                            </div>
                            <div style={{ marginBottom: "10px" }}>
                                <label htmlFor="userWeight">User Weight (kg)</label>
                                <input
                                    id="userWeight"
                                    type="number"
                                    value={userWeight}
                                    onChange={(e) => setUserWeight(e.target.value)}
                                    placeholder="Enter user weight (optional)"
                                    style={{ width: "100%", padding: "8px" }}
                                />
                            </div>
                            <div style={{ marginBottom: "10px" }}>
                                <label htmlFor="sleepScore">Sleep Score</label>
                                <input
                                    id="sleepScore"
                                    type="number"
                                    value={sleepScore}
                                    onChange={(e) => setSleepScore(e.target.value)}
                                    placeholder="Enter sleep score (optional)"
                                    style={{ width: "100%", padding: "8px" }}
                                />
                            </div>
                            <div style={{ marginBottom: "10px" }}>
                                <label htmlFor="sleepQuality">Sleep Quality</label>
                                <input
                                    id="sleepQuality"
                                    type="text"
                                    value={sleepQuality}
                                    onChange={(e) => setSleepQuality(e.target.value)}
                                    placeholder="Enter sleep quality (optional)"
                                    style={{ width: "100%", padding: "8px" }}
                                />
                            </div>
                            <div style={{ marginBottom: "10px" }}>
                                <label htmlFor="notes">Notes</label>
                                <textarea
                                    id="notes"
                                    value={notes}
                                    onChange={(e) => setNotes(e.target.value)}
                                    placeholder="Add any notes (optional)"
                                    style={{ width: "100%", padding: "8px" }}
                                />
                            </div>
                            <div style={{ display: "flex", justifyContent: "space-between" }}>
                                <button
                                    type="button"
                                    onClick={toggleModal}
                                    style={{
                                        backgroundColor: "#dc3545",
                                        color: "white",
                                        border: "none",
                                        padding: "8px 16px",
                                        borderRadius: "5px",
                                        cursor: "pointer",
                                    }}
                                >
                                    Cancel
                                </button>
                                <button
                                    type="button"
                                    onClick={handleSubmit}
                                    style={{
                                        backgroundColor: "#28a745",
                                        color: "white",
                                        border: "none",
                                        padding: "8px 16px",
                                        borderRadius: "5px",
                                        cursor: "pointer",
                                    }}
                                >
                                    Create Workout
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CreateWorkout;
