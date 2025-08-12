import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ResetPassword: React.FC = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const handleSend = () => {
    if (newPassword.length < 8) {
      alert('Password must be at least 8 characters long');
      return;
    }

    if (newPassword !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    
    alert('Password reset successfully!');
    navigate('/signinn'); 
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
    fontSize: '35px',
    fontWeight: 'bold',
    marginBottom: '60px',
  };

  const fieldContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '400px',
    marginBottom: '20px',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '19px',
    fontWeight: 500,
    marginBottom: '6px',
  };

  const inputStyle: React.CSSProperties = {
    padding: '12px 16px',
    fontSize: '16px',
    borderRadius: '12px',
    border: '2px solid #1E3A8A',
    outline: 'none',
  };

  const buttonStyle: React.CSSProperties = {
    backgroundColor: '#1E3A8A',
    color: '#fff',
    padding: '10px 30px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    cursor: 'pointer',
    marginTop: '10px',
  };

  return (
    <div style={containerStyle}>
      <div style={headingStyle}>New Password</div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Enter New Password</label>
        <input
          type="password"
          placeholder="At least 8 digits"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Confirm New Password</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          style={inputStyle}
        />
      </div>

      <button style={buttonStyle} onClick={handleSend}>
        Send
      </button>
    </div>
  );
};

export default ResetPassword;
