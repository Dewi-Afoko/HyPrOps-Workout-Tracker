import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Table } from "react-bootstrap";
import CompleteWorkout from "./MarkWorkoutComplete";
import { useNavigate } from "react-router-dom";

const GetWorkouts = ({ onRefresh }) => {
    const [myWorkouts, setMyWorkouts] = useState([]);
    const navigate = useNavigate();

    const fetchWorkouts = async () => {
        const user_id = localStorage.getItem("user_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token) {
            alert("User ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/api/workouts`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setMyWorkouts(response.data.workouts);
            console.log(response.data.workouts)
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    useEffect(() => {
        fetchWorkouts();
    }, []);

    useEffect(() => {
        if (onRefresh) {
            onRefresh(fetchWorkouts);
        }
    }, [onRefresh]);

    const handleStatusChange = (workoutId, newCompleteStatus) => {
        // Update the specific workout's status in myWorkouts state
        setMyWorkouts((prevWorkouts) =>
            prevWorkouts.map((workout) =>
                workout.id === workoutId
                    ? { ...workout, complete: newCompleteStatus }
                    : workout
            )
        );
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <ul style={{ listStyleType: "none", padding: 0, marginTop: "20px" }}>
                {myWorkouts.map((workout) => (
                    <li
                        key={workout}
                        style={{
                            backgroundColor: "#f8f9fa",
                            margin: "10px auto",
                            padding: "10px",
                            borderRadius: "8px",
                            width: "50%",
                            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
                        }}
                    >
                        <h3
                            style={{ cursor: "pointer", color: "red" }}
                            onClick={() => {
                                localStorage.setItem("workout_id", workout.id);
                                navigate('/thisworkout');
                            }}
                        >
                            {`Workout ${workout}`}
                        </h3>
                        {`Created: ${workout.date}`}
                        <br />
                        {`Complete? ${workout.complete}`}
                        <br />
                        {/* Pass handleStatusChange as a prop to CompleteWorkout */}
                        <CompleteWorkout
                            workoutId={workout.id}
                            initialComplete={workout.complete}
                            onStatusChange={handleStatusChange}
                        />
                        <br />
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Exercise</th>
                                    <th>Loading</th>
                                    <th>Rest Interval</th>
                                    <th>Reps</th>
                                    <th>Complete?</th>
                                    <th>Notes</th>
                                </tr>
                            </thead>
                            <tbody>
                                {workout.set_dicts_list.map((exercise) => {
                                    const exerciseName = exercise.exercise_name;
                                    const loading = exercise.loading.join(", ");
                                    const rest = exercise.rest.join(", ");
                                    const reps = exercise.reps.join(", ");
                                    const complete = exercise.complete.toString();
                                    const notes = exercise.performance_notes.join(", ");

                                    return (
                                        <tr key={`${index}-${exerciseIndex}`}>
                                            <td
                                                style={{ cursor: "pointer", color: "red" }}
                                                onClick={() => {
                                                    localStorage.setItem("exercise_name", exerciseName);
                                                    alert(`Exercise: ${exerciseName} set in localStorage!`);
                                                    console.log(complete);
                                                }}
                                            >
                                                {exerciseName}
                                            </td>
                                            <td>{loading}</td>
                                            <td>{rest}</td>
                                            <td>{reps}</td>
                                            <td>{complete}</td>
                                            <td>{notes}</td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </Table>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GetWorkouts;
