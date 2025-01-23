import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
    const [userId, setUserId] = useState(localStorage.getItem("user_id"));
    const [workoutId, setWorkoutId] = useState(localStorage.getItem("workout_id"));

    // ✅ Function to update state from localStorage
    const updateLocalStorageState = () => {
        setUserId(localStorage.getItem("user_id"));
        setWorkoutId(localStorage.getItem("workout_id"));
    };

    useEffect(() => {
        // ✅ 1. Listen for changes from other tabs/windows
        const handleStorageChange = () => updateLocalStorageState();
        window.addEventListener("storage", handleStorageChange);

        // ✅ 2. Interval to detect changes in the same tab
        const interval = setInterval(updateLocalStorageState, 500);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
            clearInterval(interval); // ✅ Cleanup to prevent memory leaks
        };
    }, []);

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
