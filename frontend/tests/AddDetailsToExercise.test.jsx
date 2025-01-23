import { render, screen } from '@testing-library/react';
import AddDetailsToExercise from '../src/components/AddDetailsToExercise';
import userEvent from '@testing-library/user-event'
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios');

beforeEach(() => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
        const mockData = {
            user_id: 'testUser123',
            workout_id: 'testWorkout456',
            exercise_name: 'Push-ups',
        };
        return mockData[key];
    });
});

afterEach(() => {
    vi.restoreAllMocks(); 
});

describe('AddDetailsToExercise Component', () => {
    it('renders correctly', () => {
    render(<AddDetailsToExercise />);
    expect(screen.getByText("Add Exercise Details!")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter reps")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter loading (weight)")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter any additional notes")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter rest interval (seconds)")).toBeInTheDocument();
    });

    it('updates input fields correctly', async () => {
    render(<AddDetailsToExercise />);

    const repsInput = screen.getByPlaceholderText("Enter reps");
    const restInput = screen.getByPlaceholderText("Enter rest interval (seconds)");
    const notesInput = screen.getByPlaceholderText("Enter any additional notes");
    const loadingInput = screen.getByPlaceholderText("Enter loading (weight)");

    await userEvent.type(repsInput, '12');
    await userEvent.type(restInput, '30');
    await userEvent.type(notesInput, 'Boom!');
    await userEvent.type(loadingInput, '55');

    expect(repsInput.value).toBe('12');
    expect(restInput.value).toBe('30');
    expect(notesInput.value).toBe('Boom!');
    expect(loadingInput.value).toBe('55');
    });

    it('makes API call on button click with correct data', async () => {
        const mockResponse = { data: { message: 'Details added successfully' } };
        axios.patch.mockResolvedValueOnce(mockResponse);
    
        render(<AddDetailsToExercise />);

        const repsInput = screen.getByPlaceholderText("Enter reps");
        const restInput = screen.getByPlaceholderText("Enter rest interval (seconds)");
        const notesInput = screen.getByPlaceholderText("Enter any additional notes");
        const loadingInput = screen.getByPlaceholderText("Enter loading (weight)");
        const button = screen.getByText("Add Exercise Details!")

        await userEvent.type(repsInput, '12');
        await userEvent.type(restInput, '30');
        await userEvent.type(notesInput, 'Boom!');
        await userEvent.type(loadingInput, '55');    
        
        await userEvent.click(button);

        expect(axios.patch).toHaveBeenCalledWith('${API_BASE_URL}/workouts/testUser123/testWorkout456/add_details',
            expect.objectContaining({
                exercise_name: "Push-ups",
                reps: 12,
                loading: 55,
                rest: 30,
                notes: "Boom!",
            })
            );
            
    })

    it('alerts if exercise_name is missing', async () => {
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    
        vi.spyOn(Storage.prototype, 'getItem').mockImplementation((key) => {
            const mockData = {
                user_id: 'testUser123',
                workout_id: 'testWorkout456',
            };
            return mockData[key]; // Return no exercise_name
        });
    
        render(<AddDetailsToExercise />);
        const button = screen.getByText("Add Exercise Details!");
    
        await userEvent.click(button);
    
        expect(window.alert).toHaveBeenCalledWith("No exercise found!");
    });
    
    it('alerts on API call failure', async () => {
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    
        axios.patch.mockRejectedValueOnce({
            response: { data: { error: "Something went wrong" } },
        });
    
        render(<AddDetailsToExercise />);
    
        const repsInput = screen.getByPlaceholderText("Enter reps");
        const restInput = screen.getByPlaceholderText("Enter rest interval (seconds)");
        const notesInput = screen.getByPlaceholderText("Enter any additional notes");
        const loadingInput = screen.getByPlaceholderText("Enter loading (weight)");
        const button = screen.getByText("Add Exercise Details!");
    
        await userEvent.type(repsInput, '12');
        await userEvent.type(restInput, '30');
        await userEvent.type(notesInput, 'Boom!');
        await userEvent.type(loadingInput, '55');
        await userEvent.click(button);
    
        expect(window.alert).toHaveBeenCalledWith("Something went wrong");
    });

    it('alerts on successful API call', async () => {
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    
        axios.patch.mockResolvedValueOnce({
            data: { message: "Details added successfully" },
        });
    
        render(<AddDetailsToExercise />);
    
        const repsInput = screen.getByPlaceholderText("Enter reps");
        const restInput = screen.getByPlaceholderText("Enter rest interval (seconds)");
        const notesInput = screen.getByPlaceholderText("Enter any additional notes");
        const loadingInput = screen.getByPlaceholderText("Enter loading (weight)");
        const button = screen.getByText("Add Exercise Details!");
    
        await userEvent.type(repsInput, '12');
        await userEvent.type(restInput, '30');
        await userEvent.type(notesInput, 'Boom!');
        await userEvent.type(loadingInput, '55');
        await userEvent.click(button);
    
        expect(window.alert).toHaveBeenCalledWith(
            'API Response: {"message":"Details added successfully"}'
        );
    });
    
    it('does not make an API call if inputs are empty', async () => {
        render(<AddDetailsToExercise />);
        const button = screen.getByText("Add Exercise Details!");
    
        await userEvent.click(button);
    
        expect(axios.patch).not.toHaveBeenCalled();
    });
    
    
});