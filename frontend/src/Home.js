
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
    return (
        <div>
            <h2>Welcome to the File Upload App</h2>
            <Link to="/upload">Go to Upload Page</Link>
        </div>
    );
}

export default Home;
