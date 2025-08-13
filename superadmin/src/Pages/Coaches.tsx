 import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import {
  FaUserTie,
  FaLockOpen,
  FaUsers,
  FaLayerGroup,
  FaBuilding,
  FaHashtag,
  FaBullseye,
  FaCog,
  FaTachometerAlt,
  FaBell,
} from 'react-icons/fa';

const CoachesPage: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState('All');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Form fields
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [experience, setExperience] = useState('');
  const [rating, setRating] = useState('');
  const [photo, setPhoto] = useState('');

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
    { to: '/dashboard', label: 'Dashboard', icon: <FaTachometerAlt /> },
    { to: '/players', label: 'Players', icon: <FaUsers /> },
    { to: '/teams', label: 'Teams', icon: <FaLayerGroup /> },
    { to: '/coaches', label: 'Coaches', icon: <FaUserTie /> },
    { to: '/clubs', label: 'Clubs', icon: <FaBuilding /> },
    { to: '/socialmedia', label: 'Social Media', icon: <FaHashtag /> },
    { to: '/balltrack', label: 'Ball Track', icon: <FaBullseye /> },
    { to: '/settings', label: 'Settings', icon: <FaCog /> },
  ];

  const [coachData, setCoachData] = useState([
    { name: 'Bilal Ali', role: 'Batting Coach', experience: '5 Years', rating: 4.7, image: '/coach1.jpg' },
    { name: 'Waisi Khan', role: 'Fitness Coach', experience: '8 Years', rating: 4.4, image: '/coach2.jpg' },
    { name: 'Umer Khan', role: 'Fielding Coach', experience: '5 Years', rating: 4.7, image: '/coach3.jpg' },
    { name: 'Usman', role: 'Fielding Coach', experience: '9 Years', rating: 4.1, image: '/coach4.jpg' },
    { name: 'Hassan', role: 'Bowling Coach', experience: '3 Years', rating: 4.9, image: '/coach5.jpg' },
    { name: 'Mustafa', role: 'Batting Coach', experience: '3 Years', rating: 4.9, image: '/coach7.jpg' },
  ]);

  const filteredCoaches = coachData.filter((coach) => {
    const matchesFilter =
      activeFilter === 'All' || coach.role.toLowerCase().includes(activeFilter.toLowerCase());
    const matchesSearch =
      coach.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      coach.role.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const handleAddCoach = () => {
    const newCoach = {
      name,
      role,
      experience,
      rating: parseFloat(rating),
      image: photo || '/coach-placeholder.jpg',
    };
    setCoachData([...coachData, newCoach]);
    setIsModalOpen(false);
    setName('');
    setRole('');
    setExperience('');
    setRating('');
    setPhoto('');
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
      {/* Sidebar */}
      <div
        style={{
          width: '230px',
          background: '#fff',
          padding: '24px 16px',
          borderRight: '1px solid #ddd',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
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
                  overflow: 'hidden',
                  border: '1px solid #ccc',
                  backgroundColor: '#f0f0f0',
                }}
              >
                <img
                  src={image || '/profile.png'}
                  alt="Profile"
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>
              <input
                id="upload-photo"
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: 'none' }}
              />
            </label>
            <h2 style={{ fontSize: '20px', margin: 0 }}>CricketZone</h2>
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
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px' }}>
        {/* Header */}
        <div
          style={{
            background: '#f5f5f5',
            padding: '12px 20px',
            marginBottom: '20px',
            borderRadius: '12px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>Coaches</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <input
              type="text"
              placeholder="  🔍︎ Search …"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                background: '#f5f5f5',
                padding: '8px 12px',
                borderRadius: '10px',
                border: '1px solid #ccc',
                width: '220px',
              }}
            />
            <FaBell size={20} color="#555" />
          </div>
        </div>

        {/* Filter Tabs + Add Coach */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px',
            flexWrap: 'wrap',
          }}
        >
          <div style={{ display: 'flex', gap: '60px', flexWrap: 'wrap' }}>
            {['All', 'Batting', 'Bowling', 'Fitness', 'Fielding'].map((tab) => (
              <span
                key={tab}
                onClick={() => setActiveFilter(tab)}
                style={{
                  fontWeight: 'bold',
                  fontSize: '19px',
                  color: activeFilter === tab ? '#2d6096' : '#000',
                  cursor: 'pointer',
                  borderBottom: activeFilter === tab ? '2px solid #2d6096' : 'none',
                  paddingBottom: '6px',
                }}
              >
                {tab}
              </span>
            ))}
          </div>

          <button
            onClick={() => setIsModalOpen(true)}
            style={{
              backgroundColor: '#2d6096',
              color: '#fff',
              border: 'none',
              borderRadius: '8px',
              padding: '10px 16px',
              cursor: 'pointer',
              fontSize: '21px',
              fontWeight: 600,
              marginTop: '8px',
            }}
          >
            Add Coach
          </button>
        </div>

        {/* Coach Grid */}
        <div style={{ display: 'flex', justifyContent: 'center' }}></div>
       <div
  style={{
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
      gap: '16px 16px', 
  }}
