import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { vi } from 'vitest';
import CreateWorkout from '../src/components/CreateWorkout';

vi.mock('axios'); // Mock axios

describe('CreateWorkout Component', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            if (key === 'user_id') return 'testUser123'; // Mock valid user ID
            return null; // Default to null for other keys
        });
        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {}); // Mock localStorage.setItem
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    });

    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it('renders the button correctly', () => {
        render(<CreateWorkout />);
        const button = screen.getByText("Create Workout");
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
        render(<CreateWorkout />);
        const button = screen.getByText("Create Workout");

        await userEvent.click(button);

        expect(window.alert).toHaveBeenCalledWith("User ID not found in localStorage.");
        expect(axios.post).not.toHaveBeenCalled();
    });

    it('makes an API call and saves workout ID on success', async () => {
        const mockResponse = { data: { workout_id: 'workout456' } };
        axios.post.mockResolvedValueOnce(mockResponse); // Mock successful API response

        render(<CreateWorkout />);
        const button = screen.getByText("Create Workout");

        await userEvent.click(button);

        expect(axios.post).toHaveBeenCalledWith("http://127.0.0.1:5000/workouts/testUser123");
        expect(window.alert).toHaveBeenCalledWith('API Response: {"workout_id":"workout456"}');
        expect(localStorage.setItem).toHaveBeenCalledWith("workout_id", "workout456");
    });

    it('alerts on API call failure', async () => {
        const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error
        axios.post.mockRejectedValueOnce(new Error("Network error")); // Mock failed API call
    
        render(<CreateWorkout />);
        const button = screen.getByText("Create Workout");
    
        await userEvent.click(button);
    
        expect(axios.post).toHaveBeenCalledWith("http://127.0.0.1:5000/workouts/testUser123");
        expect(window.alert).toHaveBeenCalledWith("Failed to fetch data. Check console for details.");
        expect(consoleSpy).toHaveBeenCalledWith("Error making API call:", expect.any(Error));
    
        consoleSpy.mockRestore(); // Ensure we clean up the mock
    });
});
