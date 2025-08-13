import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  FaUser,
  FaLockOpen,
  FaBell,
  FaUsers,
  FaLayerGroup,
  FaUserTie,
  FaBuilding,
  FaHashtag,
  FaBullseye,
  FaCog,
} from "react-icons/fa";

const SettingsPage: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [activeModal, setActiveModal] = useState<string | null>(null);
  const [formValues, setFormValues] = useState<any>({});

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const navLinks = [
    { to: "/dashboard", label: "Dashboard", icon: <FaUsers /> },
    { to: "/players", label: "Players", icon: <FaUser /> },
    { to: "/teams", label: "Teams", icon: <FaLayerGroup /> },
    { to: "/coaches", label: "Coaches", icon: <FaUserTie /> },
    { to: "/clubs", label: "Clubs", icon: <FaBuilding /> },
    { to: "/socialmedia", label: "Social Media", icon: <FaHashtag /> },
    { to: "/balltrack", label: "Ball Track", icon: <FaBullseye /> },
    { to: "/settings", label: "Settings", icon: <FaCog /> },
  ];

  const settingsData = [
    {
      category: "General",
      items: [
        { title: "App settings", description: "Manage the overall settings of app" },
        { title: "Appearance", description: "Configure the appearance" },
        { title: "Player Registration", description: "Manage player registration" },
        { title: "Team Management Settings", description: "Manage team" },
        { title: "Coach Permissions", description: "Manage Permissions" },
      ],
    },
    {
      category: "Notifications",
      items: [
        { title: "Push Notifications", description: "Manage push notification settings" },
        { title: "Email Notifications", description: "Manage email notification settings" },
        { title: "Admin Alerts", description: "Manage alert settings" },
      ],
    },
    {
      category: "Account",
      items: [
        { title: "Account Details", description: "Manage your account details" },
        { title: "Change Password", description: "Change your password" },
        { title: "Subscription", description: "Manage your subscription plan" },
      ],
    },
  ];

  const renderForm = (setting: string) => {
    switch (setting) {
      case "App settings":
        return (
          <>
            <label>
              Enable Auto Updates:
              <input type="checkbox" checked={formValues.autoUpdate || false} onChange={(e) => setFormValues({ ...formValues, autoUpdate: e.target.checked })} />
            </label>
            <label>
              Default Language:
              <select value={formValues.language || ""} onChange={(e) => setFormValues({ ...formValues, language: e.target.value })}>
                <option value="">Select</option>
                <option value="en">English</option>
                <option value="hi">Hindi</option>
              </select>
            </label>
          </>
        );
      case "Appearance":
        return (
          <>
            <label>
              Theme:
              <select value={formValues.theme || ""} onChange={(e) => setFormValues({ ...formValues, theme: e.target.value })}>
                <option value="">Select</option>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
              </select>
            </label>
          </>
        );
      case "Player Registration":
      case "Team Management Settings":
      case "Coach Permissions":
        return (
          <>
            <label>
              Allow Edits:
              <input type="checkbox" checked={formValues.allowEdits || false} onChange={(e) => setFormValues({ ...formValues, allowEdits: e.target.checked })} />
            </label>
            <label>
              Allow Deletion:
              <input type="checkbox" checked={formValues.allowDelete || false} onChange={(e) => setFormValues({ ...formValues, allowDelete: e.target.checked })} />
            </label>
          </>
        );
      case "Push Notifications":
      case "Email Notifications":
      case "Admin Alerts":
        return (
          <>
            <label>
              Enable:
              <input type="checkbox" checked={formValues.enable || false} onChange={(e) => setFormValues({ ...formValues, enable: e.target.checked })} />
            </label>
          </>
        );
      case "Account Details":
        return (
          <>
            <label>
              Full Name:
              <input type="text" value={formValues.name || ""} onChange={(e) => setFormValues({ ...formValues, name: e.target.value })} />
            </label>
            <label>
              Email:
              <input type="email" value={formValues.email || ""} onChange={(e) => setFormValues({ ...formValues, email: e.target.value })} />
            </label>
          </>
        );
      case "Change Password":
        return (
          <>
            <label>
              Current Password:
              <input type="password" />
            </label>
            <label>
              New Password:
              <input type="password" />
            </label>
            <label>
              Confirm Password:
              <input type="password" />
            </label>
          </>
        );
      case "Subscription":
        return (
          <>
            <label>
              Plan:
              <select value={formValues.plan || ""} onChange={(e) => setFormValues({ ...formValues, plan: e.target.value })}>
                <option value="">Select</option>
                <option value="basic">Basic</option>
                <option value="pro">Pro</option>
              </select>
            </label>
          </>
        );
      default:
        return <p>No form available.</p>;
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <div style={{ width: "230px", background: "#fff", padding: "24px 16px", display: "flex", flexDirection: "column", justifyContent: "space-between", borderRight: "1px solid #ddd" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "20px" }}>
            <label htmlFor="upload-photo" style={{ cursor: "pointer" }}>
              <div style={{ width: "58px", height: "58px", borderRadius: "50%", backgroundColor: "#f0f0f0", overflow: "hidden", display: "flex", alignItems: "center", justifyContent: "center", border: "1px solid #ccc" }}>
                <img src={image || "/profile.png"} alt="Profile" style={{ width: "100%", height: "100%", objectFit: "cover" }} />
              </div>
              <input id="upload-photo" type="file" accept="image/*" onChange={handleImageUpload} style={{ display: "none" }} />
            </label>
            <h2 style={{ fontSize: "20px", fontWeight: "bold", margin: 0 }}>CricketZone</h2>
          </div>
          {navLinks.map((link) => (
            <NavLink key={link.to} to={link.to} style={({ isActive }) => ({
              color: isActive ? "#fff" : "#000",
              textDecoration: "none",
              padding: "10px 14px",
              fontSize: "16px",
              borderRadius: "8px",
              backgroundColor: isActive ? "#2d6096" : "transparent",
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginBottom: "8px",
            })}>
              {link.icon}
              {link.label}
            </NavLink>
          ))}
        </div>
        <button style={{ backgroundColor: "#fff", color: "#000", border: "none", borderRadius: "8px", padding: "10px", fontSize: "14px", cursor: "pointer", display: "flex", alignItems: "center", gap: "6px" }}>
          <FaLockOpen /> Logout
        </button>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", background: "#fff" }}>
        {/* Header */}
        <div style={{ background: "#e9e7e7ff", padding: "10px 20px", marginBottom: "20px", display: "flex", justifyContent: "space-between", alignItems: "center", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.05)" }}>
          <h2 style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>Settings</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <input type="text" placeholder=" 🔍︎ Search ......" style={{ background: "#e9e7e7ff",padding: "8px 12px", borderRadius: "10px", border: "1px solid #ccc", width: "220px" }} />
            <FaBell size={20} color="#555" style={{ cursor: "pointer" }} />
          </div>
        </div>

        {/* Settings List */}
        {settingsData.map((section, idx) => (
          <div key={idx} style={{ marginBottom: "30px" }}>
            <h3 style={{ marginBottom: "15px" }}>{section.category}</h3>
            {section.items.map((item, i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: "1px solid #eee" }}>
                <div>
                  <div style={{ fontWeight: "500" }}>{item.title}</div>
                  <div style={{ fontSize: "14px", color: "#2d6096", cursor: "pointer",marginTop: "9px"  }}>{item.description}</div>
                </div>
                <button style={{ background: "#ddd", border: "none", borderRadius: "6px", padding: "6px 12px", cursor: "pointer" }} onClick={() => setActiveModal(item.title)}>Manage</button>
              </div>
            ))}
          </div>
        ))}

        {/* Modal */}
        {activeModal && (
          <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", background: "rgba(0,0,0,0.4)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 9999 }}>
            <div style={{ background: "#fff", padding: "20px", borderRadius: "12px", width: "400px" }}>
              <h2>{activeModal}</h2>
              <form style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                {renderForm(activeModal)}
                <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px", marginTop: "10px" }}>
                  <button type="button" style={{ background: "#ccc", padding: "6px 12px", border: "none", borderRadius: "6px", cursor: "pointer" }} onClick={() => setActiveModal(null)}>Cancel</button>
                  <button type="submit" style={{ background: "#2d6096", color: "#fff", padding: "6px 12px", border: "none", borderRadius: "6px", cursor: "pointer" }}>Save</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SettingsPage;
