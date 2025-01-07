import axios from "axios";
import { useEffect, useState } from "react"


const WorkoutDetailsById = () => {
    const [thisWorkout, setThisWorkout] = useState(null);

    const getThisWorkout = async () => {
        const token = localStorage.getItem("token");
        const workout_id = localStorage.getItem("workout_id");
        const user_id = localStorage.getItem("user_id");
        if (!user_id || !token || !workout_id) {
            alert("User ID, Workout ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts/${workout_id}`,
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

    if (!thisWorkout) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div>
            <h1>Workout Details</h1>
            {/* Display workout properties */}
            <p>ID: {thisWorkout.id}</p>
            <p>Name: {thisWorkout.workout_name}</p>
            <p>Created At: {thisWorkout.date}</p>
            <p>Notes: {thisWorkout.notes}</p>

            {/* Display sets if available */}
            <h2>Sets</h2>
            {thisWorkout.sets_dict_list ? (
                <ul>
                    {thisWorkout.sets_dict_list
        .sort((a, b) => a.set_order - b.set_order) // Sort by set_order in ascending order
        .map((set) => (
            <li key={set.set_order}>
                <strong>Performance Order:</strong> {set.set_order} | 
                <strong>Exercise:</strong> {set.exercise_name} | 
                <strong>Set Number:</strong> {set.set_number} | 
                <strong>Set Type:</strong> {set.set_type || "N/A"} | 
                <strong> Focus:</strong> {set.focus || "N/A"} | 
                <strong> Reps:</strong> {set.reps || "N/A"} | 
                <strong> Loading:</strong> {set.loading || "N/A"}
                <strong> Rest:</strong> {set.rest || "N/A"}
                <strong> Complete?:</strong> {set.complete || "N/A"}
                <strong> Notes:</strong> {set.notes || "N/A"}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No sets found for this workout.</p>
            )}
        </div>
    );
};
export default WorkoutDetailsById;