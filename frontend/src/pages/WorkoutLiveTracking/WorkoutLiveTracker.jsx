import React from "react";
import WorkoutLiveTrackingFeed from "../../components/WorkoutLiveTrackingFeed";

export function LiveTracking() {
    const workoutId = localStorage.getItem("workout_id");

    if (!workoutId) {
        return <div>Workout ID not found in localStorage.</div>;
    }

    return <WorkoutLiveTrackingFeed workoutId={workoutId} />;
}
