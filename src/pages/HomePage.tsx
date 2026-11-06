import React, { useState } from "react";
import { Link } from "react-router-dom";
import { CityCanvas, ExtendedCameraMode } from "../components/CityCanvas";
import { CornerSceneController } from "../components/CornerSceneController";
import { CarCard } from "../components/CarCard";
import { CARS_DATA } from "../data/cars";
import { TimeOfDay } from "../types";
import { useTheme } from "../context/ThemeContext";
import {
  ArrowRight,
  Compass,
  Shield,
  Zap,
  Sparkles,
  ChevronDown,
  ChevronRight,
  Gauge,
  Cpu,
  Layers,
  BatteryCharging,
  Eye,
  Radio,
  CheckCircle2,
  Quote,
  Video,
  Mountain
} from "lucide-react";

export const HomePage: React.FC = () => {
  const [timeOfDay, setTimeOfDay] = useState<TimeOfDay>("cyberpunk");
  const [cameraPreset, setCameraPreset] = useState<ExtendedCameraMode>("chase");
  const [activeCarId, setActiveCarId] = useState<string>("Car_BlueCoupe");
  const [trafficSpeed, setTrafficSpeed] = useState<number>(1.0);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [customColor, setCustomColor] = useState<{ carId: string; colorHex: string } | undefined>(undefined);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const { theme } = useTheme();
  const isDark = theme === "dark";

  const filteredCars = CARS_DATA.filter(
    (car) => selectedCategory === "all" || car.category === selectedCategory
  );

  return (
    <div className={`pt-16 min-h-screen transition-colors duration-300 ${isDark ? "bg-slate-950 text-slate-100" : "bg-slate-50 text-slate-800"}`}>
      {/* =========================================================================
          HERO SECTION: 3D CITY & MOUNTAIN WITH CHASE CAMERA & ENDLESS DRIVE
          ========================================================================= */}
      <section className="relative w-full h-[90vh] min-h-[620px] bg-slate-950 overflow-hidden">
        {/* Three.js Canvas Container */}
        <div className="absolute inset-0 z-0">
          <CityCanvas
            timeOfDay={timeOfDay}
            cameraPreset={cameraPreset}
            activeCarId={activeCarId}
            onSelectCar={(id) => {
              setActiveCarId(id);
              setCameraPreset("chase");
            }}
            trafficSpeed={trafficSpeed}
            isPaused={isPaused}
            customCarColor={customColor}
          />
        </div>

        {/* Cinematic Vignettes */}
        <div
          className={`absolute inset-0 pointer-events-none z-10 transition-colors ${
            isDark
              ? "bg-gradient-to-t from-slate-950 via-transparent to-slate-950/60"
              : "bg-gradient-to-t from-slate-50/90 via-transparent to-slate-900/40"
          }`}
        />
        <div className="absolute inset-0 pointer-events-none bg-gradient-to-r from-slate-950/90 via-slate-950/30 to-transparent z-10 max-w-2xl" />

        {/* Hero Overlay Content */}
        <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-between py-10 pointer-events-none">
          <div className="max-w-xl pt-6 space-y-4">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900/80 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-semibold pointer-events-auto backdrop-blur-xl shadow-lg shadow-cyan-500/10">
              <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
              <span>ĐÔ THỊ & ĐÈO NÚI 3D • CHASE CAM • XE CHẠY VÔ TẬN</span>
            </div>

            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-black font-display tracking-tight text-white leading-[0.95]">
              ĐÔ THỊ & <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-400 to-indigo-400">
                CUNG ĐƯỜNG NÚI.
              </span>
            </h1>

            <p className="text-sm sm:text-base text-slate-200 leading-relaxed font-light">
              Mô phỏng xe ô tô lướt đi vô tận từ các tòa nhà chọc trời qua cung đường đèo núi hiểm trở. Camera bám đuôi tự động với tính năng chuyển cảnh Ngày, Đêm, Hoàng hôn linh hoạt.
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-3 pointer-events-auto">
              <Link
                to="/city-experience"
                className="flex items-center gap-2 px-6 py-3.5 rounded-2xl font-bold text-xs bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-xl shadow-cyan-500/25 transition-all hover:scale-105"
              >
                <Compass className="w-4 h-4" />
                <span>Trải nghiệm toàn màn hình</span>
              </Link>
              <button
                onClick={() => setCameraPreset(cameraPreset === "chase" ? "mountain" : "chase")}
                className="flex items-center gap-2 px-5 py-3.5 rounded-2xl font-semibold text-xs bg-slate-900/85 hover:bg-slate-800 text-slate-200 border border-slate-700/80 backdrop-blur-md transition-all"
              >
                {cameraPreset === "chase" ? <Mountain className="w-4 h-4 text-cyan-400" /> : <Video className="w-4 h-4 text-cyan-400" />}
                <span>{cameraPreset === "chase" ? "Xem cung đường núi" : "Camera bám đuôi xe"}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-3 left-1/2 -translate-x-1/2 z-20 pointer-events-none flex flex-col items-center gap-1 opacity-70">
          <span className="text-[10px] font-mono tracking-widest uppercase text-slate-400">CUỘN XUỐNG KHÁM PHÁ</span>
          <ChevronDown className="w-4 h-4 text-cyan-400 animate-bounce" />
        </div>

        {/* Floating Corner Scene Controller ("Khúc ở góc để đổi") */}
        <CornerSceneController
          timeOfDay={timeOfDay}
          onTimeChange={setTimeOfDay}
          cameraPreset={cameraPreset}
          onCameraChange={setCameraPreset}
          activeCarId={activeCarId}
          onCarChange={setActiveCarId}
          trafficSpeed={trafficSpeed}
          onSpeedChange={setTrafficSpeed}
          isPaused={isPaused}
          onTogglePause={() => setIsPaused(!isPaused)}
        />
      </section>

      {/* =========================================================================
          SECTION 1: BENTO GRID INNOVATION (AWWWARDS / MOBBIN STYLE)
          ========================================================================= */}
      <section
        id="bento-innovation"
        className={`py-24 relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 transition-colors ${
          isDark ? "text-slate-100" : "text-slate-800"
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-cyan-500 dark:text-cyan-400 text-xs font-mono font-bold uppercase tracking-wider mb-3">
              <span className="text-slate-400">//</span>
              <span>01 • NGHỆ THUẬT CƠ KHÍ & ĐIỆN TỬ</span>
            </div>
            <h2 className={`text-3xl sm:text-5xl font-black font-display tracking-tight ${isDark ? "text-white" : "text-slate-900"}`}>
              ĐỈNH CAO KỸ NGHỆ ĐÔ THỊ
            </h2>
          </div>
          <p className={`text-xs sm:text-sm max-w-md font-light leading-relaxed ${isDark ? "text-slate-400" : "text-slate-600"}`}>
            Mỗi chi tiết đều được tối ưu hóa từ phần mềm dựng hình 3D Blender đến hệ thống pin và khung gầm thực tế, mang lại trải nghiệm lái êm ái tuyệt đối.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Bento Card 1: Power & Acceleration */}
          <div
            className={`md:col-span-8 group relative rounded-3xl p-8 sm:p-10 backdrop-blur-xl border transition-all duration-300 overflow-hidden flex flex-col justify-between ${
              isDark
                ? "bg-slate-900/40 hover:bg-slate-900/70 border-slate-800/80 hover:border-cyan-500/40 shadow-xl"
                : "bg-white border-slate-200/90 hover:border-blue-400 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
            }`}
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-500 dark:text-cyan-400 flex items-center justify-center font-bold">
                <Zap className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-cyan-500 dark:text-cyan-400 font-bold block">
                HỆ TRUYỀN ĐỘNG DUAL-MOTOR
              </span>
              <h3 className={`text-2xl sm:text-3xl font-bold font-display leading-tight ${isDark ? "text-white" : "text-slate-900"}`}>
                650 Mã Lực • Bứt Tốc 0-100 km/h Trong 2.8 Giây
              </h3>
              <p className={`text-xs sm:text-sm font-light leading-relaxed max-w-xl ${isDark ? "text-slate-400" : "text-slate-600"}`}>
                Động cơ nam châm vĩnh cửu kép phân bổ mô-men xoắn tức thời lên từng bánh xe độc lập. Hệ thống kiểm soát lực kéo thông minh đảm bảo xe bám chặt mặt đường kể cả khi vào cua ở tốc độ cao trong mưa đêm.
              </p>
            </div>

            <div className={`grid grid-cols-3 gap-4 pt-8 mt-6 border-t ${isDark ? "border-slate-800/80" : "border-slate-200"}`}>
              <div>
                <span className="text-[11px] text-slate-400 font-mono">MÔ-MEN XOẮN</span>
                <p className={`text-2xl font-bold font-mono mt-0.5 ${isDark ? "text-white" : "text-slate-900"}`}>850 Nm</p>
              </div>
              <div className={`border-x px-4 ${isDark ? "border-slate-800/80" : "border-slate-200"}`}>
                <span className="text-[11px] text-slate-400 font-mono">HIỆU SUẤT PIN</span>
                <p className="text-2xl font-bold font-mono text-cyan-500 dark:text-cyan-400 mt-0.5">97.2%</p>
              </div>
              <div>
                <span className="text-[11px] text-slate-400 font-mono">TRỌNG TÂM THẤP</span>
                <p className="text-2xl font-bold font-mono text-emerald-500 dark:text-emerald-400 mt-0.5">420 mm</p>
              </div>
            </div>
          </div>

          {/* Bento Card 2: 800V Ultra-Fast Charging */}
          <div
            className={`md:col-span-4 group relative rounded-3xl p-8 backdrop-blur-xl border transition-all duration-300 flex flex-col justify-between overflow-hidden ${
              isDark
                ? "bg-slate-900/40 hover:bg-slate-900/70 border-slate-800/80 hover:border-cyan-500/40 shadow-xl"
                : "bg-white border-slate-200/90 hover:border-amber-400 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
            }`}
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-500 dark:text-amber-400 flex items-center justify-center font-bold">
                <BatteryCharging className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-amber-500 dark:text-amber-400 font-bold block">
                KIẾN TRÚC ĐIỆN ÁP 800V
              </span>
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${isDark ? "text-white" : "text-slate-900"}`}>
                Sạc 18 Phút • Chạy Thêm 400 Km
              </h3>
              <p className={`text-xs font-light leading-relaxed ${isDark ? "text-slate-400" : "text-slate-600"}`}>
                Tương thích trạm sạc siêu tốc DC công suất 350kW. Hệ thống làm mát pin bằng chất lỏng kiểm soát nhiệt độ tế bào pin luôn ở trạng thái lý tưởng.
              </p>
            </div>

            <div className={`pt-6 mt-4 border-t flex items-center justify-between text-xs font-mono ${isDark ? "border-slate-800/80" : "border-slate-200"}`}>
              <span className="text-slate-400">CHU KỲ SẠC:</span>
              <span className="text-amber-500 dark:text-amber-300 font-bold">5.000+ LẦN (BẢO HÀNH 8 NĂM)</span>
            </div>
          </div>

          {/* Bento Card 3: Autonomous Driving & Radar */}
          <div
            className={`md:col-span-4 group relative rounded-3xl p-8 backdrop-blur-xl border transition-all duration-300 flex flex-col justify-between overflow-hidden ${
              isDark
                ? "bg-slate-900/40 hover:bg-slate-900/70 border-slate-800/80 hover:border-cyan-500/40 shadow-xl"
                : "bg-white border-slate-200/90 hover:border-indigo-400 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
            }`}
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-500 dark:text-indigo-400 flex items-center justify-center font-bold">
                <Radio className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-indigo-500 dark:text-indigo-400 font-bold block">
                RADAR LIDAR 360° & AI
              </span>
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${isDark ? "text-white" : "text-slate-900"}`}>
                Tự Hành Cấp Độ 3 Trong Đô Thị
              </h3>
              <p className={`text-xs font-light leading-relaxed ${isDark ? "text-slate-400" : "text-slate-600"}`}>
                Quét 2.000.000 điểm mỗi giây giúp nhận diện người đi bộ, vật cản và tín hiệu đèn giao thông trong mọi điều kiện sương mù hay mưa rào.
              </p>
            </div>

            <div className={`pt-6 mt-4 border-t flex items-center justify-between text-xs font-mono ${isDark ? "border-slate-800/80" : "border-slate-200"}`}>
              <span className="text-slate-400">ĐỘ TRỄ PHẢN ỨNG:</span>
              <span className="text-indigo-500 dark:text-indigo-300 font-bold">&lt; 15 MILLISECONDS</span>
            </div>
          </div>

          {/* Bento Card 4: Lightweight Carbon Monocoque */}
          <div
            className={`md:col-span-8 group relative rounded-3xl p-8 sm:p-10 backdrop-blur-xl border transition-all duration-300 flex flex-col justify-between overflow-hidden ${
              isDark
                ? "bg-slate-900/40 hover:bg-slate-900/70 border-slate-800/80 hover:border-cyan-500/40 shadow-xl"
                : "bg-white border-slate-200/90 hover:border-emerald-400 shadow-[0_8px_30px_rgb(0,0,0,0.04)]"
            }`}
          >
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 dark:text-emerald-400 flex items-center justify-center font-bold">
                <Layers className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-emerald-500 dark:text-emerald-400 font-bold block">
                KHUNG GẦM NGUYÊN KHỐI
              </span>
              <h3 className={`text-2xl sm:text-3xl font-bold font-display ${isDark ? "text-white" : "text-slate-900"}`}>
                Hợp Kim Nhôm Hàng Không & Sợi Carbon Đúc
              </h3>
              <p className={`text-xs sm:text-sm font-light leading-relaxed max-w-xl ${isDark ? "text-slate-400" : "text-slate-600"}`}>
                Cấu trúc lồng an toàn bảo vệ khoang hành khách với độ cứng xoắn 45.000 Nm/độ. Giảm 25% trọng lượng thân xe giúp kéo dài quãng đường di chuyển và tăng độ nhạy phản hồi vô-lăng.
              </p>
            </div>

            <div className={`grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8 mt-6 border-t text-xs font-mono ${isDark ? "border-slate-800/80" : "border-slate-200"}`}>
              <div>
                <span className="text-slate-400">ĐẠT CHUẨN</span>
                <p className={`font-bold mt-0.5 ${isDark ? "text-slate-200" : "text-slate-800"}`}>EURO NCAP 5 SAO</p>
              </div>
              <div>
                <span className="text-slate-400">HỆ SỐ CẢN GIÓ</span>
                <p className="text-cyan-500 dark:text-cyan-400 font-bold mt-0.5">Cd = 0.21</p>
              </div>
              <div>
                <span className="text-slate-400">TỈ LỆ TRỌNG LƯỢNG</span>
                <p className="text-emerald-500 dark:text-emerald-400 font-bold mt-0.5">50 : 50 HOÀN HẢO</p>
              </div>
              <div>
                <span className="text-slate-400">CÁCH ÂM</span>
                <p className={`font-bold mt-0.5 ${isDark ? "text-slate-200" : "text-slate-800"}`}>KÍNH 2 LỚP CHỦ ĐỘNG</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 2: EDITORIAL NARRATIVE WITH EMBEDDED INLINE ICONS
          ========================================================================= */}
      <section
        className={`py-24 border-y transition-colors ${
          isDark
            ? "bg-gradient-to-b from-slate-950 via-slate-900/60 to-slate-950 border-slate-800/80"
            : "bg-gradient-to-b from-slate-100/70 via-white to-slate-100/70 border-slate-200"
        }`}
      >
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
          <div className="flex items-center gap-3 text-cyan-500 dark:text-cyan-400 text-xs font-mono font-bold uppercase tracking-widest">
            <span className="w-8 h-px bg-cyan-400" />
            <span>02 • TRIẾT LÝ VẬN HÀNH VỀ ĐÊM</span>
          </div>

          <div className="relative">
            <Quote className="w-16 h-16 text-cyan-500/10 absolute -top-8 -left-8 pointer-events-none" />
            <h3 className={`text-2xl sm:text-4xl lg:text-5xl font-black font-display tracking-tight leading-snug ${isDark ? "text-white" : "text-slate-900"}`}>
              “Khi thành phố lên đèn, con đường không còn là lối đi đơn thuần — đó là sàn diễn của ánh sáng, năng lượng và tốc độ thuần khiết.”
            </h3>
          </div>

          {/* Editorial Paragraphs with Woven Icon Badges */}
          <div className={`grid grid-cols-1 md:grid-cols-2 gap-10 text-sm sm:text-base font-light leading-relaxed ${isDark ? "text-slate-300" : "text-slate-600"}`}>
            <p>
              Được thiết kế để chinh phục cả những khúc cua đô thị lẫn cung đường đèo núi hiểm trở, chiếc xe sở hữu cụm đèn chiếu sáng{" "}
              <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 shadow-sm ${
                isDark ? "bg-cyan-500/10 text-cyan-300 border border-cyan-500/30" : "bg-cyan-50 text-cyan-700 border border-cyan-200"
              }`}>
                <Eye className="w-3 h-3 text-cyan-500" /> LED Matrix Thấu Kính
              </span>{" "}
              với khả năng tự động cắt luồng sáng chống lóa. Khi kim đồng hồ điểm quá nửa đêm, hệ thống động cơ điện kép{" "}
              <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 shadow-sm ${
                isDark ? "bg-amber-500/10 text-amber-300 border border-amber-500/30" : "bg-amber-50 text-amber-700 border border-amber-200"
              }`}>
                <Zap className="w-3 h-3 text-amber-500" /> 650 Mã Lực
              </span>{" "}
              vẫn vận hành trong sự tĩnh lặng tuyệt đối, biến mỗi chuyến đi dạo phố thành một trải nghiệm thiền định cơ khí.
            </p>

            <p>
              Khung gầm liền khối kết hợp pin thế hệ mới{" "}
              <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 shadow-sm ${
                isDark ? "bg-emerald-500/10 text-emerald-300 border border-emerald-500/30" : "bg-emerald-50 text-emerald-700 border border-emerald-200"
              }`}>
                <BatteryCharging className="w-3 h-3 text-emerald-500" /> Tầm Hoạt Động 580km
              </span>{" "}
              giúp ní tự tin lướt qua mọi đỉnh đèo mà không phải lo lắng về việc sạc giữa chừng. Màn hình cong trung tâm điều khiển bằng chip AI{" "}
              <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 shadow-sm ${
                isDark ? "bg-indigo-500/10 text-indigo-300 border border-indigo-500/30" : "bg-indigo-50 text-indigo-700 border border-indigo-200"
              }`}>
                <Cpu className="w-3 h-3 text-indigo-500" /> NPU Xử Lý 30 TOPS
              </span>{" "}
              liên tục cập nhật thông số mật độ giao thông 3D thời gian thực tương thích hoàn toàn với nền tảng Three.js.
            </p>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 3: VEHICLE CATALOG
          ========================================================================= */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <div className="inline-flex items-center gap-2 text-cyan-500 dark:text-cyan-400 text-xs font-mono font-bold uppercase tracking-wider mb-2">
              <span className="text-slate-400">//</span>
              <span>03 • BỘ SƯU TẬP Ô TÔ 2026</span>
            </div>
            <h2 className={`text-3xl sm:text-5xl font-black font-display tracking-tight ${isDark ? "text-white" : "text-slate-900"}`}>
              CHỌN CỖ MÁY CỦA NÍ
            </h2>
          </div>

          {/* Filter Chips */}
          <div className={`flex items-center gap-1.5 p-1.5 rounded-2xl border overflow-x-auto ${
            isDark ? "bg-slate-900/60 border-slate-800" : "bg-white border-slate-200 shadow-sm"
          }`}>
            {[
              { id: "all", label: "Tất cả" },
              { id: "sports", label: "Thể thao" },
              { id: "sedan", label: "Sedan" },
              { id: "commercial", label: "Dịch vụ / Tải" }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedCategory(tab.id)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                  selectedCategory === tab.id
                    ? isDark
                      ? "bg-cyan-500 text-slate-950 font-bold shadow-md shadow-cyan-500/20"
                      : "bg-blue-600 text-white font-bold shadow-md shadow-blue-600/20"
                    : isDark
                    ? "text-slate-400 hover:text-white hover:bg-slate-800/60"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Cars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredCars.map((car) => (
            <CarCard
              key={car.id}
              car={car}
              onCustomizeColor={(carId, colorHex) => setCustomColor({ carId, colorHex })}
            />
          ))}
        </div>
      </section>
    </div>
  );
};
