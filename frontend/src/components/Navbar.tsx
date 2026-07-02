import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/dashboard" className="text-xl font-bold">
              DocMind
            </Link>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link to="/dashboard" className="hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/documents" className="hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Documents
                </Link>
                <Link to="/conversations" className="hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Conversations
                </Link>
                <Link to="/ai" className="hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  AI
                </Link>
                <Link to="/clients" className="hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                  Clients
                </Link>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            {user ? (
              <button onClick={handleLogout} className="bg-red-600 hover:bg-red-700 px-3 py-2 rounded-md text-sm font-medium">
                Logout
              </button>
            ) : null}
          </div>
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
            >
              <span className="sr-only">Open main menu</span>
              <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={isMobileMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'} />
              </svg>
            </button>
          </div>
        </div>
      </div>
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link to="/dashboard" className="hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Dashboard
            </Link>
            <Link to="/documents" className="hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Documents
            </Link>
            <Link to="/conversations" className="hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Conversations
            </Link>
            <Link to="/ai" className="hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              AI
            </Link>
            <Link to="/clients" className="hover:bg-gray-700 block px-3 py-2 rounded-md text-base font-medium">
              Clients
            </Link>
            {user ? (
              <button onClick={handleLogout} className="w-full text-left bg-red-600 hover:bg-red-700 px-3 py-2 rounded-md text-base font-medium">
                Logout
              </button>
            ) : null}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;