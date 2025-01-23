import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
    const [userId, setUserId] = useState(localStorage.getItem("user_id"));
    const [workoutId, setWorkoutId] = useState(localStorage.getItem("workout_id"));
    const [isNavCollapsed, setIsNavCollapsed] = useState(true); // ✅ Track collapse state

    // ✅ Function to update localStorage state
    const updateLocalStorageState = () => {
        setUserId(localStorage.getItem("user_id"));
        setWorkoutId(localStorage.getItem("workout_id"));
    };

    useEffect(() => {
        // ✅ 1. Listen for localStorage changes from other tabs
        const handleStorageChange = () => updateLocalStorageState();
        window.addEventListener("storage", handleStorageChange);

        // ✅ 2. Check for updates in the same tab (every 500ms)
        const interval = setInterval(updateLocalStorageState, 500);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
            clearInterval(interval);
        };
    }, []);

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">Home</Link>
                
                {/* ✅ Toggle Button to Expand Navbar on Mobile */}
                <button
                    className="navbar-toggler"
                    type="button"
                    aria-controls="navbarNav"
                    aria-expanded={!isNavCollapsed}
                    aria-label="Toggle navigation"
                    onClick={() => setIsNavCollapsed(!isNavCollapsed)} // ✅ Manually toggle
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                {/* ✅ Conditional class for collapsing navbar */}
                <div className={`collapse navbar-collapse ${isNavCollapsed ? "" : "show"}`} id="navbarNav">
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
