import React, { useState } from "react";
import { CarCard } from "../components/CarCard";
import { CARS_DATA } from "../data/cars";
import { Search, Sparkles } from "lucide-react";

export const CarsInventoryPage: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const categories = [
    { id: "all", label: "Tất cả các dòng xe" },
    { id: "sports", label: "Siêu xe thể thao" },
    { id: "sedan", label: "Sedan đô thị" },
    { id: "commercial", label: "Xe vận tải & Dịch vụ" }
  ];

  const filteredCars = CARS_DATA.filter((car) => {
    const matchesCategory = selectedCategory === "all" || car.category === selectedCategory;
    const matchesSearch =
      car.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      car.subtitle.toLowerCase().includes(searchQuery.toLowerCase()) ||
      car.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="pt-24 pb-20 min-h-screen bg-slate-50 text-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="max-w-2xl mb-10">
          <div className="flex items-center gap-2 text-orange-600 text-xs font-mono font-bold uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span>Showroom Online 2026</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-black font-display text-slate-900 tracking-tight">
            DANH MỤC CÁC DÒNG XE
          </h1>
          <p className="text-sm text-slate-600 mt-2 font-normal">
            Tất cả mẫu xe đều được dựng 3D chi tiết với Blender và tối ưu hóa hiển thị thời gian thực trên Three.js.
          </p>
        </div>

        {/* Filter & Search Bar */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 mb-10 bg-white p-3 rounded-2xl border border-slate-200 shadow-sm">
          {/* Categories */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-2 md:pb-0">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                  selectedCategory === cat.id
                    ? "bg-orange-500 text-white font-bold shadow-md shadow-orange-500/20"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Search Input */}
          <div className="relative min-w-[260px]">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Tìm kiếm theo tên xe..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-orange-500 transition-colors"
            />
          </div>
        </div>

        {/* Grid of Cars */}
        {filteredCars.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredCars.map((car) => (
              <CarCard key={car.id} car={car} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <p className="text-slate-500 text-base">Không tìm thấy mẫu xe nào phù hợp với từ khóa.</p>
            <button
              onClick={() => {
                setSelectedCategory("all");
                setSearchQuery("");
              }}
              className="mt-4 px-4 py-2 rounded-xl text-xs font-bold bg-orange-500 text-white hover:bg-orange-600"
            >
              Đặt lại bộ lọc
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
