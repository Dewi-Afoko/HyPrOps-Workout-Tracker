import React from "react";
import { Table, Button } from "react-bootstrap";
import axios from "axios";
import "./../styles/tables.css";
import API_BASE_URL from "../config";

const NextFiveSets = ({ workoutData, onSetUpdate }) => {
    if (!workoutData || !workoutData.set_dicts_list) {
        return <div>Loading sets...</div>;
    }

    const handleCompleteClick = async (setOrder, restTime) => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            // ✅ API call to mark set as complete in the backend
            await axios.patch(
                `${API_BASE_URL}/workouts/${workoutData.id}/${setOrder}/mark_complete`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );

            // ✅ Trigger workout update and start rest timer
            onSetUpdate(restTime);
        } catch (error) {
            console.error("Error marking set complete:", error);
            alert("Failed to update set status.");
        }
    };

    const nextFiveSets = workoutData.set_dicts_list
        .filter((set) => !set.complete)
        .sort((a, b) => a.set_order - b.set_order)
        .slice(0, 5);

    return (
        <div className="next-five-sets">
            <h2>Next Five Sets</h2>
            {nextFiveSets.length > 0 ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Exercise</th>
                            <th>Set Number</th>
                            <th>Set Type</th>
                            <th>Focus</th>
                            <th>Reps</th>
                            <th>Loading</th>
                            <th>Rest</th>
                            <th>Notes</th>
                            <th>Complete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {nextFiveSets.map((set, index) => (
                            <tr key={set.set_order}>
                                <td>{set.exercise_name}</td>
                                <td>{set.set_number || "N/A"}</td>
                                <td>{set.set_type || "N/A"}</td>
                                <td>{set.focus || "N/A"}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading} kg` : "Bodyweight"}</td>
                                <td>{set.rest || "N/A"} s</td>
                                <td>{set.notes || "N/A"}</td>
                                <td>
                                    {index === 0 && ( // ✅ Only show button on the first exercise
                                        <Button
                                            variant="success"
                                            onClick={() => handleCompleteClick(set.set_order, set.rest)}
                                        >
                                            Mark Complete
                                        </Button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            ) : (
                <p>No incomplete sets found.</p>
            )}
        </div>
    );
};

export default NextFiveSets;
