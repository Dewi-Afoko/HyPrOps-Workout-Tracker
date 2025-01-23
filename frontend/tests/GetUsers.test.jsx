import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { vi } from 'vitest';
import GetUsers from '../src/components/GetUsers';

vi.mock('axios'); // Mock axios

describe('GetUsers Component', () => {
    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it('renders the button correctly', () => {
        render(<GetUsers />);
        const button = screen.getByText("Click Me to Call GET Users");
        expect(button).toBeInTheDocument();
        expect(button).toHaveStyle({
            backgroundColor: "black",
            color: "red",
            borderRadius: "50px",
            fontSize: "16px",
            padding: "10px 20px",
        });
    });

    it('makes an API call and alerts with the response data on success', async () => {
        const mockResponse = { data: [{ id: 1, name: "John Doe" }] };
        axios.get.mockResolvedValueOnce(mockResponse); // Mock successful API call
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert

        render(<GetUsers />);
        const button = screen.getByText("Click Me to Call GET Users");
        await userEvent.click(button);

        expect(axios.get).toHaveBeenCalledWith("${API_BASE_URL}/users");
        expect(window.alert).toHaveBeenCalledWith('API Response: [{"id":1,"name":"John Doe"}]');
    });

    it('alerts an error message on API call failure', async () => {
        axios.get.mockRejectedValueOnce(new Error("Network error")); // Mock failed API call
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
        vi.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error

        render(<GetUsers />);
        const button = screen.getByText("Click Me to Call GET Users");
        await userEvent.click(button);

        expect(axios.get).toHaveBeenCalledWith("${API_BASE_URL}/users");
        expect(window.alert).toHaveBeenCalledWith("Failed to fetch data. Check console for details.");
        expect(console.error).toHaveBeenCalledWith("Error making API call:", expect.any(Error));
    });
});
