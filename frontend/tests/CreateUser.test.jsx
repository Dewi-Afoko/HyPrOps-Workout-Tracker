import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import { vi } from 'vitest';
import CreateUser from '../src/components/CreateUser';

vi.mock('axios'); // Mock axios

describe('CreateUser Component', () => {
    beforeEach(() => {
        vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {}); // Mock localStorage.setItem
        vi.spyOn(window, 'alert').mockImplementation(() => {}); // Mock alert
    });

    afterEach(() => {
        vi.restoreAllMocks(); // Restore mocks after each test
    });

    it('renders the form correctly', () => {
        render(<CreateUser />);
        expect(screen.getByPlaceholderText("Enter username")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Enter password")).toBeInTheDocument();
        expect(screen.getByText("Register Now!")).toBeInTheDocument();
    });

    it('alerts if username or password is missing', async () => {
        render(<CreateUser />);
        const button = screen.getByText("Register Now!");

        // No username or password
        await userEvent.click(button);
        expect(window.alert).toHaveBeenCalledWith("Please enter both username and password.");
        expect(axios.post).not.toHaveBeenCalled();

        // Only username
        await userEvent.type(screen.getByPlaceholderText("Enter username"), "testuser");
        await userEvent.click(button);
        expect(window.alert).toHaveBeenCalledWith("Please enter both username and password.");
        expect(axios.post).not.toHaveBeenCalled();

        // Only password
        await userEvent.clear(screen.getByPlaceholderText("Enter username"));
        await userEvent.type(screen.getByPlaceholderText("Enter password"), "testpass");
        await userEvent.click(button);
        expect(window.alert).toHaveBeenCalledWith("Please enter both username and password.");
        expect(axios.post).not.toHaveBeenCalled();
    });

    it('makes an API call and saves user ID on success', async () => {
        const mockResponse = { data: { id: 'user123' } };
        axios.post.mockResolvedValueOnce(mockResponse); // Mock successful API response

        render(<CreateUser />);
        const usernameInput = screen.getByPlaceholderText("Enter username");
        const passwordInput = screen.getByPlaceholderText("Enter password");
        const button = screen.getByText("Register Now!");

        await userEvent.type(usernameInput, "testuser");
        await userEvent.type(passwordInput, "testpass");
        await userEvent.click(button);

        expect(axios.post).toHaveBeenCalledWith("${API_BASE_URL}/users", {
            username: "testuser",
            password: "testpass",
        });
        expect(window.alert).toHaveBeenCalledWith('API Response: {"id":"user123"}');
        expect(localStorage.setItem).toHaveBeenCalledWith("user_id", "user123");
    });

    it('alerts an error message on API call failure', async () => {
        axios.post.mockRejectedValueOnce(new Error("Network error")); // Mock failed API call

        render(<CreateUser />);
        const usernameInput = screen.getByPlaceholderText("Enter username");
        const passwordInput = screen.getByPlaceholderText("Enter password");
        const button = screen.getByText("Register Now!");

        await userEvent.type(usernameInput, "testuser");
        await userEvent.type(passwordInput, "testpass");
        await userEvent.click(button);

        expect(axios.post).toHaveBeenCalledWith("${API_BASE_URL}/users", {
            username: "testuser",
            password: "testpass",
        });
        expect(window.alert).toHaveBeenCalledWith("Failed to register. Check console for details.");
    });
});
