import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  FaUser,
  FaLockOpen,
  FaBell,
  FaPlusCircle,
  FaEdit,
  FaCalendarAlt,
  FaTrashAlt,
  FaTachometerAlt,
  FaUsers,
  FaLayerGroup,
  FaUserTie,
  FaBuilding,
  FaHashtag,
  FaBullseye,
  FaCog,
} from 'react-icons/fa';
import { Modal } from '../components/Modal'; // adjust the path if needed

type ModalType = 'addPlayer' | 'updateMatch' | 'scheduleMatch' | 'deleteRecord' | 'generateReport' | null;
const DashboardPage = () => {
  const [image, setImage] = useState<string | null>(null);
  const [activeModal, setActiveModal] = useState<ModalType>(null); // ✅ VALID

const renderModalContent = () => {
  switch (activeModal) {
    case 'addPlayer':
      return (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            console.log('Player added');
            setActiveModal(null);
          }}
        >
          <label>Player Name</label>
          <input type="text" placeholder="Enter name" style={inputStyle} />
          <label>Team</label>
          <input type="text" placeholder="Enter team" style={inputStyle} />
          <button type="submit" style={submitStyle}>Add Player</button>
        </form>
      );

    case 'updateMatch':
      return (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            console.log('Match updated');
            setActiveModal(null);
          }}
        >
          <label>Match ID</label>
          <input type="text" placeholder="Enter match ID" style={inputStyle} />
          <label>New Details</label>
          <input type="text" placeholder="Enter new details" style={inputStyle} />
          <button type="submit" style={submitStyle}>Update Match</button>
        </form>
      );

    case 'scheduleMatch':
      return (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            console.log('Match scheduled');
            setActiveModal(null);
          }}
        >
          <label>Team 1</label>
          <input type="text" placeholder="Team 1" style={inputStyle} />
          <label>Team 2</label>
          <input type="text" placeholder="Team 2" style={inputStyle} />
          <label>Date/Time</label>
          <input type="datetime-local" style={inputStyle} />
          <label>Venue</label>
          <input type="text" placeholder="Venue" style={inputStyle} />
          <button type="submit" style={submitStyle}>Schedule</button>
        </form>
      );

    case 'deleteRecord':
      return (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            console.log('Record deleted');
            setActiveModal(null);
          }}
        >
          <label>Record Type</label>
          <select style={inputStyle}>
            <option value="player">Player</option>
            <option value="match">Match</option>
          </select>
          <label>ID</label>
          <input type="text" placeholder="Enter ID to delete" style={inputStyle} />
          <button type="submit" style={submitStyle}>Delete</button>
        </form>
      );

    case 'generateReport':
      return (
        <div>
          <p>Select a report type to generate:</p>
          <button
            style={submitStyle}
            onClick={() => {
              console.log('Players report generated');
              setActiveModal(null);
            }}
          >
            Players Report
          </button>
          <button
            style={{ ...submitStyle, marginLeft: '10px' }}
            onClick={() => {
              console.log('Match summary generated');
              setActiveModal(null);
            }}
          >
            Match Summary
          </button>
        </div>
      );

    default:
      return null;
  }
};





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
    { to: '/Dashboard', label: 'Dashboard', icon: <FaTachometerAlt /> },
    { to: '/players', label: 'Players', icon: <FaUsers /> },
    { to: '/teams', label: 'Teams', icon: <FaLayerGroup /> },
    { to: '/coaches', label: 'Coaches', icon: <FaUserTie /> },
    { to: '/clubs', label: 'Clubs', icon: <FaBuilding /> },
    { to: '/socialmedia', label: 'Social Media', icon: <FaHashtag /> },
    { to: '/balltrack', label: 'Ball Track', icon: <FaBullseye /> },
    { to: '/settings', label: 'Settings', icon: <FaCog /> },
  ];
  const footerButtonStyle: React.CSSProperties = {
  padding: '10px 16px',
  borderRadius: '8px',
  border: 'none',
  background: '#e0e0e0',
  cursor: 'pointer',
};


const inputStyle: React.CSSProperties = {
  width: '95%',
  padding: '8px',
  marginBottom: '10px',
  borderRadius: '6px',
  border: '1px solid #ccc'
};
const modalTitles: Record<Exclude<ModalType, null>, string> = {
  addPlayer: 'Add New Player',
  updateMatch: 'Update Match Details',
  scheduleMatch: 'Schedule New Match',
  deleteRecord: 'Delete Record',
  generateReport: 'Generate Report',
};



