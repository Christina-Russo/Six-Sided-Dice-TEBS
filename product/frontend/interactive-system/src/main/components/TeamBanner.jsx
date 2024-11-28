import React from 'react';
import logo from '../assets/Team-Logo.png'
import '../styles/styles.css';

/**
 * Displays the team logo and name.
 * 
 * @returns {JSX Element} The <TeamBanner /> component
 */
function TeamBanner() {

    return (
        <div className="team-banner">
            <div className="team-container">
                {/* Team logo */}
                <div className="logo">
                    <img src={logo} alt="Six-Sided Dice Logo" />
                    {/* Six Sided Dice logo adapted from design created using Dali 3 via Copilot Designer:  
                     https://copilot.microsoft.com/images/create/a-logo-of-a-design-company-showing-a-6-sided-dice-/1-66a2e8ea4f64491c9184c987cd5d10bb */} 
                </div>
                {/* Team name */}
                <div className="team-name">
                    <h2>Six-Sided Dice Productions</h2>
                </div>
            </div>
        </div>
    );
}

export default TeamBanner;