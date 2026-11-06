import React, { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { CARS_DATA } from "../data/cars";
import { Compass, Zap, Gauge, BatteryCharging, CheckCircle, ArrowLeft, Calculator } from "lucide-react";

export const CarDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const car = CARS_DATA.find((c) => c.id === id) || CARS_DATA[0];

  const [selectedColor, setSelectedColor] = useState(car.colors[0]);
  const [downPaymentPercent, setDownPaymentPercent] = useState<number>(20);
  const [loanMonths, setLoanMonths] = useState<number>(60);
  const [bookingSuccess, setBookingSuccess] = useState<boolean>(false);
  const [formName, setFormName] = useState<string>("");
  const [formPhone, setFormPhone] = useState<string>("");

  const downPayment = (car.price * downPaymentPercent) / 100;
  const loanAmount = car.price - downPayment;
  const interestRateYear = 0.065;
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
    <div className="pt-24 pb-20 min-h-screen bg-slate-50 text-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link
          to="/cars"
          className="inline-flex items-center gap-2 text-xs font-semibold text-slate-500 hover:text-orange-600 transition-colors mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Quay lại danh mục xe</span>
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
          {/* Left Column: Visual presentation & Specs */}
          <div className="lg:col-span-7 space-y-8">
            {/* Visual Hero Banner */}
            <div className="relative rounded-3xl overflow-hidden bg-white border border-slate-200 p-8 sm:p-12 shadow-sm">
              <div className="relative z-10">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-orange-700 px-3 py-1 rounded-full bg-orange-50 border border-orange-200">
                  {car.category.toUpperCase()} EDITION
                </span>
                <h1 className="text-3xl sm:text-5xl font-black font-display text-slate-900 mt-3">
                  {car.name}
                </h1>
                <p className="text-base text-slate-600 mt-2 font-normal">{car.subtitle}</p>

                {/* 3D Test Drive Banner Button */}
                <div className="mt-8 pt-6 border-t border-slate-100 flex flex-wrap items-center gap-4">
                  <Link
                    to={`/city-experience?car=${car.blenderModelId}`}
                    className="flex items-center gap-2 px-6 py-3.5 rounded-xl text-xs font-bold bg-orange-500 hover:bg-orange-600 text-white shadow-md shadow-orange-500/20 transition-all hover:scale-105"
                  >
                    <Compass className="w-4 h-4" />
                    <span>Lái thử trong thành phố 3D</span>
                  </Link>
                  <span className="text-xs text-slate-500">Xem xe chạy thực tế trên cung đường đèo núi Three.js</span>
                </div>
              </div>
            </div>

            {/* Performance Specs Grid */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-display font-bold text-lg text-slate-900">Thông số kỹ thuật vận hành</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                    <Zap className="w-4 h-4 text-orange-500" />
                    <span>Công suất</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-slate-900">{car.horsepower} HP</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                    <Gauge className="w-4 h-4 text-orange-500" />
                    <span>0-100 km/h</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-slate-900">{car.acceleration}</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                    <BatteryCharging className="w-4 h-4 text-emerald-600" />
                    <span>Tầm hoạt động</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-slate-900">{car.range}</p>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-1">
                    <Gauge className="w-4 h-4 text-slate-700" />
                    <span>Tốc độ tối đa</span>
                  </div>
                  <p className="text-xl font-bold font-mono text-slate-900">{car.topSpeed} km/h</p>
                </div>
              </div>
            </div>

            {/* Overview & Features */}
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-display font-bold text-lg text-slate-900">Tổng quan mẫu xe</h3>
              <p className="text-sm text-slate-600 leading-relaxed font-normal">{car.description}</p>
              <div className="pt-4 border-t border-slate-100">
                <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-500 mb-3">
                  Trang bị nổi bật
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {car.features.map((feat, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-slate-700">
                      <CheckCircle className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Pricing, Color Selector, Financing & Booking */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-5">
              <div className="flex items-baseline justify-between pb-4 border-b border-slate-100">
                <div>
                  <span className="text-xs text-slate-500 uppercase font-mono">Giá niêm yết chính hãng</span>
                  <div className="text-3xl font-black font-display text-slate-900 mt-0.5">
                    ${car.price.toLocaleString("en-US")}
                  </div>
                </div>
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                  Sẵn hàng
                </span>
              </div>

              {/* Color Customizer */}
              <div className="space-y-2">
                <span className="text-xs text-slate-600 font-medium">
                  Màu ngoại thất đã chọn:{" "}
                  <strong className="text-slate-900 font-bold">{selectedColor.name}</strong>
                </span>
                <div className="flex items-center gap-3 pt-1">
                  {car.colors.map((c) => (
                    <button
                      key={c.name}
                      onClick={() => setSelectedColor(c)}
                      className={`w-8 h-8 rounded-full border-2 transition-all ${
                        selectedColor.name === c.name
                          ? "border-orange-500 scale-110 shadow-md"
                          : "border-slate-300 hover:scale-105"
                      }`}
                      style={{ backgroundColor: c.hex }}
                      title={c.name}
                    />
                  ))}
                </div>
              </div>

              {/* Financing Calculator */}
              <div className="pt-4 border-t border-slate-100 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <span className="flex items-center gap-1.5 text-slate-800 font-bold">
                    <Calculator className="w-4 h-4 text-orange-500" />
                    <span>Dự toán trả góp ngân hàng</span>
                  </span>
                  <span className="font-bold font-mono text-orange-600 text-sm">
                    ~${monthlyPayment.toLocaleString()}/tháng
                  </span>
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-600">
                    <span>Trả trước: {downPaymentPercent}%</span>
                    <span className="text-slate-900 font-mono font-bold">${Math.round(downPayment).toLocaleString()}</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="50"
                    step="5"
                    value={downPaymentPercent}
                    onChange={(e) => setDownPaymentPercent(Number(e.target.value))}
                    className="w-full accent-orange-500 h-1.5 bg-slate-200 rounded-lg cursor-pointer"
                  />
                </div>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-600">
                    <span>Thời hạn vay: {loanMonths} tháng ({loanMonths / 12} năm)</span>
                  </div>
                  <div className="grid grid-cols-4 gap-2">
                    {[24, 36, 48, 60].map((m) => (
                      <button
                        key={m}
                        onClick={() => setLoanMonths(m)}
                        className={`py-1.5 rounded-lg text-[11px] font-mono font-bold transition-all ${
                          loanMonths === m
                            ? "bg-orange-500 text-white shadow-sm"
                            : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                        }`}
                      >
                        {m}T
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Test Drive / Booking Form */}
              <div className="pt-4 border-t border-slate-100">
                {bookingSuccess ? (
                  <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-center space-y-2">
                    <CheckCircle className="w-8 h-8 text-emerald-600 mx-auto" />
                    <h4 className="font-bold text-slate-900 text-sm">Đã ghi nhận lịch hẹn lái thử!</h4>
                    <p className="text-xs text-slate-600">
                      Chuyên viên CyberCity Motors sẽ liên hệ ní qua số {formPhone} trong 15 phút.
                    </p>
                  </div>
                ) : (
                  <form onSubmit={handleBookingSubmit} className="space-y-3">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Đăng ký tư vấn & Nhận báo giá
                    </h4>
                    <input
                      type="text"
                      placeholder="Họ và tên của ní..."
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      required
                      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs text-slate-800 focus:outline-none focus:border-orange-500"
                    />
                    <input
                      type="tel"
                      placeholder="Số điện thoại..."
                      value={formPhone}
                      onChange={(e) => setFormPhone(e.target.value)}
                      required
                      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs text-slate-800 focus:outline-none focus:border-orange-500"
                    />
                    <button
                      type="submit"
                      className="w-full py-3 rounded-xl font-bold text-xs bg-orange-500 hover:bg-orange-600 text-white shadow-md shadow-orange-500/20 transition-all"
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
