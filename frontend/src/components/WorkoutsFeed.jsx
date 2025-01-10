import React, { useState, useEffect } from "react";
import { Table, Button, Modal } from "react-bootstrap";
import axios from "axios";
import WorkoutEditDetails from "./WorkoutEditDetails";
import WorkoutDelete from "./WorkoutDelete";
import CreateWorkout from "./WorkoutCreate";

const WorkoutsFeed = () => {
    const [myWorkouts, setMyWorkouts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showEditModal, setShowEditModal] = useState(false);
    const [editWorkoutId, setEditWorkoutId] = useState(null);
    const [refreshWorkouts, setRefreshWorkouts] = useState(false);

    const getMyWorkouts = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            setLoading(false);
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMyWorkouts(response.data.workouts || []);
        } catch (error) {
            console.error("Error fetching workouts:", error);
            alert("Failed to fetch workouts. Check console for details.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getMyWorkouts();
    }, [refreshWorkouts]);

    const toggleCompleteStatus = async (workoutId) => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/mark_complete`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            setRefreshWorkouts(!refreshWorkouts); // Refresh the table
        } catch (error) {
            console.error("Error toggling workout status:", error);
            alert("Failed to toggle workout status.");
        }
    };

    const handleWorkoutClick = (workoutId) => {
        localStorage.setItem("workout_id", workoutId);
        window.location.href = "/thisworkout"; // Navigate to the workout details page
    };

    const handleEditClick = (workoutId) => {
        setEditWorkoutId(workoutId);
        setShowEditModal(true);
    };

    const handleDeleteSuccess = () => {
        alert("Workout deleted successfully.");
        setRefreshWorkouts(!refreshWorkouts); // Refresh the workouts table after deletion
    };

    if (loading) {
        return <div>Loading workouts...</div>;
    }

    if (myWorkouts.length === 0) {
        return <div>No workouts found.</div>;
    }

    return (


        <div>
            <CreateWorkout/>
            <h3>Workouts</h3>
            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Date</th>
                        <th>Lifts</th>
                        <th>Complete</th>
                        <th>Edit</th>
                        <th>Delete</th>
                    </tr>
                </thead>
                <tbody>
                    {myWorkouts.map((workout) => {
                        const uniqueLifts = workout.sets_dict_list
                            ? [...new Set(workout.sets_dict_list.map((set) => set.exercise_name))]
                            : [];
                        return (
                            <tr key={workout.id}>
                                <td
                                    style={{ color: "blue", cursor: "pointer" }}
                                    onClick={() => handleWorkoutClick(workout.id)}
                                >
                                    {workout.workout_name}
                                </td>
                                <td>{workout.date.split("T")[0]}</td>
                                <td>{uniqueLifts.length > 0 ? uniqueLifts.join(", ") : "No exercises"}</td>
                                <td>
                                    <Button
                                        variant={workout.complete ? "success" : "warning"}
                                        onClick={() => toggleCompleteStatus(workout.id)}
                                    >
                                        {workout.complete ? "Complete" : "Incomplete"}
                                    </Button>
                                </td>
                                <td>
                                {editWorkoutId === workout.id && (
                                    <WorkoutEditDetails
                                        workoutId={workout.id}
                                        onUpdateSuccess={() => {
                                            setEditWorkoutId(null);
                                            setRefreshWorkouts(!refreshWorkouts);
                                        }}
                                        onClose={() => setEditWorkoutId(null)}
                                    />
                                )}
                                <Button
                                    variant="info"
                                    onClick={() => setEditWorkoutId(workout.id)}
                                >
                                    Edit
                                </Button>
                            </td>
                            <td>
                                <WorkoutDelete
                                    workoutId={workout.id}
                                    onDeleteSuccess={() => setRefreshWorkouts(!refreshWorkouts)} // Trigger a refresh
                                />
                            </td>
                            </tr>
                        );
                    })}
                </tbody>
            </Table>

            {/* Edit Workout Modal */}
            <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Edit Workout</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {editWorkoutId && (
                        <WorkoutEditDetails
                            workoutId={editWorkoutId}
                            onUpdateSuccess={() => {
                                setShowEditModal(false);
                                setRefreshWorkouts(!refreshWorkouts);
                            }}
                        />
                    )}
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default WorkoutsFeed;
