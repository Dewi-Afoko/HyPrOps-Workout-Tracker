import React from "react";
import ReactDOM from "react-dom/client";
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { HomePage } from "./pages/Homepage/LandingPage";
import { RegisterUser } from "./pages/Register/Register";
import { Login } from "./pages/Login/Login";
import { Dashboard } from "./pages/Dashboard/UserProfile";
import { WorkoutsProvider } from "./context/WorkoutsContext";
import { SpecificWorkout } from "./pages/WorkoutDetails/SpecificWorkout";
import NavBar from "./components/Navbar";
import { AllMyWorkouts } from "./pages/WorkoutFeed/AllMyWorkouts";
import { LiveTracking } from "./pages/WorkoutLiveTracking/WorkoutLiveTracker";

const App = () => {
    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>GainsTrust Granular Workout App ALPHA</h1>
            <BrowserRouter>
                <NavBar />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/register" element={<RegisterUser />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/profile" element={<Dashboard />} />
                    <Route path="/thisworkout" element={<SpecificWorkout />} />
                    <Route path="/myworkouts" element={<AllMyWorkouts />} />
                    <Route path="/livetracker" element={<LiveTracking />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
};

ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <WorkoutsProvider>
            <App />
        </WorkoutsProvider>
    </React.StrictMode>
);
