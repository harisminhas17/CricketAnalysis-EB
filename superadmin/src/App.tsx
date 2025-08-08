
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SplashScreen from './Pages/SplashScreen';
import LoadingScreen from './Pages/LoadingScreen';
import AdminPanel from './Pages/AdminPanel';
import RealTimeScoring from './Pages/RealTimeScoring';
import Signinn from './Pages/Signinn';
import Signup from "./Pages/Signup";
import ForgotPassword from "./Pages/ForgotPassword";
import Verification from "./Pages/Verification";
import Dashboard from "./Pages/Dashboard";
import ResetPassword from "./Pages/ResetPassword";
import Signup2 from "./Pages/Signup2";
import Players from "./Pages/Players";
import Teams from "./Pages/Teams";
import Coaches from "./Pages/Coaches";
import Clubs from "./Pages/Clubs";
import SocialMedia from "./Pages/SocialMedia";
import Settings from "./Pages/Settings";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SplashScreen />} />
        <Route path="/splash" element={<SplashScreen />} />
        <Route path="/loading" element={<LoadingScreen />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/scoring" element={<RealTimeScoring />} />
        <Route path="/signinn" element={<Signinn />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/Verification" element={<Verification />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/ResetPassword" element={<ResetPassword />} />
        <Route path="/Signup2" element={<Signup2/>} />
        <Route path="/Players" element={<Players/>} />
        <Route path="/Teams" element={<Teams/>} />
        <Route path="/Coaches" element={<Coaches/>} />
        <Route path="/Clubs" element={<Clubs/>} />
        <Route path="/SocialMedia" element={<SocialMedia/>} />
        <Route path="/Settings" element={<Settings/>} />
      </Routes>
    </Router>
  );
};

export default App;
