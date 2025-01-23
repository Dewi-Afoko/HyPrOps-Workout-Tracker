import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axios from "axios";
import { vi } from "vitest";
import GetWorkouts from "../src/components/GetMyWorkouts";

vi.mock("axios"); // Mock axios

describe("GetWorkouts Component", () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, "getItem").mockImplementation((key) => {
            if (key === "user_id") return "testUser123"; // Mock valid user ID
            return null; // Default to null for other keys
        });
        vi.spyOn(window, "alert").mockImplementation(() => {}); // Mock alert
    });

    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it("renders the button correctly", () => {
        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");
        expect(button).toBeInTheDocument();
        expect(button).toHaveStyle({
            backgroundColor: "black",
            color: "red",
            borderRadius: "50px",
            fontSize: "16px",
            padding: "10px 20px",
        });
    });

    it("alerts if user ID is missing in localStorage", async () => {
        vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => null); // Mock no user ID
        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        expect(window.alert).toHaveBeenCalledWith("User ID not found in localStorage.");
        expect(axios.get).not.toHaveBeenCalled(); // Ensure no API call is made
    });

    it("makes an API call and updates the workout list on success", async () => {
        const mockResponse = { data: [{ id: 1, date: "2024-01-01" }, { id: 2, date: "2024-01-02" }] };
        axios.get.mockResolvedValueOnce(mockResponse); // Mock successful API response

        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        // Assert that axios.get was called with the correct URL
        expect(axios.get).toHaveBeenCalledWith("${API_BASE_URL}/workouts/testUser123");

        // Assert that the workouts are rendered correctly
        const workoutItems = await screen.findAllByRole("listitem");
        expect(workoutItems).toHaveLength(2);
        expect(workoutItems[0]).toHaveTextContent("Workout 1 - 2024-01-01");
        expect(workoutItems[1]).toHaveTextContent("Workout 2 - 2024-01-02");
    });

    it("alerts on API call failure", async () => {
        const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {}); // Mock console.error
        axios.get.mockRejectedValueOnce(new Error("Network error")); // Mock failed API call

        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        // Assert that axios.get was called with the correct URL
        expect(axios.get).toHaveBeenCalledWith("${API_BASE_URL}/workouts/testUser123");

        // Assert that the failure alert is shown
        expect(window.alert).toHaveBeenCalledWith("Failed to fetch data. Check console for details.");

        // Assert that the error was logged to the console
        expect(consoleSpy).toHaveBeenCalledWith("Error making API call:", expect.any(Error));
    });
});
