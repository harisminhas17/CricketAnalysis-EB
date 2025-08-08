import React from "react";
import { useNavigate } from "react-router-dom";

const ForgotPassword: React.FC = () => {
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/verification"); 
  };

  return (
    <div style={styles.container}>
     
     

     
      <h2 style={styles.heading}>Forgot Password</h2>

      <form onSubmit={handleSubmit} style={styles.form}>
        <label style={styles.label}>Enter Email Address</label>
        <input
          type="email"
          placeholder="Enter Email Address"
          required
          style={styles.input}
        />

       
        <div style={styles.backToSignIn} onClick={() => navigate("/Signinn")}>
          Back to Sign In
        </div>

       
        <button type="submit" style={styles.sendButton}>
          Send
        </button>
      </form>

    
      <div style={styles.orText}>or</div>

      
      <div style={styles.socialIcons}>
        <img
          src="https://img.icons8.com/color/48/google-logo.png"
          alt="Google"
          style={styles.icon}
        />
        <img
          src="https://img.icons8.com/fluency/48/facebook-new.png"
          alt="Facebook"
          style={{ ...styles.icon, marginLeft: "16px" }}
        />
      </div>

     
      <div style={styles.signupText}>
        Don’t&nbsp; have an account?
        <span style={styles.signupLink} onClick={() => navigate("/signup")}>
          {" "}Sign Up
        </span>
      </div>
    </div>
  );
};

export default ForgotPassword;

const styles = {
  container: {
    maxWidth: "400px",
    margin: "80px auto",
    padding: "0 20px",
    textAlign: "center" as const,
    fontFamily: "'Inter', sans-serif",
  },
  backArrow: {
    position: "absolute" as const,
    left: "20px",
    top: "30px",
    fontSize: "24px",
    cursor: "pointer",
  },
  heading: {
    fontSize: "30px",
    fontWeight: 700,
    marginBottom: "60px",
  },
  form: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center" as const,
    gap: "20px",
  },
  label: {
    fontWeight: 600,
    fontSize: "16px",
    alignSelf: "flex-start" as const,
    marginBottom: "-10px",
  },
  input: {
    padding: "14px",
    width: "100%",
    fontSize: "16px",
    borderRadius: "12px",
    border: "1.5px solid #1F3C88",
    outline: "none",
    backgroundColor: "#fff",
    color: "#000",
    appearance: "none" as const,
    WebkitBoxShadow: "0 0 0 1000px #ffffff inset",
    WebkitTextFillColor: "#000",
  },
  backToSignIn: {
    fontSize: "17px",
    color: "#243150ff",
    cursor: "pointer",
  },
  sendButton: {
    padding: "12px 40px",
    fontSize: "16px",
    backgroundColor: "#2d4fa1",
    color: "#fff",
    border: "none",
    borderRadius: "12px",
    cursor: "pointer",
    fontWeight: "bold" as const,
    marginTop: "10px",
  },
  orText: {
    margin: "20px 0 10px",
    fontSize: "14px",
    color: "#000",
  },
  socialIcons: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "20px",
  },
  icon: {
    width: "24px",
    height: "24px",
    cursor: "pointer",
  },
  signupText: {
    fontSize: "17px",
    color: "#000",
  },
  signupLink: {
    color: "#2d4fa1",
    fontWeight: 500,
    cursor: "pointer",
  },
};
