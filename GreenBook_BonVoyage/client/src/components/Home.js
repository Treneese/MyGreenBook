// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
    return (
        <div>
            <h1>Welcome to the Green Book</h1>
            <p>Your go-to app for safe route navigation and place finding.</p>
            <img className='GreenBook' src='/GreenBook.png' alt='GreenBook'/>
            <Link className="Places" to="/places">Explore Places</Link>
        </div>
    );
}

export default Home;
