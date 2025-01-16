import React, { useState, useEffect } from "react";
import { Modal, Form, Button } from "react-bootstrap";
import axios from "axios";

const LiveSetEdit = ({ workoutId, setData, field, show, handleClose, onUpdateSuccess }) => {
    if (!setData || !field) return null; // Don't render if no set is selected

    const [editingValue, setEditingValue] = useState(setData[field] || "");

    // Update the state when the modal opens with new data
    useEffect(() => {
        if (setData && field) {
            setEditingValue(setData[field] || "");
        }
    }, [setData, field]);

    const handleSave = async () => {
        if (!workoutId || !setData || !field) {
            alert("Missing workout ID, set data, or field.");
            return;
        }
    
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found.");
            return;
        }
    
        // Convert number fields from strings to actual numbers, or set to null if empty
        let formattedValue = editingValue;
        if (["reps", "loading", "rest"].includes(field)) {
            formattedValue = editingValue === "" ? null : Number(editingValue);
        }
    
        // Construct payload according to backend requirements
        const requestData = {
            set_order: setData.set_order, // Backend requires set_order
            [field]: formattedValue // Only updating the specific field
        };
    
        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/edit_set`,
                requestData,
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
    
            alert(response.data.message || "Update successful!");
            onUpdateSuccess(); // Refresh the workout data
            handleClose();
        } catch (error) {
            console.error("Error updating set:", error);
            alert("Failed to update set. Check console for details.");
        }
    };
    
    

    return (
        <Modal show={show} onHide={handleClose} centered>
            <Modal.Header closeButton>
                <Modal.Title>Edit {field.replace("_", " ")}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3">
                        <Form.Label>{field.replace("_", " ")}</Form.Label>
                        <Form.Control
                            type={["reps", "loading", "rest"].includes(field) ? "number" : "text"}
                            value={editingValue}
                            onChange={(e) => setEditingValue(e.target.value)}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>Cancel</Button>
                <Button variant="primary" onClick={handleSave}>Save</Button>
            </Modal.Footer>
        </Modal>
    );
};

export default LiveSetEdit;
