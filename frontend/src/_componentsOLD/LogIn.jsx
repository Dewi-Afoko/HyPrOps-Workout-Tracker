import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form"; 
import "bootstrap/dist/css/bootstrap.min.css"; 
import { useNavigate } from "react-router-dom";

const LogIn = () => {
    const [username, setUsername] = useState(""); 
    const [password, setPassword] = useState(""); 
    const navigate = useNavigate();

    const handleButtonClick = async () => {
        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/api/login`, { username, password });
            const token = response.data.token;
            localStorage.setItem('token', token);
            alert(`API Response: ${JSON.stringify(response.data.message)}`);
            // localStorage.setItem("user_id", response.data.user_id);  #TODO Add logic for getting user from token, so user details readily available
            navigate('/profile');
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to log in. Check console for details.");
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px", textAlign: "center" }}>
            <Form>
                <Form.Group controlId="formUsername" style={{ marginBottom: "15px" }}>
                    <Form.Label style={{ color: "black", fontWeight: "bold" }}>Username</Form.Label>
                    <Form.Control
                        type="text"
                        placeholder="Enter username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{
                            borderRadius: "50px",
                            fontSize: "16px",
                            padding: "10px 15px",
                            textAlign: "center",
                        }}
                    />
                </Form.Group>
                <Form.Group controlId="formPassword" style={{ marginBottom: "20px" }}>
                    <Form.Label style={{ color: "black", fontWeight: "bold" }}>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Enter password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{
                            borderRadius: "50px",
                            fontSize: "16px",
                            padding: "10px 15px",
                            textAlign: "center",
                        }}
                    />
                </Form.Group>
                <Button
                    onClick={handleButtonClick}
                    variant="dark"
                    style={{
                        backgroundColor: "black",
                        color: "red",
                        borderRadius: "50px",
                        fontSize: "16px",
                        padding: "10px 20px",
                    }}
                >
                    Log In
                </Button>
            </Form>
        </div>
    );
};

export default LogIn;
