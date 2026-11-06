export type TimeOfDay = "day" | "sunset" | "night" | "cyberpunk";

export type ExtendedCameraMode =
  | "chase"
  | "hood"
  | "drone"
  | "street"
  | "mountain"
  | "isometric"
  | "topdown";

export interface CarSpec {
  id: string;
  name: string;
  subtitle: string;
  category: "sports" | "sedan" | "commercial" | "electric";
  price: number;
  monthlyPayment: number;
  horsepower: number;
  acceleration: string; // 0-100 km/h
  topSpeed: number; // km/h
  range: string;
  drivetrain: string;
  colors: { name: string; hex: string }[];
  blenderModelId: "Car_BlueCoupe" | "Car_RedSedan" | "Car_Taxi" | "Car_WhiteVan";
  description: string;
  features: string[];
  inStock: boolean;
}
