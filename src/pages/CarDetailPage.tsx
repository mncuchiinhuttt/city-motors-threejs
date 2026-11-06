import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { CARS_DATA } from "../data/cars";
import { Compass, Zap, Gauge, BatteryCharging, Shield, CheckCircle, ArrowLeft, PhoneCall, Calculator } from "lucide-react";

export const CarDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const car = CARS_DATA.find((c) => c.id === id) || CARS_DATA[0];

  const [selectedColor, setSelectedColor] = useState(car.colors[0]);
  const [downPaymentPercent, setDownPaymentPercent] = useState<number>(20);
  const [loanMonths, setLoanMonths] = useState<number>(60);
  const [bookingSuccess, setBookingSuccess] = useState<boolean>(false);
  const [formName, setFormName] = useState<string>("");
  const [formPhone, setFormPhone] = useState<string>("");

  // Financing calculation
  const downPayment = (car.price * downPaymentPercent) / 100;
  const loanAmount = car.price - downPayment;
  const interestRateYear = 0.065; // 6.5% annual
  const monthlyRate = interestRateYear / 12;
  const monthlyPayment = Math.round(
    (loanAmount * (monthlyRate * Math.pow(1 + monthlyRate, loanMonths))) /
      (Math.pow(1 + monthlyRate, loanMonths) - 1)
  );

  const handleBookingSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName || !formPhone) return;
    setBookingSuccess(true);
  };

  return (
    <div className="pt-24 pb-20 min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Back Link */}
        <Link
          to="/cars"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Quay lại danh mục xe</span>
        </Link>

        {/* Main Details Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Left Column: Visual presentation & Specs */}
          <div className="lg:col-span-7 space-y-8">
            {/* Visual Hero Banner */}
            <div className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-slate-900 via-slate-900/90 to-indigo-950/70 border border-slate-800 p-8 sm:p-12 shadow-2xl">
              <div className="relative z-10">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-cyan-400 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20">
                  {car.category.toUpperCase()} EDITION
                </span>
                <h1 className="text-3xl sm:text-5xl font-black font-display text-white mt-3">
                  {car.name}
                </h1>
                <p className="text-base text-slate-300 mt-2 font-light">{car.subtitle}</p>

                {/* 3D Test Drive Banner Button */}
                <div className="mt-8 pt-6 border-t border-slate-800 flex flex-wrap items-center gap-4">
                  <Link
                    to={`/city-experience?car=${car.blenderModelId}`}
                    className="flex items-center gap-2 px-6 py-3.5 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-lg shadow-cyan-500/25 transition-all hover:scale-105"
                  >
                    <Compass className="w-4 h-4" />
                    <span>Lái thử trong thành phố 3D</span>
                  </Link>
                  <span className="text-xs text-slate-400">Xem xe chạy thực tế trên đường phố Three.js</span>
                </div>
              </div>
            </div>

            {/* Performance Specs Grid */}
            <div className="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 className="font-display font-bold text-lg text-white">Thông số kỹ thuật vận hành</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                    <Zap className="w-4 h-4 text-amber-400" />
                    <span>Công suất</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-white">{car.horsepower} HP</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                    <Gauge className="w-4 h-4 text-cyan-400" />
                    <span>0-100 km/h</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-white">{car.acceleration}</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                    <BatteryCharging className="w-4 h-4 text-emerald-400" />
                    <span>Tầm hoạt động</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-white">{car.range}</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-950/70 border border-slate-800/80">
                  <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                    <Gauge className="w-4 h-4 text-indigo-400" />
                    <span>Tốc độ tối đa</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-white">{car.topSpeed} km/h</p>
                </div>
              </div>
            </div>

            {/* Overview & Features */}
            <div className="bg-slate-900/50 p-6 rounded-3xl border border-slate-800 space-y-4">
              <h3 className="font-display font-bold text-lg text-white">Tổng quan mẫu xe</h3>
              <p className="text-sm text-slate-300 leading-relaxed font-light">{car.description}</p>
              <div className="pt-4 border-t border-slate-800">
                <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 mb-3">
                  Trang bị nổi bật
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {car.features.map((feat, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-slate-300">
                      <CheckCircle className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Pricing, Color Selector, Financing & Booking */}
          <div className="lg:col-span-5 space-y-6">
            {/* Price Box */}
            <div className="bg-slate-900/70 p-6 rounded-3xl border border-slate-800 space-y-5">
              <div className="flex items-baseline justify-between pb-4 border-b border-slate-800">
                <div>
                  <span className="text-xs text-slate-400 uppercase font-mono">Giá niêm yết chính hãng</span>
                  <div className="text-3xl font-black font-display text-white mt-0.5">
                    ${car.price.toLocaleString("en-US")}
                  </div>
                </div>
                <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                  Sẵn hàng
                </span>
              </div>

              {/* Color Customizer */}
              <div className="space-y-2">
                <span className="text-xs text-slate-400 font-medium">
                  Màu ngoại thất đã chọn:{" "}
                  <strong className="text-white font-bold">{selectedColor.name}</strong>
                </span>
                <div className="flex items-center gap-3 pt-1">
                  {car.colors.map((c) => (
                    <button
                      key={c.name}
                      onClick={() => setSelectedColor(c)}
                      className={`w-8 h-8 rounded-full border-2 transition-all ${
                        selectedColor.name === c.name
                          ? "border-cyan-400 scale-110 shadow-lg shadow-cyan-500/30"
                          : "border-slate-700 hover:scale-105"
                      }`}
                      style={{ backgroundColor: c.hex }}
                      title={c.name}
                    />
                  ))}
                </div>
              </div>

              {/* Financing Calculator */}
              <div className="pt-4 border-t border-slate-800 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="flex items-center gap-1.5 text-slate-300 font-bold">
                    <Calculator className="w-4 h-4 text-cyan-400" />
                    <span>Dự toán trả góp ngân hàng</span>
                  </span>
                  <span className="font-bold font-mono text-cyan-400 text-sm">
                    ~${monthlyPayment.toLocaleString()}/tháng
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Trả trước: {downPaymentPercent}%</span>
                    <span className="text-white font-mono">${Math.round(downPayment).toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="50"
                    step="5"
                    value={downPaymentPercent}
                    onChange={(e) => setDownPaymentPercent(Number(e.target.value))}
                    className="w-full accent-cyan-500 h-1.5 bg-slate-800 rounded-lg cursor-pointer"
                  />
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Thời hạn vay: {loanMonths} tháng ({loanMonths / 12} năm)</span>
                  </div>
                  <div className="grid grid-cols-4 gap-2">
                    {[24, 36, 48, 60].map((m) => (
                      <button
                        key={m}
                        onClick={() => setLoanMonths(m)}
                        className={`py-1 rounded-lg text-[11px] font-mono font-bold transition-all ${
                          loanMonths === m
                            ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40"
                            : "bg-slate-950 text-slate-400 border border-slate-800"
                        }`}
                      >
                        {m}T
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Test Drive / Booking Form */}
              <div className="pt-4 border-t border-slate-800">
                {bookingSuccess ? (
                  <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-center space-y-2">
                    <CheckCircle className="w-8 h-8 text-emerald-400 mx-auto" />
                    <h4 className="font-bold text-white text-sm">Đã ghi nhận lịch hẹn lái thử!</h4>
                    <p className="text-xs text-slate-300">
                      Chuyên viên CyberCity Motors sẽ liên hệ ní qua số {formPhone} trong 15 phút.
                    </p>
                  </div>
                ) : (
                  <form onSubmit={handleBookingSubmit} className="space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                      Đăng ký tư vấn & Nhận báo giá
                    </h4>
                    <input
                      type="text"
                      placeholder="Họ và tên của ní..."
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      required
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
                    />
                    <input
                      type="tel"
                      placeholder="Số điện thoại..."
                      value={formPhone}
                      onChange={(e) => setFormPhone(e.target.value)}
                      required
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
                    />
                    <button
                      type="submit"
                      className="w-full py-3 rounded-xl font-bold text-xs bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-lg shadow-cyan-500/20 transition-all"
                    >
                      Xác nhận đăng ký nhận ưu đãi
                    </button>
                  </form>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
