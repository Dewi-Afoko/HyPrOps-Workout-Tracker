import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const UserUpdateDetails = () => {
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
    const navigate = useNavigate();

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
            navigate(0); 
        } catch (error) {
            console.error(error);
            const errorMessage = error.response?.data?.error || "An error occurred";
            alert(`Error updating user details: ${errorMessage}`);
        }
    };

    return (
        <div>
            <h1>Update Personal Details</h1>

            {/* Display current user details */}
            <h2>Current Details</h2>
            <p><strong>Name:</strong> {currentDetails.name || "Not provided"}</p>
            <p><strong>Date of Birth:</strong> {currentDetails.dob || "Not provided"}</p>
            <p><strong>Height:</strong> {currentDetails.height ? `${currentDetails.height} cm` : "Not provided"}</p>
            <p><strong>Weight:</strong> {currentDetails.weight ? `${currentDetails.weight} kg` : "Not provided"}</p>

            {/* Form for updating details */}
            <form>
                <div>
                    <label htmlFor="name">Name</label>
                    <input
                        id="name"
                        type="text"
                        placeholder={currentDetails.name || "Enter your name"}
                        value={name} // Keep this empty for no prefilled values
                        onChange={(event) => setName(event.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="dob">Date of Birth</label>
                    <input
                        id="dob"
                        type="text"
                        placeholder={currentDetails.dob || "Enter your date of birth (YYYY/MM/DD)"}
                        value={dob} // Keep this empty for no prefilled values
                        onChange={(event) => setDob(event.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="height">Height</label>
                    <input
                        id="height"
                        type="number"
                        placeholder={currentDetails.height ? `${currentDetails.height} cm` : "Enter your height (cm)"}
                        value={height} // Keep this empty for no prefilled values
                        onChange={(event) => setHeight(event.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="weight">Weight</label>
                    <input
                        id="weight"
                        type="number"
                        placeholder={currentDetails.weight ? `${currentDetails.weight} kg` : "Enter your weight (kg)"}
                        value={weight} // Keep this empty for no prefilled values
                        onChange={(event) => setWeight(event.target.value)}
                    />
                </div>
                <button type="button" onClick={handleSubmit}>
                    Update Personal Details
                </button>
            </form>
        </div>
    );
};

export default UserUpdateDetails;
