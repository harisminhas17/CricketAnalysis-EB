import React, { useState, ChangeEvent, FormEvent, CSSProperties } from 'react';
import { useNavigate, NavigateFunction } from 'react-router-dom';

interface FormState {
  id: string;
  email: string;
  password: string;
}

const Signup: React.FC = () => {
  const [form, setForm] = useState<FormState>({
    id: '',
    email: '',
    password: '',
  });

  const navigate: NavigateFunction = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    localStorage.setItem('signupStep1', JSON.stringify(form));
    navigate('/SuperAdmin/Signup2');
  };

  const styles: {
    container: CSSProperties;
    form: CSSProperties;
    heading: CSSProperties;
    label: CSSProperties;
    input: CSSProperties;
    button: CSSProperties;
    dotContainer: CSSProperties;
    dot: CSSProperties;
    dotActive: CSSProperties;
  } = {
    container: {
      display: 'flex',
      width: '100vw',
      height: '100vh',
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#ffffff',
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      width: '100%',
      height: '100%',
      maxWidth: '600px',
      padding: '40px',
      borderRadius: '0',
      backgroundColor: '#ffffff',
      boxSizing: 'border-box',
    },
    heading: {
      textAlign: 'center',
      marginBottom: '30px',
      fontSize: '32px',
      fontWeight: '700',
    },
    label: {
      fontWeight: '600',
      marginBottom: '8px',
      marginTop: '20px',
      fontSize: '16px',
    },
    input: {
      padding: '14px',
      borderRadius: '10px',
      border: '1px solid #003399',
      outline: 'none',
      fontSize: '16px',
    },
    button: {
      alignSelf: 'center',
      marginTop: '30px',
      width: '150px',
      height: '50px',
      border: 'none',
      borderRadius: '10px',
      backgroundColor:
        form.id && form.email && form.password ? '#003399' : '#b3b3b3',
      color: '#ffffff',
      fontWeight: 'bold',
      fontSize: '16px',
      cursor:
        form.id && form.email && form.password ? 'pointer' : 'not-allowed',
    },
    dotContainer: {
      display: 'flex',
      justifyContent: 'center',
      marginTop: '50px',
      gap: '10px',
    },
    dot: {
      height: '10px',
      width: '10px',
      backgroundColor: '#bbb',
      borderRadius: '50%',
      display: 'inline-block',
    },
    dotActive: {
      backgroundColor: '#003399',
    },
  };

  return (
    <div style={styles.container}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <h2 style={styles.heading}>Sign Up</h2>

        <label style={styles.label} htmlFor="id">
          Id
        </label>
        <input
          style={styles.input}
          type="text"
          id="id"
          name="id"
          value={form.id}
          onChange={handleChange}
          placeholder="Enter your Id"
          required
        />

        <label style={styles.label} htmlFor="email">
          Email
        </label>
        <input
          style={styles.input}
          type="email"
          id="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Enter your Email"
          required
        />

        <label style={styles.label} htmlFor="password">
          Password
        </label>
        <input
          style={styles.input}
          type="password"
          id="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Enter Password"
          required
        />

        <div style={styles.dotContainer}>
          <span style={{ ...styles.dot, ...styles.dotActive }}></span>
          <span style={styles.dot}></span>
          <span style={styles.dot}></span>
        </div>

        <button
          type="submit"
          style={styles.button}
          disabled={!form.id || !form.email || !form.password}
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default Signup;
