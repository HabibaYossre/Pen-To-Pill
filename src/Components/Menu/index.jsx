import React, { useState } from 'react';
import { FaBars, FaTimes } from 'react-icons/fa'; // Importing icons from react-icons

const VerticalMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex">
      {/* Menu */}
      <div
        className={`fixed top-0 left-0 h-full bg-gray-800 text-white transition-all duration-300 ease-in-out ${isOpen ? 'w-64' : 'w-16'} p-4`}
      >
        {/* Hamburger Icon */}
        <div
          className="text-white cursor-pointer absolute top-4 left-4"
          onClick={toggleMenu}
        >
          {isOpen ? (
            <FaTimes size={24} /> // Close icon when the menu is open
          ) : (
            <FaBars size={24} /> // Hamburger icon when the menu is closed
          )}
        </div>

        {/* Menu Items */}
        <div className="mt-12 space-y-4">
          <a href="#" className="block p-2 hover:bg-gray-700 rounded">Home</a>
          <a href="#" className="block p-2 hover:bg-gray-700 rounded">My Schedule</a>
          <a href="#" className="block p-2 hover:bg-gray-700 rounded">Add New Prescription</a>
        </div>
      </div>
    </div>
  );
};

export default VerticalMenu;
