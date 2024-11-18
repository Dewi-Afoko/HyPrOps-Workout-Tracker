import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { vi } from 'vitest';
import GetWorkouts from '../src/components/GetMyWorkouts';

vi.mock('axios'); // Mock axios

describe('GetWorkouts Component', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            if (key === 'user_id') return 'testUser123'; // Mock valid user ID
            return null; // Default to null for other keys
        });
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    });

    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it('renders the button correctly', () => {
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

    it('alerts if user ID is missing in localStorage', async () => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => null); // Mock no user ID
        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        expect(window.alert).toHaveBeenCalledWith("User ID not found in localStorage.");
        expect(axios.get).not.toHaveBeenCalled();
    });

    it('makes an API call and alerts with the response data on success', async () => {
        const mockResponse = { data: [{ id: 1, name: "Workout 1" }, { id: 2, name: "Workout 2" }] };
        axios.get.mockResolvedValueOnce(mockResponse); // Mock successful API response

        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        expect(axios.get).toHaveBeenCalledWith("http://127.0.0.1:5000/workouts/testUser123");
        expect(window.alert).toHaveBeenCalledWith(
            'API Response: [{"id":1,"name":"Workout 1"},{"id":2,"name":"Workout 2"}]'
        );
    });

    it('alerts on API call failure', async () => {
        const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error
        axios.get.mockRejectedValueOnce(new Error("Network error")); // Mock failed API call

        render(<GetWorkouts />);
        const button = screen.getByText("Get My Workouts");

        await userEvent.click(button);

        expect(axios.get).toHaveBeenCalledWith("http://127.0.0.1:5000/workouts/testUser123");
        expect(window.alert).toHaveBeenCalledWith("Failed to fetch data. Check console for details.");
        expect(consoleSpy).toHaveBeenCalledWith("Error making API call:", expect.any(Error));
    });
});
