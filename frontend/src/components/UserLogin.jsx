import { useState } from "react"
import { useNavigate } from "react-router-dom";
import axios from "axios";

const UserLogin = () => {
    const [username, setUsername] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!username || !password) {
            alert("Please enter your username and password");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/auth/login`, {username, password});
            localStorage.setItem('token', response.data.token);
            alert(`message: ${JSON.stringify(response.data.message)}`);
            navigate('/profile')
        } catch (error) {
            console.log(error)
            const errorMessage = error.response.error
            alert(`Error logging in: ${errorMessage}`);
        }
    };

    return (
        <div>
            <form>
                <div>
                    <label htmlFor="username">Username</label>
                    <input
                    id="username"
                    type="text"
                    placeholder="Enter your username"
                    value= {username}
                    onChange = {(event) => setUsername(event.target.value)}
                    />
                </div>
                <div>
                <label htmlFor="password">Password</label>
                    <input
                    id="password"
                    type="password"
                    placeholder="Enter your password"
                    value= {password}
                    onChange = {(event) => setPassword(event.target.value)}
                    />                    
                </div>
                <button type="button" onClick={handleSubmit}>
                    Login!
                </button>
            </form>
        </div>
    );
};

export default UserLogin;