import React from "react";
import { Sun, Sunset, Moon, Zap, Video, Eye, Compass, Pause, Play, Gauge } from "lucide-react";
import { CameraPreset, TimeOfDay } from "../types";

interface TimeControllerProps {
  timeOfDay: TimeOfDay;
  onTimeChange: (time: TimeOfDay) => void;
  cameraPreset: CameraPreset;
  onCameraChange: (preset: CameraPreset) => void;
  trafficSpeed: number;
  onSpeedChange: (speed: number) => void;
  isPaused: boolean;
  onTogglePause: () => void;
}

export const TimeController: React.FC<TimeControllerProps> = ({
  timeOfDay,
  onTimeChange,
  cameraPreset,
  onCameraChange,
  trafficSpeed,
  onSpeedChange,
  isPaused,
  onTogglePause
}) => {
  const times: { id: TimeOfDay; label: string; icon: React.ReactNode; color: string }[] = [
    { id: "day", label: "Ban ngày", icon: <Sun className="w-4 h-4" />, color: "hover:text-amber-300" },
    { id: "sunset", label: "Hoàng hôn", icon: <Sunset className="w-4 h-4" />, color: "hover:text-orange-400" },
    { id: "night", label: "Ban đêm", icon: <Moon className="w-4 h-4" />, color: "hover:text-indigo-400" },
    { id: "cyberpunk", label: "Cyberpunk", icon: <Zap className="w-4 h-4" />, color: "hover:text-cyan-400" }
  ];

  const cameras: { id: CameraPreset; label: string; icon: React.ReactNode }[] = [
    { id: "isometric", label: "Toàn cảnh", icon: <Compass className="w-4 h-4" /> },
    { id: "street", label: "Góc phố", icon: <Eye className="w-4 h-4" /> },
    { id: "follow", label: "Bám xe", icon: <Video className="w-4 h-4" /> },
    { id: "topdown", label: "Trên cao", icon: <Gauge className="w-4 h-4" /> }
  ];

  return (
    <div className="flex flex-col md:flex-row items-center gap-3 bg-slate-900/85 backdrop-blur-xl border border-slate-700/60 p-2.5 rounded-2xl shadow-2xl text-slate-200 text-xs">
      {/* Time of Day Modes */}
      <div className="flex items-center gap-1 bg-slate-950/70 p-1 rounded-xl border border-slate-800">
        {times.map((t) => {
          const active = timeOfDay === t.id;
          return (
            <button
              key={t.id}
              onClick={() => onTimeChange(t.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                active
                  ? "bg-cyan-500 text-slate-950 font-bold shadow-lg shadow-cyan-500/25"
                  : `text-slate-400 hover:bg-slate-800/80 ${t.color}`
              }`}
            >
              {t.icon}
              <span className="hidden sm:inline">{t.label}</span>
            </button>
          );
        })}
      </div>

      <div className="hidden md:block w-px h-6 bg-slate-800" />

      {/* Camera Presets */}
      <div className="flex items-center gap-1 bg-slate-950/70 p-1 rounded-xl border border-slate-800">
        {cameras.map((c) => {
          const active = cameraPreset === c.id;
          return (
            <button
              key={c.id}
              onClick={() => onCameraChange(c.id)}
              className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg transition-all ${
                active
                  ? "bg-slate-700 text-cyan-300 font-semibold border border-cyan-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
              title={c.label}
            >
              {c.icon}
              <span className="hidden sm:inline">{c.label}</span>
            </button>
          );
        })}
      </div>

      <div className="hidden md:block w-px h-6 bg-slate-800" />

      {/* Traffic Controls */}
      <div className="flex items-center gap-2 px-1">
        <button
          onClick={onTogglePause}
          className={`p-1.5 rounded-lg border transition-all ${
            isPaused
              ? "bg-amber-500/20 text-amber-400 border-amber-500/40"
              : "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700"
          }`}
          title={isPaused ? "Tiếp tục chạy" : "Tạm dừng giao thông"}
        >
          {isPaused ? <Play className="w-4 h-4" /> : <Pause className="w-4 h-4" />}
        </button>

        <div className="flex items-center gap-1 bg-slate-950/70 p-1 rounded-lg border border-slate-800">
          {[0.5, 1.0, 1.8].map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-2 py-1 rounded text-[11px] font-mono transition-all ${
                trafficSpeed === s ? "bg-cyan-500/20 text-cyan-300 font-bold" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
