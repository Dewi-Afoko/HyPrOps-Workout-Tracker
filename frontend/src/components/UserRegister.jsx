import { useState } from "react"
import { useNavigate } from "react-router-dom";
import axios from "axios";


const UserRegister = () => {
    const [username, setUsername] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
        if (!username || !password) {
            alert("Please enter a valid username and password");
            return;
        }
        try {
            const response = await axios.post(`http://127.0.0.1:5000/user/register`, {username, password});
            alert(`message: ${JSON.stringify(response.data.message)}`);
            navigate('/login')
        } catch (error) {
            const errorMessage = error.response.data.error
            alert(`Error during registration: ${errorMessage}`);
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
                    placeholder="Enter a username"
                    value= {username}
                    onChange = {(event) => setUsername(event.target.value)}
                    />
                </div>
                <div>
                <label htmlFor="password">Password</label>
                    <input
                    id="password"
                    type="password"
                    placeholder="Enter a password"
                    value= {password}
                    onChange = {(event) => setPassword(event.target.value)}
                    />                    
                </div>
                <button type="button" onClick={handleSubmit}>
                    Register Now!
                </button>
            </form>
        </div>
    );
};

export default UserRegister;