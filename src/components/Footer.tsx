import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Car, MapPin, Phone, Mail, ArrowUpRight, Sparkles, Clock, Globe, ShieldCheck } from "lucide-react";

export const Footer: React.FC = () => {
  const [localTime, setLocalTime] = useState<string>("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setLocalTime(
        now.toLocaleTimeString("vi-VN", {
          timeZone: "Asia/Ho_Chi_Minh",
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit"
        })
      );
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <footer className="relative bg-slate-950 border-t border-slate-900 text-slate-400 text-xs overflow-hidden">
      {/* Subtle Ambient Glow and Grid Lines */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Main Container */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-12">
        {/* Top Pre-footer CTA Header (Awwwards style) */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between pb-16 border-b border-slate-800/80 gap-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 font-mono text-[11px] font-bold tracking-wider uppercase mb-4">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Sẵn sàng cho cuộc hành trình mới</span>
            </div>
            <h2 className="text-3xl sm:text-5xl font-black font-display text-white tracking-tight leading-tight">
              TRẢI NGHIỆM ĐẲNG CẤP <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-indigo-400">
                LÁI THỬ TRỰC TIẾP
              </span>
            </h2>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
            <Link
              to="/city-experience"
              className="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-2xl font-bold text-xs bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-xl shadow-cyan-500/20 transition-all hover:scale-105"
            >
              <span>Vào thành phố 3D</span>
              <ArrowUpRight className="w-4 h-4" />
            </Link>
            <Link
              to="/cars"
              className="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-2xl font-semibold text-xs bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 transition-all"
            >
              <span>Xem danh sách xe</span>
              <ArrowUpRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* 4-Column Navigation & Info */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-10 py-16 border-b border-slate-900">
          {/* Brand Info & Live Time */}
          <div className="lg:col-span-4 space-y-5">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-slate-950 font-bold shadow-lg shadow-cyan-500/25">
                <Car className="w-5 h-5 font-bold" />
              </div>
              <div>
                <span className="font-display font-black text-lg text-white tracking-wider">CYBERCITY</span>
                <span className="text-xs ml-1.5 px-1.5 py-0.5 rounded font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  MOTORS
                </span>
              </div>
            </div>

            <p className="text-slate-400 text-xs font-light leading-relaxed max-w-sm">
              Nền tảng đại lý xe hơi thế hệ mới, kết hợp trải nghiệm đồ họa 3D tương tác trên WebGL và hệ thống phân phối xe điện, xe sang chính hãng.
            </p>

            {/* Live Showroom Status & Time */}
            <div className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800/80 space-y-2 max-w-xs">
              <div className="flex items-center justify-between text-[11px]">
                <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                  <span>Showroom Đang Mở Cửa</span>
                </span>
                <span className="text-slate-500 font-mono">08:00 - 21:00</span>
              </div>
              <div className="flex items-center justify-between text-[11px] pt-1.5 border-t border-slate-800/60">
                <span className="flex items-center gap-1 text-slate-400 font-mono">
                  <Clock className="w-3 h-3 text-cyan-400" />
                  <span>GIỜ TP. HỒ CHÍ MINH:</span>
                </span>
                <span className="text-cyan-300 font-mono font-bold">{localTime || "12:00:00"}</span>
              </div>
            </div>
          </div>

          {/* Column 2: Navigation */}
          <div className="lg:col-span-2 space-y-3">
            <h4 className="font-mono text-xs uppercase font-bold tracking-wider text-slate-200">HỆ THỐNG</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/" className="hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  Trang chủ
                </Link>
              </li>
              <li>
                <Link to="/city-experience" className="hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  Thành phố 3D <span className="text-[10px] text-cyan-400 font-mono font-bold bg-cyan-500/10 px-1 rounded">Live</span>
                </Link>
              </li>
              <li>
                <Link to="/cars" className="hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  Bảng giá xe 2026
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-cyan-400 transition-colors inline-flex items-center gap-1">
                  Showroom & Công nghệ
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Models */}
          <div className="lg:col-span-3 space-y-3">
            <h4 className="font-mono text-xs uppercase font-bold tracking-wider text-slate-200">DÒNG XE CHỦ LỰC</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/cars/apex-gt90" className="hover:text-cyan-400 transition-colors flex items-center justify-between pr-4">
                  <span>Apex GT-90 (Super Coupe)</span>
                  <span className="font-mono text-[10px] text-slate-500">650 HP</span>
                </Link>
              </li>
              <li>
                <Link to="/cars/horizon-metro" className="hover:text-cyan-400 transition-colors flex items-center justify-between pr-4">
                  <span>Horizon Metro (Sedan)</span>
                  <span className="font-mono text-[10px] text-slate-500">240 HP</span>
                </Link>
              </li>
              <li>
                <Link to="/cars/cybercab-pro" className="hover:text-cyan-400 transition-colors flex items-center justify-between pr-4">
                  <span>CyberCab Pro (Taxi điện)</span>
                  <span className="font-mono text-[10px] text-slate-500">210 HP</span>
                </Link>
              </li>
              <li>
                <Link to="/cars/titan-cargo-van" className="hover:text-cyan-400 transition-colors flex items-center justify-between pr-4">
                  <span>Titan Cargo Van</span>
                  <span className="font-mono text-[10px] text-slate-500">320 HP</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Location & Cloudflare Badge */}
          <div className="lg:col-span-3 space-y-3">
            <h4 className="font-mono text-xs uppercase font-bold tracking-wider text-slate-200">ĐỊA ĐIỂM & HẠ TẦNG</h4>
            <div className="space-y-2.5 text-xs text-slate-400">
              <p className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                <span>Khu Đô Thị Công Nghệ Cao, TP. Thủ Đức, TP. Hồ Chí Minh</span>
              </p>
              <p className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>1900 888 999 • (028) 7777 9999</span>
              </p>
              <p className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-cyan-400 shrink-0" />
                <span>contact@cybercity-motors.vn</span>
              </p>
              <div className="pt-2 text-[10px] font-mono text-slate-500">
                <span>TỌA ĐỘ: 10°51'20"N 106°48'05"E</span>
              </div>
            </div>
          </div>
        </div>

        {/* Giant Artistic Background Watermark (Awwwards Style) */}
        <div className="relative py-10 select-none pointer-events-none text-center overflow-hidden">
          <span className="text-[12vw] font-black font-display tracking-widest text-slate-900/30 block leading-none">
            CYBERCITY
          </span>
        </div>

        {/* Bottom Bar: Copyright & Platform Status */}
        <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
          <div className="flex items-center gap-2">
            <Globe className="w-3.5 h-3.5 text-cyan-400" />
            <span>© 2026 CyberCity Motors. Vận hành trên Cloudflare Workers Edge Network & Three.js.</span>
          </div>

          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-emerald-400 font-mono">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Edge 99.99% Uptime</span>
            </span>
            <span className="hover:text-slate-400 cursor-pointer">Bảo mật</span>
            <span className="hover:text-slate-400 cursor-pointer">Điều khoản</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
