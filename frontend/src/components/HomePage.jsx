import React, { useEffect, useState } from 'react';
import axios from 'axios';

const HomePage = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        // Make a GET request to the Flask backend to fetch the ranked JSON data
        axios.get('http://localhost:5000/ranked-json')
            .then(response => {
                setData(response.data); // Save the JSON data in state
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }, []);

    return (
        <div>
            <h1>Ranked Data</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre> {/* Pretty print JSON */}
        </div>
    );
};

export default HomePage;
