import React from "react";
import ReactDOM from "react-dom/client";
import GetUsers from "./components/GetUsers";
import 'bootstrap/dist/css/bootstrap.min.css';
import GetWorkouts from "./components/GetMyWorkouts";
import CreateWorkout from "./components/CreateWorkout"
import CreateUser from "./components/CreateUser"
import AddExerciseToWorkout from "./components/AddExerciseToWorkout";
import AddDetailsToExercise from "./components/AddDetailsToExercise";

//TODO: Separate components to their own pages, create Navbar to link to them - don't render everything here

const App = () => {
    return (
        <div style={{ textAlign: "center", marginTop: "50px" }}>
            <h1>HyPrOps Fullstack Workout App</h1>
            <GetUsers />
            <GetWorkouts/>
            <CreateWorkout/>
            <CreateUser/>
            <AddExerciseToWorkout/>
            <AddDetailsToExercise/>
        </div>

    );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App />);