import React, { useState, useEffect } from "react";
import { ReactTabulator } from "react-tabulator";
import "react-tabulator/lib/styles.css"; // Tabulator base styles
import "react-tabulator/css/tabulator_simple.min.css"; // Simplified Tabulator theme
import axios from "axios";

const WorkoutsFeed = () => {
    const [myWorkouts, setMyWorkouts] = useState([]);
    const [loading, setLoading] = useState(true);

    const getMyWorkouts = async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            setLoading(false);
            return;
        }
        try {
            const response = await axios.get(`http://127.0.0.1:5000/workouts`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMyWorkouts(response.data.workouts || []);
        } catch (error) {
            console.error("Error fetching workouts:", error);
            alert("Failed to fetch workouts. Check console for details.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        getMyWorkouts();
    }, []);

    const toggleCompleteStatus = async (workoutId) => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Token not found in localStorage.");
            return;
        }
        try {
            const response = await axios.patch(
                `http://127.0.0.1:5000/workouts/${workoutId}/mark_complete`,
                {},
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            alert(response.data.message);
            getMyWorkouts(); // Refresh the table
        } catch (error) {
            console.error("Error toggling workout status:", error);
            alert("Failed to toggle workout status.");
        }
    };

    const columns = [
        {
            title: "Name",
            field: "workout_name",
            formatter: "link",
            formatterParams: {
                labelField: "workout_name",
                urlPrefix: "#",
            },
            cellClick: (e, cell) => {
                const workoutId = cell.getRow().getData().id;
                localStorage.setItem("workout_id", workoutId);
                window.location.href = "/thisworkout";
            },
        },
        {
            title: "Date",
            field: "date",
            formatter: (cell) => cell.getValue().split("T")[0], // Format as YYYY-MM-DD
        },
        {
            title: "Lifts",
            field: "sets_dict_list",
            formatter: (cell) => {
                const sets = cell.getValue() || [];
                const uniqueLifts = [...new Set(sets.map((set) => set.exercise_name))];
                return uniqueLifts.length > 0 ? uniqueLifts.join(", ") : "No exercises";
            },
        },
        {
            title: "Complete",
            field: "complete",
            formatter: "tickCross",
            cellClick: (e, cell) => {
                const workoutId = cell.getRow().getData().id;
                toggleCompleteStatus(workoutId);
            },
        },
    ];

    if (loading) {
        return <div>Loading workouts...</div>;
    }

    if (myWorkouts.length === 0) {
        return <div>No workouts found.</div>;
    }

    return (
        <div>
            <h3>Workouts</h3>
            <ReactTabulator
                data={myWorkouts}
                columns={columns}
                layout="fitColumns"
            />
        </div>
    );
};

export default WorkoutsFeed;
