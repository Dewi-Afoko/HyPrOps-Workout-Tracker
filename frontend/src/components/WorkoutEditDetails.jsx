import React, { useState } from "react";
import axios from "axios";

const WorkoutEditDetails = ({ workoutId, onUpdateSuccess }) => {
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
            onUpdateSuccess(); // Refresh parent component details
        } catch (error) {
            console.error("Error updating workout details:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating workout details: ${errorMessage}`);
        }
    };

    return (
        <div>
            <h2>Edit Workout Details</h2>
            <form>
                <div>
                    <label htmlFor="name">Workout Name</label>
                    <input
                        id="name"
                        type="text"
                        placeholder="Enter workout name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="date">Workout Date</label>
                    <input
                        id="date"
                        type="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="userWeight">User Weight (kg)</label>
                    <input
                        id="userWeight"
                        type="number"
                        placeholder="Enter user weight"
                        value={userWeight}
                        onChange={(e) => setUserWeight(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="sleepScore">Sleep Score</label>
                    <input
                        id="sleepScore"
                        type="number"
                        placeholder="Enter sleep score"
                        value={sleepScore}
                        onChange={(e) => setSleepScore(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="sleepQuality">Sleep Quality</label>
                    <input
                        id="sleepQuality"
                        type="text"
                        placeholder="Enter sleep quality"
                        value={sleepQuality}
                        onChange={(e) => setSleepQuality(e.target.value)}
                    />
                </div>
                <button type="button" onClick={handleSubmit}>
                    Update Details
                </button>
            </form>
        </div>
    );
};

export default WorkoutEditDetails;
