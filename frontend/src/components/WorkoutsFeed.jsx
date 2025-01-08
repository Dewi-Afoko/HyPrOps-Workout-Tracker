import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import WorkoutToggleComplete from "./WorkoutToggleComplete";
import WorkoutDelete from "./WorkoutDelete";

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
            setMyWorkouts(response.data.workouts || []);
            console.log("Workouts:", response.data.workouts);
        } catch (error) {
            console.error("Error fetching workouts:", error);
            if (error.response && error.response.status === 404) {
                setMyWorkouts([]); // Handle no workouts found
            } else {
                alert("An error occurred while fetching workouts.");
            }}
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

    if (myWorkouts === null) {
        return <div>Loading workouts...</div>; // While data is being fetched
    }

    if (myWorkouts.length === 0) {
        return <div>No workouts found.</div>; // When the workouts list is empty
    }

    return (
        <div>
            <h1>Workouts</h1>
            {myWorkouts.length === 0 ? (
                <p>No workouts found. Add a workout to get started!</p>
            ) : (
                <ul>
                    {myWorkouts.map((workout) => (
                        <li key={workout.id}>
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
                                {workout.notes?.length > 0 ? workout.notes.join(", ") : "No notes"}
                            </p>
                            <WorkoutToggleComplete
                                workoutId={workout.id}
                                onToggleComplete={getMyWorkouts} // Refresh list after toggling
                            />
                            <WorkoutDelete
                                workoutId={workout.id}
                                onDeleteSuccess={getMyWorkouts} // Refresh the feed
                            />
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
    }

export default WorkoutsFeed;
