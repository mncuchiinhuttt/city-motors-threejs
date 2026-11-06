import React, { useState } from "react";
import { Link } from "react-router-dom";
import { CityCanvas } from "../components/CityCanvas";
import { CornerSceneController } from "../components/CornerSceneController";
import { CarCard } from "../components/CarCard";
import { CARS_DATA } from "../data/cars";
import { SceneMode, SimpleCameraMode, TimeOfDay } from "../types";
import {
  ArrowRight,
  Compass,
  Zap,
  Sparkles,
  ChevronDown,
  BatteryCharging,
  Eye,
  Radio,
  Layers,
  CheckCircle2,
  Quote,
  Video,
  Globe,
  Mountain,
  Building2,
  Cpu
} from "lucide-react";

export const HomePage: React.FC = () => {
  const [sceneMode, setSceneMode] = useState<SceneMode>("mountain"); // Default: Mountain Pass as requested!
  const [timeOfDay, setTimeOfDay] = useState<TimeOfDay>("day");
  const [cameraMode, setCameraMode] = useState<SimpleCameraMode>("close"); // Exactly 2 modes: close vs wide!
  const [trafficSpeed, setTrafficSpeed] = useState<number>(1.0);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");

  const filteredCars = CARS_DATA.filter(
    (car) => selectedCategory === "all" || car.category === selectedCategory
  );

  return (
    <div className="pt-16 min-h-screen bg-white text-slate-800">
      {/* =========================================================================
          HERO SECTION: 3D VIEWPORT WITH ZERO SCROLL INTERFERENCE
          ========================================================================= */}
      <section className="relative w-full h-[85vh] min-h-[580px] bg-slate-100">
        {/* Three.js Canvas: enableZoom = false prevents scroll trapping! */}
        <div className="absolute inset-0 z-0">
          <CityCanvas
            sceneMode={sceneMode}
            timeOfDay={timeOfDay}
            cameraMode={cameraMode}
            trafficSpeed={trafficSpeed}
            isPaused={isPaused}
            enableZoom={false}
          />
        </div>

        {/* Crisp Bottom Vignette into Page Content */}
        <div className="absolute inset-x-0 bottom-0 h-24 pointer-events-none bg-gradient-to-t from-white to-transparent z-10" />

        {/* Hero Overlay Content */}
        <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex flex-col justify-between py-8 pointer-events-none">
          <div className="max-w-xl pt-4 space-y-3.5">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/95 border border-slate-200 text-orange-600 text-xs font-mono font-bold pointer-events-auto shadow-sm">
              <span className="w-2 h-2 rounded-full bg-orange-500 animate-ping" />
              <span>BLENDER 5.2 • 2 PHÂN CẢNH 3D RIÊNG BIỆT</span>
            </div>

            <h1 className="text-4xl sm:text-6xl font-black font-display tracking-tight text-slate-900 leading-none">
              {sceneMode === "mountain" ? (
                <>
                  CUNG ĐƯỜNG <br />
                  <span className="text-orange-500">ĐÈO NÚI TOUGE.</span>
                </>
              ) : (
                <>
                  ĐẠI LỘ <br />
                  <span className="text-orange-500">ĐÔ THỊ HIỆN ĐẠI.</span>
                </>
              )}
            </h1>

            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed font-normal max-w-lg bg-white/85 p-3 rounded-2xl border border-slate-200/70 shadow-sm backdrop-blur-md">
              {sceneMode === "mountain"
                ? "Chiếc xe thể thao cam lướt đi vòng quanh cung đường đèo núi dốc thoai thoải, qua rào chắn và đài vọng cảnh. Camera bám sát sau đuôi xe mượt mà."
                : "Chiếc xe thể thao cam lăn bánh tuần hoàn qua ngã tư trung tâm giữa các tòa nhà chọc trời và hàng đèn đường lung linh."}
            </p>

            {/* Quick Scene & Camera Toggle Buttons */}
            <div className="flex flex-wrap items-center gap-2.5 pt-1 pointer-events-auto">
              <button
                onClick={() => setSceneMode(sceneMode === "mountain" ? "city" : "mountain")}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs bg-orange-500 hover:bg-orange-600 text-white shadow-md shadow-orange-500/20 transition-all hover:scale-105"
              >
                {sceneMode === "mountain" ? <Building2 className="w-4 h-4" /> : <Mountain className="w-4 h-4" />}
                <span>{sceneMode === "mountain" ? "Đổi sang Thành Phố" : "Đổi sang Đèo Núi"}</span>
              </button>

              <button
                onClick={() => setCameraMode(cameraMode === "close" ? "wide" : "close")}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-bold text-xs bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 shadow-sm transition-all"
              >
                {cameraMode === "close" ? <Globe className="w-4 h-4 text-orange-500" /> : <Video className="w-4 h-4 text-orange-500" />}
                <span>{cameraMode === "close" ? "Góc Rộng (Toàn cảnh)" : "Góc Gần (Theo xe)"}</span>
              </button>
            </div>
          </div>

          {/* Scroll Down Hint Link (Clicking scrolls directly to Bento section!) */}
          <div className="self-center pointer-events-auto pb-1">
            <a
              href="#bento-innovation"
              className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/90 border border-slate-200 text-slate-600 text-[11px] font-mono font-bold hover:text-orange-600 shadow-sm transition-colors"
            >
              <span>CUỘN XUỐNG XEM CHI TIẾT</span>
              <ChevronDown className="w-3.5 h-3.5 text-orange-500 animate-bounce" />
            </a>
          </div>
        </div>

        {/* Floating Corner Controller ("Khúc ở góc để đổi") */}
        <CornerSceneController
          sceneMode={sceneMode}
          onSceneChange={setSceneMode}
          timeOfDay={timeOfDay}
          onTimeChange={setTimeOfDay}
          cameraMode={cameraMode}
          onCameraChange={setCameraMode}
          trafficSpeed={trafficSpeed}
          onSpeedChange={setTrafficSpeed}
          isPaused={isPaused}
          onTogglePause={() => setIsPaused(!isPaused)}
        />
      </section>

      {/* =========================================================================
          SECTION 1: BENTO GRID (60/30/10 RULE, SOLID ORANGE ACCENT, NO GRADIENTS)
          ========================================================================= */}
      <section id="bento-innovation" className="py-24 relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-4">
          <div>
            <div className="inline-flex items-center gap-2 text-orange-600 text-xs font-mono font-bold uppercase tracking-wider mb-3">
              <span className="text-slate-400">//</span>
              <span>01 • NGHỆ THUẬT CƠ KHÍ & ĐIỆN TỬ</span>
            </div>
            <h2 className="text-3xl sm:text-5xl font-black font-display text-slate-900 tracking-tight">
              KỸ NGHỆ Ô TÔ HIỆN ĐẠI
            </h2>
          </div>
          <p className="text-xs sm:text-sm text-slate-600 max-w-md font-normal leading-relaxed">
            Mỗi chi tiết được dựng tỉ mỉ từ phần mềm 3D Blender đến hệ thống khung gầm thực tế, kết hợp phong cách thiết kế tối giản và màu sắc hài hòa.
          </p>
        </div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Bento Card 1: Power & Acceleration (8 cols) */}
          <div className="md:col-span-8 group relative bg-white border border-slate-200 hover:border-orange-500 rounded-3xl p-8 sm:p-10 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-orange-50 border border-orange-200 text-orange-600 flex items-center justify-center font-bold">
                <Zap className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-orange-600 font-bold block">
                HỆ TRUYỀN ĐỘNG DUAL-MOTOR
              </span>
              <h3 className="text-2xl sm:text-3xl font-bold font-display text-slate-900 leading-tight">
                650 Mã Lực • Bứt Tốc 0-100 km/h Trong 2.8 Giây
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 font-normal leading-relaxed max-w-xl">
                Động cơ nam châm vĩnh cửu kép phân bổ mô-men xoắn tức thời lên từng bánh xe độc lập. Hệ thống kiểm soát lực kéo thông minh đảm bảo xe bám chặt mặt đường kể cả khi vào cua ở tốc độ cao.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-4 pt-8 mt-6 border-t border-slate-100">
              <div>
                <span className="text-[11px] text-slate-400 font-mono">MÔ-MEN XOẮN</span>
                <p className="text-2xl font-bold font-mono text-slate-900 mt-0.5">850 Nm</p>
              </div>
              <div className="border-x border-slate-200 px-4">
                <span className="text-[11px] text-slate-400 font-mono">HIỆU SUẤT PIN</span>
                <p className="text-2xl font-bold font-mono text-orange-600 mt-0.5">97.2%</p>
              </div>
              <div>
                <span className="text-[11px] text-slate-400 font-mono">TRỌNG TÂM THẤP</span>
                <p className="text-2xl font-bold font-mono text-emerald-600 mt-0.5">420 mm</p>
              </div>
            </div>
          </div>

          {/* Bento Card 2: 800V Ultra-Fast Charging (4 cols) */}
          <div className="md:col-span-4 group relative bg-white border border-slate-200 hover:border-orange-500 rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-orange-50 border border-orange-200 text-orange-600 flex items-center justify-center font-bold">
                <BatteryCharging className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-orange-600 font-bold block">
                KIẾN TRÚC ĐIỆN ÁP 800V
              </span>
              <h3 className="text-xl sm:text-2xl font-bold font-display text-slate-900">
                Sạc 18 Phút • Chạy Thêm 400 Km
              </h3>
              <p className="text-xs text-slate-600 font-normal leading-relaxed">
                Tương thích trạm sạc siêu tốc DC công suất 350kW. Hệ thống làm mát pin bằng chất lỏng kiểm soát nhiệt độ tế bào pin luôn ở trạng thái lý tưởng.
              </p>
            </div>

            <div className="pt-6 mt-4 border-t border-slate-100 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400">CHU KỲ SẠC:</span>
              <span className="text-orange-600 font-bold">5.000+ LẦN (BẢO HÀNH 8 NĂM)</span>
            </div>
          </div>

          {/* Bento Card 3: Autonomous Driving & Radar (4 cols) */}
          <div className="md:col-span-4 group relative bg-white border border-slate-200 hover:border-orange-500 rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-slate-100 border border-slate-200 text-slate-800 flex items-center justify-center font-bold">
                <Radio className="w-6 h-6 text-orange-500" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                RADAR LIDAR 360° & AI
              </span>
              <h3 className="text-xl sm:text-2xl font-bold font-display text-slate-900">
                Tự Hành Cấp Độ 3 Trong Đô Thị
              </h3>
              <p className="text-xs text-slate-600 font-normal leading-relaxed">
                Quét 2.000.000 điểm mỗi giây giúp nhận diện người đi bộ, vật cản và tín hiệu đèn giao thông trong mọi điều kiện thời tiết.
              </p>
            </div>

            <div className="pt-6 mt-4 border-t border-slate-100 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400">ĐỘ TRỄ PHẢN HỒI:</span>
              <span className="text-slate-900 font-bold">&lt; 15 MILLISECONDS</span>
            </div>
          </div>

          {/* Bento Card 4: Lightweight Carbon Monocoque (8 cols) */}
          <div className="md:col-span-8 group relative bg-white border border-slate-200 hover:border-orange-500 rounded-3xl p-8 sm:p-10 shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between">
            <div className="space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-slate-100 border border-slate-200 text-slate-800 flex items-center justify-center font-bold">
                <Layers className="w-6 h-6 text-orange-500" />
              </div>
              <span className="text-[11px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
                KHUNG GẦM NGUYÊN KHỐI
              </span>
              <h3 className="text-2xl sm:text-3xl font-bold font-display text-slate-900">
                Hợp Kim Nhôm Hàng Không & Sợi Carbon Đúc
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 font-normal leading-relaxed max-w-xl">
                Cấu trúc lồng an toàn bảo vệ khoang hành khách với độ cứng xoắn 45.000 Nm/độ. Giảm 25% trọng lượng thân xe giúp kéo dài quãng đường di chuyển và tăng độ nhạy phản hồi vô-lăng.
              </p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-8 mt-6 border-t border-slate-100 text-xs font-mono">
              <div>
                <span className="text-slate-400">ĐẠT CHUẨN</span>
                <p className="text-slate-900 font-bold mt-0.5">EURO NCAP 5 SAO</p>
              </div>
              <div>
                <span className="text-slate-400">HỆ SỐ CẢN GIÓ</span>
                <p className="text-orange-600 font-bold mt-0.5">Cd = 0.21</p>
              </div>
              <div>
                <span className="text-slate-400">TỈ LỆ TRỌNG LƯỢNG</span>
                <p className="text-slate-900 font-bold mt-0.5">50 : 50 HOÀN HẢO</p>
              </div>
              <div>
                <span className="text-slate-400">CÁCH ÂM</span>
                <p className="text-slate-900 font-bold mt-0.5">KÍNH 2 LỚP CHỦ ĐỘNG</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 2: EDITORIAL NARRATIVE (ARTISTIC ICONS IN PARAGRAPHS, SOLID COLORS)
          ========================================================================= */}
      <section className="py-24 bg-slate-50 border-y border-slate-200">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
          <div className="flex items-center gap-3 text-orange-600 text-xs font-mono font-bold uppercase tracking-widest">
            <span className="w-8 h-px bg-orange-500" />
            <span>02 • TRIẾT LÝ VẬN HÀNH & TRẢI NGHIỆM</span>
          </div>

          <div className="relative">
            <Quote className="w-16 h-16 text-orange-200 absolute -top-8 -left-8 pointer-events-none" />
            <h3 className="text-2xl sm:text-4xl font-black font-display text-slate-900 tracking-tight leading-snug">
              “Khi lăn bánh qua những con phố và đỉnh đèo, con đường không còn là lối đi đơn thuần — đó là sàn diễn của ánh sáng, kỹ nghệ và tốc độ thuần khiết.”
            </h3>
          </div>

          {/* Paragraphs with Embedded Solid Icon Badges */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10 text-sm sm:text-base text-slate-700 font-normal leading-relaxed">
            <p>
              Được thiết kế để chinh phục cả những khúc cua đô thị lẫn cung đường đèo núi hiểm trở, chiếc xe sở hữu cụm đèn chiếu sáng{" "}
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 bg-orange-50 text-orange-700 border border-orange-200">
                <Eye className="w-3 h-3 text-orange-600" /> LED Matrix Thấu Kính
              </span>{" "}
              với khả năng tự động cắt luồng sáng chống lóa. Hệ thống động cơ điện kép{" "}
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 bg-orange-50 text-orange-700 border border-orange-200">
                <Zap className="w-3 h-3 text-orange-600" /> 650 Mã Lực
              </span>{" "}
              vận hành trong sự tĩnh lặng tuyệt đối, biến mỗi chuyến đi dạo phố thành một trải nghiệm thiền định cơ khí.
            </p>

            <p>
              Khung gầm liền khối kết hợp viên pin thế hệ mới{" "}
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 bg-slate-200/80 text-slate-800 border border-slate-300">
                <BatteryCharging className="w-3 h-3 text-emerald-600" /> Tầm Hoạt Động 580km
              </span>{" "}
              giúp ní tự tin lướt qua mọi đỉnh đèo mà không phải lo lắng về sạc giữa chừng. Màn hình cong trung tâm điều khiển bằng chip AI{" "}
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold align-middle mx-1 bg-slate-200/80 text-slate-800 border border-slate-300">
                <Cpu className="w-3 h-3 text-slate-800" /> NPU Xử Lý 30 TOPS
              </span>{" "}
              liên tục cập nhật thông số mật độ giao thông 3D thời gian thực tương thích hoàn toàn với nền tảng Three.js.
            </p>
          </div>

          {/* Quick Technical Highlights Row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 pt-8 border-t border-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-200 flex items-center justify-center text-orange-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="text-xs text-slate-800 font-bold">Bảo hành 8 năm toàn diện</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-200 flex items-center justify-center text-orange-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="text-xs text-slate-800 font-bold">Cứu hộ khẩn cấp 24/7</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-200 flex items-center justify-center text-orange-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="text-xs text-slate-800 font-bold">Sạc siêu tốc 300+ trạm</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-orange-50 border border-orange-200 flex items-center justify-center text-orange-600">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="text-xs text-slate-800 font-bold">Cập nhật phần mềm qua OTA</span>
            </div>
          </div>
        </div>
      </section>

      {/* =========================================================================
          SECTION 3: VEHICLE CATALOG
          ========================================================================= */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <div className="inline-flex items-center gap-2 text-orange-600 text-xs font-mono font-bold uppercase tracking-wider mb-2">
              <span className="text-slate-400">//</span>
              <span>03 • BỘ SƯU TẬP Ô TÔ 2026</span>
            </div>
            <h2 className="text-3xl sm:text-5xl font-black font-display text-slate-900 tracking-tight">
              CHỌN CỖ MÁY CỦA NÍ
            </h2>
          </div>

          {/* Filter Chips */}
          <div className="flex items-center gap-1.5 p-1 rounded-2xl bg-slate-100 border border-slate-200">
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
                    ? "bg-orange-500 text-white font-bold shadow-md shadow-orange-500/20"
                    : "text-slate-600 hover:text-slate-900 hover:bg-white"
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
            <CarCard key={car.id} car={car} />
          ))}
        </div>
      </section>
    </div>
  );
};
