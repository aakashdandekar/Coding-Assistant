import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./register/Register.jsx";
import Login from "./login/Login.jsx";
import Dashboard from "./dashboard/Dashboard.jsx";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App;