import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Car, Compass, Sun, Moon, Menu, X, ArrowUpRight } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();

  const isDark = theme === "dark";

  const navLinks = [
    { to: "/", label: "Trang chủ" },
    { to: "/city-experience", label: "Thành phố 3D", badge: "Live" },
    { to: "/cars", label: "Bộ sưu tập xe" },
    { to: "/about", label: "Showroom & Dịch vụ" }
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-40 backdrop-blur-xl transition-colors duration-300 ${
        isDark
          ? "bg-slate-950/80 border-b border-slate-800/80 text-slate-100"
          : "bg-white/85 border-b border-slate-200/90 text-slate-800 shadow-sm"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div
            className={`w-10 h-10 rounded-xl flex items-center justify-center font-bold shadow-md transition-transform group-hover:scale-105 ${
              isDark
                ? "bg-gradient-to-br from-cyan-500 to-blue-600 text-slate-950 shadow-cyan-500/20"
                : "bg-blue-600 text-white shadow-blue-600/20"
            }`}
          >
            <Car className="w-5 h-5 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className={`font-display font-black text-lg tracking-wider ${isDark ? "text-white" : "text-slate-900"}`}>
                CYBERCITY
              </span>
              <span
                className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold border ${
                  isDark
                    ? "bg-cyan-500/10 text-cyan-400 border-cyan-500/20"
                    : "bg-blue-50 text-blue-700 border-blue-200"
                }`}
              >
                MOTORS
              </span>
            </div>
            <p className={`text-[10px] font-mono tracking-tight -mt-0.5 ${isDark ? "text-slate-400" : "text-slate-500"}`}>
              3D AUTOMOTIVE DEALERSHIP
            </p>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav
          className={`hidden md:flex items-center gap-1 p-1.5 rounded-full border transition-colors ${
            isDark
              ? "bg-slate-900/60 border-slate-800/80"
              : "bg-slate-100/80 border-slate-200/80 shadow-inner"
          }`}
        >
          {navLinks.map((link) => {
            const active = location.pathname === link.to;
            return (
              <Link
                key={link.to}
                to={link.to}
                className={`relative px-4 py-1.5 rounded-full text-xs font-semibold transition-all ${
                  active
                    ? isDark
                      ? "text-cyan-300 bg-slate-800 shadow-sm border border-cyan-500/30 font-bold"
                      : "text-blue-700 bg-white shadow-sm border border-slate-200/80 font-bold"
                    : isDark
                    ? "text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
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

        {/* Action Controls: Theme Switcher & 3D Explore CTA */}
        <div className="hidden sm:flex items-center gap-3">
          {/* Light / Dark Mode Toggle */}
          <button
            onClick={toggleTheme}
            className={`p-2.5 rounded-xl border transition-all ${
              isDark
                ? "bg-slate-900 text-amber-400 border-slate-800 hover:bg-slate-800"
                : "bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200/80"
            }`}
            title={isDark ? "Chuyển sang giao diện Sáng (Light Mode)" : "Chuyển sang giao diện Tối (Dark Mode)"}
            aria-label="Toggle theme"
          >
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          <Link
            to="/city-experience"
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold shadow-md transition-all hover:scale-105 ${
              isDark
                ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 hover:brightness-110 shadow-cyan-500/20"
                : "bg-blue-600 hover:bg-blue-700 text-white shadow-blue-600/20"
            }`}
          >
            <Compass className="w-4 h-4" />
            <span>Khám phá 3D</span>
          </Link>
        </div>

        {/* Mobile menu toggle */}
        <div className="flex md:hidden items-center gap-2">
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-lg border ${
              isDark ? "bg-slate-900 text-amber-400 border-slate-800" : "bg-slate-100 text-slate-700 border-slate-200"
            }`}
          >
            {isDark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className={`p-2 rounded-lg ${isDark ? "text-slate-400 hover:text-white" : "text-slate-600 hover:text-slate-900"}`}
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div
          className={`md:hidden border-b p-4 space-y-2 ${
            isDark ? "bg-slate-950/95 border-slate-800 text-slate-200" : "bg-white/95 border-slate-200 text-slate-800 shadow-xl"
          }`}
        >
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setMobileMenuOpen(false)}
              className={`block px-3 py-2 rounded-lg text-sm font-medium ${
                isDark ? "hover:bg-slate-800 hover:text-cyan-400" : "hover:bg-slate-100 hover:text-blue-600"
              }`}
            >
              {link.label}
            </Link>
          ))}
          <Link
            to="/city-experience"
            onClick={() => setMobileMenuOpen(false)}
            className={`block text-center mt-3 py-2.5 rounded-xl font-bold ${
              isDark ? "bg-cyan-500 text-slate-950" : "bg-blue-600 text-white"
            }`}
          >
            Khám phá thành phố 3D
          </Link>
        </div>
      )}
    </header>
  );
};
