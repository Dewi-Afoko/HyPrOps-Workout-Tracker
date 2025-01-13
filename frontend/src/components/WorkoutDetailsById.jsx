import React, { useState, useEffect } from "react";
import { Table, Button, Modal } from "react-bootstrap";
import axios from "axios";
import SetEdit from "./WorkoutSetEdit";
import AddSetToWorkout from "./WorkoutAddSet";
import SetDuplicate from "./WorkoutSetDuplicate";
import SetDeleteButton from "./WorkoutSetDelete";

const WorkoutDetailsById = () => {
    const [thisWorkout, setThisWorkout] = useState(null);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editSetData, setEditSetData] = useState(null);
    const [showAddSetModal, setShowAddSetModal] = useState(false);

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
        setEditSetData(setData);
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

    const handleAddSetClick = () => {
        setShowAddSetModal(true);
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
            <p><strong>Weight:</strong> {thisWorkout.user_weight || "None"}</p>
            <p><strong>Sleep Score:</strong> {thisWorkout.sleep_score || "None"}</p>
            <p><strong>Sleep Quality:</strong> {thisWorkout.sleep_quality || "None"}</p>
            <p><strong>Complete:</strong> {thisWorkout.complete ? "Yes" : "No"}</p>


            {/* Add Set Modal */}
            <Button variant="primary" onClick={() => setShowAddSetModal(true)}>
    Add Set
</Button>
<AddSetToWorkout
    show={showAddSetModal}
    handleClose={() => setShowAddSetModal(false)}
    onSetAdded={getThisWorkout}
/>

            <h2>Sets</h2>
            {thisWorkout.set_dicts_list?.length > 0 ? (
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
                            <th>Duplicate Set</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {thisWorkout.set_dicts_list
                            .sort((a, b) => a.set_order - b.set_order)
                            .map((set) => (
                                <tr key={set.set_order}>
                                    <td>{set.set_order}</td>
                                    <td>{set.exercise_name}</td>
                                    <td>{set.set_number}</td>
                                    <td>{set.set_type || "N/A"}</td>
                                    <td>{set.focus || "N/A"}</td>
                                    <td>{set.reps || "N/A"}</td>
                                    <td>{set.loading ? `${set.loading}kg` : "Bodyweight"}</td>
                                    <td>{set.rest || "N/A"} secs</td>
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
                                        <SetDuplicate
                                            workoutId={thisWorkout.id}
                                            setOrder={set.set_order}
                                            onDuplicateSuccess={getThisWorkout}
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
                                            workoutId={thisWorkout.id}
                                            setOrder={set.set_order}
                                            onDeleteSuccess={getThisWorkout}
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
                            show={showEditModal}
                            handleClose={() => setShowEditModal(false)}
                            onUpdateSuccess={getThisWorkout}
                        />
                    )}
                </Modal.Body>
            </Modal>


        </div>
    );
};

export default WorkoutDetailsById;
