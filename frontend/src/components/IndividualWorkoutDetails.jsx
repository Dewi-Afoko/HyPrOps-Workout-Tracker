import { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Table } from "react-bootstrap";
import AddDetailsToExercise from "./AddDetailsToExercise";
import AddExerciseToWorkout from "./AddExerciseToWorkout";
import CompleteSet from "./MarkExerciseComplete";
import DeleteDetails from "./DeleteExerciseDetails";

const IndividualWorkoutDetails = () => {
    const [thisWorkout, setThisWorkout] = useState({
        exercise_list: [],
    });

    const [selectedData, setSelectedData] = useState({}); // Tracks selected data for each exercise

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

    const handleNewExercise = async () => {
        await getThisWorkout();
    };

    useEffect(() => {
        getThisWorkout();
    }, []);

    const isSelected = (exerciseName, column, valueIndex) => {
        const localStorageKey = `payload_${exerciseName}`;
        const existingPayload = JSON.parse(localStorage.getItem(localStorageKey)) || {};
        return Array.isArray(existingPayload[column]) && existingPayload[column].includes(valueIndex);
    };
    

    const handleButtonClick = (exerciseName, column, valueIndex) => {
        const localStorageKey = `payload_${exerciseName}`;
        const existingPayload = JSON.parse(localStorage.getItem(localStorageKey)) || { exercise_name: exerciseName };
    
        if (!Array.isArray(existingPayload[column])) {
            existingPayload[column] = [];
        }
    
        const columnData = existingPayload[column];
    
        if (columnData.includes(valueIndex)) {
            existingPayload[column] = columnData.filter((index) => index !== valueIndex);
        } else {
            columnData.push(valueIndex);
        }
    
        if (Object.keys(existingPayload).length === 1 && existingPayload.exercise_name) {
            localStorage.removeItem(localStorageKey);
        } else {
            localStorage.setItem(localStorageKey, JSON.stringify(existingPayload));
        }
    
        // Update the selectedData state to match the new localStorage
        setSelectedData((prev) => ({ ...prev }));
    };
    

    const renderButton = (data, exerciseName, column, index) => {
        if (data && data[index] !== undefined) {
            return (
                <button
                    className={`btn btn-sm ${
                        isSelected(exerciseName, column, index) ? "btn-success" : "btn-primary"
                    }`}
                    style={{ marginLeft: "10px" }}
                    onClick={() => handleButtonClick(exerciseName, column, index)}
                >
                    {isSelected(exerciseName, column, index) ? "Selected" : "Select"}
                </button>
            );
        }
        return null; // Do not render the button if the data is invalid
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
                        <CompleteSet
                            exerciseName={exercise.exercise_name}
                            currentComplete={exercise.complete}
                            onCompleteStatusChange={() => getThisWorkout()}
                        />
<DeleteDetails
    exerciseName={exercise.exercise_name}
    onDeleteSuccess={getThisWorkout}
/>
                        <Table striped bordered hover>
                            <thead>
                                <tr>
                                    <th>Entry</th>
                                    <th>Reps</th>
                                    <th>Loading</th>
                                    <th>Rest Interval</th>
                                    <th>Complete?</th>
                                    <th>Notes</th>
                                    <th>Actions</th>
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
                                            <td>
                                                {exercise.reps?.[index] || ""}
                                                {renderButton(exercise.reps, exercise.exercise_name, "reps_index", index)}
                                            </td>
                                            <td>
                                                {exercise.loading?.[index] || "Bodyweight"}
                                                {renderButton(
                                                    exercise.loading,
                                                    exercise.exercise_name,
                                                    "loading_index",
                                                    index
                                                )}
                                            </td>
                                            <td>
                                                {exercise.rest?.[index] || ""}
                                                {renderButton(exercise.rest, exercise.exercise_name, "rest_index", index)}
                                            </td>
                                            <td>{exercise.complete.toString()}</td>
                                            <td>
                                                {exercise.performance_notes?.[index] || ""}
                                                {renderButton(
                                                    exercise.performance_notes,
                                                    exercise.exercise_name,
                                                    "performance_notes_index",
                                                    index
                                                )}
                                            </td>
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