>

          {filteredCoaches.map((coach, idx) => (
            <div
              key={idx}
               style={{
          background: '#fff',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
          textAlign: 'center',
          position: 'relative',
          width: '500px',
          height: '300px',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
            >
              <img
                src={coach.image}
                alt={coach.name}
                style={{
                  width: '190px',
                  height: '190px',
                  borderRadius: '50%',
                  objectFit: 'cover',
                  marginBottom: '12px',
                  alignSelf: 'center',

                }}
              />
              <h4 style={{ margin: '0', fontSize: '18px', fontWeight: 'bold' }}>{coach.name}</h4>
              <p style={{ margin: '4px 0', fontSize: '15px', color: '#666' }}>{coach.role}</p>
              <p style={{ margin: '4px 0', fontSize: '15px', color: '#555' }}>
                Experience: {coach.experience}
              </p>
              <p style={{ margin: '4px 0', fontSize: '15px', color: '#555' }}>
                Rating: <span style={{ color: '#f4c542' }}>⭐</span> {coach.rating}
              </p>
              <div style={{ position: 'absolute', top: '10px', right: '10px', fontSize: '20px' }}>⋮</div>
            </div>
          ))}
        </div>
      </div>

      {/* Add Coach Modal */}
      {isModalOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100vw',
            height: '100vh',
            background: 'rgba(0, 0, 0, 0.4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 999,
          }}
          onClick={() => setIsModalOpen(false)}
        >
          <div
            style={{
              background: '#fff',
              borderRadius: '12px',
              padding: '24px',
              width: '500px',
              boxShadow: '0 2px 10px rgba(0,0,0,0.3)',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ marginBottom: '20px' }}>Add New Coach</h3>

           <input
  type="text"
  placeholder="Name"
  value={name}
  onChange={(e) => setName(e.target.value)}
  style={inputStyle}
/>

<input
  type="text"
  placeholder="Role (e.g. Bowling Coach)"
  value={role}
  onChange={(e) => setRole(e.target.value)}
  style={inputStyle}
/>

<input
  type="text"
  placeholder="Experience (e.g. 3 Years)"
  value={experience}
  onChange={(e) => setExperience(e.target.value)}
  style={inputStyle}
/>

<input
  type="text"
  placeholder="Rating (e.g. 4.8)"
  value={rating}
  onChange={(e) => setRating(e.target.value)}
  style={inputStyle}
/>

<input
  type="text"
  placeholder="Image URL"
  value={photo}
  onChange={(e) => setPhoto(e.target.value)}
  style={inputStyle}
/>


            <div style={{ display: 'flex', justifyContent: 'space-between', width: '80%', marginTop: '20px' }}>
              <button onClick={() => setIsModalOpen(false)} style={buttonStyle}>Cancel</button>
              <button onClick={handleAddCoach} style={buttonStyle}>Add</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const inputStyle: React.CSSProperties = {
  width: '80%',
  padding: '10px',
  marginBottom: '15px',
  borderRadius: '8px',
  border: '1px solid #ccc',
  fontSize: '16px',
};

const buttonStyle: React.CSSProperties = {
  padding: '10px 20px',
  borderRadius: '8px',
  border: 'none',
  backgroundColor: '#2d6096',
  color: '#fff',
  cursor: 'pointer',
};

export default CoachesPage; 