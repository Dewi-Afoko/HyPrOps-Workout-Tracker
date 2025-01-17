import React, { useState } from "react";
import { Table, Modal } from "react-bootstrap";
import SetEdit from "./WorkoutSetEdit";
import "./../styles/tables.css";

const WorkoutSplitSetView = ({ workoutData, onSetUpdate }) => {
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedSet, setSelectedSet] = useState(null);

    if (!workoutData || !workoutData.set_dicts_list) {
        return <div>Loading sets...</div>;
    }

    const completedSets = workoutData.set_dicts_list.filter((set) => set.complete);
    const uncompletedSets = workoutData.set_dicts_list.filter((set) => !set.complete);

    const handleExerciseClick = (set) => {
        setSelectedSet(set);
        setShowEditModal(true);
    };

    const handleClose = () => {
        setShowEditModal(false);
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
                                <td
                                    style={{ color: "blue", cursor: "pointer", whiteSpace: "nowrap" }}
                                    onClick={() => handleExerciseClick(set)}
                                >
                                    {set.exercise_name}
                                </td>
                                <td>{set.set_type || "N/A"}</td>
                                <td>{set.focus || "N/A"}</td>
                                <td>{set.reps || "N/A"}</td>
                                <td>{set.loading ? `${set.loading}kg` : "Bodyweight"}</td>
                                <td>{set.rest || "N/A"}s</td>
                                <td style={{ wordWrap: "break-word", overflowWrap: "break-word" }}>
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
            {/* Flexbox Layout for Incomplete & Complete Sets Side by Side */}
            <div className="split-tables-container">
                <div className="table-wrapper">{renderTable(uncompletedSets, "All Remaining Sets")}</div>
                <div className="table-wrapper">{renderTable(completedSets, "All Completed Sets")}</div>
            </div>

            {/* Edit Modal */}
            <Modal show={showEditModal} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Edit Set</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {selectedSet && (
                        <SetEdit
                            workoutId={workoutData.id}
                            setOrder={selectedSet.set_order}
                            exerciseName={selectedSet.exercise_name}
                            onUpdateSuccess={() => {
                                handleClose();
                                onSetUpdate();
                            }}
                            handleClose={handleClose}
                        />
                    )}
                </Modal.Body>
            </Modal>
        </div>
    );
};

export default WorkoutSplitSetView;

