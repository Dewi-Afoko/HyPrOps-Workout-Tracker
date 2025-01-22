import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
    // ✅ Track userId & workoutId in state
    const [userId, setUserId] = useState(localStorage.getItem("user_id"));
    const [workoutId, setWorkoutId] = useState(localStorage.getItem("workout_id"));

    useEffect(() => {
        // ✅ Function to check for changes in localStorage
        const checkLocalStorage = () => {
            const newUserId = localStorage.getItem("user_id");
            const newWorkoutId = localStorage.getItem("workout_id");

            // ✅ Update state if values change
            if (newUserId !== userId) setUserId(newUserId);
            if (newWorkoutId !== workoutId) setWorkoutId(newWorkoutId);
        };

        // ✅ Check every 250ms
        const interval = setInterval(checkLocalStorage, 250);

        return () => clearInterval(interval); // ✅ Cleanup on unmount
    }, [userId, workoutId]); // ✅ Dependencies to re-run effect when state changes

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Home</Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        {/* ✅ Show Profile & My Workouts only if user_id exists */}
                        {userId && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/profile">Profile</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/myworkouts">My Workouts</Link>
                                </li>
                            </>
                        )}

                        {/* ✅ Show Detailed Workout View & Live Tracker if both user_id & workout_id exist */}
                        {userId && workoutId && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/thisworkout">Detailed Workout View</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/livetracker">Live Workout Tracker</Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;
