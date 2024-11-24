import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS

const GetWorkouts = () => {
    const [myWorkouts, setMyWorkouts] = useState([]); // State to store the list of workouts

    useEffect(() => {
        const fetchWorkouts = async () => {
            const user_id = localStorage.getItem("user_id");
            const token = localStorage.getItem("token"); // Retrieve token from localStorage
            if (!user_id || !token) {
                alert("User ID or token not found in localStorage.");
                return;
            }
            try {
                const response = await axios.get(
                    `http://127.0.0.1:5000/workouts/${user_id}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`, // Add token to Authorization header
                        },
                    }
                );
                setMyWorkouts(response.data); // Update state with the fetched workouts
            } catch (error) {
                console.error("Error making API call:", error);
                alert("Failed to fetch data. Check console for details.");
            }
        };

        fetchWorkouts(); // Call the function on component mount
    }, []); // Empty dependency array ensures it runs only once when the component mounts

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
                        {/* Currently requires refresh to update; use state to fix this */}
                        <ul style={{ listStyleType: "disc", paddingLeft: "20px", marginTop: "10px" }}>
                            {workout.exercise_list.map((exercise, exerciseIndex) => (
                                <li key={exerciseIndex}>{`${exerciseIndex + 1}: ${exercise.exercise_name}`}
                                <br></br>
                                {`Reps: ${exercise.reps}`}
                                <br></br>
                                {`Loading: ${exercise.loading}`}
                                <br></br>
                                {`Rest: ${exercise.rest}`}
                                <br></br>
                                {`Notes: ${exercise.performance_notes}`}
                                </li>
                                
                            ))}
                        </ul>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GetWorkouts;
