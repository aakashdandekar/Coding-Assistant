import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./style.css"

function Dashboard() {
    const navigate = useNavigate();

    useEffect(() => {
        const response = await fetch();
    }, []);

    const html = (
        <div></div>
    );

    return html;
}

export default Dashboard;