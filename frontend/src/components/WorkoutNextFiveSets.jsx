import React from "react";
import { Table, Button } from "react-bootstrap";
import axios from "axios";
import "./../styles/tables.css"; // Ensure consistent table styling across the app

const NextFiveSets = ({ workoutData, onSetUpdate }) => {
    const handleCompleteClick = async (setOrder, restTime) => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }

        try {
            await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutData.id}/${setOrder}/mark_complete`,
                {},
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            onSetUpdate(restTime); // Pass restTime to trigger countdown
        } catch (error) {
            console.error("Error marking set complete:", error);
            alert("Failed to update set status.");
        }
    };

    // Filter the next five incomplete sets
    const nextFiveSets = workoutData.set_dicts_list
        ?.filter((set) => !set.complete)
        .sort((a, b) => a.set_order - b.set_order)
        .slice(0, 5);

    return (
        <div className="next-five-sets">
            <h2>Next Five Sets</h2>
            {nextFiveSets && nextFiveSets.length > 0 ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Order</th>
                            <th>Exercise</th>
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
                        {nextFiveSets.map((set) => (
                            <tr key={set.set_order}>
                                <td>{set.set_order}</td>
                                <td>{set.exercise_name}</td>
                                <td>{set.set_type || "N/A"}</td>
                                <td>{set.focus || "N/A"}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading} kg` : "Bodyweight"}</td>
                                <td>{set.rest || "N/A"} s</td>
                                <td>{set.notes || "N/A"}</td>
                                <td>
                                <Button
    variant="success"
    onClick={() => {
        handleCompleteClick(set.set_order);
        onSetUpdate(set.rest); // Pass the rest time to trigger the timer
    }}
>
    Mark Complete
</Button>

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
