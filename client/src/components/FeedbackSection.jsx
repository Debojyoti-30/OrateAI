import React from 'react';

const FeedbackSection = ({ feedback }) => {
  return (
    <div className="feedback-section">
      <h3>AI Feedback</h3>
      <p>{feedback}</p>
    </div>
  );
};

export default FeedbackSection;
