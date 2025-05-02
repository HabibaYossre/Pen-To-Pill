import React from 'react';
import { FaPhone, FaLanguage, FaCamera } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import '../Home/styles.css'; 
import PrescriptionTracker from '../PrescriptionTracker';
const Home = () => {
  return (
    <div className="App">
      {/* Header with dark background that spans the full width */}
      <header className="relative h-screen w-full bg-gray-900">

        {/* Hero Section with background image defined in CSS */}
        <div className="hero-section relative h-full w-full flex items-center justify-center">
          {/* Dark overlay */}
          <div className="absolute inset-0 bg-black opacity-80"></div>
          
          {/* Content */}
          <div className="relative z-10 text-center px-4">
            
            <h6 className="text-5xl md:text-6xl lg:text-7xl text-white font-light tracking-wider leading-tight">Pen-to-Pill</h6>
            
            <h1 className="text-white  mb-6 tracking-widest">
            Your Pill Planner,
            Your Health Partner
            </h1>
            
          </div>          
        </div>
      </header>
    </div>
  );
}

export default Home;