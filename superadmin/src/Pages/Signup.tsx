
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const isFormValid = username.trim() !== '' && email.trim() !== '' && password.trim() !== '';

  const handleSignup = () => {
    if (!isFormValid) {
      alert('Please fill in all fields.');
      return;
    }

    navigate('/signup2'); 
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    fontFamily: 'Arial, sans-serif',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '36px',
    fontWeight: 'bold',
    marginBottom: '40px',
  };

  const fieldContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '420px',
    marginBottom: '24px',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '16px',
    fontWeight: 600,
    marginBottom: '6px',
  };

  const inputStyle: React.CSSProperties = {
    padding: '14px 16px',
    fontSize: '16px',
    borderRadius: '16px',
    border: '2px solid #1E3A8A',
    outline: 'none',
  };

  const buttonStyle: React.CSSProperties = {
    marginTop: '30px',
    backgroundColor: isFormValid ? '#1E3A8A' : '#A3A3A3',
    color: 'white',
    padding: '19px 40px',
    fontSize: '16px',
    border: 'none',
    borderRadius: '12px',
    cursor: isFormValid ? 'pointer' : 'not-allowed',
    transition: 'background-color 0.3s ease',
  };

  const dotsContainerStyle: React.CSSProperties = {
    display: 'flex',
    gap: '8px',
    marginTop: '16px',
    marginBottom: '20px',
  };

  const dotStyle = (active: boolean): React.CSSProperties => ({
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: active ? '#1E3A8A' : '#D4D4D4',
  });

  return (
    <div style={containerStyle}>
      <div style={headingStyle}>Sign Up</div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>User Name</label>
        <input
          type="text"
          placeholder="Enter username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Email</label>
        <input
          type="email"
          placeholder="Enter email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Password</label>
        <input
          type="password"
          placeholder="Enter password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={dotsContainerStyle}>
        <div style={dotStyle(true)} />
        <div style={dotStyle(false)} />
      </div>

      <button
        style={buttonStyle}
        onClick={handleSignup}
        disabled={!isFormValid}
      >
        Sign Up
      </button>
    </div>
  );
};

export default Signup;
