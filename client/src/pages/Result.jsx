import React from 'react';
import ResultCard from '../components/ResultCard';
import AnalysisChart from '../components/AnalysisChart';
import FeedbackSection from '../components/FeedbackSection';

const Result = () => {
  // Placeholder data
  const analysisData = {
    facialExpression: 'Confident',
    voiceTone: 'Clear',
    speechPattern: 'Well-paced',
    bodyLanguage: 'Open',
    feedback: 'Great job! Keep maintaining eye contact and vary your tone for emphasis.',
  };

  return (
    <section className="result">
      <h2>Analysis Results</h2>
      <ResultCard title="Facial Expression" content={analysisData.facialExpression} />
      <ResultCard title="Voice Tone" content={analysisData.voiceTone} />
      <ResultCard title="Speech Pattern" content={analysisData.speechPattern} />
      <ResultCard title="Body Language" content={analysisData.bodyLanguage} />
      <AnalysisChart data={analysisData} />
      <FeedbackSection feedback={analysisData.feedback} />
    </section>
  );
};

export default Result;
