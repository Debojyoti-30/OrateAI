import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <section className="home">
      <h1>Welcome to OrateAI</h1>
      <p>
        Analyze your presentation skills with AI-powered insights on facial expressions, voice tone, speech patterns, and body language.
      </p>
      <Link to="/upload">
        <button>Upload Your Presentation</button>
      </Link>
    </section>
  );
};

export default Home;
