import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react'; // Lucide or Heroicons for icons


const Header = () => {
  const location = useLocation();
  const currentPath = location.pathname;
  const [menuOpen, setMenuOpen] = useState(false);

  
  const isHome = currentPath === '/';

  const linkClasses = (path) =>
    currentPath === path
      ? `${isHome ? 'text-indigo-400' : 'text-black'} font-semibold`
      : `${isHome ? 'text-white' : 'text-black'} hover:text-indigo-500`;

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <nav className={`fixed top-0 left-0 w-full z-50 px-6 py-4 shadow transition-colors duration-300 ${isHome ? 'bg-transparent' : 'bg-white'}`}>
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <div className="text-indigo-600">
          <h3 className="text-2xl font-serif">P2P</h3>
          <small className="text-sm">Pen to Pill</small>
        </div>

        {/* Desktop Nav */}
        <div className="hidden lg:block">
          <ul className="flex space-x-6">
            <li><Link to="/" className={linkClasses('/')}>HOME</Link></li>
            <li><Link to="/About-us" className={linkClasses('/About-us')}>ABOUT US</Link></li>
            <li><Link to="/View-Schedule" className={linkClasses('/View-Schedule')}>VIEW MY SCHEDULE</Link></li>
            <li><Link to="/Add-Prescription" className={linkClasses('/Add-Prescription')}>ADD PRESCRIPTION</Link></li>
          </ul>
        </div>

        {/* Mobile Menu Icon */}
        <div className="lg:hidden">
          <button onClick={toggleMenu} className="text-indigo-700">
            {menuOpen ? <X size={28} /> : <Menu size={28} />}
          </button>
        </div>
      </div>

      {/* Mobile Nav Links */}
      {menuOpen && (
        <div className="lg:hidden mt-4 px-6">
          <ul className="flex flex-col space-y-4 bg-slate-300 rounded shadow p-4">
            <li><Link to="/" className={linkClasses('/')} onClick={toggleMenu}>HOME</Link></li>
            <li><Link to="/About-us" className={linkClasses('/About-us')} onClick={toggleMenu}>ABOUT US</Link></li>
            <li><Link to="/View-Schedule" className={linkClasses('/View-Schedule')} onClick={toggleMenu}>VIEW MY SCHEDULE</Link></li>
            <li><Link to="/Add-Prescription" className={linkClasses('/Add-Prescription')} onClick={toggleMenu}>ADD PRESCRIPTION</Link></li>
          </ul>
        </div>
      )}
    </nav>
  );
};

export default Header;
