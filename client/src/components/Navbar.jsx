import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ toggleTheme, currentTheme }) => {
  return (
    <nav>
      <Link to="/">OrateAI</Link>
      <div>
        <Link to="/upload">Upload</Link>
        <button onClick={toggleTheme}>
          {currentTheme === 'light' ? 'Dark Mode' : 'Light Mode'}
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
