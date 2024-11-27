import { Link } from "react-router-dom";
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import GetWorkouts from "../../components/GetMyWorkouts";
import CreateWorkout from "../../components/CreateWorkout";
import AddExerciseToWorkout from "../../components/AddExerciseToWorkout";
import AddDetailsToExercise from "../../components/AddDetailsToExercise";
import IndividualWorkoutDetails from "../../components/IndividualWorkoutDetails";



export function Dashboard() {
return (
    <div>

            <CreateWorkout/>
            <GetWorkouts/>

    </div>
)}
