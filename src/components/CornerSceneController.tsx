import React, { useState } from "react";
import {
  Sun,
  Sunset,
  Moon,
  Zap,
  Video,
  Eye,
  Compass,
  Play,
  Pause,
  Mountain,
  Building2,
  ChevronDown,
  ChevronUp,
  Camera,
  Layers,
  Sparkles
} from "lucide-react";
import { ExtendedCameraMode, TimeOfDay } from "../types";
import { useTheme } from "../context/ThemeContext";

interface CornerSceneControllerProps {
  timeOfDay: TimeOfDay;
  onTimeChange: (time: TimeOfDay) => void;
  cameraPreset: ExtendedCameraMode;
  onCameraChange: (preset: ExtendedCameraMode) => void;
  activeCarId: string;
  onCarChange: (carId: string) => void;
  trafficSpeed: number;
  onSpeedChange: (speed: number) => void;
  isPaused: boolean;
  onTogglePause: () => void;
}

export const CornerSceneController: React.FC<CornerSceneControllerProps> = ({
  timeOfDay,
  onTimeChange,
  cameraPreset,
  onCameraChange,
  activeCarId,
  onCarChange,
  trafficSpeed,
  onSpeedChange,
  isPaused,
  onTogglePause
}) => {
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<"time" | "camera" | "car">("time");
  const { theme } = useTheme();
  const isDark = theme === "dark";

  const timeOptions: { id: TimeOfDay; label: string; icon: React.ReactNode; color: string }[] = [
    { id: "day", label: "Ban ngày", icon: <Sun className="w-4 h-4" />, color: "text-amber-400" },
    { id: "sunset", label: "Hoàng hôn", icon: <Sunset className="w-4 h-4" />, color: "text-orange-400" },
    { id: "night", label: "Ban đêm", icon: <Moon className="w-4 h-4" />, color: "text-indigo-400" },
    { id: "cyberpunk", label: "Cyberpunk", icon: <Zap className="w-4 h-4" />, color: "text-cyan-400" }
  ];

  const cameraOptions: { id: ExtendedCameraMode; label: string; icon: React.ReactNode; desc: string }[] = [
    { id: "chase", label: "Đuổi theo xe", icon: <Video className="w-4 h-4" />, desc: "Camera bám đuôi xe đua" },
    { id: "hood", label: "Nắp ca-pô", icon: <Eye className="w-4 h-4" />, desc: "Góc nhìn người lái" },
    { id: "drone", label: "Flycam bên hông", icon: <Camera className="w-4 h-4" />, desc: "Drone lượn quanh xe" },
    { id: "mountain", label: "Đỉnh đèo núi", icon: <Mountain className="w-4 h-4" />, desc: "Ngắm đèo & vực núi" },
    { id: "street", label: "Góc phố", icon: <Building2 className="w-4 h-4" />, desc: "Ngước nhìn tòa nhà" },
    { id: "isometric", label: "Tự do 360°", icon: <Compass className="w-4 h-4" />, desc: "Tự xoay & phóng to" }
  ];

  const carOptions = [
    { id: "Car_BlueCoupe", name: "Apex GT-90", type: "Coupe trên núi", color: "#0077ff" },
    { id: "Car_RedSedan", name: "Horizon Sedan", type: "Sedan đô thị", color: "#cc1122" },
    { id: "Car_Taxi", name: "CyberCab Pro", type: "Taxi phố đêm", color: "#f5b700" },
    { id: "Car_WhiteVan", name: "Titan Cargo", type: "Xe tải đèo núi", color: "#f8f9fa" }
  ];

  return (
    <div className="fixed bottom-6 right-6 z-30 flex flex-col items-end">
      {/* Collapsed Pill Button */}
      {collapsed ? (
        <button
          onClick={() => setCollapsed(false)}
          className={`flex items-center gap-2.5 px-4 py-2.5 rounded-2xl shadow-2xl backdrop-blur-xl border font-bold text-xs transition-all hover:scale-105 ${
            isDark
              ? "bg-slate-900/90 text-cyan-400 border-cyan-500/30 hover:bg-slate-800"
              : "bg-white/95 text-blue-600 border-slate-200/90 hover:bg-white shadow-lg"
          }`}
        >
          <Sparkles className="w-4 h-4" />
          <span>Bảng điều khiển khung cảnh & Camera</span>
          <ChevronUp className="w-4 h-4" />
        </button>
      ) : (
        /* Expanded Floating Corner Box (Khúc ở góc để đổi) */
        <div
          className={`w-[340px] sm:w-[380px] rounded-3xl p-4 shadow-2xl backdrop-blur-2xl border transition-all duration-300 ${
            isDark
              ? "bg-slate-900/90 border-slate-700/80 text-slate-100 shadow-cyan-950/30"
              : "bg-white/95 border-slate-200/90 text-slate-800 shadow-slate-300/50"
          }`}
        >
          {/* Header & Tabs */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-800/60 dark:border-slate-800/80">
            <div
              className={`flex items-center gap-1.5 p-1 rounded-xl border ${
                isDark ? "bg-slate-950/70 border-slate-800" : "bg-slate-100 border-slate-200"
              }`}
            >
              <button
                onClick={() => setActiveTab("time")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "time"
                    ? isDark
                      ? "bg-cyan-500 text-slate-950 shadow-sm"
                      : "bg-blue-600 text-white shadow-sm"
                    : isDark
                    ? "text-slate-400 hover:text-white"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Khung cảnh
              </button>
              <button
                onClick={() => setActiveTab("camera")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "camera"
                    ? isDark
                      ? "bg-cyan-500 text-slate-950 shadow-sm"
                      : "bg-blue-600 text-white shadow-sm"
                    : isDark
                    ? "text-slate-400 hover:text-white"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Góc Camera
              </button>
              <button
                onClick={() => setActiveTab("car")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "car"
                    ? isDark
                      ? "bg-cyan-500 text-slate-950 shadow-sm"
                      : "bg-blue-600 text-white shadow-sm"
                    : isDark
                    ? "text-slate-400 hover:text-white"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Chọn xe
              </button>
            </div>

            <button
              onClick={() => setCollapsed(true)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/40"
              title="Thu nhỏ"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>

          {/* Tab 1: Time of Day (Khung cảnh Ngày / Đêm / Hoàng hôn / Cyberpunk) */}
          {activeTab === "time" && (
            <div className="py-3 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block font-semibold">
                CHỌN ÁNH SÁNG & KHÍ HẬU
              </span>
              <div className="grid grid-cols-2 gap-2">
                {timeOptions.map((t) => {
                  const active = timeOfDay === t.id;
                  return (
                    <button
                      key={t.id}
                      onClick={() => onTimeChange(t.id)}
                      className={`flex items-center gap-2 p-2.5 rounded-xl border text-xs font-semibold transition-all ${
                        active
                          ? isDark
                            ? "bg-cyan-500/15 border-cyan-500 text-cyan-300 font-bold shadow-sm"
                            : "bg-blue-50 border-blue-600 text-blue-700 font-bold shadow-sm"
                          : isDark
                          ? "bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/60"
                          : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                      }`}
                    >
                      <span className={t.color}>{t.icon}</span>
                      <span>{t.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Tab 2: Camera Perspectives (Đuổi theo xe, Nắp ca-pô, Đỉnh đèo núi, v.v.) */}
          {activeTab === "camera" && (
            <div className="py-3 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block font-semibold">
                CHỌN GÓC QUAN SÁT CAMERA
              </span>
              <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto pr-1">
                {cameraOptions.map((c) => {
                  const active = cameraPreset === c.id;
                  return (
                    <button
                      key={c.id}
                      onClick={() => onCameraChange(c.id)}
                      className={`flex flex-col text-left p-2 rounded-xl border transition-all ${
                        active
                          ? isDark
                            ? "bg-cyan-500/15 border-cyan-500 text-cyan-300 font-bold"
                            : "bg-blue-50 border-blue-600 text-blue-700 font-bold"
                          : isDark
                          ? "bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/60"
                          : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-1.5 text-xs font-bold">
                        {c.icon}
                        <span>{c.label}</span>
                      </div>
                      <span className="text-[10px] text-slate-500 mt-0.5 line-clamp-1">{c.desc}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Tab 3: Car Selection (Apex GT-90 trên núi, Horizon Sedan, Taxi, v.v.) */}
          {activeTab === "car" && (
            <div className="py-3 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block font-semibold">
                CHỌN XE ĐỂ THEO DÕI VÔ TẬN
              </span>
              <div className="space-y-1.5">
                {carOptions.map((car) => {
                  const active = activeCarId === car.id;
                  return (
                    <button
                      key={car.id}
                      onClick={() => {
                        onCarChange(car.id);
                        onCameraChange("chase");
                      }}
                      className={`w-full flex items-center justify-between p-2 rounded-xl border text-xs transition-all ${
                        active
                          ? isDark
                            ? "bg-cyan-500/15 border-cyan-500 text-cyan-300 font-bold"
                            : "bg-blue-50 border-blue-600 text-blue-700 font-bold"
                          : isDark
                          ? "bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/60"
                          : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span
                          className="w-3 h-3 rounded-full border border-black/40"
                          style={{ backgroundColor: car.color }}
                        />
                        <span className="font-bold">{car.name}</span>
                      </div>
                      <span className="text-[10px] text-slate-400 font-mono">{car.type}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Bottom Bar: Traffic Control & Infinite Run Status */}
          <div className="pt-2.5 mt-1 border-t border-slate-800/60 dark:border-slate-800/80 flex items-center justify-between text-xs">
            {/* Speed pills */}
            <div className="flex items-center gap-1">
              <button
                onClick={onTogglePause}
                className={`p-1.5 rounded-lg border transition-all ${
                  isPaused
                    ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
                    : isDark
                    ? "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
                    : "bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200"
                }`}
                title={isPaused ? "Tiếp tục chạy" : "Tạm dừng xe"}
              >
                {isPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
              </button>

              <div className="flex items-center gap-1 bg-slate-950/40 p-0.5 rounded-lg border border-slate-800/60">
                {[0.5, 1.0, 1.8].map((s) => (
                  <button
                    key={s}
                    onClick={() => onSpeedChange(s)}
                    className={`px-2 py-0.5 rounded text-[10px] font-mono transition-all ${
                      trafficSpeed === s
                        ? isDark
                          ? "bg-cyan-500 text-slate-950 font-bold"
                          : "bg-blue-600 text-white font-bold"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {s}x
                  </button>
                ))}
              </div>
            </div>

            {/* Infinite Loop Status Badge */}
            <div className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-400 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              <span>VÒNG LẶP VÔ TẬN</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
