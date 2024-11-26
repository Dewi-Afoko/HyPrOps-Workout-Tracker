import { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import { Table } from "react-bootstrap";

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

    return (
<div>
Workout ID: {thisWorkout.id}
<Table striped bordered hover>
    <thead>
        <tr>
            <th>Exercise</th>
            <th>Set Number</th>
            <th>Loading</th>
            <th>Rest Interval</th>
            <th>Reps</th>
            <th>Complete?</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        {thisWorkout.exercise_list &&
            thisWorkout.exercise_list.map((exercise, exerciseIndex) => {
                // For each exercise, create rows for each item in the reps array
                return exercise.reps.map((rep, repIndex) => {
                    return (
                        <tr key={`exercise-${exerciseIndex}-rep-${repIndex}`}>
                            <td>{repIndex === 0 ? exercise.exercise_name : ''}</td> {/* Only show exercise name for the first row */}
                            <td>{repIndex + 1}</td> {/* Set number starts from 1 */}
                            <td>{exercise.loading[repIndex] || ''}</td>
                            <td>{exercise.rest[repIndex] || ''}</td>
                            <td>{rep}</td>
                            <td>{exercise.complete}</td>
                            <td>{exercise.performance_notes[repIndex] || ''}</td>
                        </tr>
                    );
                });
            })}
    </tbody>
</Table>

</div>
    );
};

export default IndividualWorkoutDetails;
