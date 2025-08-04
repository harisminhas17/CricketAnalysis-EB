import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SignupStep2: React.FC = () => {
  const navigate = useNavigate();

  const [address, setAddress] = useState('');
  const [country, setCountry] = useState('');
  const [city, setCity] = useState('');
  const [phone, setPhone] = useState('');
  const [isFormValid, setIsFormValid] = useState(false);

  useEffect(() => {
    setIsFormValid(address.trim() !== '' && country.trim() !== '' && city.trim() !== '' && phone.trim() !== '');
  }, [address, country, city, phone]);

  const handleSignup = () => {
    if (isFormValid) {
      navigate("/superadmin/signin");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>Sign Up</h1>

      <div style={styles.formGroup}>
        <label style={styles.label}>Address</label>
        <input
          type="text"
          placeholder="Enter Address"
          style={styles.input}
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
      </div>

      <div style={styles.row}>
        <div style={{ ...styles.formGroup, marginRight: '10px', flex: 1 }}>
          <label style={styles.label}>Country</label>
          <select
            style={styles.select}
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          >
            <option value="">Country</option>
            <option value="Pakistan">Pakistan</option>
            <option value="USA">USA</option>
          </select>
        </div>
        <div style={{ ...styles.formGroup, flex: 1 }}>
          <label style={styles.label}>City</label>
          <select
            style={styles.select}
            value={city}
            onChange={(e) => setCity(e.target.value)}
          >
            <option value="">City</option>
            <option value="Lahore">Lahore</option>
            <option value="Karachi">Karachi</option>
          </select>
        </div>
      </div>

      <div style={styles.formGroup}>
        <label style={styles.label}>Phone no</label>
        <input
          type="text"
          placeholder="Enter Phoneno."
          style={styles.input}
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
      </div>

      
      <div style={styles.dots}>
        <div style={styles.dot}></div>
        <div style={styles.dot}></div>
        <div style={{ ...styles.dot, backgroundColor: '#2F4CD3' }}></div>
      </div>

      
      <button
        style={{
          ...styles.button,
          backgroundColor: isFormValid ? '#2F4CD3' : '#cccccc',
          cursor: isFormValid ? 'pointer' : 'not-allowed',
        }}
        onClick={handleSignup}
        disabled={!isFormValid}
      >
        Sign Up
      </button>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: '500px',
    margin: '60px auto',
    padding: '10px',
    borderRadius: '10px',
    textAlign: 'center',
    backgroundColor: '#fff',
     
     
     
  },
  heading: {
    fontSize: '28px',
    fontWeight: 700,
    marginBottom: '40px',
  },
  formGroup: {
    marginBottom: '25px',
    textAlign: 'left',
  },
  label: {
    fontWeight: 600,
    display: 'block',
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '16px 20px',
    fontSize: '16px',
    border: '1.5px solid #2F4CD3',
    borderRadius: '12px',
    outline: 'none',
  },
  select: {
    width: '100%',
    padding: '16px 20px',
    fontSize: '16px',
    border: '1.5px solid #2F4CD3',
    borderRadius: '12px',
    outline: 'none',
    appearance: 'none',
    backgroundColor: '#fff',
    backgroundImage:
      'url("data:image/svg+xml;utf8,<svg fill=\'%232F4CD3\' height=\'20\' viewBox=\'0 0 24 24\' width=\'20\' xmlns=\'http://www.w3.org/2000/svg\'><path d=\'M7 10l5 5 5-5z\'/></svg>")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right 12px center',
    backgroundSize: '18px',
  },
  row: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '8px',
  },
  dots: {
    display: 'flex',
    justifyContent: 'center',
    gap: '10px',
    marginBottom: '25px',
    marginTop: '10px',
  },
  dot: {
    height: '8px',
    width: '8px',
    borderRadius: '50%',
    backgroundColor: '#c4c4c4',
  },
  button: {
    width: '160px',
    padding: '12px 20px',
    fontSize: '16px',
    fontWeight: 600,
    border: 'none',
    borderRadius: '10px',
    color: '#fff',
  },
};

export default SignupStep2;
