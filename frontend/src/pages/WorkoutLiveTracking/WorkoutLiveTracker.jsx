import React, { useState, useEffect } from "react";
import WorkoutSplitSetView from "../../components/WorkoutSpliSetView";
import NextFiveSets from "../../components/WorkoutNextFiveSets";
import WorkoutDetailsById from "../../components/WorkoutDetailsById";
import axios from "axios";
import "../../styles/LiveTracking.css";

export function LiveTracking() {
    const workoutId = localStorage.getItem("workout_id");
    const [workoutData, setWorkoutData] = useState(null);

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
    }, []);

    const handleSetUpdate = () => {
        fetchWorkoutData(); // Refresh workout data when a set is updated
    };

    if (!workoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div className="live-tracking-container">
            {/* NextFiveSets section */}
            <div className="next-five">
                <NextFiveSets workoutData={workoutData} onSetUpdate={handleSetUpdate} />
            </div>

            {/* Split view section */}
            <div className="split-view">
                <WorkoutSplitSetView workoutData={workoutData} onSetUpdate={handleSetUpdate} />
            </div>

        </div>
    );
}
