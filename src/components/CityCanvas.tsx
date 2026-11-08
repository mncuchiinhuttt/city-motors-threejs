import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { SceneMode, SimpleCameraMode, TimeOfDay } from "../types";

interface CityCanvasProps {
  sceneMode?: SceneMode;
  timeOfDay?: TimeOfDay;
  cameraMode?: SimpleCameraMode;
  trafficSpeed?: number;
  isPaused?: boolean;
  enableZoom?: boolean;
}

export const CityCanvas: React.FC<CityCanvasProps> = ({
  sceneMode = "mountain",
  timeOfDay = "day",
  cameraMode = "close",
  trafficSpeed = 1.0,
  isPaused = false,
  enableZoom = false
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);

  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  const currentModelRef = useRef<THREE.Object3D | null>(null);

  const heroCarRef = useRef<{
    object: THREE.Object3D;
    curve: THREE.CatmullRomCurve3;
    progress: number;
    speed: number;
    wheels: THREE.Object3D[];
    headlights: THREE.SpotLight[];
  } | null>(null);

  const lightsRef = useRef<{
    sun: THREE.DirectionalLight;
    ambient: THREE.AmbientLight;
    moon: THREE.DirectionalLight;
    sunMesh: THREE.Mesh;
    streetlights: THREE.PointLight[];
  } | null>(null);

  const windowMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const streetlampMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const starsRef = useRef<THREE.Points | null>(null);

  const propsRef = useRef({ sceneMode, timeOfDay, cameraMode, trafficSpeed, isPaused });
  useEffect(() => {
    propsRef.current = { sceneMode, timeOfDay, cameraMode, trafficSpeed, isPaused };
  }, [sceneMode, timeOfDay, cameraMode, trafficSpeed, isPaused]);

  // --- Splines for Mountain and City Circuits ---
  // In Three.js coordinates: Y is UP, Z is depth!
  // Mountain Pass Circuit: Climbs up from Y=0.35m to peak Y=5.15m and loops around peaks
  const mtnPoints = [
    new THREE.Vector3( -6.0, 0.35,  22.0),
    new THREE.Vector3(  8.0, 0.65,  22.0),
    new THREE.Vector3( 22.0, 1.55,  16.0),
    new THREE.Vector3( 26.0, 2.55,   7.0),
    new THREE.Vector3( 18.0, 3.45,  -2.0), // S-curve cutting inward
    new THREE.Vector3( 24.0, 4.45, -12.0),
    new THREE.Vector3( 26.0, 5.25, -20.0), // Mountain Summit Overlook
    new THREE.Vector3( 16.0, 4.45, -26.0), // Hairpin turn
    new THREE.Vector3(  4.0, 3.45, -26.0),
    new THREE.Vector3( -8.0, 2.45, -22.0),
    new THREE.Vector3(-18.0, 1.55, -14.0),
    new THREE.Vector3(-24.0, 0.85,  -4.0),
    new THREE.Vector3(-24.0, 0.45,   8.0),
    new THREE.Vector3(-16.0, 0.35,  18.0),
    new THREE.Vector3( -6.0, 0.35,  22.0)
  ];
  const mountainCurve = new THREE.CatmullRomCurve3(mtnPoints, true, "catmullrom", 0.15);

  // City Loop Circuit
  const cityPoints = [
    new THREE.Vector3( 0.0, 0.20,  34.0),
    new THREE.Vector3( 0.0, 0.20,  15.0),
    new THREE.Vector3( 0.0, 0.20, -15.0),
    new THREE.Vector3( 0.0, 0.20, -32.0),
    new THREE.Vector3( 0.0, 0.20,  34.0)
  ];
  const cityCurve = new THREE.CatmullRomCurve3(cityPoints, true, "catmullrom", 0.15);

  // Initialize Scene, Renderer, and Camera once
  useEffect(() => {
    if (!mountRef.current) return;
    const container = mountRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbfe0f7);
    scene.fog = new THREE.Fog(0xd8ecfa, 45, 170);
    sceneRef.current = scene;

    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.4, 500);
    camera.position.set(0, 8, 20);
    cameraRef.current = camera;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = enableZoom; // FIX: Zoom disabled so mouse wheel scrolls page naturally!
    controls.maxPolarAngle = Math.PI / 2 - 0.04;
    controlsRef.current = controls;

    // Celestial Sun Orb
    const sunGeo = new THREE.SphereGeometry(3.5, 16, 16);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfff4aa });
    const sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunMesh.position.set(45, 65, 35);
    scene.add(sunMesh);

    // Starfield for night
    const starCount = 600;
    const starGeo = new THREE.BufferGeometry();
    const starPos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i += 3) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 220;
      starPos[i] = r * Math.sin(phi) * Math.cos(theta);
      starPos[i + 1] = Math.abs(r * Math.cos(phi)) + 15;
      starPos[i + 2] = r * Math.sin(phi) * Math.sin(theta);
    }
    starGeo.setAttribute("position", new THREE.BufferAttribute(starPos, 3));
    const starMat = new THREE.PointsMaterial({ color: 0xffffff, size: 1.4, transparent: true, opacity: 0.8 });
    const stars = new THREE.Points(starGeo, starMat);
    stars.visible = false;
    scene.add(stars);
    starsRef.current = stars;

    // Atmospheric Sunlight
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.1);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfffaec, 2.6);
    sunLight.position.set(40, 60, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 5;
    sunLight.shadow.camera.far = 160;
    const d = 45;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0006;
    scene.add(sunLight);

    const moonLight = new THREE.DirectionalLight(0x7799cc, 0.0);
    moonLight.position.set(-30, 50, -30);
    scene.add(moonLight);

    lightsRef.current = {
      sun: sunLight,
      ambient: ambientLight,
      moon: moonLight,
      sunMesh,
      streetlights: []
    };

    // --- Animation & Chase Loop ---
    let animationFrameId: number;
    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = Math.min((currentTime - lastTime) / 1000, 0.1);
      lastTime = currentTime;

      const { cameraMode: curCam, trafficSpeed: curSpeed, isPaused: curPaused } = propsRef.current;

      const heroCar = heroCarRef.current;
      if (heroCar && !curPaused) {
        // Endless driving loop along curve
        heroCar.progress = (heroCar.progress + heroCar.speed * curSpeed * delta * 60) % 1.0;

        const pt = heroCar.curve.getPointAt(heroCar.progress);
        const tangent = heroCar.curve.getTangentAt(heroCar.progress).normalize();

        // Position car firmly on the road
        heroCar.object.position.copy(pt);

        // Smooth heading orientation along tangent
        const lookTarget = pt.clone().add(tangent);
        heroCar.object.lookAt(lookTarget);
        heroCar.object.rotateY(Math.PI);
        // Rotate wheels
        heroCar.wheels.forEach((w) => {
          w.rotation.x += delta * 20 * curSpeed;
        });

        // CAMERA PERSPECTIVE:
        if (curCam === "close") {
          // GÓC GẦN (CHASE CAM): Locked 7.5m behind car, 2.8m above road, looking 4.5m ahead
          const behind = tangent.clone().multiplyScalar(-7.5);
          const desiredCamPos = pt.clone().add(behind).add(new THREE.Vector3(0, 2.8, 0));
          camera.position.lerp(desiredCamPos, 0.12);

          const forwardLook = pt.clone().add(tangent.clone().multiplyScalar(4.5)).add(new THREE.Vector3(0, 0.9, 0));
          controls.target.lerp(forwardLook, 0.15);
        } else if (curCam === "wide") {
          // GÓC RỘNG (PANORAMIC OVERVIEW): High vantage point showing the whole mountain pass or city
          const wideCamPos = heroCar.curve === mountainCurve
            ? new THREE.Vector3(15, 35, 45)
            : new THREE.Vector3(0, 36, 42);
          camera.position.lerp(wideCamPos, 0.05);
          controls.target.lerp(new THREE.Vector3(0, 2.0, 0), 0.08);
        }
      }

      controls.update();
      renderer.render(scene, camera);
    };

    animationFrameId = requestAnimationFrame(animate);

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
      controls.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [enableZoom]);

  // --- Load Model based on active sceneMode (mountain or city) ---
  useEffect(() => {
    const scene = sceneRef.current;
    const camera = cameraRef.current;
    const controls = controlsRef.current;
    if (!scene || !camera || !controls) return;

    setLoading(true);

    // Remove old model if present
    if (currentModelRef.current) {
      scene.remove(currentModelRef.current);
      currentModelRef.current = null;
    }

    const glbUrl = sceneMode === "mountain" ? "/assets/mountain.glb" : "/assets/city.glb";
    const activeCurve = sceneMode === "mountain" ? mountainCurve : cityCurve;

    const loader = new GLTFLoader();
    loader.load(
      glbUrl,
      (gltf) => {
        const model = gltf.scene;
        scene.add(model);
        currentModelRef.current = model;

        windowMaterialsRef.current = [];
        streetlampMaterialsRef.current = [];

        let heroCarObj: THREE.Object3D | null = null;

        model.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.castShadow = true;
            child.receiveShadow = true;

            const mat = child.material as THREE.MeshStandardMaterial;
            if (mat) {
              if (mat.name.includes("Window") || mat.name.includes("Neon")) {
                if (!windowMaterialsRef.current.includes(mat)) {
                  windowMaterialsRef.current.push(mat);
                }
              }
              if (mat.name.includes("StreetlampGlow")) {
                if (!streetlampMaterialsRef.current.includes(mat)) {
                  streetlampMaterialsRef.current.push(mat);
                }
              }
            }
          }

          if (child.name === "Car_HeroOrange" || child.name === "Car_BlueCoupe" || (child.name.startsWith("Car_") && !heroCarObj)) {
            heroCarObj = child;
          }
        });

        if (heroCarObj) {
          const wheels: THREE.Object3D[] = [];
          heroCarObj.traverse((p) => {
            if (p.name.includes("Wheel")) wheels.push(p);
          });

          // Headlights
          const spotLeft = new THREE.SpotLight(0xfffae0, 6.0, 24, Math.PI / 5, 0.4, 1.2);
          spotLeft.position.set(-0.6, 0.6, 2.0);
          const targetLeft = new THREE.Object3D();
          targetLeft.position.set(-0.6, 0.0, 16.0);
          heroCarObj.add(targetLeft);
          spotLeft.target = targetLeft;
          heroCarObj.add(spotLeft);

          const spotRight = new THREE.SpotLight(0xfffae0, 6.0, 24, Math.PI / 5, 0.4, 1.2);
          spotRight.position.set(0.6, 0.6, 2.0);
          const targetRight = new THREE.Object3D();
          targetRight.position.set(0.6, 0.0, 16.0);
          heroCarObj.add(targetRight);
          spotRight.target = targetRight;
          heroCarObj.add(spotRight);

          heroCarRef.current = {
            object: heroCarObj,
            curve: activeCurve,
            progress: 0.05,
            speed: sceneMode === "mountain" ? 0.00032 : 0.00038,
            wheels,
            headlights: [spotLeft, spotRight]
          };

          // SNAP CAMERA IMMEDIATELY ON LOAD TO CLOSE CHASE VIEW!
          const initPt = activeCurve.getPointAt(0.05);
          const initTangent = activeCurve.getTangentAt(0.05).normalize();
          heroCarObj.position.copy(initPt);
          heroCarObj.lookAt(initPt.clone().add(initTangent));
          heroCarObj.rotateY(Math.PI);
          const initCam = initPt.clone().add(initTangent.clone().multiplyScalar(-7.5)).add(new THREE.Vector3(0, 2.8, 0));
          const initTarget = initPt.clone().add(initTangent.clone().multiplyScalar(4.5)).add(new THREE.Vector3(0, 0.9, 0));

          camera.position.copy(initCam);
          controls.target.copy(initTarget);
        }

        setLoading(false);
      },
      undefined,
      (err) => {
        console.error("Error loading scene GLB:", err);
        setLoading(false);
      }
    );
  }, [sceneMode]);

  // --- Dynamic Lighting & Atmosphere based on timeOfDay ---
  useEffect(() => {
    const scene = sceneRef.current;
    const lights = lightsRef.current;
    const heroCar = heroCarRef.current;
    if (!scene || !lights) return;

    if (timeOfDay === "day") {
      scene.background = new THREE.Color(0xb5daf5);
      scene.fog = new THREE.Fog(0xd4e9fa, 45, 170);

      lights.sun.intensity = 2.8;
      lights.sun.color.setHex(0xfffaec);
      lights.ambient.intensity = 1.1;
      lights.ambient.color.setHex(0xf0f6ff);
      lights.moon.intensity = 0;

      lights.sunMesh.visible = true;
      lights.sunMesh.position.set(45, 65, 35);
      (lights.sunMesh.material as THREE.MeshBasicMaterial).color.setHex(0xfff0aa);

      lights.streetlights.forEach((l) => (l.intensity = 0));
      if (heroCar) heroCar.headlights.forEach((h) => (h.intensity = 0));

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));
      if (starsRef.current) starsRef.current.visible = false;
    } else if (timeOfDay === "sunset") {
      scene.background = new THREE.Color(0xf57c38);
      scene.fog = new THREE.Fog(0xc95232, 35, 130);

      lights.sun.intensity = 2.2;
      lights.sun.color.setHex(0xff6015);
      lights.ambient.intensity = 0.75;
      lights.ambient.color.setHex(0x73362a);
      lights.moon.intensity = 0.1;

      lights.sunMesh.visible = true;
      lights.sunMesh.position.set(55, 25, 25);
      (lights.sunMesh.material as THREE.MeshBasicMaterial).color.setHex(0xff4400);

      lights.streetlights.forEach((l) => {
        l.intensity = 1.2;
        l.color.setHex(0xffd59e);
      });
      if (heroCar) heroCar.headlights.forEach((h) => {
        h.intensity = 3.5;
        h.color.setHex(0xfff0cc);
      });

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 1.2));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.5));
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "night") {
      scene.background = new THREE.Color(0x0f172a);
      scene.fog = new THREE.Fog(0x0f172a, 30, 120);

      lights.sun.intensity = 0.0;
      lights.ambient.intensity = 0.45;
      lights.ambient.color.setHex(0x1e293b);
      lights.moon.intensity = 0.7;
      lights.moon.color.setHex(0x94a3b8);

      lights.sunMesh.visible = true;
      lights.sunMesh.position.set(-45, 60, -35);
      (lights.sunMesh.material as THREE.MeshBasicMaterial).color.setHex(0xe2e8f0);

      lights.streetlights.forEach((l) => {
        l.intensity = 2.5;
        l.color.setHex(0xffeaad);
      });
      if (heroCar) heroCar.headlights.forEach((h) => {
        h.intensity = 6.0;
        h.color.setHex(0xfffde8);
      });

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.5));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 4.5));
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "cyberpunk") {
      scene.background = new THREE.Color(0x1e1b4b);
      scene.fog = new THREE.Fog(0x311042, 25, 100);

      lights.sun.intensity = 0.0;
      lights.ambient.intensity = 0.5;
      lights.ambient.color.setHex(0x3b0764);
      lights.moon.intensity = 0.9;
      lights.moon.color.setHex(0x06b6d4);

      lights.sunMesh.visible = false;

      lights.streetlights.forEach((l, idx) => {
        l.intensity = 3.5;
        l.color.setHex(idx % 2 === 0 ? 0x06b6d4 : 0xf97316);
      });
      if (heroCar) heroCar.headlights.forEach((h) => {
        h.intensity = 7.5;
        h.color.setHex(0xe0f2fe);
      });

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 3.5));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 5.0));
      if (starsRef.current) starsRef.current.visible = true;
    }
  }, [timeOfDay]);

  return (
    <div className="relative w-full h-full select-none overflow-hidden bg-slate-100">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {loading && (
        <div className="absolute inset-0 z-30 flex flex-col items-center justify-center bg-white/95 backdrop-blur-md text-slate-800">
          <div className="relative flex items-center justify-center mb-5">
            <div className="w-12 h-12 border-4 border-orange-500/20 border-t-orange-500 rounded-full animate-spin" />
          </div>
          <h3 className="text-base font-bold font-display tracking-wider text-slate-900">
            {sceneMode === "mountain" ? "Đang tải Cung Đường Đèo Núi 3D..." : "Đang tải Thành Phố Đô Thị 3D..."}
          </h3>
          <p className="text-xs text-slate-500 mt-1 font-normal">
            Xe chạy vô tận • Camera bám đuôi trực tiếp
          </p>
        </div>
      )}
    </div>
  );
};
