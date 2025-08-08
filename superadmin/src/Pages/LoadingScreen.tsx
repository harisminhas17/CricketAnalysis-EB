
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const LoadingScreen: React.FC = () => {
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            navigate('/admin');
          }, 500);
          return 100;
        }
        return prev + 2;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [navigate]);

  return (
    <div style={styles.container}>
      <div style={styles.progressBarContainer}>
        <div style={{ ...styles.progressBar, width: `${progress}%` }} />
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  progressBarContainer: {
    width: '200px', 
    height: '10px',
    backgroundColor: '#ddd',
    borderRadius: '10px',
    overflow: 'hidden',
    marginBottom: '10px',
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#263EA8',
    transition: 'width 0.1s ease-in-out',
  },
};

export default LoadingScreen;
