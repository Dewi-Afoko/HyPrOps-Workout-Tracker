import { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Table } from "react-bootstrap";
import AddDetailsToExercise from "./AddDetailsToExercise";
import AddExerciseToWorkout from "./AddExerciseToWorkout";

const IndividualWorkoutDetails = () => {
    const [thisWorkout, setThisWorkout] = useState({
        exercise_list: [],
    });

    const getThisWorkout = async () => {
        const token = localStorage.getItem("token");
        const user_id = localStorage.getItem("user_id");
        const workout_id = localStorage.getItem("workout_id");
        if (!user_id || !token || !workout_id) {
            alert("User ID, Workout ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/workouts/${user_id}/${workout_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setThisWorkout(response.data.workout);
            console.log("Workout Data:", response.data.workout);
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    useEffect(() => {
        getThisWorkout();
    }, []);

    const handleNewExercise = async () => {
        // Re-fetch the updated workout data to include the new exercise
        await getThisWorkout();
    };

    return (
        <div>
            <p>Workout ID: {thisWorkout.id}</p>
            <AddExerciseToWorkout onNewExercise={handleNewExercise} />
            {thisWorkout.exercise_list &&
                thisWorkout.exercise_list.map((exercise, exerciseIndex) => (
                    <div key={`exercise-table-${exerciseIndex}`} style={{ marginBottom: "20px" }}>
                        <h4
                            style={{ cursor: "pointer", color: "red" }}
                            onClick={() => {
                                localStorage.setItem("exercise_name", exercise.exercise_name);
                                alert(`Exercise: ${exercise.exercise_name} set in localStorage!`);
                            }}
                        >
                            {exercise.exercise_name}
                        </h4>
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Entry</th>
                                    <th>Reps</th>
                                    <th>Loading</th>
                                    <th>Rest Interval</th>
                                    <th>Complete?</th>
                                    <th>Notes</th>
                                </tr>
                            </thead>
                            <tbody>
                                {(() => {
                                    const maxLength = Math.max(
                                        exercise.reps?.length || 0,
                                        exercise.loading?.length || 0,
                                        exercise.rest?.length || 0,
                                        exercise.performance_notes?.length || 0
                                    );

                                    return Array.from({ length: maxLength }).map((_, index) => (
                                        <tr key={`exercise-${exerciseIndex}-entry-${index}`}>
                                            <td>{index + 1}</td>
                                            <td>{exercise.reps?.[index] || ""}</td>
                                            <td>{exercise.loading?.[index] || "Bodyweight"}</td>
                                            <td>{exercise.rest?.[index] || ""}</td>
                                            <td>{exercise.complete}</td>
                                            <td>{exercise.performance_notes?.[index] || ""}</td>
                                        </tr>
                                    ));
                                })()}
                            </tbody>
                        </Table>
                        <AddDetailsToExercise exerciseName={exercise.exercise_name} onUpdate={getThisWorkout} />
                    </div>
                ))}
        </div>
    );
};

export default IndividualWorkoutDetails;
