import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import axios from "axios";

const LiveSetEdit = ({ workoutId, setData, field, onUpdateSuccess }) => {
    const [inputValue, setInputValue] = useState(setData ? setData[field] || "" : "");

    if (!setData || !field) return null; // Prevent rendering if no data is available

    const handleSave = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            // ✅ Ensure input values are properly formatted
            const formattedValue = typeof setData[field] === "number" ? Number(inputValue) : inputValue;

            // ✅ Ensure request body follows the expected API format
            const requestBody = {
                set_order: setData.set_order, // Ensure set_order is included
                [field]: formattedValue, // Update only the specific field
            };

            // ✅ Send PATCH request
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/edit_set`,
                requestBody,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            console.log("Update success:", response.data);

            onUpdateSuccess(); // Refresh workout data on success
        } catch (error) {
            console.error("Error updating set:", error.response ? error.response.data : error);
            alert(`Failed to update set: ${error.response?.data?.error || "Unknown error"}`);
        }
    };

    return (

            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Edit {field.replace("_", " ")}</Form.Label>
                    <Form.Control
                        type={typeof setData[field] === "number" ? "number" : "text"} // Auto detect input type
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        autoFocus
                    />
                </Form.Group>
                <Button variant="primary" onClick={handleSave}>
                    Save Changes
                </Button>
            </Form>

    );
};

export default LiveSetEdit;
