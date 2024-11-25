import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS
import { Table } from "react-bootstrap";

const GetWorkouts = ({ onRefresh }) => {
    const [myWorkouts, setMyWorkouts] = useState([]);

    const fetchWorkouts = async () => {
        const user_id = localStorage.getItem("user_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token) {
            alert("User ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/workouts/${user_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setMyWorkouts(response.data);
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    useEffect(() => {
        fetchWorkouts();
    }, []);

    // Optionally expose fetchWorkouts via props
    useEffect(() => {
        if (onRefresh) {
            onRefresh(fetchWorkouts);
        }
    }, [onRefresh]);

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            {/* Renders workoutList as numbered objects with creation date/time */}
            <ul style={{ listStyleType: "none", padding: 0, marginTop: "20px" }}>
                {myWorkouts.map((workout, index) => (
                    <li
                        key={index}
                        style={{
                            backgroundColor: "#f8f9fa",
                            margin: "10px auto",
                            padding: "10px",
                            borderRadius: "8px",
                            width: "50%",
                            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                        }}
                    >
                        {`Workout ${index + 1}`}
                        <br />
                        {`Created: ${workout.date}`}
                        <br />
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Exercise</th>
                                    <th>Loading</th>
                                    <th>Rest Interval</th>
                                    <th>Reps</th>
                                    <th>Notes</th>
                                </tr>
                            </thead>
                            <tbody>
                                {(() => {
                                    // Initialize variables to track the last seen value for each column
                                    let lastExercise = "";
                                    let lastLoading = "";
                                    let lastRest = "";
                                    let lastReps = "";
                                    let lastNotes = "";

                                    return workout.exercise_list.map((exercise, exerciseIndex) => {
                                        // Check if current value exists; if not, inherit the previous value
                                        const exerciseName = exercise.exercise_name || lastExercise;
                                        const loading = exercise.loading || lastLoading;
                                        const rest = exercise.rest || lastRest;
                                        const reps = exercise.reps || lastReps;
                                        const notes = exercise.performance_notes || lastNotes;

                                        // Update the "last seen" values
                                        lastExercise = exerciseName;
                                        lastLoading = loading;
                                        lastRest = rest;
                                        lastReps = reps;
                                        lastNotes = notes;

                                        return (
                                            <tr key={`${index}-${exerciseIndex}`}>
                                                <td>{exerciseName}</td>
                                                <td>{loading}</td>
                                                <td>{rest}</td>
                                                <td>{reps}</td>
                                                <td>{notes}</td>
                                            </tr>
                                        );
                                    });
                                })()}
                            </tbody>
                        </Table>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GetWorkouts;
