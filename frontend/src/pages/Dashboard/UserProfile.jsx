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
      {/* Full-width header */}
    <header className="text-center py-5">
        <Container>
        <Row className="justify-content-center align-items-center">
            <Col xs={12} md={8}>
            <div className="mt-4 d-flex justify-content-center">
            <CreateWorkout/>
            <AddExerciseToWorkout/>
            <AddDetailsToExercise/>
            <br></br>
            </div>
            </Col>
        </Row>
        </Container>
    </header>

      {/* Feature cards */}
    <Container className="mt-5 pb-5">

        <h1 className="display-4 mb-4">Your Workouts</h1>
        <GetWorkouts/>

    </Container>
    </div>
)}
