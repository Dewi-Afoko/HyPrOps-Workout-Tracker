import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import "bootstrap/dist/css/bootstrap.min.css"; // Import Bootstrap CSS

const GetWorkouts = () => {
    const [myWorkouts, setMyWorkouts] = useState([]); // State to store the list of workouts

    const handleButtonClick = async () => {
        const user_id = localStorage.getItem("user_id");
        if (!user_id) {
            alert("User ID not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts/${user_id}`);
            setMyWorkouts(response.data); // Update state with the fetched workouts
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
            <Button 
                onClick={handleButtonClick} 
                variant="dark" 
                style={{
                    backgroundColor: "black",
                    color: "red",
                    borderRadius: "50px",
                    fontSize: "16px",
                    padding: "10px 20px",
                }}
            >
                Get My Workouts
            </Button>
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
                        {`Workout ${index + 1} - ${workout.date}`} {/*${workout.id} works to diplay*/}
                        <br></br>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default GetWorkouts;