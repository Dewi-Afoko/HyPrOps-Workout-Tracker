import React, { useState, useEffect } from "react";
import { Table, Button, Modal } from "react-bootstrap";
import axios from "axios";
import SetEdit from "./WorkoutSetEdit";
import AddSetToWorkout from "./WorkoutAddSet";
import SetDuplicate from "./WorkoutSetDuplicate";
import SetDeleteButton from "./WorkoutSetDelete";
import "./../styles/tables.css";

const WorkoutDetailsById = ({ workoutId, workoutData, onSetUpdate }) => {
    const [localWorkoutData, setLocalWorkoutData] = useState(workoutData || null);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editSetData, setEditSetData] = useState(null);
    const [showAddSetModal, setShowAddSetModal] = useState(false);

    // Fetch workout data if not passed as a prop
    const fetchWorkoutData = async () => {
        const token = localStorage.getItem("token");

        if (!token || !workoutId) {
            alert("Token or workout ID not found.");
            return;
        }

        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts/${workoutId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setLocalWorkoutData(response.data.workout);
            if (onSetUpdate) onSetUpdate(response.data.workout);
        } catch (error) {
            console.error("Error fetching workout details:", error);
            alert("Failed to fetch workout details.");
        }
    };

    useEffect(() => {
        if (!workoutData) {
            fetchWorkoutData();
        }
    }, [workoutId, workoutData]);

    const handleEditClick = (setData) => {
        setEditSetData(setData);
        setShowEditModal(true);
    };

    const handleAddSetClick = () => {
        setShowAddSetModal(true);
    };

    const handleCompleteToggle = async (setOrder) => {
        const token = localStorage.getItem("token");
        try {
            await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/${setOrder}/mark_complete`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            fetchWorkoutData();
        } catch (error) {
            console.error("Error toggling set completion:", error);
            alert("Failed to toggle set completion.");
        }
    };

    const currentWorkoutData = workoutData || localWorkoutData;

    if (!currentWorkoutData) {
        return <div>Loading workout details...</div>;
    }

    return (
        <div>
            <h1>Workout Details</h1>
            <p><strong>ID:</strong> {currentWorkoutData.id}</p>
            <p><strong>Name:</strong> {currentWorkoutData.workout_name}</p>
            <p><strong>Date:</strong> {currentWorkoutData.date.split("T")[0]}</p>
            <p><strong>Weight:</strong> {currentWorkoutData.user_weight || "None"}</p>
            <p><strong>Sleep Score:</strong> {currentWorkoutData.sleep_score || "None"}</p>
            <p><strong>Sleep Quality:</strong> {currentWorkoutData.sleep_quality || "None"}</p>
            <p><strong>Complete:</strong> {currentWorkoutData.complete ? "Yes" : "No"}</p>

            <Button
                variant="primary"
                onClick={handleAddSetClick}
                style={{ marginBottom: "20px" }}
            >
                Add Set
            </Button>

            <h2>Sets</h2>
            {currentWorkoutData.set_dicts_list?.length > 0 ? (
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
                            <th>Duplicate</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentWorkoutData.set_dicts_list
                            .sort((a, b) => a.set_order - b.set_order)
                            .map((set) => (
                                <tr key={set.set_order}>
                                    <td>{set.set_order}</td>
                                    <td>{set.exercise_name}</td>
                                    <td>{set.set_number}</td>
                                    <td>{set.set_type || "N/A"}</td>
                                    <td>{set.focus || "N/A"}</td>
                                    <td>{set.reps || "N/A"}</td>
                                    <td>{set.loading ? `${set.loading} kg` : "N/A"}</td>
                                    <td>{set.rest || "N/A"} s</td>
                                    <td>{set.notes || "N/A"}</td>
                                    <td>
                                        <Button
                                            variant={set.complete ? "success" : "warning"}
                                            onClick={() => handleCompleteToggle(set.set_order)}
                                        >
                                            {set.complete ? "Complete" : "Incomplete"}
                                        </Button>
                                    </td>
                                    <td>
                                        <SetDuplicate
                                            workoutId={workoutId}
                                            setOrder={set.set_order}
                                            onDuplicateSuccess={fetchWorkoutData}
                                        />
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
                                        <SetDeleteButton
                                            workoutId={workoutId}
                                            setOrder={set.set_order}
                                            onDeleteSuccess={fetchWorkoutData}
                                        />
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </Table>
            ) : (
                <p>No sets found for this workout.</p>
            )}

            {/* Edit Modal */}
            <Modal show={showEditModal} onHide={() => setShowEditModal(false)} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Edit Set</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {editSetData && (
                        <SetEdit
                            workoutId={workoutId}
                            setOrder={editSetData.set_order}
                            exerciseName={editSetData.exercise_name}
                            show={showEditModal}
                            handleClose={() => setShowEditModal(false)}
                            onUpdateSuccess={fetchWorkoutData}
                        />
                    )}
                </Modal.Body>
            </Modal>

            {/* Add Set Modal */}
            <Modal show={showAddSetModal} onHide={() => setShowAddSetModal(false)} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Add a Set</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <AddSetToWorkout
                        onSetAdded={() => {
                            setShowAddSetModal(false);
                            fetchWorkoutData();
                        }}
                    />
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default WorkoutDetailsById;
