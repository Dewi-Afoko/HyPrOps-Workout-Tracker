import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import WorkoutToggleComplete from "./WorkoutToggleComplete";

const WorkoutsFeed = () => {
    const [myWorkouts, setMyWorkouts] = useState(null);
    const navigate = useNavigate();

    const getMyWorkouts = async () => {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");
        if (!user_id || !token) {
            alert("User ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMyWorkouts(response.data.workouts);
            console.log("Workouts:", response.data.workouts);
        } catch (error) {
            console.error(error);
            alert("An error occurred, check console for details.");
        }
    };

    // Fetch workouts on component mount
    useEffect(() => {
        getMyWorkouts();
    }, []);

    // Handle clicking on a workout name
    const handleWorkoutClick = (workoutId) => {
        localStorage.setItem("workout_id", workoutId); // Set workout ID in localStorage
        navigate("/thisworkout"); // Navigate to the "thisworkout" page
    };

    if (!myWorkouts) {
        return <div>Loading workouts...</div>;
    }

    return (
        <div>
            <h1>Workouts</h1>
            <ul>
                {myWorkouts.map((workout) => (
                    <li key={workout.date}>
                        {/* Workout name as a clickable element */}
                        <p>
                            <strong>Name:</strong>{" "}
                            <span
                                style={{ color: "blue", cursor: "pointer" }}
                                onClick={() => handleWorkoutClick(workout.id)}
                            >
                                {workout.workout_name}
                            </span>
                        </p>
                        <p><strong>Date:</strong> {workout.date}</p>
                        <p><strong>Complete:</strong> {workout.complete ? "Yes" : "No"}</p>
                        <p>
                            <strong>Notes:</strong>{" "}
                            {workout.notes && workout.notes.length > 0 ? workout.notes.join(", ") : "No notes"}
                        </p>
                        <WorkoutToggleComplete
                            workoutId={workout.id}
                            onToggleComplete={getMyWorkouts} // Refresh list after toggling
                        />
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default WorkoutsFeed;
