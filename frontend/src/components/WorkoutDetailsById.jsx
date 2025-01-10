import React, { useState, useEffect } from "react";
import { Table, Button, Modal } from "react-bootstrap";
import axios from "axios";
import SetEdit from "./WorkoutSetEdit";

const WorkoutDetailsById = () => {
    const [thisWorkout, setThisWorkout] = useState(null);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editSetData, setEditSetData] = useState(null);

    const getThisWorkout = async () => {
        const token = localStorage.getItem("token");
        const workout_id = localStorage.getItem("workout_id");

        if (!token || !workout_id) {
            alert("Token or Workout ID not found in localStorage.");
            return;
        }

        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/workouts/${workout_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setThisWorkout(response.data.workout);
        } catch (error) {
            console.error("Error fetching workout details:", error);
            alert("Failed to fetch workout details. Check console for more details.");
        }
    };

    useEffect(() => {
        getThisWorkout();
    }, []);

    const handleEditClick = (setData) => {
        setEditSetData(setData); // Open the modal with the set data
        setShowEditModal(true);
    };

    const handleCompleteClick = async (setOrder) => {
        const token = localStorage.getItem("token");
        try {
            await axios.patch(
                `http://127.0.0.1:5000/workouts/${thisWorkout.id}/${setOrder}/mark_complete`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            getThisWorkout();
        } catch (error) {
            console.error("Error toggling set completion:", error);
            alert("Failed to toggle set completion.");
        }
    };

    const handleDeleteClick = async (setOrder) => {
        const token = localStorage.getItem("token");

        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/workouts/${thisWorkout.id}/delete_set/${setOrder}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            getThisWorkout(); // Refresh the table after deletion
        } catch (error) {
            console.error("Error deleting set:", error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error deleting set: ${errorMessage}`);
        }
    };

    if (!thisWorkout) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div>
            <h1>Workout Details</h1>
            <p><strong>ID:</strong> {thisWorkout.id}</p>
            <p><strong>Name:</strong> {thisWorkout.workout_name}</p>
            <p><strong>Date:</strong> {thisWorkout.date.split("T")[0]}</p>
            <p><strong>Notes:</strong> {thisWorkout.notes || "None"}</p>
            <p><strong>Complete:</strong> {thisWorkout.complete ? "Yes" : "No"}</p>

            <h2>Sets</h2>
            {thisWorkout.sets_dict_list?.length > 0 ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Order</th>
                            <th>Exercise</th>
                            <th>Set Number</th>
                            <th>Set Type</th>
                            <th>Focus</th>
                            <th>Reps</th>
                            <th>Loading</th>
                            <th>Rest</th>
                            <th>Notes</th>
                            <th>Complete</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {thisWorkout.sets_dict_list
                            .sort((a, b) => a.set_order - b.set_order)
                            .map((set) => (
                                <tr key={set.set_order}>
                                    <td>{set.set_order}</td>
                                    <td>{set.exercise_name}</td>
                                    <td>{set.set_number}</td>
                                    <td>{set.set_type || "N/A"}</td>
                                    <td>{set.focus || "N/A"}</td>
                                    <td>{set.reps || "N/A"}</td>
                                    <td>{set.loading || "N/A"}</td>
                                    <td>{set.rest || "N/A"}</td>
                                    <td>{set.notes || "N/A"}</td>
                                    <td>
                                        <Button
                                            variant={set.complete ? "success" : "warning"}
                                            onClick={() => handleCompleteClick(set.set_order)}
                                        >
                                            {set.complete ? "Complete" : "Incomplete"}
                                        </Button>
                                    </td>
                                    <td>
                                        <Button
                                            variant="info"
                                            onClick={() => handleEditClick(set)}
                                        >
                                            Edit
                                        </Button>
                                    </td>
                                    <td>
                                        <Button
                                            variant="danger"
                                            onClick={() => handleDeleteClick(set.set_order)}
                                        >
                                            Delete
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </Table>
            ) : (
                <p>No sets found for this workout.</p>
            )}

            {/* Edit Modal */}
            <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
    <Modal.Header closeButton>
        <Modal.Title>Edit Set</Modal.Title>
    </Modal.Header>
    <Modal.Body>
        {editSetData && (
            <SetEdit
                workoutId={thisWorkout.id}
                setOrder={editSetData.set_order}
                exerciseName={editSetData.exercise_name}
                onUpdateSuccess={() => {
                    setShowEditModal(false);
                    getThisWorkout();
                }}
            />
        )}
    </Modal.Body>
</Modal>

        </div>
    );
};

export default WorkoutDetailsById;
