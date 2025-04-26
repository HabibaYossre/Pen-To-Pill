import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 px-6 py-4 bg-gradient-to-r">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-amber-700">
          <h3 className="text-2xl font-serif">P2P</h3>
          <small className="text-sm">Pen to Pill</small>
        </div>
        
        <div className="hidden lg:block">
          <ul className="flex space-x-6 text-white">
            <li><Link to="/" className="hover:text-amber-700">HOME</Link></li>
            <li><Link to="/About-us" className="hover:text-amber-700">ABOUT US</Link></li>
            <li><Link to="/Add-Prescription" className="hover:text-amber-700">VIEW MY SCHEDULE</Link></li>  
            <li><Link to="/Add-Prescription" className="hover:text-amber-700">ADD PRESCRIPTION</Link></li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;