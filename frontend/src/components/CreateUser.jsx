import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form"; 
import "bootstrap/dist/css/bootstrap.min.css"; 
import { useNavigate } from "react-router-dom";

const CreateUser = () => {
    const [username, setUsername] = useState(""); // State for username
    const [password, setPassword] = useState(""); // State for password
    const navigate = useNavigate();

    const handleButtonClick = async () => {
        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/api/user`, { username, password });
            alert(`API Response: ${JSON.stringify(response.data)}`);
            localStorage.setItem("user_id", response.data.id); // Set user's ID in localStorage
            navigate('/login');
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to register. Check console for details.");
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
                    Register Now!
                </Button>
            </Form>
        </div>
    );
};

export default CreateUser;