const submitStyle: React.CSSProperties = {
  backgroundColor: '#2d6096',
  color: '#fff',
  padding: '8px 12px',
  borderRadius: '6px',
  border: 'none',
  cursor: 'pointer'
};

  const cardCommon: React.CSSProperties = {
    background: '#fff',
    borderRadius: '12px',
    padding: '13px',
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
        width: '58px',
        height: '58px',
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
        <img
          src="/profile.png" 
          alt="Default Profile"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
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
  <h2 style={{ fontSize: '20px', fontWeight: 'bold', margin: 0 }}>Cricket Zone</h2>
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
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                marginBottom: '8px',
              })}
            >
              {link.icon}
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
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
          onClick={() => alert('Logged out!')}
        >
          <FaLockOpen /> Logout
        </button>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', background: '#ffffffff' }}>
        {/* Header */}
        <div
          style={{
            background: '#f5f5f5ff',
            padding: '10px 20px',
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
              placeholder="🔍︎  Search ........"
              style={{
                background: '#f5f5f5ff',
                padding: '8px 12px',
                borderRadius: '10px',
                border: '1px solid #ccc',
                width: '220px',
              }}
            />
            <FaBell size={20} color="#555" style={{ cursor: 'pointer' }} />
          </div>
        </div>

        {/* Stats Cards */}
        <div style={{ display: 'flex', gap: '16px', marginBottom: '20px' }}>
          <div style={{ ...cardCommon, backgroundColor: '#b3c7f7' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FaUsers size={28}/>
              <h4 style={{ margin: 0 }}>Total Players</h4>
            </div>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>112</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#a9d4c9' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FaLayerGroup size={28} />
              <h4 style={{ margin: 0 }}>Total Teams</h4>
            </div>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>12</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#f0d1b3' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FaUserTie size={28}/>
              <h4 style={{ margin: 0 }}>Total Coaches</h4>
            </div>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>15</p>
          </div>
          <div style={{ ...cardCommon, backgroundColor: '#b3baf7' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FaBuilding size={28} />
              <h4 style={{ margin: 0 }}>Total Clubs</h4>
            </div>
            <p style={{ fontSize: '24px', fontWeight: 'bold' }}>10</p>
          </div>
        </div>

        {/* Section Headings */}
        
        <h4 style={{ marginBottom: '8px' }}>Upcoming Matches</h4>
        <div style={{ display: 'flex', gap: '20px', marginBottom: '10px' }}>
          <div style={{ ...cardCommon, flex: 2 }}>
            <table style={{ width: '100%', fontSize: '16px', marginTop: '10px', borderCollapse: 'collapse', lineHeight: '4' }}>
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
                  <td>⋮</td>
                </tr>
                <tr>
                  <td>Titans</td>
                  <td>Khanns</td>
                  <td>25-3-2025 10:00am</td>
                  <td>Peshawar</td>
                  <td>⋮</td>
                </tr>
                <tr>
                  <td>Khanns</td>
                  <td>Lions</td>
                  <td>26-3-2025 10:00am</td>
                  <td>Peshawar</td>
                  <td>⋮</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style={{ flex: 1.4 }}>
             <h4 style={{ marginBottom: '8px' }}>Performance</h4>
             

  <div style={{ ...cardCommon }}>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h4>Players/Runs</h4>
              <span>⋮</span>
            </div>
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
         </div>
         

       <h4 style={{ marginBottom: '8px' }}>Admin Activity Log</h4>
<div style={{ ...cardCommon, marginBottom: '20px' }}>
  <div style={{ position: 'relative', paddingLeft: '60px' }}>
    {/* Vertical Line */}
    <div
      style={{
        position: 'absolute',
        left: '28px', // this is the exact center for the icons (28px wide icon + padding)
        top: '0',
        bottom: '0',
        width: '2px',
        backgroundColor: '#ccc',
        zIndex: 0,
      }}
    ></div>

    {[
      {
        icon: <FaPlusCircle />,
        text: 'Admin added new player:',
        detail: 'Ali Khan (Titans)',
        date: '23-3-2025 | 11:00am',
      },
      {
        icon: <FaEdit />,
        text: 'Admin updated match:',
        detail: 'Titans vs Lion (Venue Changed)',
        date: '23-3-2025 | 11:00am',
      },
      {
        icon: <FaCalendarAlt />,
        text: 'Scheduled new match:',
        detail: 'Khanns vs Titans',
        date: '24-3-2025 | 11:00am',
      },
      {
        icon: <FaTrashAlt />,
        text: 'Deleted player:',
        detail: 'Umer Hussain (Titans)',
        date: '26-3-2025 | 11:00am',
      },
    ].map((item, index) => (
      <div
        key={index}
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          marginBottom: index !== 3 ? '40px' : '0',
          position: 'relative',
        }}
      >
        {/* Icon (Center aligned on vertical line) */}
        <div
          style={{
            position: 'absolute',
            left: '-50px',
            top: '0',
            width: '28px',
            height: '28px',
            borderRadius: '50%',
            backgroundColor: '#fff',
            border: '2px solid #ccc',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1,
          }}
        >
          {item.icon}
        </div>

        {/* Text content */}
        <div style={{ marginLeft: '2px', fontSize: '14px', lineHeight: '1.1' }}>
          <div style={{ marginBottom: '4px' }}>
            {item.text} <strong>{item.detail}</strong>
          </div>
          <div style={{ color: '#777', fontSize: '12px' }}>{item.date}</div>
        </div>

        {/* Vertical dots */}
        <div style={{ marginLeft: 'auto', paddingRight: '10px' }}>⋮</div>
      </div>
    ))}
  </div>
</div>


        {/* Footer Buttons */}
       <div style={{ display: 'flex', gap: '12px' }}>
  <button style={footerButtonStyle} onClick={() => setActiveModal('addPlayer')}>Add player</button>
  <button style={footerButtonStyle} onClick={() => setActiveModal('updateMatch')}>Update match</button>
  <button style={footerButtonStyle} onClick={() => setActiveModal('scheduleMatch')}>Schedule match</button>
  <button style={footerButtonStyle} onClick={() => setActiveModal('deleteRecord')}>Deleted record</button>
  <button style={footerButtonStyle} onClick={() => setActiveModal('generateReport')}>Generate report</button>
</div>
{/* Modal Popup */}
{activeModal && (
  <Modal title={modalTitles[activeModal]} onClose={() => setActiveModal(null)}>
    {renderModalContent()}
  </Modal>
)}




         
        </div>
      </div>
    
  );
};

export default DashboardPage;
