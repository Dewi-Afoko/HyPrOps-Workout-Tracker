import React, { createContext, useContext, useState } from 'react';
import API_BASE_URL from '../config';

const WorkoutsContext = createContext();

export const WorkoutsProvider = ({ children }) => {
    const [workouts, setWorkouts] = useState([]);

    const fetchWorkouts = async () => {
        const user_id = localStorage.getItem("user_id");
        const token = localStorage.getItem("token");
        if (!user_id || !token) {
            alert("User ID or token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.get(
                `${API_BASE_URL}/workouts/${user_id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setWorkouts(response.data);
        } catch (error) {
            console.error("Error making API call:", error);
            alert("Failed to fetch data. Check console for details.");
        }
    };

    return (
        <WorkoutsContext.Provider value={{ workouts, fetchWorkouts }}>
            {children}
        </WorkoutsContext.Provider>
    );
};

export const useWorkouts = () => useContext(WorkoutsContext);
