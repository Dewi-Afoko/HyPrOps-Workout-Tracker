import React, { useState, useEffect } from "react";
import WorkoutSplitSetView from "./WorkoutSpliSetView";
import NextFiveSets from "./WorkoutNextFiveSets";
import Countdown from "react-countdown";
import axios from "axios";
import "../styles/tables.css";
import LastFiveSets from "./WorkoutLastFiveSets";

const WorkoutLiveTrackingFeed = ({ workoutId }) => {
    const [workoutData, setWorkoutData] = useState(null);
    const [restTime, setRestTime] = useState(null); // Store rest time for countdown
    const [isCountdownActive, setIsCountdownActive] = useState(false); // Manage countdown visibility
    const [countdownExpired, setCountdownExpired] = useState(false);


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
        setCountdownExpired(true); // ✅ Show the expired message instead of hiding the countdown
    };
    

    if (!workoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div className="live-tracking-container">
            {/* NextFiveSets section */}
            <div className="next-five">
                <NextFiveSets
                    workoutData={workoutData}
                    onSetUpdate={(updatedRestTime) => handleSetUpdate(updatedRestTime)}
                />
            </div>
    
{/* Countdown Timer */}
<div className="countdown-timer">
    {isCountdownActive && restTime && !countdownExpired && (
        <Countdown
            date={Date.now() + restTime * 1000}
            onComplete={handleCountdownComplete}
            renderer={({ minutes, seconds }) => {
                const isBlinking = minutes === 0 && seconds <= 10;
                return (
                    <div className={`timer-display ${isBlinking ? "blink" : ""}`}>
                        Rest Time Until Next Set: {minutes}:{seconds < 10 ? `0${seconds}` : seconds}
                    </div>
                );
            }}
        />
    )}

    {/* Expired Message: Show when countdown reaches zero */}
    {countdownExpired && (
        <div className="timer-complete">
            <strong style={{ color: "red", fontSize: "1.5rem", fontWeight: "bold" }}>
                Time to start your next set!
            </strong>
        </div>
    )}
</div>




    
            {/* LastFiveSets section */}
            <div className="last-five">
                <LastFiveSets workoutData={workoutData} />
            </div>
    
            {/* WorkoutSplitSetView */}
            <div className="split-set-view">
                <WorkoutSplitSetView
                    workoutData={workoutData}
                    onSetUpdate={(updatedRestTime) => handleSetUpdate(updatedRestTime)}
                />
            </div>
        </div>
    );
};

export default WorkoutLiveTrackingFeed;
