import { Link } from "react-router-dom";
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import LogIn from "../../components/LogIn";


export function Login() {
return (
    <div>
      {/* Full-width header */}
    <header className="text-center py-5">
        <Container>
        <Row className="justify-content-center align-items-center">
        <LogIn/>
        </Row>
        </Container> 
    </header>

      {/* Feature cards */}
    <Container className="mt-5 pb-5">
        <Row>
        <h1 className="display-4 mb-4">Features</h1>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Design Workouts</Card.Title>
                <Card.Text>
                Fully customisable and programmable workouts! Add any exercise you want, add reps, sets, loading, rest intervals and performance notes – both for individual exercises and your session as a whole!
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Record Progress/Change Workout Details in Real Time!</Card.Title>
                <Card.Text>
                Couldn't quite lift that much? Have a few more reps in the tank than you thought you would? Don't let a plan get in the way of REAL progress! Change the loading, reps or even exercise itself with our real-time tracker! You can even dynamically record rest intervals!
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        <Col md={4}>
            <Card className="text-center shadow">
            <Card.Body>
                <Card.Title>Personalised feedback based on YOUR data</Card.Title>
                <Card.Text>
                Maximise growth, strength, fitness and overall well-being with recommendations based on your training data – as well as any other information you've provided. We'll suggest loading, reps, rest-times, new exercises, deload and even REST weeks!
                </Card.Text>
            </Card.Body>
            </Card>
        </Col>
        </Row>
    </Container>
    </div>
)}
