
import React from 'react';
import { useNavigate } from 'react-router-dom';

const RealTimeScoring: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', backgroundColor: '#ffffff', padding: '20px', textAlign: 'center' }}>
      <h1 style={{ fontSize: '30px', fontWeight: 'bold', marginBottom: '16px', color: '#000000' }}>
        Real Time Scoring–Made Easy!
      </h1>
      <p style={{ fontSize: '19px', color: '#333333', marginBottom: '24px', maxWidth: '300px' }}>
        Track every run, wicket and over live.
      </p>
      <div style={{ width: '450px', height: '200px', marginBottom: '24px', position: 'relative' }}>
        <img src="/realtime.JPG" alt="Real Time Scoring" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '24px' }}>
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#dddddd', margin: '0 4px' }} />
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#263EA8', margin: '0 4px' }} />
      </div>
      <button onClick={() => navigate('/signinn')} style={{ backgroundColor: '#263EA8', color: '#ffffff', border: 'none', padding: '12px 24px', borderRadius: '6px', fontSize: '16px', cursor: 'pointer' }}>
        Get Started
      </button>
    </div>
  );
};

export default RealTimeScoring;
