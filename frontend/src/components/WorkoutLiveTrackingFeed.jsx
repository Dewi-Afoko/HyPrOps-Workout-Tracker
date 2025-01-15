import React, { useState, useEffect } from "react";
import WorkoutSplitSetView from "./WorkoutSpliSetView";
import NextFiveSets from "./WorkoutNextFiveSets";
import Countdown from "react-countdown";
import axios from "axios";
import "../styles/tables.css";

const WorkoutLiveTrackingFeed = ({ workoutId }) => {
    const [workoutData, setWorkoutData] = useState(null);
    const [restTime, setRestTime] = useState(null); // Store rest time for countdown
    const [isCountdownActive, setIsCountdownActive] = useState(false); // Manage countdown visibility

    const fetchWorkoutData = async () => {
        const token = localStorage.getItem("token");
        if (!token || !workoutId) {
            alert("Token or workout ID not found in localStorage.");
            return;
        }

        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/workouts/${workoutId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setWorkoutData(response.data.workout);
        } catch (error) {
            console.error("Error fetching workout data:", error);
            alert("Failed to fetch workout data. Check console for details.");
        }
    };

    useEffect(() => {
        fetchWorkoutData(); // Fetch data on component mount
    }, [workoutId]);

    const handleSetUpdate = (restTime) => {
        fetchWorkoutData(); // Refresh workout data when a set is updated

        if (restTime) {
            setRestTime(restTime); // Set the rest time for the countdown
            setIsCountdownActive(true); // Show the countdown timer
        }
    };

    const handleCountdownComplete = () => {
        setIsCountdownActive(false); // Hide the countdown timer when complete
    };

    if (!workoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div className="live-tracking-container">
            {/* Countdown Timer */}
            <div className="countdown-timer">
                {isCountdownActive && restTime && (
                    <Countdown
    date={Date.now() + restTime * 1000}
    onComplete={handleCountdownComplete}
    renderer={({ minutes, seconds }) => {
        const isBlinking = restTime <= 10; // Blink if time is less than or equal to 10 seconds
        return (
            <div className={`timer-display ${isBlinking ? 'blink' : ''}`}>
                Rest Time Until Next Set: {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
            </div>
        );
    }}
/>

                )}
            </div>

            {/* NextFiveSets section */}
            <div className="next-five">
                <NextFiveSets
                    workoutData={workoutData}
                    onSetUpdate={(updatedRestTime) => handleSetUpdate(updatedRestTime)}
                />
            </div>

            {/* WorkoutSplitSetView */}
            <div>
                <WorkoutSplitSetView
                    workoutData={workoutData}
                    onSetUpdate={(updatedRestTime) => handleSetUpdate(updatedRestTime)}
                />
            </div>
        </div>
    );
};

export default WorkoutLiveTrackingFeed;
