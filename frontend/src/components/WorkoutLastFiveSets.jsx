import React from "react";
import { Table } from "react-bootstrap";
import "./../styles/tables.css";

const LastFiveSets = ({ workoutData }) => {
    if (!workoutData || !workoutData.set_dicts_list) {
        return <div>Loading sets...</div>;
    }

    const lastFiveSets = workoutData.set_dicts_list
        .filter((set) => set.complete)
        .sort((a, b) => b.set_order - a.set_order)
        .slice(0, 5);

    return (
        <div className="last-five-sets">
            <h2>Last Five Completed Sets</h2>
            {lastFiveSets.length > 0 ? (
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Exercise</th>
                            <th>Set Number</th>
                            <th>Reps</th>
                            <th>Loading</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lastFiveSets.map((set) => (
                            <tr key={set.set_order}>
                                <td>{set.exercise_name}</td>
                                <td>{set.set_number}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading}kg` : "Bodyweight"}</td>
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
