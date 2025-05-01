import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <section className="not-found">
      <h2>404 - Page Not Found</h2>
      <Link to="/">Go back to Home</Link>
    </section>
  );
};

export default NotFound;
