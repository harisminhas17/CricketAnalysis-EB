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
  FaBan,
  FaEye,
} from "react-icons/fa";

const TeamsPage: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);

  const [teamStatus, setTeamStatus] = useState<Record<number, boolean>>({
    0: true,
    1: true,
    2: false,
    3: true,
  });

  const [allTeams, setAllTeams] = useState([
  { id: "#1233", name: "Titans", coach: "Bilal Ali", players: 11 },
  { id: "#6675", name: "Khanns", coach: "Waisi Khan", players: 22 },
  { id: "#2233", name: "Lions", coach: "Sajid", players: 13 },
  { id: "#3333", name: "Titans", coach: "Balil", players: 18 },
  { id: "#4455", name: "Dragons", coach: "Hamza", players: 16 },
  { id: "#5566", name: "Warriors", coach: "Asim", players: 19 },
]);


  const [newTeam, setNewTeam] = useState({
    id: "",
    name: "",
    coach: "",
    players: "",
  });

  const toggleStatus = (index: number) => {
    setTeamStatus((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const handleAddTeam = () => {
    if (newTeam.id && newTeam.name && newTeam.coach && newTeam.players) {
      const updatedTeams = [
        ...allTeams,
        {
          id: newTeam.id,
          name: newTeam.name,
          coach: newTeam.coach,
          players: Number(newTeam.players),
        },
      ];
      setAllTeams(updatedTeams);
      setTeamStatus((prev) => ({
        ...prev,
        [updatedTeams.length - 1]: true,
      }));
      setNewTeam({ id: "", name: "", coach: "", players: "" });
      setShowAddForm(false);
    } else {
      alert("Please fill all fields");
    }
  };

  const filteredTeams = allTeams.filter((t) =>
    t.name.toLowerCase().includes(searchTerm.toLowerCase())
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
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              marginBottom: "20px",
            }}
          >
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
            <h2 style={{ fontSize: "20px", fontWeight: "bold", margin: 0 }}>
              CricketZone
            </h2>
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
            background: "#eeececff",
            padding: "10px 20px",
            marginBottom: "20px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
          }}
        >
          <h2 style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>Teams</h2>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <input
              type="text"
              placeholder="  🔍︎ Search ......."
              style={{
                padding: "8px 12px",
                borderRadius: "10px",
                border: "1px solid #ccc",
                width: "220px",
                background: "#eeececff",
              }}
            />
            <FaBell size={20} color="#555" style={{ cursor: "pointer" }} />
          </div>
        </div>

        {/* Top Cards */}
        <div style={{ display: "flex", gap: "16px", marginBottom: "20px" }}>
          <div style={{ ...topCardStyle, background: "#ffffffff" }}>
            <FaUsers size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Total Players</h4>
              <p style={{ fontSize: "24px", fontWeight: "bold", marginTop: "12px", marginBottom: 0 }}>112</p>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#ffffffff" }}>
            <FaCheckCircle size={28} />
            <div>
              <div>Active Players</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>12</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#ffffffff" }}>
            <FaBan size={28} />
            <div>
              <div>Injured Players</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>15</div>
            </div>
          </div>

          <div style={{ ...topCardStyle, background: "#ffffffff" }}>
            <FaUsers size={28} />
            <div>
              <div>Unassigned Players</div>
              <div style={{ fontSize: "20px", fontWeight: "bold", marginTop: "12px" }}>10</div>
            </div>
          </div>
        </div>

        {/* Search & Add */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            marginBottom: "12px",
          }}
        >
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            <h3 style={{ margin: 0 }}>Team Management</h3>
            <input
              type="text"
              placeholder=" 🔍︎ search for team....."
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
              fontSize: "16px",
            }}
          >
            Add Team
          </button>
        </div>

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
            <h3 style={{ marginBottom: "20px", color: "#2d6096" }}>Add New Team</h3>

            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <input
                type="text"
                placeholder="Team ID"
                value={newTeam.id}
                onChange={(e) => setNewTeam({ ...newTeam, id: e.target.value })}
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
                value={newTeam.name}
                onChange={(e) => setNewTeam({ ...newTeam, name: e.target.value })}
                style={{
                  padding: "10px 14px",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                  fontSize: "16px",
                }}
              />
              <input
                type="text"
                placeholder="Coach Name"
                value={newTeam.coach}
                onChange={(e) => setNewTeam({ ...newTeam, coach: e.target.value })}
                style={{
                  padding: "10px 14px",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                  fontSize: "16px",
                }}
              />
              <input
                type="number"
                placeholder="No. of Players"
                value={newTeam.players}
                onChange={(e) => setNewTeam({ ...newTeam, players: e.target.value })}
                style={{
                  padding: "10px 14px",
                  borderRadius: "8px",
                  border: "1px solid #ccc",
                  fontSize: "16px",
                }}
              />

              <div style={{ display: "flex", gap: "12px", marginTop: "10px" }}>
                <button
                  onClick={handleAddTeam}
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

        {/* Teams Table */}
        <div
          style={{
             backgroundColor: "#f0f0f0",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            padding: "35px",
          }}
        >
         <table style={{ width: "100%", borderCollapse: "collapse" }}>
  <thead>
    <tr style={{ borderBottom: "1px solid #ddd" }}>
      <th style={{ textAlign: "left", padding: "16px" }}>ID</th>
      <th style={{ textAlign: "left", padding: "16px" }}>Team Name</th>
      <th style={{ textAlign: "left", padding: "16px" }}>Coach Name</th>
      <th style={{ textAlign: "left", padding: "16px" }}>No. of players</th>
      <th style={{ textAlign: "left", padding: "16px" }}>Status</th>
      <th style={{ textAlign: "left", padding: "16px" }}>Actions</th>
    </tr>
  </thead>
  <tbody>
    {(showAll ? filteredTeams : filteredTeams.slice(0, 4)).map((t, i) => (
      <tr key={i}>
        <td style={{ padding: "16px", lineHeight: "1.8" }}>{t.id}</td>
        <td style={{ padding: "16px", lineHeight: "1.8" }}>{t.name}</td>
        <td style={{ padding: "16px", lineHeight: "1.8" }}>{t.coach}</td>
        <td style={{ padding: "16px", lineHeight: "1.8" }}>{t.players}</td>
        <td
          style={{ padding: "16px", cursor: "pointer", lineHeight: "1.8" }}
          onClick={() => toggleStatus(i)}
        >
          {teamStatus[i] ? <FaCheckCircle color="green" /> : <FaBan color="red" />}
        </td>
        <td style={{ padding: "16px", lineHeight: "1.8" }}>
          <FaEye style={{ cursor: "pointer" }} /> ⋮
        </td>
      </tr>
    ))}
  </tbody>
</table>
{filteredTeams.length > 4 && (
  <div style={{ marginTop: "12px" }}>
    <button
      onClick={() => setShowAll(!showAll)}
      style={{
        background: "transparent",
        border: "none",
        color: "#2d6096",
        cursor: "pointer",
        fontSize: "16px",
      }}
    >
      {showAll ? "View Less" : "View All"}
    </button>
  </div>
)}

        </div>
      </div>
    </div>
  );
};

export default TeamsPage;
