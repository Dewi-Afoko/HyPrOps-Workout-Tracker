import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import axios from "axios";
import API_BASE_URL from "../config";

const UserUpdateDetails = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentDetails, setCurrentDetails] = useState({
        name: "",
        dob: "",
        height: "",
        weight: "",
    });

    // ✅ Use a separate state for form inputs to prevent deselection
    const [formData, setFormData] = useState({
        name: "",
        dob: "",
        height: "",
        weight: "",
    });

    useEffect(() => {
        const fetchCurrentDetails = async () => {
            try {
                const token = localStorage.getItem("token");

                const response = await axios.get(`${API_BASE_URL}/user/details`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                setCurrentDetails(response.data);
            } catch (error) {
                console.error("Error fetching user details:", error);
                alert("Failed to fetch current user details.");
            }
        };

        fetchCurrentDetails();
    }, []);

    // ✅ Pre-fill modal inputs when it opens
    useEffect(() => {
        if (isModalOpen) {
            setFormData({ ...currentDetails });
        }
    }, [isModalOpen, currentDetails]);

    const handleChange = (event) => {
        setFormData({ ...formData, [event.target.name]: event.target.value });
    };

    const handleSubmit = async () => {
        const data = {};

        if (formData.name) data.name = formData.name;
        if (formData.dob) data.dob = formData.dob;
        if (formData.height) data.height = formData.height;
        if (formData.weight) data.weight = formData.weight;

        if (Object.keys(data).length === 0) {
            alert("Please enter the personal details you wish to update.");
            return;
        }

        try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(
                `${API_BASE_URL}/user/update_personal_data`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`Message: ${response.data.message}`);
            setIsModalOpen(false);
            setCurrentDetails({ ...currentDetails, ...data });
        } catch (error) {
            console.error(error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating user details: ${errorMessage}`);
        }
    };

    const Modal = () =>
        createPortal(
            <div style={modalStyles.overlay}>
                <div style={modalStyles.content}>
                    <h2 style={modalStyles.header}>Update Personal Details</h2>
                    <form>
                        <div style={modalStyles.formGroup}>
                            <label htmlFor="name">Name</label>
                            <input
                                id="name"
                                name="name"
                                type="text"
                                placeholder="Enter your name"
                                value={formData.name}
                                onChange={handleChange}
                                style={modalStyles.input}
                            />
                        </div>
                        <div style={modalStyles.formGroup}>
                            <label htmlFor="dob">Date of Birth</label>
                            <input
                                id="dob"
                                name="dob"
                                type="date"  // ✅ Changed to Date Picker
                                value={formData.dob}
                                onChange={handleChange}
                                style={modalStyles.input}
                            />
                        </div>
                        <div style={modalStyles.formGroup}>
                            <label htmlFor="height">Height (cm)</label>
                            <input
                                id="height"
                                name="height"
                                type="number"
                                placeholder="Enter your height"
                                value={formData.height}
                                onChange={handleChange}
                                style={modalStyles.input}
                            />
                        </div>
                        <div style={modalStyles.formGroup}>
                            <label htmlFor="weight">Weight (kg)</label>
                            <input
                                id="weight"
                                name="weight"
                                type="number"
                                placeholder="Enter your weight"
                                value={formData.weight}
                                onChange={handleChange}
                                style={modalStyles.input}
                            />
                        </div>
                        <div style={modalStyles.buttonGroup}>
                            <button
                                type="button"
                                onClick={handleSubmit}
                                style={modalStyles.primaryButton}
                            >
                                Update Details
                            </button>
                            <button
                                type="button"
                                onClick={() => setIsModalOpen(false)}
                                style={modalStyles.secondaryButton}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>,
            document.body
        );

    return (
        <>
            <br />
            <button
                style={{
                    backgroundColor: "#007bff",
                    color: "white",
                    border: "none",
                    padding: "10px 20px",
                    borderRadius: "5px",
                    fontSize: "16px",
                    cursor: "pointer",
                }}
                onClick={() => setIsModalOpen(true)}
            >
                Update Personal Details
            </button>
            {isModalOpen && <Modal />}
            <div>
                <br />
                <h3>User Details</h3>
                <p><strong>Name:</strong> {currentDetails.name || "Not provided"}</p>
                <p><strong>Date of Birth:</strong> {currentDetails.dob || "Not provided"}</p>
                <p><strong>Height:</strong> {currentDetails.height ? `${currentDetails.height} cm` : "Not provided"}</p>
                <p><strong>Weight:</strong> {currentDetails.weight ? `${currentDetails.weight} kg` : "Not provided"}</p>
                <p><strong>Last Weigh In:</strong> {currentDetails.weight ? `${currentDetails.last_weighed_on}` : "Not provided"}</p>
            </div>
        </>
    );
};

const modalStyles = {
    overlay: {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
    },
    content: {
        backgroundColor: "white",
        padding: "20px",
        borderRadius: "8px",
        boxShadow: "0 2px 10px rgba(0, 0, 0, 0.1)",
        width: "400px",
    },
    header: {
        marginBottom: "20px",
    },
    formGroup: {
        marginBottom: "10px",
    },
    input: {
        width: "100%",
        padding: "10px",
        borderRadius: "5px",
        border: "1px solid #ccc",
        fontSize: "16px",
    },
    buttonGroup: {
        display: "flex",
        justifyContent: "space-between",
        marginTop: "20px",
    },
    primaryButton: {
        backgroundColor: "#007bff",
        color: "white",
        border: "none",
        padding: "10px 20px",
        borderRadius: "5px",
        fontSize: "16px",
        cursor: "pointer",
    },
    secondaryButton: {
        backgroundColor: "#6c757d",
        color: "white",
        border: "none",
        padding: "10px 20px",
        borderRadius: "5px",
        fontSize: "16px",
        cursor: "pointer",
    },
};

export default UserUpdateDetails;
