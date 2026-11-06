import React from "react";
import { Compass, Cpu, Cloud, MapPin, Phone, Mail, CheckCircle } from "lucide-react";

export const AboutPage: React.FC = () => {
  return (
    <div className="pt-24 pb-20 min-h-screen bg-slate-50 text-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        {/* Header */}
        <div className="max-w-3xl">
          <span className="text-xs font-mono font-bold text-orange-700 uppercase tracking-wider px-3 py-1 rounded-md bg-orange-50 border border-orange-200">
            SHOWROOM THẾ HỆ MỚI
          </span>
          <h1 className="text-3xl sm:text-5xl font-black font-display text-slate-900 mt-4 tracking-tight">
            VỀ CYBERCITY MOTORS
          </h1>
          <p className="text-base text-slate-600 mt-3 font-normal leading-relaxed">
            Chúng tôi tiên phong ứng dụng công nghệ 3D mô phỏng thời gian thực (Real-time WebGL) vào trải nghiệm xem xe và mua sắm ô tô trực tuyến tại Việt Nam.
          </p>
        </div>

        {/* Tech Stack Behind The Experience */}
        <div className="bg-white p-8 sm:p-10 rounded-3xl border border-slate-200 shadow-sm space-y-8">
          <div>
            <h3 className="font-display font-bold text-2xl text-slate-900">Kiến trúc Công nghệ Đằng Sau Trải Nghiệm</h3>
            <p className="text-xs text-slate-500 mt-1">Sự kết hợp giữa 3D Modeling Blender, Three.js và Cloudflare Global Network</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 border border-orange-200 flex items-center justify-center font-bold">
                <Cpu className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-slate-900 text-base">Blender 5.2 & Python Scripting</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Tất cả các tòa nhà, đường xá, cung đường đèo núi và 4 dòng xe đều được dựng bằng Blender với pipeline low-poly tối ưu, xuất chuẩn glTF/GLB siêu nhẹ.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 border border-orange-200 flex items-center justify-center font-bold">
                <Compass className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-slate-900 text-base">Three.js & WebGL 2.0</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Render 60fps mượt mà trên trình duyệt với đổ bóng mềm PCFSoftShadow, tone mapping ACESFilmic, chuyển cảnh ánh sáng và xe tự động chạy theo quỹ đạo spline vô tận.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-orange-50 text-orange-600 border border-orange-200 flex items-center justify-center font-bold">
                <Cloud className="w-5 h-5" />
              </div>
              <h4 className="font-bold text-slate-900 text-base">Bun & Cloudflare Workers</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Được build và tối ưu bằng Bun runtime siêu tốc, phục vụ qua mạng lưới Edge Network hơn 300 thành phố của Cloudflare Workers với độ trễ dưới 10ms.
              </p>
            </div>
          </div>
        </div>

        {/* Showroom Physical Experience & Warranties */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-display font-bold text-xl text-slate-900">Cam kết Chất lượng & Dịch vụ</h3>
            <ul className="space-y-3 text-xs text-slate-600">
              <li className="flex items-start gap-2.5">
                <CheckCircle className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                <span>Bảo hành xe và pin động cơ điện lên đến 8 năm hoặc 160.000 km.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                <span>Cứu hộ giao thông 24/7 và hỗ trợ sạc pin lưu động khẩn cấp miễn phí.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                <span>Chính sách đổi trả trong 7 ngày đầu nếu không hài lòng về trải nghiệm.</span>
              </li>
              <li className="flex items-start gap-2.5">
                <CheckCircle className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                <span>Hỗ trợ thủ tục đăng ký xe, đăng kiểm và giao xe tận nhà trên toàn quốc.</span>
              </li>
            </ul>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-display font-bold text-xl text-slate-900">Địa điểm Showroom Flagship</h3>
            <div className="space-y-3 text-xs text-slate-600">
              <div className="flex items-start gap-2.5">
                <MapPin className="w-4 h-4 text-orange-500 shrink-0 mt-0.5" />
                <span>Đại lộ Ánh Sáng, Khu Công nghệ Cao, TP. Thủ Đức, TP. Hồ Chí Minh</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Phone className="w-4 h-4 text-orange-500 shrink-0" />
                <span>Hotline: 1900 888 999 - (028) 7777 9999</span>
              </div>
              <div className="flex items-center gap-2.5">
                <Mail className="w-4 h-4 text-orange-500 shrink-0" />
                <span>Email: showroom@cybercity-motors.vn</span>
              </div>
              <p className="text-slate-400 text-[11px] pt-2">
                Thời gian mở cửa: Thứ Hai - Chủ Nhật, từ 08:00 đến 21:00 hàng ngày.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
