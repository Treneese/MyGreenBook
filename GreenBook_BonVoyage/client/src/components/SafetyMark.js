// SafetyMark.js
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const SafetyMark = ({ placeId }) => {
    const [isSafe, setIsSafe] = useState(true);
    const navigate = useNavigate();

    const handleMarkSafe = async () => {
        const token = localStorage.getItem('token');
        try {
            await axios.post(`http://localhost:5555/api/places/${placeId}/mark_safe`, { is_safe: isSafe }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            alert('Place marked successfully');
            navigate.push('http://localhost:5555/api/places');
        } catch (error) {
            console.error('Error marking place:', error);
            alert('Failed to mark place');
        }
    };

    return (
        <div>
            <h3>Mark this place</h3>
            <label>
                <input
                    type="radio"
                    value={true}
                    checked={isSafe === true}
                    onChange={() => setIsSafe(true)}
                />
                Safe
            </label>
            <label>
                <input
                    type="radio"
                    value={false}
                    checked={isSafe === false}
                    onChange={() => setIsSafe(false)}
                />
                Not Safe
            </label>
            <button onClick={handleMarkSafe}>Submit</button>
        </div>
    );
};

export default SafetyMark;
