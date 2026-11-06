export type TimeOfDay = "day" | "sunset" | "night" | "cyberpunk";

export type SceneMode = "city" | "mountain";

export type SimpleCameraMode = "close" | "wide";

export interface CarSpec {
  id: string;
  name: string;
  subtitle: string;
  category: "sports" | "sedan" | "commercial" | "electric";
  price: number;
  monthlyPayment: number;
  horsepower: number;
  acceleration: string;
  topSpeed: number;
  range: string;
  drivetrain: string;
  colors: { name: string; hex: string }[];
  blenderModelId: "Car_BlueCoupe" | "Car_RedSedan" | "Car_Taxi" | "Car_WhiteVan";
  description: string;
  features: string[];
  inStock: boolean;
}
