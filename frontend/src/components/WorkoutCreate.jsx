import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const CreateWorkout = () => {
    const navigate = useNavigate();
    const [workoutName, setWorkoutName] = useState();

    const handleWorkoutName = (e) => {
        setWorkoutName(e.target.value);
    };

    const handleButtonClick = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            alert("Auth token found, try logging in again.");
            return;
        }
        try {
            const response = await axios.post(
                `http://127.0.0.1:5000/workouts`, 
                {'workout_name' : workoutName}, 
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            alert(`API Response: ${JSON.stringify(response.data)}`);
            console.log(response.data);
            localStorage.setItem('workout_id', response.data.workout.id);
            navigate('/thisworkout');
        } catch (error) {
            console.error("Error making API call:", error.response.data.error);
            alert(error.response.data.error);
        }
    };

    return (
        <div>
        <input
        type="text"
        value={workoutName}
        onChange={handleWorkoutName}
        placeholder="Enter workout name"
        style={{
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px",
        }}
    />
        <button 
            onClick={handleButtonClick} 
        >
            Create Workout
        </button>
        </div>
    );
};

export default CreateWorkout;
