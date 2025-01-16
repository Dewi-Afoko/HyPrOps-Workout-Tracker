import React from "react";
import { Table } from "react-bootstrap";
import "./../styles/tables.css"; // Ensure consistent table styling across the app

const LastFiveSets = ({ workoutData }) => {
    // Get the last five completed sets in reverse order
    const lastFiveSets = workoutData.set_dicts_list
        ?.filter((set) => set.complete) // Get only completed sets
        .sort((a, b) => b.set_order - a.set_order) // Reverse order (most recent first)
        .slice(0, 5); // Take only the last five

    return (
        <div className="last-five-sets">
            <h2>Last Five Sets</h2>
            {lastFiveSets && lastFiveSets.length > 0 ? (
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
                        </tr>
                    </thead>
                    <tbody>
                        {lastFiveSets.map((set) => (
                            <tr key={set.set_order}>
                                <td>{set.set_order}</td>
                                <td>{set.exercise_name}</td>
                                <td>{set.set_type || "N/A"}</td>
                                <td>{set.focus || "N/A"}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading}kg` : "Bodyweight"}</td>
                                <td>{set.rest || "N/A"}s</td>
                                <td>{set.notes || "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            ) : (
                <p>No completed sets found.</p>
            )}
        </div>
    );
};

export default LastFiveSets;
