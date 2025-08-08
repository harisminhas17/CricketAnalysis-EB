import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const DashboardPage = () => {
  const [image, setImage] = useState<string | null>(null);

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

  const navLinks = [
    { to: '/Dashboard', label: 'Dashboard' },
    { to: '/players', label: 'Players' },
    { to: '/teams', label: 'Teams' },
    { to: '/coaches', label: 'Coaches' },
    { to: '/clubs', label: 'Clubs' },
    { to: '/socialmedia', label: 'Social Media' },
    { to: '/balltrack', label: 'Ball Track' },
    { to: '/settings', label: 'Settings' },
  ];

  const cardCommon: React.CSSProperties = {
    background: '#fff',
    borderRadius: '12px',
    padding: '16px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
    flex: 1,
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
      {/* Sidebar */}
      <div
        style={{
          width: '230px',
          background: '#fff',
          color: '#000',
          padding: '24px 16px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          borderRight: '1px solid #ddd',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
            <label htmlFor="upload-photo" style={{ cursor: 'pointer' }}>
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '50%',
                  backgroundColor: '#f0f0f0',
                  overflow: 'hidden',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  border: '1px solid #ccc',
                }}
              >
                {image ? (
                  <img
                    src={image}
                    alt="Profile"
                    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                  />
                ) : (
                  <span style={{ fontSize: '24px' }}>👤</span>
                )}
              </div>
              <input
                id="upload-photo"
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: 'none' }}
              />
            </label>
            <h2 style={{ fontSize: '20px', fontWeight: 'bold', margin: 0 }}>CricketZone</h2>
          </div>

          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              style={({ isActive }) => ({
                color: isActive ? '#fff' : '#000',
                textDecoration: 'none',
                padding: '10px 14px',
                fontSize: '16px',
                fontWeight: isActive ? 'bold' : 'normal',
                borderRadius: '8px',
                backgroundColor: isActive ? '#2d6096' : 'transparent',
                display: 'block',
                marginBottom: '8px',
              })}
            >
              {link.label}
            </NavLink>
          ))}
        </div>

        <button
          style={{
            backgroundColor: '#fff',
            color: '#000',
            border: 'none',
            borderRadius: '8px',
            padding: '10px',
            fontSize: '14px',
            cursor: 'pointer',
            marginTop: 'auto',
          }}
          onClick={() => alert('Logged out!')}
        >
          🔓 Logout
        </button>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', background: '#fafafa' }}>
        {/* Header */}
        <div
          style={{
            background: '#fff',
            padding: '12px 20px',
            marginBottom: '20px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            borderRadius: '12px',
          }}
        >
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>Dashboard</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <input
              type="text"
              placeholder="Search ........"
              style={{
                padding: '8px 12px',
                borderRadius: '20px',
                border: '1px solid #ccc',
                width: '220px',
              }}
            />
            <div style={{ fontSize: '20px', cursor: 'pointer' }}>🔔</div>
          </div>
        </div>

        {/* Stats Cards */}
        <div style={{ display: 'flex', gap: '16px', marginBottom: '20px' }}>
          <div style={{ ...cardCommon, backgroundColor: '#b3c7f7' }}>
            <h4>Total Players</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>112</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#a9d4c9' }}>
            <h4>Total Teams</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>12</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#f0d1b3' }}>
            <h4>Total Coaches</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>15</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#b3baf7' }}>
            <h4>Total Clubs</h4>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>10</p>
          </div>
        </div>

        {/* Upcoming Matches & Performance */}
        <div style={{ display: 'flex', gap: '16px', marginBottom: '20px' }}>
          <div style={{ ...cardCommon, flex: 2 }}>
            <h4>Upcoming Matches</h4>
            <table style={{ width: '100%', fontSize: '14px', marginTop: '10px', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #ddd' }}>
                  <th align="left">Team1</th>
                  <th align="left">Team2</th>
                  <th align="left">Date/Time</th>
                  <th align="left">Venue</th>
                  <th align="left">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Titans</td>
                  <td>Khanns</td>
                  <td>23-3-2025 10:00am</td>
                  <td>Lahore</td>
                  <td>...</td>
                </tr>
                <tr>
                  <td>Titans</td>
                  <td>Khanns</td>
                  <td>25-3-2025 10:00am</td>
                  <td>Peshawar</td>
                  <td>...</td>
                </tr>
                <tr>
                  <td>Khanns</td>
                  <td>Lions</td>
                  <td>26-3-2025 10:00am</td>
                  <td>Peshawar</td>
                  <td>...</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style={{ ...cardCommon, flex: 1 }}>
            <h4>Performance</h4>
            <div
              style={{
                height: '250px',
                background: '#f8f8f8',
                borderRadius: '8px',
                marginTop: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#555',
                overflow: 'hidden', 
              }}
            >
              <img
      src="/Capture.JPG"
      alt="Performance Chart"
      style={{ width: '140%', height: '100%', objectFit: 'contain' }}
    />
            </div>
          </div>
        </div>

        {/* Admin Activity Log */}
        <div style={{ ...cardCommon, marginBottom: '20px' }}>
          <h4>Admin Activity Log</h4>
          <div style={{ marginTop: '10px', fontSize: '14px', lineHeight: '1.6' }}>
            <div>➕ Admin added new player: Ali Khan (Titans) — 23-3-2025 | 11:00am</div>
            <div>✏️ Admin updated match: Titans vs Lion (Venue Changed) — 23-3-2025 | 11:00am</div>
            <div>📅 Scheduled new match: Khanns vs Titans — 24-3-2025 | 11:00am</div>
            <div>🗑 Deleted player: Umer Hussain (Titans) — 26-3-2025 | 11:00am</div>
          </div>
        </div>

        {/* Footer Buttons */}
        <div style={{ display: 'flex', gap: '12px' }}>
          {['Add player', 'Update match', 'Schedule match', 'Deleted record', 'Generate report'].map((btn) => (
            <button
              key={btn}
              style={{
                padding: '10px 16px',
                borderRadius: '8px',
                border: 'none',
                background: '#e0e0e0',
                cursor: 'pointer',
              }}
            >
              {btn}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
