import React, { useEffect, useState } from 'react';
const API_URL = "http://127.0.0.1:5000";

const HomePage = () => {
    const [rankedResumes, setRankedResumes] = useState([]);

    useEffect(() => {
        fetch(`${API_URL}/rank-resumes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Ranked Resumes:", data);
            setRankedResumes(data);
        })
        .catch(error => console.error('Error fetching ranked resumes:', error));
    }, []);
    

    return (
        <div className="container mx-auto mt-5">
            <h1 className="text-3xl font-bold">Ranked Resumes</h1>
            <ul className="mt-4">
    {rankedResumes.map((resume, index) => (
        <li key={index} className="border p-4 my-2 rounded-lg">
            <p><strong>Rank:</strong> {resume.rank}</p>
            <p><strong>Filename:</strong> {resume.name}</p>
            <p><strong>Similarity:</strong> {resume.similarity}%</p>
        </li>
    ))}
</ul>

        </div>
    );
}

export default HomePage;
