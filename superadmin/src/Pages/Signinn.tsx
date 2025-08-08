import React from "react";
import { useNavigate } from "react-router-dom";

const Signin: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.heading}>Sign In</h2>

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Email</label>
          <input
            type="email"
            placeholder="Enter Email"
            style={styles.input}
            required
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Password</label>
          <input
            type="password"
            placeholder="*********"
            style={styles.input}
            required
          />
        </div>

        <div style={styles.forgotContainer}>
          <span
            style={styles.forgotLink}
            onClick={() => navigate("/forgot-password")}
          >
            Forgot Password?
          </span>
        </div>

        <button type="submit" style={styles.button}>
          Sign In
        </button>
      </form>

      <div style={styles.signupText}>
        Don’t&nbsp; have an account?{" "}
        <span
          style={styles.signupLink}
          onClick={() => navigate("/signup")}
        >
          Sign Up
        </span>
      </div>
    </div>
  );
};

export default Signin;

const styles = {
  container: {
    maxWidth: "400px",
    margin: "100px auto",
    padding: "0 20px",
    textAlign: "center" as const,
    fontFamily: "'Inter', sans-serif",
  },
  heading: {
    fontSize: "32px",
    fontWeight: 600,
    marginBottom: "40px",
  },
  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "20px",
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column" as const,
    textAlign: "left" as const,
  },
  label: {
    fontWeight: 600,
    fontSize: "16px",
    marginBottom: "8px",
  },
 input: {
  padding: "14px",
  fontSize: "16px",
  borderRadius: "12px",
  border: "1.5px solid #1F3C88",
  outline: "none",
  backgroundColor: "#ffffff", 
  color: "#000",
  appearance: "none" as const, 
  WebkitBoxShadow: "0 0 0 1000px #ffffff inset", 
  WebkitTextFillColor: "#000", 
},
  forgotContainer: {
    textAlign: "right" as const,
    marginTop: "-10px",
  },
  forgotLink: {
    fontSize: "16px",
    color: "#000",
    cursor: "pointer",
  },
  button: {
    margin: "20px auto 0",
    padding: "12px 30px",
    fontSize: "16px",
    backgroundColor: "#2d4fa1",
    color: "#fff",
    border: "none",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold" as const,
    width: "30%", 
   
  },
  signupText: {
    marginTop: "25px",
    fontSize: "16px",
    color: "#000",
  },
  signupLink: {
    color: "#2d4fa1",
    cursor: "pointer",
    fontWeight: 500,
    textDecoration: "none",
  },
};
