import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignIn: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && password) {
      navigate('/home'); 
    }
  };

  return (
    <div style={styles.container}>
      <form onSubmit={handleSubmit} style={styles.form}>
        <h2 style={styles.heading}>Sign In</h2>

        <label style={styles.label}>Email</label>
        <input
          type="email"
          style={styles.input}
          placeholder="Enter your Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label style={styles.label}>Password</label>
        <input
          type="password"
          style={styles.input}
          placeholder="********"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <div style={styles.forgotContainer}>
          <a href="#" style={styles.forgotPassword}>Forgot Password?</a>
        </div>

        <button type="submit" style={styles.button}>Sign In</button>

        <p style={styles.footerText}>
          Don’t have an account? <a href="/signup" style={styles.signUp}>Sign Up</a>
        </p>

       
      </form>
    </div>
  );
};

export default SignIn;

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    display: 'flex',
    height: '100vh',
    justifyContent: 'center',
    alignItems: 'center',
    background: '#fff',
  },
  form: {
    width: '95%',
    maxWidth: '480px', 
    padding: '40px', 
    boxSizing: 'border-box',
    textAlign: 'center',
    borderRadius: '10px',
  },
  heading: {
    fontSize: '32px',
    marginBottom: '30px',
    fontWeight: '600',
  },
  label: {
    display: 'block',
    fontSize: '16px',
    marginBottom: '8px',
    textAlign: 'left',
    fontWeight: '500',
  },
  input: {
    width: '100%',
    padding: '12px',
    marginBottom: '20px',
    borderRadius: '10px',
    border: '1.5px solid #3b5bdb',
    fontSize: '16px',
  },
  forgotContainer: {
    textAlign: 'right',
    marginBottom: '20px',
  },
  forgotPassword: {
    fontSize: '14px',
    textDecoration: 'none',
    color: '#333',
  },
  button: {
    width: '40%', 
    padding: '12px',
    backgroundColor: '#3b5bdb',
    color: '#fff',
    fontSize: '16px',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    marginBottom: '20px',
  },
  footerText: {
    fontSize: '14px',
    color: '#333',
  },
  signUp: {
    color: '#3b5bdb',
    textDecoration: 'none',
    marginLeft: '5px',
  },
 
  
};
