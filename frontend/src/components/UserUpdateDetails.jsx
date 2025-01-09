import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import axios from "axios";

const UserUpdateDetails = () => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [currentDetails, setCurrentDetails] = useState({
        name: "",
        dob: "",
        height: "",
        weight: "",
    });
    const [name, setName] = useState("");
    const [dob, setDob] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");

    useEffect(() => {
        const fetchCurrentDetails = async () => {
            try {
                const token = localStorage.getItem("token");

                const response = await axios.get("http://127.0.0.1:5000/user/details", {
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

    const handleSubmit = async () => {
        const data = {};

        if (name) data.name = name;
        if (dob) data.dob = dob;
        if (height) data.height = height;
        if (weight) data.weight = weight;

        if (Object.keys(data).length === 0) {
            alert("Please enter the personal details you wish to update.");
            return;
        }

        try {
            const token = localStorage.getItem("token");
            const response = await axios.patch(
                `http://127.0.0.1:5000/user/update_personal_data`,
                data,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(`message: ${response.data.message}`);
            setIsModalOpen(false); // Close modal
            setCurrentDetails({ ...currentDetails, ...data }); // Update current details
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
                    <h2>Update Personal Details</h2>
                    <form>
                        <div>
                            <label htmlFor="name">Name</label>
                            <input
                                id="name"
                                type="text"
                                placeholder="Enter your name"
                                value={name}
                                onChange={(event) => setName(event.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="dob">Date of Birth</label>
                            <input
                                id="dob"
                                type="text"
                                placeholder="Enter your date of birth (YYYY/MM/DD)"
                                value={dob}
                                onChange={(event) => setDob(event.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="height">Height</label>
                            <input
                                id="height"
                                type="number"
                                placeholder="Enter your height (cm)"
                                value={height}
                                onChange={(event) => setHeight(event.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="weight">Weight</label>
                            <input
                                id="weight"
                                type="number"
                                placeholder="Enter your weight (kg)"
                                value={weight}
                                onChange={(event) => setWeight(event.target.value)}
                            />
                        </div>
                        <button type="button" onClick={handleSubmit}>
                            Update Details
                        </button>
                        <button type="button" onClick={() => setIsModalOpen(false)}>
                            Cancel
                        </button>
                    </form>
                </div>
            </div>,
            document.body
        );

    return (
        <>
            <div>
                <h3>User Details</h3>
                <p><strong>Name:</strong> {currentDetails.name || "Not provided"}</p>
                <p><strong>Date of Birth:</strong> {currentDetails.dob || "Not provided"}</p>
                <p><strong>Height:</strong> {currentDetails.height ? `${currentDetails.height} cm` : "Not provided"}</p>
                <p><strong>Weight:</strong> {currentDetails.weight ? `${currentDetails.weight} kg` : "Not provided"}</p>
            </div>
            <button onClick={() => setIsModalOpen(true)}>Update Personal Details</button>
            {isModalOpen && <Modal />}
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
        minWidth: "300px",
    },
};

export default UserUpdateDetails;
