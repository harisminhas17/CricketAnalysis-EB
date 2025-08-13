import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SignupStep2: React.FC = () => {
  const navigate = useNavigate();

  const [address, setAddress] = useState('');
  const [country, setCountry] = useState('');
  const [city, setCity] = useState('');
  const [phone, setPhone] = useState('');
  const [profilePic, setProfilePic] = useState<File | null>(null);
  const [isFormValid, setIsFormValid] = useState(false);

  useEffect(() => {
    setIsFormValid(
      address.trim() !== '' &&
      country.trim() !== '' &&
      city.trim() !== '' &&
      phone.trim() !== ''
    );
  }, [address, country, city, phone]);

  const handleSignup = () => {
    if (isFormValid) {
      navigate('/Dashboard');
    } else {
      alert('Please fill in all fields.');
    }
  };

  const containerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px 16px',
    minHeight: '100vh',
    fontFamily: 'Arial, sans-serif',
  };

  const headingStyle: React.CSSProperties = {
    fontSize: '32px',
    fontWeight: 'bold',
    marginBottom: '32px',
  };

  const fieldContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    maxWidth: '480px',
    marginBottom: '20px',
  };

  const labelStyle: React.CSSProperties = {
    fontSize: '18px',
    fontWeight: 600,
    marginBottom: '8px',
  };

  const inputStyle: React.CSSProperties = {
    padding: '16px',
    fontSize: '16px',
    borderRadius: '16px',
    border: '1.5px solid #22327c',
    outline: 'none',
  };

  const selectStyle: React.CSSProperties = {
    ...inputStyle,
    appearance: 'none',
    backgroundColor: '#fff',
    backgroundImage:
      'url("data:image/svg+xml;utf8,<svg fill=\'%2322327c\' height=\'20\' viewBox=\'0 0 24 24\' width=\'20\' xmlns=\'http://www.w3.org/2000/svg\'><path d=\'M7 10l5 5 5-5z\'/></svg>")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right 16px center',
    backgroundSize: '18px',
    width: '100%',
  };

  const rowStyle: React.CSSProperties = {
    display: 'flex',
    gap: '20px',
    marginBottom: '20px',
    width: '100%',
    maxWidth: '480px',
  };

  const selectContainerStyle: React.CSSProperties = {
    flex: 1,
    position: 'relative',
  };

  const fileInputWrapper: React.CSSProperties = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    border: '1.5px solid #22327c',
    borderRadius: '16px',
    padding: '14px 16px',
  };

  const hiddenFileInput: React.CSSProperties = {
    display: 'none',
  };

  const customFileLabel: React.CSSProperties = {
    display: 'inline-block',
    padding: '8px 16px',
    backgroundColor: '#f2f2f2',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '17px',
    border: '1px solid #ccc',
  };

  const buttonStyle: React.CSSProperties = {
    marginTop: '20px',
    backgroundColor: '#22327c',
    color: 'white',
    padding: '16px 36px',
    fontSize: '19px',
    border: 'none',
    borderRadius: '12px',
    cursor: 'pointer',
  };

  const dotsContainerStyle: React.CSSProperties = {
    display: 'flex',
    gap: '8px',
    marginTop: '16px',
    marginBottom: '16px',
  };

  const dotStyle = (active: boolean): React.CSSProperties => ({
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: active ? '#22327c' : '#d4d4d4',
  });

  return (
    <div style={containerStyle}>
      <div style={headingStyle}>Sign Up</div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Address</label>
        <input
          type="text"
          placeholder="Enter address"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={rowStyle}>
        <div style={selectContainerStyle}>
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            style={selectStyle}
          >
            <option value="">Country</option>
            <option value="Pakistan">Pakistan</option>
            <option value="USA">USA</option>
          </select>
        </div>

        <div style={selectContainerStyle}>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={selectStyle}
          >
            <option value="">City</option>
            <option value="Karachi">Karachi</option>
            <option value="Lahore">Lahore</option>
            <option value="Rawalpindi">Rawalpindi</option>
          </select>
        </div>
      </div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Phone no</label>
        <input
          type="text"
          placeholder="Enter phone number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          style={inputStyle}
        />
      </div>

      <div style={fieldContainerStyle}>
        <label style={labelStyle}>Select Profile Picture</label>
        <div style={fileInputWrapper}>
          <span style={{ fontWeight: 600, fontSize: '17px' }}>
            Select Profile Picture
          </span>
          <label htmlFor="profileUpload" style={customFileLabel}>
            📁 Choose File
          </label>
          <input
            type="file"
            id="profileUpload"
            onChange={(e) => setProfilePic(e.target.files?.[0] || null)}
            style={hiddenFileInput}
          />
        </div>
      </div>

      <div style={dotsContainerStyle}>
        <div style={dotStyle(false)} />
        <div style={dotStyle(true)} />
      </div>

      <button style={buttonStyle} onClick={handleSignup}>
        Sign Up
      </button>
    </div>
  );
};

export default SignupStep2;
