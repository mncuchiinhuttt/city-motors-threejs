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
  Car,
  Sparkles
} from "lucide-react";
import { ExtendedCameraMode, TimeOfDay } from "../types";

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

  const timeOptions: { id: TimeOfDay; label: string; icon: React.ReactNode }[] = [
    { id: "day", label: "Ban ngày", icon: <Sun className="w-4 h-4 text-amber-500" /> },
    { id: "sunset", label: "Hoàng hôn", icon: <Sunset className="w-4 h-4 text-orange-500" /> },
    { id: "night", label: "Ban đêm", icon: <Moon className="w-4 h-4 text-indigo-500" /> },
    { id: "cyberpunk", label: "Cyberpunk", icon: <Zap className="w-4 h-4 text-cyan-500" /> }
  ];

  const cameraOptions: { id: ExtendedCameraMode; label: string; icon: React.ReactNode; desc: string }[] = [
    { id: "chase", label: "Theo đuôi xe", icon: <Video className="w-4 h-4 text-orange-600" />, desc: "Camera bám đuổi xe đua" },
    { id: "hood", label: "Nắp ca-pô", icon: <Eye className="w-4 h-4 text-slate-700" />, desc: "Góc nhìn người lái" },
    { id: "drone", label: "Flycam hông", icon: <Camera className="w-4 h-4 text-slate-700" />, desc: "Bay lượn quanh xe" },
    { id: "mountain", label: "Đỉnh đèo núi", icon: <Mountain className="w-4 h-4 text-slate-700" />, desc: "Ngắm đèo & vực núi" },
    { id: "street", label: "Góc phố", icon: <Building2 className="w-4 h-4 text-slate-700" />, desc: "Ngước nhìn tòa nhà" },
    { id: "isometric", label: "Tự do 360°", icon: <Compass className="w-4 h-4 text-slate-700" />, desc: "Xoay & phóng to tự do" }
  ];

  const carOptions = [
    { id: "Car_BlueCoupe", name: "Apex GT-90", type: "Coupe Cam thể thao", color: "#f97316" },
    { id: "Car_RedSedan",  name: "Horizon Sedan", type: "Sedan trắng ngọc", color: "#ffffff" },
    { id: "Car_Taxi",      name: "CyberCab Pro",  type: "Taxi vàng đô thị", color: "#f5b700" },
    { id: "Car_WhiteVan",  name: "Titan Cargo",   type: "Xe tải xanh đèo", color: "#0284c7" }
  ];

  return (
    <div className="fixed bottom-6 right-6 z-30 flex flex-col items-end">
      {collapsed ? (
        <button
          onClick={() => setCollapsed(false)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-bold text-xs shadow-xl hover:bg-slate-50 transition-all hover:scale-105"
        >
          <Sparkles className="w-4 h-4 text-orange-500" />
          <span>Bảng điều khiển khung cảnh & Camera</span>
          <ChevronUp className="w-4 h-4 text-slate-400" />
        </button>
      ) : (
        <div className="w-[330px] sm:w-[360px] rounded-3xl p-4 bg-white/95 backdrop-blur-xl border border-slate-200 shadow-2xl text-slate-800 transition-all">
          {/* Header & Tabs */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-1 p-1 rounded-xl bg-slate-100 border border-slate-200">
              <button
                onClick={() => setActiveTab("time")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "time" ? "bg-orange-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Khung cảnh
              </button>
              <button
                onClick={() => setActiveTab("camera")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "camera" ? "bg-orange-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Góc Camera
              </button>
              <button
                onClick={() => setActiveTab("car")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                  activeTab === "car" ? "bg-orange-500 text-white shadow-sm" : "text-slate-600 hover:text-slate-900"
                }`}
              >
                Chọn xe
              </button>
            </div>

            <button
              onClick={() => setCollapsed(true)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              title="Thu nhỏ"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>

          {/* Tab 1: Time of Day */}
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
                          ? "bg-orange-50 border-orange-500 text-orange-700 font-bold shadow-sm"
                          : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                      }`}
                    >
                      <span>{t.icon}</span>
                      <span>{t.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Tab 2: Camera Modes */}
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
                          ? "bg-orange-50 border-orange-500 text-orange-700 font-bold shadow-sm"
                          : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-1.5 text-xs font-bold">
                        {c.icon}
                        <span>{c.label}</span>
                      </div>
                      <span className="text-[10px] text-slate-400 mt-0.5 line-clamp-1">{c.desc}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Tab 3: Car Selection */}
          {activeTab === "car" && (
            <div className="py-3 space-y-2">
              <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 block font-semibold">
                CHỌN XE ĐỂ THEO DÕI
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
                          ? "bg-orange-50 border-orange-500 text-orange-700 font-bold shadow-sm"
                          : "bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span
                          className="w-3.5 h-3.5 rounded-full border border-slate-300 shadow-sm"
                          style={{ backgroundColor: car.color }}
                        />
                        <span className="font-bold">{car.name}</span>
                      </div>
                      <span className="text-[10px] text-slate-500 font-mono">{car.type}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* Bottom Bar */}
          <div className="pt-2.5 mt-1 border-t border-slate-100 flex items-center justify-between text-xs">
            <div className="flex items-center gap-1.5">
              <button
                onClick={onTogglePause}
                className={`p-1.5 rounded-lg border transition-all ${
                  isPaused
                    ? "bg-amber-100 text-amber-700 border-amber-300"
                    : "bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200"
                }`}
                title={isPaused ? "Tiếp tục chạy" : "Tạm dừng xe"}
              >
                {isPaused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
              </button>

              <div className="flex items-center gap-0.5 bg-slate-100 p-0.5 rounded-lg border border-slate-200">
                {[0.5, 1.0, 1.8].map((s) => (
                  <button
                    key={s}
                    onClick={() => onSpeedChange(s)}
                    className={`px-2 py-0.5 rounded text-[10px] font-mono transition-all ${
                      trafficSpeed === s ? "bg-orange-500 text-white font-bold" : "text-slate-500 hover:text-slate-800"
                    }`}
                  >
                    {s}x
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-1.5 text-[10px] font-mono text-emerald-600 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
              <span>VÒNG LẶP VÔ TẬN</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
