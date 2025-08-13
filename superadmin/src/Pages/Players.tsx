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

const PlayersPage: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPlayer, setNewPlayer] = useState({
    image: "",
    name: "",
    age: "",
    team: "",
  });

  const [playerStatus, setPlayerStatus] = useState<Record<number, boolean>>({
    0: true,
    1: true,
    2: false,
    3: true,
    4: true,
    5: false,
  });

  const [allPlayers, setAllPlayers] = useState([
    { profile: "/player1.jpg", name: "Usama Ali", age: "23 yrs", team: "Titans" },
    { profile: "/player2.jpg", name: "Shah Ali", age: "25 yrs", team: "Lions" },
    { profile: "/player3.jpg", name: "Shehbaz", age: "20 yrs", team: "Khanss" },
    { profile: "/player4.jpg", name: "Rizwan", age: "20 yrs", team: "Khanss" },
    { profile: "/player5.webp", name: "Aamir", age: "22 yrs", team: "Wolves" },
    { profile: "/player6.jpg", name: "Hassan", age: "24 yrs", team: "Falcons" },
  ]);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleNewPlayerImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setNewPlayer((prev) => ({ ...prev, image: reader.result as string }));
      };
      reader.readAsDataURL(file);
    }
  };

  const toggleStatus = (index: number) => {
    setPlayerStatus((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const handleAddPlayer = () => {
    if (newPlayer.name && newPlayer.age && newPlayer.team) {
      const updatedPlayers = [...allPlayers, {
        profile: newPlayer.image || "/profile.png",
        name: newPlayer.name,
        age: newPlayer.age,
        team: newPlayer.team,
      }];
      setAllPlayers(updatedPlayers);
      setPlayerStatus((prev) => ({
        ...prev,
        [updatedPlayers.length - 1]: true,
      }));
      setNewPlayer({ image: "", name: "", age: "", team: "" });
      setShowAddForm(false);
    } else {
      alert("Please fill all fields");
    }
  };

  const filteredPlayers = allPlayers.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
    flex: 1,
    minWidth: "200px",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    fontWeight: "bold",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  };

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Sidebar */}
      <div
        style={{
          width: "230px",
          background: "#fff",
          color: "#000",
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
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: "1px solid #ccc",
                }}
              >
                <img
                  src={image || "/profile.png"}
                  alt="Profile"
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                  }}
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
            marginTop: "auto",
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
            background: "#ffffffff",
            padding: "10px 20px",
            marginBottom: "20px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
          }}
        >
          <h2 style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>Players</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <input
              type="text"
              placeholder=" 🔍︎ Search ......."
              style={{
                padding: "8px 12px",
                                borderRadius: "10px",
                border: "1px solid #ccc",
                width: "220px",
              }}
            />
            <FaBell size={20} color="#555" style={{ cursor: "pointer" }} />
          </div>
        </div>

        {/* Top Cards */}
        <div style={{ display: "flex", gap: "16px", marginBottom: "20px" }}>
          <div style={{ ...topCardStyle, background: "#b3c7f7" }}>
            <FaUsers size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Total Players</h4>
              <p style={{ fontSize: '24px', fontWeight: 'bold', marginTop: '12px', marginBottom: 0 }}>{allPlayers.length}</p>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#a9d4c9", flex: 1.5 }}>
            <FaCheckCircle size={28} />
            <div>
              <div>Active Teams</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>10</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#f0d1b3", flex: 1.5 }}>
            <FaBan size={28} />
            <div>
              <div>Inactive Teams</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>2</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#b3baf7", flex: 1.5 }}>
            <FaHourglassHalf size={28} />
            <div>
              <div>Pending Teams</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>10</div>
            </div>
          </div>
        </div>

        {/* Player List Header & Search */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            marginBottom: "12px",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <h3 style={{ margin: 0 }}>Player List</h3>
            <input
              type="text"
              placeholder=" 🔍︎ Search for player....."
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
            onClick={() => setShowAddForm(true)}
            style={{
              background: "#2d6096",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              padding: "10px 16px",
              cursor: "pointer",
              fontSize: '21px',
            }}
          >
            Add Team
          </button>
        </div>

        {/* Add Team Form */}
        {/* Add Team Form */}
{showAddForm && (
  <div
    style={{
      background: "#ffffff",
      borderRadius: "12px",
      padding: "30px",
      marginBottom: "24px",
      boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
      maxWidth: "500px",
    }}
  >
    <h3 style={{ marginBottom: "20px", color: "#2d6096" }}>Add New Player</h3>

    <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
      {/* Upload Image Preview */}
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <div
          style={{
            width: "60px",
            height: "60px",
            borderRadius: "50%",
            overflow: "hidden",
            border: "1px solid #ccc",
            backgroundColor: "#f0f0f0",
          }}
        >
          <img
            src={newPlayer.image || "/profile.png"}
            alt="Player"
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </div>
        <input type="file" accept="image/*" onChange={handleNewPlayerImage} />
      </div>

      {/* Input Fields */}
      <input
        type="text"
        placeholder="Full Name"
        value={newPlayer.name}
        onChange={(e) => setNewPlayer({ ...newPlayer, name: e.target.value })}
        style={{
          padding: "10px 14px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontSize: "16px",
        }}
      />

      <input
        type="text"
        placeholder="Age (e.g., 23 yrs)"
        value={newPlayer.age}
        onChange={(e) => setNewPlayer({ ...newPlayer, age: e.target.value })}
        style={{
          padding: "10px 14px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontSize: "16px",
        }}
      />

      <input
        type="text"
        placeholder="Team Name"
        value={newPlayer.team}
        onChange={(e) => setNewPlayer({ ...newPlayer, team: e.target.value })}
        style={{
          padding: "10px 14px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          fontSize: "16px",
        }}
      />

      {/* Action Buttons */}
      <div style={{ display: "flex", gap: "12px", marginTop: "10px" }}>
        <button
          onClick={handleAddPlayer}
          style={{
            background: "#2d6096",
            color: "#fff",
            border: "none",
            padding: "10px 20px",
            borderRadius: "8px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Add
        </button>

        <button
          onClick={() => setShowAddForm(false)}
          style={{
            background: "#ccc",
            color: "#000",
            border: "none",
            padding: "10px 20px",
            borderRadius: "8px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
)}


        {/* Player List Table */}
        <div
          style={{
            background: "#f5f5f5",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            padding: "40px",
          }}
        >
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #ddd" }}>
                <th style={{ textAlign: "left", padding: "8px" }}>Profile</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Name</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Age</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Team</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Status</th>
                <th style={{ textAlign: "left", padding: "8px" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {(showAll ? filteredPlayers : filteredPlayers.slice(0, 4)).map((p, i) => (
                <tr key={i}>
                  <td style={{ padding: "10px" }}>
                    <img
                      src={p.profile}
                      alt={p.name}
                      style={{
                        width: "45px",
                        height: "45px",
                        borderRadius: "50%",
                        objectFit: "cover",
                      }}
                    />
                  </td>
                  <td style={{ padding: "8px" }}>{p.name}</td>
                  <td style={{ padding: "8px" }}>{p.age}</td>
                  <td style={{ padding: "8px" }}>{p.team}</td>
                  <td style={{ padding: "8px", cursor: "pointer" }} onClick={() => toggleStatus(i)}>
                    {playerStatus[i] ? <FaCheckCircle color="green" /> : <FaBan color="red" />}
                  </td>
                  <td style={{ padding: "8px" }}>
                    <FaEye style={{ cursor: "pointer" }} /> ⋮
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {!showAll && filteredPlayers.length > 4 && (
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

export default PlayersPage;

