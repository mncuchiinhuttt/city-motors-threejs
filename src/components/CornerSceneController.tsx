import React, { useState } from "react";
import {
  Sun,
  Sunset,
  Moon,
  Zap,
  Video,
  Globe,
  Play,
  Pause,
  Mountain,
  Building2,
  ChevronDown,
  ChevronUp,
  Sparkles
} from "lucide-react";
import { SceneMode, SimpleCameraMode, TimeOfDay } from "../types";

interface CornerSceneControllerProps {
  sceneMode: SceneMode;
  onSceneChange: (scene: SceneMode) => void;
  timeOfDay: TimeOfDay;
  onTimeChange: (time: TimeOfDay) => void;
  cameraMode: SimpleCameraMode;
  onCameraChange: (camera: SimpleCameraMode) => void;
  trafficSpeed: number;
  onSpeedChange: (speed: number) => void;
  isPaused: boolean;
  onTogglePause: () => void;
}

export const CornerSceneController: React.FC<CornerSceneControllerProps> = ({
  sceneMode,
  onSceneChange,
  timeOfDay,
  onTimeChange,
  cameraMode,
  onCameraChange,
  trafficSpeed,
  onSpeedChange,
  isPaused,
  onTogglePause
}) => {
  const [collapsed, setCollapsed] = useState<boolean>(false);

  const timeOptions: { id: TimeOfDay; label: string; icon: React.ReactNode }[] = [
    { id: "day", label: "Ban ngày", icon: <Sun className="w-3.5 h-3.5 text-amber-500" /> },
    { id: "sunset", label: "Hoàng hôn", icon: <Sunset className="w-3.5 h-3.5 text-orange-500" /> },
    { id: "night", label: "Ban đêm", icon: <Moon className="w-3.5 h-3.5 text-indigo-500" /> },
    { id: "cyberpunk", label: "Cyberpunk", icon: <Zap className="w-3.5 h-3.5 text-cyan-500" /> }
  ];

  return (
    <div className="fixed bottom-6 right-6 z-30 flex flex-col items-end">
      {collapsed ? (
        <button
          onClick={() => setCollapsed(false)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-white border border-slate-200 text-slate-800 font-bold text-xs shadow-xl hover:bg-slate-50 transition-all hover:scale-105"
        >
          <Sparkles className="w-4 h-4 text-orange-500" />
          <span>Bảng điều khiển 3D</span>
          <ChevronUp className="w-4 h-4 text-slate-400" />
        </button>
      ) : (
        <div className="w-[310px] sm:w-[340px] rounded-3xl p-4 bg-white/95 backdrop-blur-xl border border-slate-200 shadow-2xl text-slate-800 transition-all space-y-3.5">
          {/* Header */}
          <div className="flex items-center justify-between pb-2 border-b border-slate-100">
            <div className="flex items-center gap-1.5">
              <Sparkles className="w-4 h-4 text-orange-500" />
              <span className="font-display font-bold text-xs uppercase tracking-wider text-slate-900">
                ĐIỀU KHIỂN KHUNG CẢNH 3D
              </span>
            </div>

            <button
              onClick={() => setCollapsed(true)}
              className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
              title="Thu nhỏ"
            >
              <ChevronDown className="w-4 h-4" />
            </button>
          </div>

          {/* 1. CHỌN SCENE: THÀNH PHỐ vs ĐÈO NÚI (Yêu cầu chính của user) */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
              CHỌN KHU VỰC TRẢI NGHIỆM
            </span>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => onSceneChange("mountain")}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                  sceneMode === "mountain"
                    ? "bg-orange-500 text-white border-orange-500 shadow-sm"
                    : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                }`}
              >
                <Mountain className="w-4 h-4" />
                <span>Cung đường núi</span>
              </button>
              <button
                onClick={() => onSceneChange("city")}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                  sceneMode === "city"
                    ? "bg-orange-500 text-white border-orange-500 shadow-sm"
                    : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                }`}
              >
                <Building2 className="w-4 h-4" />
                <span>Thành phố đô thị</span>
              </button>
            </div>
          </div>

          {/* 2. GÓC CAMERA: CHỈ CÓ GÓC GẦN VỚI GÓC RỘNG (Yêu cầu chính của user) */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
              GÓC QUAY CAMERA
            </span>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => onCameraChange("close")}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                  cameraMode === "close"
                    ? "bg-orange-500 text-white border-orange-500 shadow-sm"
                    : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                }`}
              >
                <Video className="w-4 h-4" />
                <span>Góc gần (Theo xe)</span>
              </button>
              <button
                onClick={() => onCameraChange("wide")}
                className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border text-xs font-bold transition-all ${
                  cameraMode === "wide"
                    ? "bg-orange-500 text-white border-orange-500 shadow-sm"
                    : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                }`}
              >
                <Globe className="w-4 h-4" />
                <span>Góc rộng (Toàn cảnh)</span>
              </button>
            </div>
          </div>

          {/* 3. THỜI TIẾT / ÁNH SÁNG */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-500 font-bold block">
              ÁNH SÁNG THỜI TIẾT
            </span>
            <div className="grid grid-cols-2 gap-1.5">
              {timeOptions.map((t) => {
                const active = timeOfDay === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => onTimeChange(t.id)}
                    className={`flex items-center gap-1.5 py-1.5 px-2.5 rounded-xl border text-[11px] font-semibold transition-all ${
                      active
                        ? "bg-orange-50 border-orange-500 text-orange-700 font-bold"
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

          {/* 4. TỐC ĐỘ VẬN HÀNH & VÒNG LẶP VÔ TẬN */}
          <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
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
