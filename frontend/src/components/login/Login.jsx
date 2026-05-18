import { useState } from "react";
import { useNavigate } from "react-router-dom";
import './style.css'

function Login() {
    const[email, setEmail] = useState("");
    const[password, setPassword] = useState("");
    
    const navigate = useNavigate();
    const formData = new FormData();

    formData.append("email", email);
    formData.append("password", password);

    const login = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                body: formData
            })

            token = response['token'];
            localStorage.setItem("token", token);
            navigate('/dashboard');

        } catch(e) {
            alert("Invalid Credentials");
            console.error(`Error: ${e}`);
        }
    }

    const html = (
        <div></div>
    );

    return html;
}

export default Login;