import React, {
  useState,
  ChangeEvent,
  FormEvent,
  CSSProperties,
} from "react";
import { useNavigate } from "react-router-dom"; 

interface FormState {
  firstName: string;
  lastName: string;
  profilePicture: File | null;
}

const SignupStep2: React.FC = () => {
  const [form, setForm] = useState<FormState>({
    firstName: "",
    lastName: "",
    profilePicture: null,
  });

  const navigate = useNavigate(); 

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, files } = e.target;
    if (name === "profilePicture" && files && files[0]) {
      setForm({ ...form, profilePicture: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(form);
    navigate("/superadmin/signup3"); 

  };

  const styles: {
    container: CSSProperties;
    form: CSSProperties;
    heading: CSSProperties;
    label: CSSProperties;
    nameRow: CSSProperties;
    input: CSSProperties;
    fileInputContainer: CSSProperties;
    fileLabelText: CSSProperties;
    fileActions: CSSProperties;
    fileInput: CSSProperties;
    envelopeIcon: CSSProperties;
    dotContainer: CSSProperties;
    dot: CSSProperties;
    dotActive: CSSProperties;
    button: CSSProperties;
  } = {
    container: {
      display: "flex",
      width: "100vw",
      height: "100vh",
      justifyContent: "center",
      alignItems: "center",
      backgroundColor: "#ffffff",
    },
    form: {
      display: "flex",
      flexDirection: "column",
      width: "100%",
      maxWidth: "600px",
      padding: "40px",
      boxSizing: "border-box",
    },
    heading: {
      textAlign: "center",
      marginBottom: "30px",
      fontSize: "32px",
      fontWeight: "700",
    },
    label: {
      fontWeight: "600",
      fontSize: "16px",
      marginBottom: "10px",
    },
    nameRow: {
      display: "flex",
      gap: "20px",
      marginBottom: "30px",
    },
    input: {
      flex: 1,
      padding: "12px",
      borderRadius: "10px",
      border: "1px solid #003399",
      outline: "none",
      fontSize: "16px",
    },
    fileInputContainer: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      border: "1px solid #003399",
      borderRadius: "10px",
      padding: "10px 15px",
      marginBottom: "150px",
    },
    fileLabelText: {
      fontWeight: "bold",
      fontSize: "16px",
      color: "#000000",
    },
    fileActions: {
      display: "flex",
      alignItems: "center",
      backgroundColor: "#f0f0f0",
      padding: "5px 20px",
      borderRadius: "6px",
      gap: "5px",
      fontSize: "16px",
    },
    fileInput: {
      display: "none",
    },
    envelopeIcon: {
      fontSize: "16px",
      color: "#555",
    },
    dotContainer: {
      display: "flex",
      justifyContent: "center",
      marginBottom: "30px",
      gap: "10px",
    },
    dot: {
      height: "10px",
      width: "10px",
      backgroundColor: "#bbb",
      borderRadius: "50%",
      display: "inline-block",
    },
    dotActive: {
      backgroundColor: "#003399",
    },
    button: {
      alignSelf: "center",
      width: "150px",
      height: "50px",
      border: "none",
      borderRadius: "10px",
      backgroundColor:
        form.firstName && form.lastName && form.profilePicture
          ? "#003399"
          : "#b3b3b3",
      color: "#ffffff",
      fontWeight: "bold",
      fontSize: "16px",
      cursor:
        form.firstName && form.lastName && form.profilePicture
          ? "pointer"
          : "not-allowed",
    },
  };

  return (
    <div style={styles.container}>
      <form style={styles.form} onSubmit={handleSubmit}>
        <h2 style={styles.heading}>Sign Up</h2>

        <label style={styles.label}>Name</label>
        <div style={styles.nameRow}>
          <input
            style={styles.input}
            type="text"
            name="firstName"
            placeholder="First name"
            value={form.firstName}
            onChange={handleChange}
            required
          />
          <input
            style={styles.input}
            type="text"
            name="lastName"
            placeholder="Last name"
            value={form.lastName}
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.fileInputContainer}>
          <span style={styles.fileLabelText}>Select Profile Picture</span>
          <label htmlFor="file-upload" style={styles.fileActions}>
            <span>Choose File</span>
            <span style={styles.envelopeIcon}>📂</span>
          </label>
          <input
            style={styles.fileInput}
            type="file"
            id="file-upload"
            name="profilePicture"
            accept="image/*"
            onChange={handleChange}
            required
          />
        </div>

        <div style={styles.dotContainer}>
          <span style={styles.dot}></span>
          <span style={{ ...styles.dot, ...styles.dotActive }}></span>
          <span style={styles.dot}></span>
        </div>

        <button
          type="submit"
          style={styles.button}
          disabled={!form.firstName || !form.lastName || !form.profilePicture}
        >
          Sign Up
        </button>
      </form>
    </div>
  );
};

export default SignupStep2;
