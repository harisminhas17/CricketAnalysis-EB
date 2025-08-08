import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Verification: React.FC = () => {
  const [code, setCode] = useState(['', '', '', '']);
  const navigate = useNavigate();

  const handleChange = (value: string, index: number) => {
    if (/^\d?$/.test(value)) {
      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);
      if (value && index < 3) {
        const nextInput = document.getElementById(`code-${index + 1}`);
        nextInput?.focus();
      }
    }
  };

  const handleSend = () => {
    const fullCode = code.join('');
    if (fullCode.length === 4) {
      navigate('/ResetPassword');
    } else {
      alert('Please enter the complete 4-digit code');
    }
  };

  const handleSignUp = () => {
    navigate('/signup');
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
    fontSize: '32px',
    fontWeight: 'bold',
    marginBottom: '45px',
  };

  const subheadingStyle: React.CSSProperties = {
    fontSize: '20px',
    marginBottom: '20px',
  };

  const inputWrapperStyle: React.CSSProperties = {
    display: 'flex',
    gap: '15px',
    marginBottom: '20px',
  };

  const inputStyle: React.CSSProperties = {
    width: '50px',
    height: '50px',
    fontSize: '20px',
    textAlign: 'center',
    border: '2px solid #1E3A8A',
    borderRadius: '50%',
  };

  const resendTextStyle: React.CSSProperties = {
    color: '#6B7280',
    fontSize: '17px',
    marginBottom: '20px',
  };

  const resendLinkStyle: React.CSSProperties = {
    color: '#1E3A8A',
    cursor: 'pointer',
    marginLeft: '5px',
  };

  const buttonStyle: React.CSSProperties = {
    backgroundColor: '#1E3A8A',
    color: '#fff',
    padding: '17px 30px',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    cursor: 'pointer',
    marginBottom: '20px',
  };

  const orStyle: React.CSSProperties = {
    margin: '10px 0',
    fontSize: '14px',
    color: '#666',
  };

  const socialIconsStyle: React.CSSProperties = {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
  };

  const footerStyle: React.CSSProperties = {
    marginTop: '20px',
    fontSize: '14px',
  };

  const signUpLinkStyle: React.CSSProperties = {
    color: '#1E3A8A',
    marginLeft: '5px',
    cursor: 'pointer',
  };

  return (
    <div style={containerStyle}>
      <div style={headingStyle}>Verification</div>
      <div style={subheadingStyle}>Enter Verification Code</div>

      <div style={inputWrapperStyle}>
        {code.map((digit, index) => (
          <input
            key={index}
            id={`code-${index}`}
            type="text"
            maxLength={1}
            value={digit}
            onChange={(e) => handleChange(e.target.value, index)}
            style={inputStyle}
          />
        ))}
      </div>

      <div style={resendTextStyle}>
        If you didn’t recieve a code.
        <span style={resendLinkStyle}> Resend</span>
      </div>

      <button style={buttonStyle} onClick={handleSend}>
        Send
      </button>

      <div style={orStyle}>or</div>

      <div style={socialIconsStyle}>
        <img src="https://img.icons8.com/color/48/google-logo.png" alt="Google" width="30" />
        <img src="https://img.icons8.com/fluency/48/facebook-new.png" alt="Facebook" width="30" />
      </div>

      <div style={footerStyle}>
        Don’t have an account?
        <span style={signUpLinkStyle} onClick={handleSignUp}>
          Sign Up
        </span>
      </div>
    </div>
  );
};

export default Verification;
