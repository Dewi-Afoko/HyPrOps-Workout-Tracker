import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button, Form } from "react-bootstrap";

const UserRegister = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!username || !password) {
            alert("Please enter a valid username and password");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/user/register`, { username, password });
            alert(`message: ${response.data.message}`);
            navigate("/login");
        } catch (error) {
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error during registration: ${errorMessage}`);
        }
    };

    return (
        <div className="form-container">
            <h2>Register</h2>
            <Form>
                <Form.Group controlId="username" className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter a username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </Form.Group>
                <Form.Group controlId="password" className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Enter a password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                    />
                </Form.Group>
                <Button variant="success" type="button" onClick={handleSubmit}>
                    Register Now!
                </Button>
            </Form>
        </div>
    );
};

export default UserRegister;
