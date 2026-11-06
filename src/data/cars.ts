import { CarSpec } from "../types";

export const CARS_DATA: CarSpec[] = [
  {
    id: "apex-gt90",
    name: "Apex GT-90",
    subtitle: "Cyberpunk Sports Coupe thuần điện",
    category: "sports",
    price: 89900,
    monthlyPayment: 1250,
    horsepower: 650,
    acceleration: "2.8s",
    topSpeed: 310,
    range: "580 km",
    drivetrain: "Dual-Motor AWD",
    colors: [
      { name: "Neon Blue", hex: "#0077ff" },
      { name: "Cyber Violet", hex: "#8800ff" },
      { name: "Stealth Black", hex: "#111115" },
      { name: "Hyper Red", hex: "#ff1133" }
    ],
    blenderModelId: "Car_BlueCoupe",
    description: "Mẫu siêu xe thể thao thuần điện với thiết kế khí động học góc cạnh, hệ thống đèn pha LED Matrix và khả năng tăng tốc tức thì từ 0 lên 100km/h chỉ trong 2.8 giây.",
    features: [
      "Hệ dẫn động 4 bánh toàn thời gian Dual-Motor",
      "Khung gầm hợp kim nhôm - carbon siêu nhẹ",
      "Màn hình cong OLED 16 inch điều khiển trung tâm",
      "Hệ thống tự lái cấp độ 3 với radar LiDAR đa hướng"
    ],
    inStock: true
  },
  {
    id: "horizon-metro",
    name: "Horizon Metro Sedan",
    subtitle: "Sedan đô thị thanh lịch & êm ái",
    category: "sedan",
    price: 34500,
    monthlyPayment: 520,
    horsepower: 240,
    acceleration: "6.4s",
    topSpeed: 215,
    range: "750 km",
    drivetrain: "Front-Wheel Drive",
    colors: [
      { name: "Crimson Red", hex: "#cc1122" },
      { name: "Pearl White", hex: "#eeeeee" },
      { name: "Metallic Grey", hex: "#555560" },
      { name: "Midnight Navy", hex: "#0f2040" }
    ],
    blenderModelId: "Car_RedSedan",
    description: "Lựa chọn hoàn hảo cho gia đình và công việc hàng ngày trong đô thị. Động cơ Turbo tiết kiệm nhiên liệu, không gian cabin rộng rãi cách âm chủ động.",
    features: [
      "Hệ thống hỗ trợ giữ làn và cảnh báo điểm mù thông minh",
      "Nội thất bọc da Nappa cao cấp kết hợp gỗ ốp tự nhiên",
      "Cửa sổ trời toàn cảnh Panorama chống tia UV",
      "Âm thanh vòm 12 loa Harman Kardon"
    ],
    inStock: true
  },
  {
    id: "cybercab-pro",
    name: "CyberCab Pro",
    subtitle: "Dòng xe dịch vụ & taxi thông minh thế hệ mới",
    category: "commercial",
    price: 38000,
    monthlyPayment: 580,
    horsepower: 210,
    acceleration: "7.1s",
    topSpeed: 185,
    range: "520 km",
    drivetrain: "Rear-Wheel Drive",
    colors: [
      { name: "Classic Taxi Yellow", hex: "#f5b700" },
      { name: "Fleet White", hex: "#f0f2f5" },
      { name: "Executive Black", hex: "#1a1a1a" }
    ],
    blenderModelId: "Car_Taxi",
    description: "Được thiết kế tối ưu cho tần suất hoạt động 24/7 trong thành phố với chi phí vận hành siêu thấp, khung gầm siêu bền và đèn nóc nhận diện từ xa.",
    features: [
      "Bộ pin LFP chu kỳ 5.000 lần sạc bảo hành 8 năm",
      "Kính ngăn cabin kháng khuẩn và hệ thống thanh toán tự động",
      "Khoang hành lý rộng 620L thoải mái cho vali cỡ lớn",
      "Bản đồ điều hướng vệ tinh cập nhật mật độ giao thông theo thời gian thực"
    ],
    inStock: true
  },
  {
    id: "titan-cargo-van",
    name: "Titan Cargo Van",
    subtitle: "Xe vận tải đô thị không phát thải",
    category: "commercial",
    price: 46000,
    monthlyPayment: 690,
    horsepower: 320,
    acceleration: "8.5s",
    topSpeed: 160,
    range: "460 km",
    drivetrain: "Dual-Motor AWD",
    colors: [
      { name: "Polar White", hex: "#f8f9fa" },
      { name: "Industrial Slate", hex: "#495057" },
      { name: "Safety Orange", hex: "#f76707" }
    ],
    blenderModelId: "Car_WhiteVan",
    description: "Giải pháp giao hàng logistics chặng cuối thông minh. Sức chứa khoang hàng lên đến 14m³, sàn tải thấp dễ bốc xếp và sạc nhanh 20-80% trong 25 phút.",
    features: [
      "Tải trọng hàng hóa tối đa 1.800 kg",
      "Camera 360 độ hỗ trợ lùi chuồng trong ngõ hẹp",
      "Cổng sạc DC công suất cao 150kW",
      "Hệ thống quản lý đội xe thông minh qua Cloud API"
    ],
    inStock: true
  }
];
