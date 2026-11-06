import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { HomePage } from "./pages/HomePage";
import { CityExperiencePage } from "./pages/CityExperiencePage";
import { CarsInventoryPage } from "./pages/CarsInventoryPage";
import { CarDetailPage } from "./pages/CarDetailPage";
import { AboutPage } from "./pages/AboutPage";

const ScrollToTop: React.FC = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <div className="min-h-screen flex flex-col bg-white text-slate-800 selection:bg-orange-500 selection:text-white">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/city-experience" element={<CityExperiencePage />} />
            <Route path="/cars" element={<CarsInventoryPage />} />
            <Route path="/cars/:id" element={<CarDetailPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
};

export default App;
