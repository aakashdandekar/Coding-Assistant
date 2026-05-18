import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./style.css"

function Register() {
    const [name, setName] = useState("");
    const [mobile, setMobile] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const register = async (e) => {
        e.preventDefault();
        const navigate = useNavigate();

        try {
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "name": name,
                    "mobile": mobile,
                    "email": email,
                    "password": password
                })
            })

            const token = response['token'];
            localStorage.setItem("token", token);
            navigate('/dashboard');

        } catch(e) {
            alert("Error occurred!");
            console.error(`Error ${e}`);
        }
    }

    const html = (
        <div></div>
    );

    return html;
}

export default Register;