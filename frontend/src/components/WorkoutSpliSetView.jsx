import React, { useState } from "react";
import { Table, Modal } from "react-bootstrap";
import LiveSetEdit from "./WorkoutLiveSetEdit"; // Component for field-specific editing
import "./../styles/tables.css";

const WorkoutSplitSetView = ({ workoutData, onSetUpdate }) => {
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedSet, setSelectedSet] = useState(null);
    const [selectedField, setSelectedField] = useState(null);

    if (!workoutData || !workoutData.set_dicts_list) {
        return <div>Loading sets...</div>;
    }

    const completedSets = workoutData.set_dicts_list.filter((set) => set.complete);
    const uncompletedSets = workoutData.set_dicts_list.filter((set) => !set.complete);

    const handleFieldClick = (set, field) => {
        setSelectedSet(set);
        setSelectedField(field);
        setShowEditModal(true);
    };

    const handleClose = () => {
        setShowEditModal(false);
        setSelectedSet(null);
        setSelectedField(null);
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
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "exercise_name")}
                                >
                                    {set.exercise_name}
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "set_type")}
                                >
                                    {set.set_type || "N/A"}
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "focus")}
                                >
                                    {set.focus || "N/A"}
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "reps")}
                                >
                                    {set.reps || "N/A"}
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "loading")}
                                >
                                    {set.loading ? `${set.loading} kg` : "Bodyweight"}
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "rest")}
                                >
                                    {set.rest || "N/A"} s
                                </td>
                                <td
                                    className="editable-cell"
                                    onClick={() => handleFieldClick(set, "notes")}
                                >
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
            <div className="split-tables-container">
                <div className="table-wrapper">{renderTable(uncompletedSets, "Incomplete Sets")}</div>
                <div className="table-wrapper">{renderTable(completedSets, "Completed Sets")}</div>
            </div>

            {/* Edit Modal (Field-Specific) */}
            <Modal show={showEditModal} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Edit {selectedField ? selectedField.replace("_", " ") : "Set"}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {selectedSet && selectedField && (
                        <LiveSetEdit
                            workoutId={workoutData.id}
                            setData={selectedSet}
                            field={selectedField}
                            onUpdateSuccess={() => {
                                handleClose();
                                onSetUpdate();
                            }}
                        />
                    )}
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default WorkoutSplitSetView;
