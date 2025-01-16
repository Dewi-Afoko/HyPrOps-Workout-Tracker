import React, { useState } from "react";
import { Table } from "react-bootstrap";
import LiveSetEdit from "./WorkoutLiveSetEdit";
import "./../styles/tables.css"; // For consistent table styling

const WorkoutSplitSetView = ({ workoutData, onSetUpdate }) => {
    const [editingField, setEditingField] = useState(null);
    const [selectedSet, setSelectedSet] = useState(null);
    const [showLiveEditModal, setShowLiveEditModal] = useState(false);

    // Separate completed and uncompleted sets
    const completedSets = workoutData.set_dicts_list?.filter((set) => set.complete) || [];
    const uncompletedSets = workoutData.set_dicts_list?.filter((set) => !set.complete) || [];

    const handleFieldClick = (set, field) => {
        setSelectedSet(set);
        setEditingField(field);
        setShowLiveEditModal(true);
    };

    const handleClose = () => {
        setShowLiveEditModal(false);
        setSelectedSet(null);
    };

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
                                <td onClick={() => handleFieldClick(set, "exercise_name")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.exercise_name}
                                </td>
                                <td onClick={() => handleFieldClick(set, "set_type")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.set_type || "N/A"}
                                </td>
                                <td onClick={() => handleFieldClick(set, "focus")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.focus || "N/A"}
                                </td>
                                <td onClick={() => handleFieldClick(set, "reps")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.reps || "N/A"}
                                </td>
                                <td onClick={() => handleFieldClick(set, "loading")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.loading ? `${set.loading} kg` : "Bodyweight"}
                                </td>
                                <td onClick={() => handleFieldClick(set, "rest")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.rest || "N/A"} s
                                </td>
                                <td onClick={() => handleFieldClick(set, "notes")} style={{ cursor: "pointer", color: "blue" }}>
                                    {set.notes || "N/A"}
                                </td>
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

            {/* LiveSetEdit Modal - Moved OUTSIDE renderTable */}
            <LiveSetEdit
                workoutId={workoutData.id}
                setData={selectedSet}
                field={editingField}
                show={showLiveEditModal}
                handleClose={handleClose}
                onUpdateSuccess={() => {
                    setShowLiveEditModal(false);
                    onSetUpdate();
                }}
            />
        </div>
    );
};

export default WorkoutSplitSetView;
