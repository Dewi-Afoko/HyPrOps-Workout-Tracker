import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { vi } from 'vitest';
import AddExerciseToWorkout from '../src/components/AddExerciseToWorkout';

vi.mock('axios'); // Mock axios

describe('AddExerciseToWorkout Component', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            const mockData = {
                user_id: 'testUser123',
                workout_id: 'testWorkout456',
            };
            return mockData[key];
        });

        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {}); // Mock localStorage.setItem
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    });

    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it('renders the input and button correctly', () => {
        render(<AddExerciseToWorkout />);
        expect(screen.getByPlaceholderText("Enter exercise")).toBeInTheDocument();
        expect(screen.getByText("Add Exercise!")).toBeInTheDocument();
    });

    it('alerts if the exercise name is missing', async () => {
        render(<AddExerciseToWorkout />);
        const button = screen.getByText("Add Exercise!");

        await userEvent.click(button);

        expect(window.alert).toHaveBeenCalledWith("Please enter an exercise!");
        expect(axios.post).not.toHaveBeenCalled();
    });

    it('makes an API call and saves exercise name on success', async () => {
        const mockResponse = { data: { message: "Exercise added successfully" } };
        axios.post.mockResolvedValueOnce(mockResponse); // Mock successful API response

        render(<AddExerciseToWorkout />);
        const input = screen.getByPlaceholderText("Enter exercise");
        const button = screen.getByText("Add Exercise!");

        await userEvent.type(input, "Push-ups");
        await userEvent.click(button);

        expect(axios.post).toHaveBeenCalledWith(
            "${API_BASE_URL}/workouts/testUser123/testWorkout456/add_exercise",
            { exercise_name: "Push-ups" }
        );
        expect(window.alert).toHaveBeenCalledWith('API Response: {"message":"Exercise added successfully"}');
        expect(localStorage.setItem).toHaveBeenCalledWith("exercise_name", "Push-ups");
    });

    it('alerts on API call failure', async () => {
        axios.post.mockRejectedValueOnce({
            response: { data: { error: "Exercise already exists" } },
        }); // Mock API failure

        render(<AddExerciseToWorkout />);
        const input = screen.getByPlaceholderText("Enter exercise");
        const button = screen.getByText("Add Exercise!");

        await userEvent.type(input, "Push-ups");
        await userEvent.click(button);

        expect(axios.post).toHaveBeenCalledWith(
            "${API_BASE_URL}/workouts/testUser123/testWorkout456/add_exercise",
            { exercise_name: "Push-ups" }
        );
        expect(window.alert).toHaveBeenCalledWith("Exercise already exists");
    });

    it('logs the user ID and workout ID', async () => {
        const consoleSpy = vi.spyOn(console, 'log');

        render(<AddExerciseToWorkout />);
        const input = screen.getByPlaceholderText("Enter exercise");
        const button = screen.getByText("Add Exercise!");

        await userEvent.type(input, "Push-ups");
        await userEvent.click(button);

        expect(consoleSpy).toHaveBeenCalledWith("user_id:", "testUser123", "workout_id:", "testWorkout456");
    });
});
