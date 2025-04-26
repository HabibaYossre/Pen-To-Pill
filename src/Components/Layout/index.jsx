import React from 'react';
import VerticalMenu from '../Menu';
import Header from '../Header';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <div className="flex h-screen">
          <Header />
          <Outlet />
              </div>
  );
};

export default Layout;
