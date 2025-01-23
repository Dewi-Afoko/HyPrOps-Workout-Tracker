import React, { useState, useEffect } from "react";
import WorkoutDetailsById from "../../components/WorkoutDetailsById";
import axios from "axios";
import API_BASE_URL from "../../config";

export function SpecificWorkout() {
    const workoutId = localStorage.getItem("workout_id");
    const [workoutData, setWorkoutData] = useState(null);

    const fetchWorkoutData = async () => {
        const token = localStorage.getItem("token");
        if (!token || !workoutId) {
            alert("Token or workout ID not found.");
            return;
        }

        try {
            const response = await axios.get(
                `${API_BASE_URL}/workouts/${workoutId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setWorkoutData(response.data.workout);
        } catch (error) {
            console.error("Error fetching workout details:", error);
            alert("Failed to fetch workout details.");
        }
    };

    useEffect(() => {
        fetchWorkoutData();
    }, [workoutId]);

    if (!workoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div>
            <h1>Workout Details</h1>
            <p><strong>Name:</strong> {workoutData.workout_name}</p>
            <p><strong>Date:</strong> {workoutData.date.split("T")[0]}</p>
            <p><strong>User Weight:</strong> {workoutData.user_weight || "None"}</p>
            <p><strong>Sleep Score:</strong> {workoutData.sleep_score || "None"}</p>
            <p><strong>Sleep Quality:</strong> {workoutData.sleep_quality || "None"}</p>
            <p><strong>Complete:</strong> {workoutData.complete ? "Yes" : "No"}</p>
            <div>
            {workoutData.notes.length > 0 ? (
                <ul>
                {workoutData.notes.map((note, index) => (
                    <li key={index}><strong>Note {index + 1}:</strong> {note}</li>
                ))}
                </ul>
            ) : (
                <p>No notes</p>
            )}
            </div>

            <WorkoutDetailsById workoutId={workoutId} workoutData={workoutData} />
        </div>
    );
}
