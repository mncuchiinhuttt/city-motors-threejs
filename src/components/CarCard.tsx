import React from "react";
import { Link } from "react-router-dom";
import { Zap, Gauge, Compass, ArrowRight, ShieldCheck, BatteryCharging } from "lucide-react";
import { CarSpec } from "../types";

interface CarCardProps {
  car: CarSpec;
  onCustomizeColor?: (carId: string, colorHex: string) => void;
}

export const CarCard: React.FC<CarCardProps> = ({ car, onCustomizeColor }) => {
  return (
    <div className="group relative bg-slate-900/60 hover:bg-slate-900/90 border border-slate-800/80 hover:border-cyan-500/40 rounded-2xl overflow-hidden shadow-xl transition-all duration-300 flex flex-col justify-between">
      {/* Top Banner & Category Badge */}
      <div className="p-6 pb-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-[11px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-md bg-slate-800 text-cyan-400 font-bold border border-slate-700/60">
            {car.category === "sports"
              ? "Super Sports"
              : car.category === "sedan"
              ? "Urban Sedan"
              : car.category === "commercial"
              ? "Commercial / Fleet"
              : "Electric EV"}
          </span>
          <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-400">
            <ShieldCheck className="w-3.5 h-3.5" />
            Sẵn xe giao ngay
          </span>
        </div>

        <h3 className="text-xl font-bold font-display text-white group-hover:text-cyan-300 transition-colors">
          {car.name}
        </h3>
        <p className="text-xs text-slate-400 mt-1 line-clamp-1">{car.subtitle}</p>

        {/* Pricing Box */}
        <div className="mt-4 pt-4 border-t border-slate-800/80 flex items-baseline justify-between">
          <div>
            <span className="text-2xl font-bold font-display text-white tracking-tight">
              ${car.price.toLocaleString("en-US")}
            </span>
            <span className="text-xs text-slate-400 ml-1.5 font-normal">giá niêm yết</span>
          </div>
          <div className="text-right">
            <span className="text-xs text-cyan-400 font-bold">~${car.monthlyPayment}/tháng</span>
            <p className="text-[10px] text-slate-500">trả góp 0% LS</p>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-3 gap-2 mt-5 py-3 px-3.5 bg-slate-950/60 rounded-xl border border-slate-800/60 text-center">
          <div>
            <div className="flex items-center justify-center gap-1 text-[11px] text-slate-400">
              <Zap className="w-3 h-3 text-amber-400" />
              <span>Công suất</span>
            </div>
            <p className="text-sm font-bold font-mono text-slate-200 mt-0.5">{car.horsepower} HP</p>
          </div>

          <div className="border-x border-slate-800">
            <div className="flex items-center justify-center gap-1 text-[11px] text-slate-400">
              <Gauge className="w-3 h-3 text-cyan-400" />
              <span>0-100 km/h</span>
            </div>
            <p className="text-sm font-bold font-mono text-slate-200 mt-0.5">{car.acceleration}</p>
          </div>

          <div>
            <div className="flex items-center justify-center gap-1 text-[11px] text-slate-400">
              <BatteryCharging className="w-3 h-3 text-emerald-400" />
              <span>Tầm vận hành</span>
            </div>
            <p className="text-sm font-bold font-mono text-slate-200 mt-0.5">{car.range}</p>
          </div>
        </div>

        {/* Available Color Dots */}
        <div className="mt-4 flex items-center justify-between">
          <span className="text-xs text-slate-400">Tùy chọn màu sắc:</span>
          <div className="flex items-center gap-1.5">
            {car.colors.map((color) => (
              <button
                key={color.name}
                onClick={() => onCustomizeColor && onCustomizeColor(car.blenderModelId, color.hex)}
                className="w-4 h-4 rounded-full border border-slate-600/80 hover:scale-125 transition-transform"
                style={{ backgroundColor: color.hex }}
                title={color.name}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Card Action Buttons */}
      <div className="p-6 pt-2 bg-slate-950/30 flex items-center gap-2.5">
        <Link
          to={`/city-experience?car=${car.blenderModelId}`}
          className="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 transition-all hover:border-cyan-500/40"
        >
          <Compass className="w-3.5 h-3.5" />
          <span>Lái thử 3D</span>
        </Link>

        <Link
          to={`/cars/${car.id}`}
          className="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl text-xs font-bold bg-cyan-500 hover:bg-cyan-400 text-slate-950 transition-all shadow-md shadow-cyan-500/20"
        >
          <span>Xem chi tiết</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
};
