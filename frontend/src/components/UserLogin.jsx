import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { Button, Form } from "react-bootstrap";

const UserLogin = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!username || !password) {
            alert("Please enter your username and password");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/auth/login`, { username, password });
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("user_id", response.data.user.id);
            alert(`message: ${response.data.message}`);
            navigate("/profile");
        } catch (error) {
            console.log(error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error logging in: ${errorMessage}`);
        }
    };

    return (
        <div className="form-container">
            <h2>Login</h2>
            <Form>
                <Form.Group controlId="username" className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter your username"
                        value={username}
                        onChange={(event) => setUsername(event.target.value)}
                    />
                </Form.Group>
                <Form.Group controlId="password" className="mb-3">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                    />
                </Form.Group>
                <Button variant="primary" type="button" onClick={handleSubmit}>
                    Log In!
                </Button>
            </Form>
        </div>
    );
};

export default UserLogin;
