import { Link } from "react-router-dom";
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import GetWorkouts from "../../components/GetMyWorkouts";
import CreateWorkout from "../../components/CreateWorkout";
import AddExerciseToWorkout from "../../components/AddExerciseToWorkout";
import AddDetailsToExercise from "../../components/AddDetailsToExercise";



export function Dashboard() {
return (
    <div>
      {/* Full-width header */}
    <header className="text-center py-5">
        <Container>
        <Row className="justify-content-center align-items-center">
            <Col xs={12} md={8}>
            <h1 className="display-4 text-center">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HyPrOps ALPHA</h1>
            <div className="mt-4 d-flex justify-content-center">
        <CreateWorkout/>
            </div>
            </Col>
        </Row>
        </Container>
    </header>

      {/* Feature cards */}
    <Container className="mt-5 pb-5">
        <Row>
        <h1 className="display-4 mb-4">User Profile Page</h1>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Your Workouts</Card.Title>
                <Card.Text>
                <GetWorkouts/>
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Add Exercise to Workout</Card.Title>
                <Card.Text>
                <AddExerciseToWorkout/>
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Add Details to Exercise</Card.Title>
                <Card.Text>
                <AddDetailsToExercise/>
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        </Row>
    </Container>
    </div>
)}
