import React, { useState, useEffect } from "react";
import WorkoutSplitSetView from "./WorkoutSpliSetView";
import NextFiveSets from "./WorkoutNextFiveSets";
import Countdown from "react-countdown";
import axios from "axios";
import "../styles/tables.css";
import LastFiveSets from "./WorkoutLastFiveSets";
import API_BASE_URL from "../config";

const WorkoutLiveTrackingFeed = ({ workoutId }) => {
    const [workoutData, setWorkoutData] = useState(null);
    const [restTime, setRestTime] = useState(null);
    const [isCountdownActive, setIsCountdownActive] = useState(false);
    const [countdownEndTime, setCountdownEndTime] = useState(null);

    const fetchWorkoutData = async () => {
        const token = localStorage.getItem("token");
        if (!token || !workoutId) {
            alert("Token or workout ID not found in localStorage.");
            return;
        }

        try {
            const response = await axios.get(
                `${API_BASE_URL}/workouts/${workoutId}`,
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
        fetchWorkoutData();
    }, [workoutId]);

    const handleSetUpdate = (newRestTime) => {
        fetchWorkoutData();

        if (newRestTime) {
            const endTime = Date.now() + newRestTime * 1000;
            setCountdownEndTime(endTime);
            setIsCountdownActive(true);
        }
    };

    const handleCountdownComplete = () => {
        setIsCountdownActive(false);
        setCountdownEndTime(null);
    };

    if (!workoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div className="live-tracking-container">
            {/* Timer Section (Centered) */}
            <div className="timer-container">
                {!isCountdownActive && !countdownEndTime && (
                    <div className="timer-complete">
                        <strong>Time to start your next set!</strong>
                    </div>
                )}

                {isCountdownActive && countdownEndTime && (
                    <Countdown
                        key={countdownEndTime}
                        date={countdownEndTime}
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
            </div>

            {/* Flexbox Layout for NextFiveSets and LastFiveSets */}
            <div className="tracking-layout">
                <div className="tracking-section">
                    <NextFiveSets
                        workoutData={workoutData}
                        onSetUpdate={(updatedRestTime) => handleSetUpdate(updatedRestTime)}
                    />
                </div>
                <div className="tracking-section">
                    <LastFiveSets workoutData={workoutData} />
                </div>
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
