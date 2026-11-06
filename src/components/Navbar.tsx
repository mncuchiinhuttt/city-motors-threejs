import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Car, Compass, Menu, X } from "lucide-react";

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { to: "/", label: "Trang chủ" },
    { to: "/city-experience", label: "Thành phố 3D", badge: "Live" },
    { to: "/cars", label: "Bộ sưu tập xe" },
    { to: "/about", label: "Showroom & Dịch vụ" }
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm text-slate-800 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo - 60/30/10: 10% Solid Orange Accent */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="w-10 h-10 rounded-xl bg-orange-500 flex items-center justify-center text-white font-bold shadow-md shadow-orange-500/20 group-hover:bg-orange-600 transition-all">
            <Car className="w-5 h-5 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-display font-black text-lg tracking-wider text-slate-900">
                CYBERCITY
              </span>
              <span className="text-[10px] px-1.5 py-0.5 rounded font-mono font-bold bg-orange-50 text-orange-700 border border-orange-200">
                MOTORS
              </span>
            </div>
            <p className="text-[10px] text-slate-500 font-mono tracking-tight -mt-0.5">
              3D AUTOMOTIVE DEALERSHIP
            </p>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 p-1 rounded-full bg-slate-100 border border-slate-200">
          {navLinks.map((link) => {
            const active = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`relative px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                  active
                    ? "text-orange-600 bg-white shadow-sm border border-slate-200 font-bold"
                    : "text-slate-600 hover:text-slate-900 hover:bg-white/60"
                }`}
              >
                {link.label}
                {link.badge && (
                  <span className="ml-1.5 inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Action Controls */}
        <div className="hidden sm:flex items-center gap-3">
          <Link
            to="/city-experience"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-md shadow-orange-500/20 transition-all hover:scale-105"
          >
            <Compass className="w-4 h-4" />
            <span>Khám phá 3D</span>
          </Link>
        </div>

        {/* Mobile menu toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white p-4 space-y-2 shadow-xl">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100 hover:text-orange-600"
            >
              {link.label}
            </Link>
          ))}
          <Link
            to="/city-experience"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-center mt-3 py-2.5 rounded-xl font-bold bg-orange-500 text-white"
          >
            Khám phá thành phố 3D
          </Link>
        </div>
      )}
    </header>
  );
};
