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
  FaCheckCircle,
  FaHourglassHalf,
  FaBan,
  FaEye,
} from "react-icons/fa";

const ClubsPage: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [clubStatus, setClubStatus] = useState<Record<number, boolean>>({
    0: true,
    1: true,
    2: false,
    3: true,
  });

  const [allClubs, setAllClubs] = useState([
    { id: "#1233", name: "Riverside", owner: "Bilal Ali", location: "Peshawar" },
    { id: "#6675", name: "Khanns", owner: "Waisi Khan", location: "Lahore" },
    { id: "#1233", name: "Lionner", owner: "Safda", location: "Multan" },
    { id: "#1233", name: "TIGERS", owner: "Ahmed", location: "Quetta" },
  ]);

  const [newClub, setNewClub] = useState({
    id: "",
    name: "",
    owner: "",
    location: "",
  });

  const handleAddClub = () => setShowAddForm(true);
  const handleCancelForm = () => {
    setShowAddForm(false);
    setNewClub({ id: "", name: "", owner: "", location: "" });
  };

  const handleFormSubmit = () => {
    setAllClubs([...allClubs, newClub]);
    setNewClub({ id: "", name: "", owner: "", location: "" });
    setShowAddForm(false);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImage(reader.result as string);
      reader.readAsDataURL(file);
    }
  };

  const toggleStatus = (index: number) => {
    setClubStatus((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const navLinks = [
    { to: "/Dashboard", label: "Dashboard", icon: <FaUsers /> },
    { to: "/players", label: "Players", icon: <FaUser /> },
    { to: "/teams", label: "Teams", icon: <FaLayerGroup /> },
    { to: "/coaches", label: "Coaches", icon: <FaUserTie /> },
    { to: "/clubs", label: "Clubs", icon: <FaBuilding /> },
    { to: "/socialmedia", label: "Social Media", icon: <FaHashtag /> },
    { to: "/balltrack", label: "Ball Track", icon: <FaBullseye /> },
    { to: "/settings", label: "Settings", icon: <FaCog /> },
  ];

  const topCardStyle: React.CSSProperties = {
    borderRadius: "12px",
    padding: "35px",
    flex: 2,
    minWidth: "140px",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    fontWeight: "bold",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  };

  const filteredClubs = allClubs.filter((club) =>
    club.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "230px",
          background: "#fff",
          padding: "24px 16px",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          borderRight: "1px solid #ddd",
        }}
      >
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "20px" }}>
            <label htmlFor="upload-photo" style={{ cursor: "pointer" }}>
              <div
                style={{
                  width: "58px",
                  height: "58px",
                  borderRadius: "50%",
                  backgroundColor: "#f0f0f0",
                  overflow: "hidden",
                  border: "1px solid #ccc",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <img
                  src={image || "/profile.png"}
                  alt="Profile"
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>
              <input
                id="upload-photo"
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: "none" }}
              />
            </label>
            <h2 style={{ fontSize: "20px", fontWeight: "bold", margin: 0 }}>CricketZone</h2>
          </div>

          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              style={({ isActive }) => ({
                color: isActive ? "#fff" : "#000",
                textDecoration: "none",
                padding: "10px 14px",
                fontSize: "16px",
                fontWeight: isActive ? "bold" : "normal",
                borderRadius: "8px",
                backgroundColor: isActive ? "#2d6096" : "transparent",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                marginBottom: "8px",
              })}
            >
              {link.icon}
              {link.label}
            </NavLink>
          ))}
        </div>

        <button
          style={{
            backgroundColor: "#fff",
            color: "#000",
            border: "none",
            borderRadius: "8px",
            padding: "10px",
            fontSize: "14px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "6px",
          }}
        >
          <FaLockOpen /> Logout
        </button>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "16px", background: "#fff" }}>
        {/* Header */}
        <div
          style={{
            padding: "10px 20px",
            marginBottom: "20px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
            background: '#f5f5f5',
          }}
        >
          <h2 style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>Clubs</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <input
              type="text"
              placeholder=" 🔍︎ Search ......."
              style={{
                padding: "8px 12px",
                borderRadius: "10px",
                border: "1px solid #ccc",
                width: "220px",
                background: '#f5f5f5',
              }}
            />
            <FaBell size={20} color="#555" style={{ cursor: "pointer" }} />
          </div>
        </div>

        {/* Top Cards */}
        <div style={{ display: "flex", gap: "16px", marginBottom: "20px" }}>
          <div style={{ ...topCardStyle, background: "#b3baf7" }}>
            <FaUsers size={28} />
            <div>
              <div>Total Clubs</div>
              <div style={{ fontSize: "24px", marginTop: "20px" }}>{allClubs.length}</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#a9d4c9" }}>
            <FaCheckCircle size={28} />
            <div>
              <div>Active Clubs</div>
              <div style={{ fontSize: "24px", marginTop: "10px" }}>
                {Object.values(clubStatus).filter(Boolean).length}
              </div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#b3baf7" }}>
            <FaHourglassHalf size={28} />
            <div>
              <div>Pending Approval</div>
              <div style={{ fontSize: "24px", marginTop: "10px" }}>5</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#a3aaf5" }}>
            <FaBan size={28} />
            <div>
              <div>Suspended Clubs</div>
              <div style={{ fontSize: "24px", marginTop: "10px" }}>3</div>
            </div>
          </div>
        </div>

        {/* Club Management Section */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <h3 style={{ margin: 0 }}>Club Management</h3>
            <input
              type="text"
              placeholder=" 🔍︎ search for club....."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                padding: "8px 12px",
                borderRadius: "10px",
                border: "1px solid #ccc",
                width: "200px",
                backgroundColor: "#f0f0f0",
              }}
            />
          </div>
          <button
            style={{
              background: "#2d6096",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              padding: "10px 16px",
              cursor: "pointer",
              fontSize: '21px',
            }}
            onClick={handleAddClub}
          >
            Add Club
          </button>
        </div>

        {/* Add Club Form */}
        {showAddForm && (
          <div
            style={{
              backgroundColor: "#f0f0f0",
              padding: "20px",
              borderRadius: "10px",
              marginBottom: "20px",
              display: "flex",
              flexDirection: "column",
              gap: "12px",
              width: "300px",
            }}
          >
            <input
              type="text"
              placeholder="Club ID"
              value={newClub.id}
              onChange={(e) => setNewClub({ ...newClub, id: e.target.value })}
              style={{ padding: "8px", borderRadius: "6px", border: "1px solid #ccc" }}
            />
            <input
              type="text"
              placeholder="Club Name"
              value={newClub.name}
              onChange={(e) => setNewClub({ ...newClub, name: e.target.value })}
              style={{ padding: "8px", borderRadius: "6px", border: "1px solid #ccc" }}
            />
            <input
              type="text"
              placeholder="Owner Name"
              value={newClub.owner}
              onChange={(e) => setNewClub({ ...newClub, owner: e.target.value })}
              style={{ padding: "8px", borderRadius: "6px", border: "1px solid #ccc" }}
            />
            <input
              type="text"
              placeholder="Location"
              value={newClub.location}
              onChange={(e) => setNewClub({ ...newClub, location: e.target.value })}
              style={{ padding: "8px", borderRadius: "6px", border: "1px solid #ccc" }}
            />
            <div style={{ display: "flex", gap: "10px" }}>
              <button onClick={handleFormSubmit} style={{ padding: "8px 12px", background: "#2d6096", color: "#fff", border: "none", borderRadius: "6px", cursor: "pointer" }}>
                Submit
              </button>
              <button onClick={handleCancelForm} style={{ padding: "8px 12px", background: "#ccc", color: "#000", border: "none", borderRadius: "6px", cursor: "pointer" }}>
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Club Table */}
        <div style={{ background: "#f5f5f5", borderRadius: "12px", boxShadow: "0 2px 8px rgba(0,0,0,0.1)", padding: "30px" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #ddd" }}>
                <th style={{ textAlign: "left", padding: "8px" }}>ID</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Club Name</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Owner Name</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Location</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Status</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {(showAll ? filteredClubs : filteredClubs.slice(0, 4)).map((club, i) => (
                <tr key={i}>
                  <td style={{ padding: "16px 10px", lineHeight: "1.8" }}>{club.id}</td>
                  <td style={{ padding: "16px 10px", lineHeight: "1.8" }}>{club.name}</td>
                  <td style={{ padding: "16px 10px", lineHeight: "1.8" }}>{club.owner}</td>
                  <td style={{ padding: "16px 10px", lineHeight: "1.8" }}>{club.location}</td>
                  <td style={{ padding: "10px", cursor: "pointer" }} onClick={() => toggleStatus(i)}>
                    {clubStatus[i] ? <FaCheckCircle color="green" /> : <FaBan color="red" />}
                  </td>
                  <td style={{ padding: "10px" }}>
                    <FaEye style={{ cursor: "pointer", marginRight: "8px" }} /> ⋮
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {!showAll && (
            <div style={{ marginTop: "12px" }}>
              <button
                onClick={() => setShowAll(true)}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "#2d6096",
                  cursor: "pointer",
                  fontSize: "18px",
                }}
              >
                View All
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ClubsPage;
