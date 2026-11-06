import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { CameraPreset, TimeOfDay } from "../types";

export type ExtendedCameraMode = "chase" | "hood" | "drone" | "street" | "mountain" | "isometric" | "topdown";

interface CityCanvasProps {
  timeOfDay: TimeOfDay;
  cameraPreset: ExtendedCameraMode;
  activeCarId?: string;
  onSelectCar?: (carId: string) => void;
  customCarColor?: { carId: string; colorHex: string };
  trafficSpeed?: number;
  isPaused?: boolean;
}

export const CityCanvas: React.FC<CityCanvasProps> = ({
  timeOfDay,
  cameraPreset,
  activeCarId = "Car_BlueCoupe",
  onSelectCar,
  customCarColor,
  trafficSpeed = 1.0,
  isPaused = false
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [loadProgress, setLoadProgress] = useState(0);

  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null);
  const controlsRef = useRef<OrbitControls | null>(null);
  
  const carsRef = useRef<{
    id: string;
    object: THREE.Object3D;
    curve: THREE.CatmullRomCurve3;
    progress: number;
    speed: number;
    wheels: THREE.Object3D[];
    headlights: THREE.SpotLight[];
    bodyMeshes: THREE.Mesh[];
  }[]>([]);

  const lightsRef = useRef<{
    sun: THREE.DirectionalLight;
    ambient: THREE.AmbientLight;
    moon: THREE.DirectionalLight;
    celestialMesh: THREE.Mesh;
    streetlights: THREE.PointLight[];
  } | null>(null);

  const windowMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const streetlampMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const roadMaterialRef = useRef<THREE.MeshStandardMaterial | null>(null);
  const starsRef = useRef<THREE.Points | null>(null);
  const cloudsRef = useRef<THREE.Group | null>(null);

  const propsRef = useRef({ timeOfDay, cameraPreset, activeCarId, trafficSpeed, isPaused });
  useEffect(() => {
    propsRef.current = { timeOfDay, cameraPreset, activeCarId, trafficSpeed, isPaused };
  }, [timeOfDay, cameraPreset, activeCarId, trafficSpeed, isPaused]);

  useEffect(() => {
    if (!mountRef.current) return;
    const container = mountRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight;

    // --- Scene & Renderer ---
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: false,
      powerPreference: "high-performance"
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // --- Camera & Orbit Controls ---
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.4, 500);
    camera.position.set(38, 30, 38);
    cameraRef.current = camera;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.03; // Don't go below ground
    controls.minDistance = 3;
    controls.maxDistance = 160;
    controls.target.set(0, 0, 0);
    controlsRef.current = controls;

    // --- Beautiful Sky Elements: Stars & Sun/Moon Celestial Sphere ---
    // Starfield for Night & Cyberpunk
    const starCount = 800;
    const starGeometry = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount * 3; i += 3) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 240;
      starPositions[i] = r * Math.sin(phi) * Math.cos(theta);
      starPositions[i + 1] = Math.abs(r * Math.cos(phi)) + 10;
      starPositions[i + 2] = r * Math.sin(phi) * Math.sin(theta);
    }
    starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
    const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 1.5, transparent: true, opacity: 0.85 });
    const stars = new THREE.Points(starGeometry, starMaterial);
    scene.add(stars);
    starsRef.current = stars;

    // Celestial Mesh (Sun / Moon orb in the sky)
    const celestialGeo = new THREE.SphereGeometry(4.5, 16, 16);
    const celestialMat = new THREE.MeshBasicMaterial({ color: 0xfff0aa });
    const celestialMesh = new THREE.Mesh(celestialGeo, celestialMat);
    celestialMesh.position.set(50, 75, 45);
    scene.add(celestialMesh);

    // Fluffy Low-Poly Clouds floating above city & mountains
    const cloudsGroup = new THREE.Group();
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.9,
      transparent: true,
      opacity: 0.85,
      flatShading: true
    });
    for (let i = 0; i < 9; i++) {
      const cloud = new THREE.Group();
      const cx = (Math.random() - 0.5) * 80;
      const cy = (Math.random() - 0.5) * 80;
      const cz = 32 + Math.random() * 12;
      for (let j = 0; j < 5; j++) {
        const puffGeo = new THREE.DodecahedronGeometry(2.5 + Math.random() * 2.0, 1);
        const puff = new THREE.Mesh(puffGeo, cloudMat);
        puff.position.set((Math.random() - 0.5) * 5, (Math.random() - 0.5) * 3, (Math.random() - 0.5) * 4);
        cloud.add(puff);
      }
      cloud.position.set(cx, cy, cz);
      cloudsGroup.add(cloud);
    }
    scene.add(cloudsGroup);
    cloudsRef.current = cloudsGroup;

    // --- Atmospheric Lighting ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfffaed, 2.8);
    sunLight.position.set(45, 60, 35);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 5;
    sunLight.shadow.camera.far = 160;
    const d = 40;
    sunLight.shadow.camera.left = -d;
    sunLight.shadow.camera.right = d;
    sunLight.shadow.camera.top = d;
    sunLight.shadow.camera.bottom = -d;
    sunLight.shadow.bias = -0.0006;
    scene.add(sunLight);

    const moonLight = new THREE.DirectionalLight(0x7799cc, 0.5);
    moonLight.position.set(-35, 55, -35);
    moonLight.castShadow = true;
    moonLight.shadow.mapSize.width = 1024;
    moonLight.shadow.mapSize.height = 1024;
    scene.add(moonLight);

    lightsRef.current = {
      sun: sunLight,
      ambient: ambientLight,
      moon: moonLight,
      celestialMesh,
      streetlights: []
    };

    // --- INFINITE 3D ROAD SPLINES (CITY & WINDING MOUNTAIN PASS) ---
    // Circuit 1: The Mountain Pass & City Highway Circuit (Winds up mountain slope to 5.5m and loops back through city)
    const mountainHighwayPoints = [
      new THREE.Vector3(1.6, -16.0, 0.0),    // Downtown south lane
      new THREE.Vector3(10.0, -16.0, 0.0),   // Turn toward East highway
      new THREE.Vector3(20.0, -16.0, 0.5),   // Approach mountain foot
      new THREE.Vector3(23.0, -12.0, 1.2),   // Climbing mountain pass curve 1
      new THREE.Vector3(26.0, -6.0, 2.2),    // Climbing mountain pass curve 2
      new THREE.Vector3(28.5, 0.0, 3.4),     // Mid-mountain winding curve
      new THREE.Vector3(30.0, 6.0, 4.6),     // Upper mountain pass
      new THREE.Vector3(29.0, 13.0, 5.5),    // Highest scenic mountain overlook!
      new THREE.Vector3(26.0, 19.0, 4.2),    // Switchback descent curve 1
      new THREE.Vector3(22.5, 24.0, 2.6),    // Switchback descent curve 2
      new THREE.Vector3(19.0, 27.0, 1.0),    // Mountain foot exit
      new THREE.Vector3(10.0, 16.0, 0.0),    // Re-entering downtown north boulevard
      new THREE.Vector3(-1.6, 16.0, 0.0),    // Downtown north lane
      new THREE.Vector3(-1.6, 0.0, 0.0),     // Crossing central intersection
      new THREE.Vector3(-1.6, -16.0, 0.0),   // Downtown south avenue
      new THREE.Vector3(1.6, -16.0, 0.0)     // Seamless closed loop!
    ];
    const mountainHighwayCurve = new THREE.CatmullRomCurve3(mountainHighwayPoints, true, "catmullrom", 0.18);

    // Circuit 2: Downtown Ring Circuit (Outer perimeter loop around city skyscrapers)
    const downtownRingPoints = [
      new THREE.Vector3(16.0, -16.0, 0.0),
      new THREE.Vector3(16.0, 16.0, 0.0),
      new THREE.Vector3(-16.0, 16.0, 0.0),
      new THREE.Vector3(-16.0, -16.0, 0.0),
      new THREE.Vector3(16.0, -16.0, 0.0)
    ];
    const downtownRingCurve = new THREE.CatmullRomCurve3(downtownRingPoints, true, "catmullrom", 0.15);

    // Circuit 3: Central Intersection Figure-8 Cruise
    const crossCruiserPoints = [
      new THREE.Vector3(1.6, -16.0, 0.0),
      new THREE.Vector3(1.6, -2.5, 0.0),
      new THREE.Vector3(4.0, 1.6, 0.0),
      new THREE.Vector3(16.0, 1.6, 0.0),
      new THREE.Vector3(16.0, -1.6, 0.0),
      new THREE.Vector3(2.5, -1.6, 0.0),
      new THREE.Vector3(-1.6, -3.5, 0.0),
      new THREE.Vector3(-1.6, -16.0, 0.0),
      new THREE.Vector3(1.6, -16.0, 0.0)
    ];
    const crossCruiserCurve = new THREE.CatmullRomCurve3(crossCruiserPoints, true, "catmullrom", 0.2);

    // --- Load City & Mountain GLB Asset ---
    const loader = new GLTFLoader();
    loader.load(
      "/assets/city.glb",
      (gltf) => {
        const model = gltf.scene;
        scene.add(model);

        const foundCars: { [key: string]: THREE.Object3D } = {};

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
              if (mat.name.includes("Road") && !mat.name.includes("Marking")) {
                roadMaterialRef.current = mat;
              }
            }
          }

          if (
            child.name === "Car_Taxi" ||
            child.name === "Car_RedSedan" ||
            child.name === "Car_BlueCoupe" ||
            child.name === "Car_WhiteVan"
          ) {
            foundCars[child.name] = child;
          }
        });

        // Setup Cars on their infinite driving circuits:
        // Apex GT-90 (Car_BlueCoupe) drives on the scenic Mountain Highway pass!
        // Red Sedan drives on the Downtown Ring Circuit.
        // Taxi & Van cruise through central avenues.
        const carConfigs = [
          { name: "Car_BlueCoupe", curve: mountainHighwayCurve, progress: 0.15, speed: 0.00035 },
          { name: "Car_RedSedan", curve: downtownRingCurve, progress: 0.45, speed: 0.0004 },
          { name: "Car_Taxi", curve: crossCruiserCurve, progress: 0.75, speed: 0.00035 },
          { name: "Car_WhiteVan", curve: mountainHighwayCurve, progress: 0.65, speed: 0.00028 }
        ];

        carsRef.current = [];

        carConfigs.forEach((cfg) => {
          const carObj = foundCars[cfg.name];
          if (!carObj) return;

          const wheels: THREE.Object3D[] = [];
          const bodyMeshes: THREE.Mesh[] = [];

          carObj.traverse((part) => {
            if (part.name.includes("Wheel")) wheels.push(part);
            if (part instanceof THREE.Mesh && (part.name.includes("LowerBody") || part.name.includes("RoofCap"))) {
              part.material = part.material.clone();
              bodyMeshes.push(part);
            }
          });

          // Headlight Spotlights pointing ahead
          const spotLeft = new THREE.SpotLight(0xfffae0, 6.0, 22, Math.PI / 5, 0.4, 1.2);
          spotLeft.position.set(-0.55, 1.8, 0.5);
          const targetLeft = new THREE.Object3D();
          targetLeft.position.set(-0.55, 14.0, 0);
          carObj.add(targetLeft);
          spotLeft.target = targetLeft;
          carObj.add(spotLeft);

          const spotRight = new THREE.SpotLight(0xfffae0, 6.0, 22, Math.PI / 5, 0.4, 1.2);
          spotRight.position.set(0.55, 1.8, 0.5);
          const targetRight = new THREE.Object3D();
          targetRight.position.set(0.55, 14.0, 0);
          carObj.add(targetRight);
          spotRight.target = targetRight;
          carObj.add(spotRight);

          carsRef.current.push({
            id: cfg.name,
            object: carObj,
            curve: cfg.curve,
            progress: cfg.progress,
            speed: cfg.speed,
            wheels,
            headlights: [spotLeft, spotRight],
            bodyMeshes
          });
        });

        // Add Streetlights and Mountain Lantern lights
        const lampPositions = [
          [-3.8, -3.8, 3.2], [3.8, -3.8, 3.2], [-3.8, 3.8, 3.2], [3.8, 3.8, 3.2],
          [-3.8, -17.0, 3.2], [3.8, -17.0, 3.2], [-17.0, 3.8, 3.2], [17.0, -3.8, 3.2],
          [32.0, 14.0, 7.3] // Mountain Overlook Deck Lantern!
        ];
        lampPositions.forEach(([lx, ly, lz]) => {
          const pLight = new THREE.PointLight(0xffeedd, 1.8, 14, 1.8);
          pLight.position.set(lx, ly, lz);
          scene.add(pLight);
          lightsRef.current?.streetlights.push(pLight);
        });

        setLoading(false);
      },
      (xhr) => {
        if (xhr.total > 0) setLoadProgress(Math.round((xhr.loaded / xhr.total) * 100));
      },
      (error) => {
        console.error("Error loading city & mountain GLB:", error);
        setLoading(false);
      }
    );

    // --- Raycaster for Clicking Cars ---
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handlePointerDown = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const carRoots = carsRef.current.map((c) => c.object);
      const intersects = raycaster.intersectObjects(carRoots, true);

      if (intersects.length > 0) {
        let cur: THREE.Object3D | null = intersects[0].object;
        while (cur && cur.parent && !carsRef.current.some((c) => c.object === cur)) {
          cur = cur.parent;
        }
        if (cur && onSelectCar) {
          const matched = carsRef.current.find((c) => c.object === cur);
          if (matched) onSelectCar(matched.id);
        }
      }
    };
    renderer.domElement.addEventListener("pointerdown", handlePointerDown);

    // --- Animation & Multi-Camera Render Loop ---
    let animationFrameId: number;
    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = Math.min((currentTime - lastTime) / 1000, 0.1);
      lastTime = currentTime;

      const {
        timeOfDay: curTimeOfDay,
        cameraPreset: curCamPreset,
        activeCarId: curActiveId,
        trafficSpeed: curSpeed,
        isPaused: curPaused
      } = propsRef.current;

      // Animate Clouds slowly across the sky
      if (cloudsRef.current) {
        cloudsRef.current.children.forEach((c, idx) => {
          c.position.x += delta * (0.8 + idx * 0.1);
          if (c.position.x > 55) c.position.x = -55;
        });
      }

      // Animate Cars along their endless loops
      if (!curPaused) {
        carsRef.current.forEach((car) => {
          car.progress = (car.progress + car.speed * curSpeed * delta * 60) % 1.0;

          const pt = car.curve.getPointAt(car.progress);
          const tangent = car.curve.getTangentAt(car.progress).normalize();

          // Position in 3D (including mountain slope height Z!)
          car.object.position.copy(pt);

          // Smooth heading orientation along tangent
          const lookTarget = pt.clone().add(tangent);
          car.object.lookAt(lookTarget);

          // Rotate wheels
          car.wheels.forEach((w) => {
            w.rotation.x += delta * 20 * curSpeed;
          });
        });
      }

      // MULTI-CAMERA MODES & CHASE LOGIC:
      const targetCar = carsRef.current.find((c) => c.id === curActiveId) || carsRef.current[0];

      if (targetCar && curCamPreset === "chase") {
        // AAA Smooth Chase Cam: follows behind the car with inertia and banked lookahead!
        const carPos = targetCar.object.position;
        const tangent = targetCar.curve.getTangentAt(targetCar.progress).normalize();

        // Camera position trailing behind car: -tangent * distance + vertical offset
        const trailOffset = tangent.clone().multiplyScalar(-8.5);
        const desiredCamPos = carPos.clone().add(trailOffset).add(new THREE.Vector3(0, 3.4, 0));

        camera.position.lerp(desiredCamPos, 0.08);

        // Look at a target slightly ahead of the car for natural forward momentum
        const lookAheadTarget = carPos.clone().add(tangent.clone().multiplyScalar(6.0)).add(new THREE.Vector3(0, 1.2, 0));
        controls.target.lerp(lookAheadTarget, 0.1);
      } else if (targetCar && curCamPreset === "hood") {
        // Hood / First-Person Cam (mounted on the front hood looking directly ahead!)
        const carPos = targetCar.object.position;
        const tangent = targetCar.curve.getTangentAt(targetCar.progress).normalize();

        const hoodPos = carPos.clone().add(tangent.clone().multiplyScalar(0.7)).add(new THREE.Vector3(0, 1.2, 0));
        camera.position.lerp(hoodPos, 0.15);

        const hoodLook = carPos.clone().add(tangent.clone().multiplyScalar(18.0)).add(new THREE.Vector3(0, 0.8, 0));
        controls.target.lerp(hoodLook, 0.2);
      } else if (targetCar && curCamPreset === "drone") {
        // Flycam / Side Drone Cam: follows from a dramatic side-angle
        const carPos = targetCar.object.position;
        const dronePos = carPos.clone().add(new THREE.Vector3(-9.0, 7.5, 7.0));
        camera.position.lerp(dronePos, 0.06);
        controls.target.lerp(carPos, 0.08);
      } else if (curCamPreset === "mountain") {
        // Scenic Mountain Overlook Deck View (watching cars wind up the mountain pass!)
        const overlookDeckPos = new THREE.Vector3(32.0, 12.0, 8.5);
        const mountainLook = new THREE.Vector3(26.0, 0.0, 2.5);
        camera.position.lerp(overlookDeckPos, 0.04);
        controls.target.lerp(mountainLook, 0.04);
      } else if (curCamPreset === "street") {
        // Street-Level View: low angle on downtown intersection looking up at skyscrapers
        const streetPos = new THREE.Vector3(0.5, 1.8, 3.5);
        const streetLook = new THREE.Vector3(0, 6.0, -16.0);
        camera.position.lerp(streetPos, 0.04);
        controls.target.lerp(streetLook, 0.04);
      } else if (curCamPreset === "topdown") {
        // Aerial Bird's-Eye View
        const topPos = new THREE.Vector3(10, 52, 0.1);
        camera.position.lerp(topPos, 0.04);
        controls.target.lerp(new THREE.Vector3(10, 0, 0), 0.04);
      } else if (curCamPreset === "isometric") {
        // Free Orbit Controls active
      }

      controls.update();
      renderer.render(scene, camera);
    };

    animationFrameId = requestAnimationFrame(animate);

    // --- Resize ---
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
      renderer.domElement.removeEventListener("pointerdown", handlePointerDown);
      cancelAnimationFrame(animationFrameId);
      controls.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  // --- Scenery Lighting & Sky Transitions ---
  useEffect(() => {
    const scene = sceneRef.current;
    const lights = lightsRef.current;
    if (!scene || !lights) return;

    if (timeOfDay === "day") {
      scene.background = new THREE.Color(0x7dc3eb);
      scene.fog = new THREE.Fog(0xb8e3f9, 45, 150);

      lights.sun.intensity = 2.8;
      lights.sun.color.setHex(0xfff8ee);
      lights.ambient.intensity = 0.95;
      lights.ambient.color.setHex(0xeaf4ff);
      lights.moon.intensity = 0;

      // Celestial Sun
      lights.celestialMesh.position.set(50, 75, 45);
      (lights.celestialMesh.material as THREE.MeshBasicMaterial).color.setHex(0xfff4aa);
      lights.celestialMesh.visible = true;

      lights.streetlights.forEach((l) => (l.intensity = 0));
      carsRef.current.forEach((c) => c.headlights.forEach((h) => (h.intensity = 0)));

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.85;
      if (starsRef.current) starsRef.current.visible = false;
    } else if (timeOfDay === "sunset") {
      scene.background = new THREE.Color(0xeb6434);
      scene.fog = new THREE.Fog(0x8c3547, 35, 125);

      lights.sun.intensity = 2.2;
      lights.sun.color.setHex(0xff5511);
      lights.ambient.intensity = 0.7;
      lights.ambient.color.setHex(0x5a3048);
      lights.moon.intensity = 0.1;

      // Low golden sun on the mountain horizon
      lights.celestialMesh.position.set(65, 30, 25);
      (lights.celestialMesh.material as THREE.MeshBasicMaterial).color.setHex(0xff4400);
      lights.celestialMesh.visible = true;

      lights.streetlights.forEach((l) => {
        l.intensity = 1.2;
        l.color.setHex(0xffd59e);
      });
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 3.0;
          h.color.setHex(0xfff0cc);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 1.0));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.5));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.75;
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "night") {
      scene.background = new THREE.Color(0x060913);
      scene.fog = new THREE.Fog(0x060913, 30, 115);

      lights.sun.intensity = 0.0;
      lights.ambient.intensity = 0.35;
      lights.ambient.color.setHex(0x182436);
      lights.moon.intensity = 0.65;
      lights.moon.color.setHex(0x7799cc);

      // Cool silvery Moon above mountains
      lights.celestialMesh.position.set(-45, 65, -40);
      (lights.celestialMesh.material as THREE.MeshBasicMaterial).color.setHex(0xddeeff);
      lights.celestialMesh.visible = true;

      lights.streetlights.forEach((l) => {
        l.intensity = 2.5;
        l.color.setHex(0xffeaad);
      });
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 6.0;
          h.color.setHex(0xfffde8);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.4));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 4.5));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.8;
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "cyberpunk") {
      scene.background = new THREE.Color(0x0a0515);
      scene.fog = new THREE.Fog(0x140724, 25, 100);

      lights.sun.intensity = 0.0;
      lights.ambient.intensity = 0.45;
      lights.ambient.color.setHex(0x38124d);
      lights.moon.intensity = 0.85;
      lights.moon.color.setHex(0x00e5ff);

      lights.celestialMesh.visible = false; // Hidden behind dense neon storm clouds

      lights.streetlights.forEach((l, idx) => {
        l.intensity = 3.5;
        l.color.setHex(idx % 2 === 0 ? 0x00f0ff : 0xff007f);
      });
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 7.5;
          h.color.setHex(0xcceeff);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 3.8));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 5.5));

      // Wet reflective asphalt in the rain!
      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.12;
      if (starsRef.current) starsRef.current.visible = true;
    }
  }, [timeOfDay]);

  // Realtime Car Color Customizer
  useEffect(() => {
    if (!customCarColor) return;
    const car = carsRef.current.find((c) => c.id === customCarColor.carId);
    if (!car) return;
    car.bodyMeshes.forEach((mesh) => {
      const mat = mesh.material as THREE.MeshStandardMaterial;
      if (mat) mat.color.set(customCarColor.colorHex);
    });
  }, [customCarColor]);

  return (
    <div className="relative w-full h-full select-none overflow-hidden bg-slate-950">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {loading && (
        <div className="absolute inset-0 z-30 flex flex-col items-center justify-center bg-slate-950/90 backdrop-blur-md text-white">
          <div className="relative flex items-center justify-center mb-6">
            <div className="w-16 h-16 border-4 border-cyan-500/20 border-t-cyan-400 rounded-full animate-spin" />
            <span className="absolute text-xs font-mono text-cyan-400 font-bold">{loadProgress}%</span>
          </div>
          <h3 className="text-xl font-bold font-display tracking-wider text-slate-100">
            Đang tải Đô Thị & Cung Đường Núi 3D...
          </h3>
          <p className="text-sm text-slate-400 mt-2 font-light">
            Blender 5.2 • Cung đường đèo vô tận • Hệ thống Camera đa góc nhìn
          </p>
        </div>
      )}
    </div>
  );
};
