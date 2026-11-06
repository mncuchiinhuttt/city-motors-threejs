import React, { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { CityCanvas } from "../components/CityCanvas";
import { CornerSceneController } from "../components/CornerSceneController";
import { CARS_DATA } from "../data/cars";
import { ExtendedCameraMode, TimeOfDay } from "../types";
import { Car, Compass, ArrowRight, Palette } from "lucide-react";

export const CityExperiencePage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialCar = searchParams.get("car") || "Car_BlueCoupe";

  const [timeOfDay, setTimeOfDay] = useState<TimeOfDay>("day");
  const [cameraPreset, setCameraPreset] = useState<ExtendedCameraMode>("chase");
  const [activeCarId, setActiveCarId] = useState<string>(initialCar);
  const [trafficSpeed, setTrafficSpeed] = useState<number>(1.0);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [customColor, setCustomColor] = useState<{ carId: string; colorHex: string } | undefined>(undefined);

  useEffect(() => {
    const carParam = searchParams.get("car");
    if (carParam) {
      setActiveCarId(carParam);
      setCameraPreset("chase");
    }
  }, [searchParams]);

  const selectedCarSpec = CARS_DATA.find((c) => c.blenderModelId === activeCarId) || CARS_DATA[0];

  return (
    <div className="relative w-full h-screen overflow-hidden bg-slate-100">
      {/* 3D City & Mountain Pass Canvas */}
      <div className="absolute inset-0 z-0">
        <CityCanvas
          timeOfDay={timeOfDay}
          cameraPreset={cameraPreset}
          activeCarId={activeCarId}
          onSelectCar={(id) => {
            setActiveCarId(id);
            setCameraPreset("chase");
          }}
          customCarColor={customColor}
          trafficSpeed={trafficSpeed}
          isPaused={isPaused}
        />
      </div>

      {/* Top Floating Header HUD */}
      <div className="absolute top-20 left-4 right-4 z-20 pointer-events-none flex items-center justify-between gap-4">
        {/* Car Name & Mode Tag */}
        <div className="pointer-events-auto p-3 px-4 rounded-2xl bg-white/95 backdrop-blur-md border border-slate-200 text-slate-800 shadow-md flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-orange-500 text-white flex items-center justify-center font-bold">
            <Car className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm text-slate-900">{selectedCarSpec.name}</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-orange-50 text-orange-700 border border-orange-200 font-bold uppercase">
                {cameraPreset === "chase"
                  ? "Camera Theo Đuôi"
                  : cameraPreset === "hood"
                  ? "Góc Nhìn Lái"
                  : cameraPreset === "mountain"
                  ? "Đỉnh Đèo Núi"
                  : cameraPreset}
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              {activeCarId === "Car_BlueCoupe" || activeCarId === "Car_WhiteVan"
                ? "Đang vượt cung đường đèo núi & khúc cua quanh co"
                : "Đang tuần hoàn trong đại lộ trung tâm đô thị"}
            </p>
          </div>
        </div>

        {/* Live Status Pill */}
        <div className="pointer-events-auto hidden sm:flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/95 backdrop-blur-md border border-slate-200 text-xs shadow-md font-mono text-slate-700">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
          <span>VÒNG LẶP VÔ TẬN:</span>
          <span className="text-orange-600 font-bold uppercase">{timeOfDay}</span>
        </div>
      </div>

      {/* Left Bottom Floating HUD: Live Selected Car Specs & Color Customizer */}
      <div className="absolute bottom-6 left-6 z-20 pointer-events-none max-w-sm w-full hidden md:block">
        <div className="pointer-events-auto bg-white/95 backdrop-blur-xl border border-slate-200 p-5 rounded-3xl shadow-xl text-slate-800 space-y-4">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-orange-600 font-bold">
                XE ĐANG THEO DÕI
              </span>
              <h3 className="text-xl font-bold font-display text-slate-900">{selectedCarSpec.name}</h3>
              <p className="text-xs text-slate-500 mt-0.5">{selectedCarSpec.subtitle}</p>
            </div>
            <div className="text-right">
              <span className="text-xl font-black font-display text-orange-600">
                ${selectedCarSpec.price.toLocaleString()}
              </span>
              <p className="text-[10px] text-slate-400">giá bán lẻ</p>
            </div>
          </div>

          {/* Telemetry Specs */}
          <div className="grid grid-cols-3 gap-2 py-2.5 px-3 rounded-2xl bg-slate-50 border border-slate-200 text-center">
            <div>
              <span className="text-[10px] text-slate-500">Công suất</span>
              <p className="text-xs font-mono font-bold text-slate-900 mt-0.5">{selectedCarSpec.horsepower} HP</p>
            </div>
            <div className="border-x border-slate-200">
              <span className="text-[10px] text-slate-500">0-100</span>
              <p className="text-xs font-mono font-bold text-slate-900 mt-0.5">{selectedCarSpec.acceleration}</p>
            </div>
            <div>
              <span className="text-[10px] text-slate-500">Tốc độ max</span>
              <p className="text-xs font-mono font-bold text-slate-900 mt-0.5">{selectedCarSpec.topSpeed} km/h</p>
            </div>
          </div>

          {/* Color Customizer */}
          <div className="space-y-1.5 pt-1">
            <span className="text-xs text-slate-600 flex items-center gap-1.5 font-medium">
              <Palette className="w-3.5 h-3.5 text-orange-500" />
              <span>Đổi màu sơn 3D thời gian thực:</span>
            </span>
            <div className="flex items-center gap-2">
              {selectedCarSpec.colors.map((c) => (
                <button
                  key={c.name}
                  onClick={() => setCustomColor({ carId: selectedCarSpec.blenderModelId, colorHex: c.hex })}
                  className="w-6 h-6 rounded-full border-2 border-slate-300 hover:border-orange-500 hover:scale-110 transition-all shadow-sm"
                  style={{ backgroundColor: c.hex }}
                  title={c.name}
                />
              ))}
              {["#f97316", "#0284c7", "#10b981", "#1e293b"].map((hex) => (
                <button
                  key={hex}
                  onClick={() => setCustomColor({ carId: selectedCarSpec.blenderModelId, colorHex: hex })}
                  className="w-6 h-6 rounded-full border border-slate-300 hover:border-orange-500 hover:scale-110 transition-all shadow-sm"
                  style={{ backgroundColor: hex }}
                  title="Màu tùy chỉnh"
                />
              ))}
            </div>
          </div>

          {/* Action Link */}
          <div className="pt-1">
            <Link
              to={`/cars/${selectedCarSpec.id}`}
              className="w-full flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-xl text-xs font-bold bg-orange-500 hover:bg-orange-600 text-white transition-colors shadow-md shadow-orange-500/20"
            >
              <span>Xem chi tiết & Đặt mua xe</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* Floating Controller Docked in the Corner ("Khúc ở góc để đổi") */}
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
    </div>
  );
};
