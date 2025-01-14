import React from "react";
import { Table } from "react-bootstrap";
import "./../styles/tables.css"; // For consistent table styling

const WorkoutSplitSetView = ({ workoutData }) => {
    // Separate completed and uncompleted sets
    const completedSets = workoutData.set_dicts_list?.filter((set) => set.complete) || [];
    const uncompletedSets = workoutData.set_dicts_list?.filter((set) => !set.complete) || [];

    const renderTable = (sets, title) => (
        <div className="table-container">
            <h3>{title}</h3>
            {sets.length > 0 ? (
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
                        {sets.map((set) => (
                            <tr key={set.set_order}>
                                <td>{set.set_order}</td>
                                <td>{set.exercise_name}</td>
                                <td>{set.set_type || "N/A"}</td>
                                <td>{set.focus || "N/A"}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading} kg` : "N/A"}</td>
                                <td>{set.rest || "N/A"} s</td>
                                <td>{set.notes || "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            ) : (
                <p>No sets found.</p>
            )}
        </div>
    );

    return (
        <div className="split-set-view">
            {renderTable(uncompletedSets, "Uncompleted Sets")}
            {renderTable(completedSets, "Completed Sets")}
        </div>
    );
};

export default WorkoutSplitSetView;

