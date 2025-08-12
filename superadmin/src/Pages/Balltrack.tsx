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
  FaEye,
  FaChartBar,
  FaEdit,
} from "react-icons/fa";
import { BsThreeDotsVertical } from "react-icons/bs";

const BallTrackPage: React.FC = () => {
  const [image] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [showAll, setShowAll] = useState(false);

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
    padding: "40px",
    flex: 1,
    minWidth: "200px",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    fontWeight: "bold",
    background: "#fff",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
  };

  const ballTrackData = [
    {
      trackerId: "#1233",
      bowler: "Titans",
      batsman: "Bilal Ali",
      speed: 11.2,
      over: 1.6,
      spin: 2.6,
      start: "10:11:09",
      end: "12:15:08",
    },
    {
      trackerId: "#6675",
      bowler: "Khanns",
      batsman: "Waisi Khan",
      speed: 19.2,
      over: 1.2,
      spin: 2.1,
      start: "10:11:09",
      end: "12:15:08",
    },
    {
      trackerId: "#1233",
      bowler: "Lions",
      batsman: "Sajid",
      speed: 10.2,
      over: 1.3,
      spin: 1.1,
      start: "10:11:09",
      end: "12:15:08",
    },
    {
      trackerId: "#1233",
      bowler: "Titans",
      batsman: "Balil",
      speed: 9.2,
      over: 1.4,
      spin: 0.8,
      start: "10:11:09",
      end: "12:15:08",
    },
    {
      trackerId: "#1433",
      bowler: "Titans",
      batsman: "Sajid",
      speed: 9.4,
      over: 1.4,
      spin: 0.9,
      start: "11:15:09",
      end: "12:15:08",
    },
  ];

  const filteredData = ballTrackData.filter(
    (row) =>
      row.bowler.toLowerCase().includes(searchTerm.toLowerCase()) ||
      row.batsman.toLowerCase().includes(searchTerm.toLowerCase()) ||
      row.trackerId.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
                backgroundColor:
                  isActive && link.to === "/balltrack"
                    ? "#2d6096"
                    : "transparent",
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
          <h2 style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>
            Ball Track
          </h2>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <input
              type="text"
              placeholder="🔍︎ Search ......."
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
          <div style={topCardStyle}>
            <FaChartBar size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Total Tracked Balls</h4>
              <p style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>
                112
              </p>
            </div>
          </div>
          <div style={topCardStyle}>
            <FaUsers size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Active Tracking User</h4>
              <p style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>
                12
              </p>
            </div>
          </div>
          <div style={topCardStyle}>
            <FaBullseye size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Most Tracked Ball type</h4>
              <p style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>
                -
              </p>
            </div>
          </div>
          <div style={topCardStyle}>
            <FaEdit size={28} />
            <div>
              <h4 style={{ margin: 0 }}>Total Edits/Deletes</h4>
              <p style={{ fontSize: "24px", fontWeight: "bold", margin: 0 }}>
                445
              </p>
            </div>
          </div>
        </div>
<h3 style={{ margin: "0 0 16px 0" }}>Detailed Tracking Table</h3>
          <input
            type="text"
            placeholder=" 🔍︎  search in table......"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              padding: "8px 12px",
              borderRadius: "10px",
              border: "1px solid #ccc",
              marginBottom: "12px",
              width: "220px",
              backgroundColor: "#f0f0f0",
            }}
          />
          
        {/* Table */}
        <div
          style={{
             background: "#f5f5f5",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            padding: "20px",
          }}
        >
          

          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #ddd" }}>
                {[
                  "Tracker ID",
                  "Bowler Name",
                  "Batsman Name",
                  "Speed (Km/h)",
                  "Over",
                  "Spin/Swing %",
                  "Start/End Time",
                  "Actions",
                ].map((head) => (
                  <th
                    key={head}
                    style={{ textAlign: "left", padding: "12px", fontWeight: "bold" }}
                  >
                    {head}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(showAll ? filteredData : filteredData.slice(0, 4)).map(
                (row, i) => (
                  <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
                    <td style={{ padding: "12px" }}>{row.trackerId}</td>
                    <td style={{ padding: "12px" }}>{row.bowler}</td>
                    <td style={{ padding: "12px" }}>{row.batsman}</td>
                    <td style={{ padding: "12px" }}>{row.speed}</td>
                    <td style={{ padding: "12px" }}>{row.over}</td>
                    <td style={{ padding: "12px" }}>{row.spin}</td>
                    <td style={{ padding: "12px" }}>
                      {row.start}
                      <br />
                      {row.end}
                    </td>
                    <td style={{ padding: "12px", display: "flex", gap: "8px" }}>
                      <FaEye style={{ cursor: "pointer" }} />
                      <BsThreeDotsVertical style={{ cursor: "pointer" }} />
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>

          {filteredData.length > 4 && (
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

export default BallTrackPage;
