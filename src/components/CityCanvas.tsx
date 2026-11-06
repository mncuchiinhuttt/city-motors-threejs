import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { ExtendedCameraMode, TimeOfDay } from "../types";

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
  timeOfDay = "day",
  cameraPreset = "chase",
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
    sunMesh: THREE.Mesh;
    streetlights: THREE.PointLight[];
  } | null>(null);

  const windowMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const streetlampMaterialsRef = useRef<THREE.MeshStandardMaterial[]>([]);
  const roadMaterialRef = useRef<THREE.MeshStandardMaterial | null>(null);
  const starsRef = useRef<THREE.Points | null>(null);

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
    scene.background = new THREE.Color(0xbfe0f7); // Crisp sunny sky blue
    scene.fog = new THREE.Fog(0xd8ecfa, 45, 170);
    sceneRef.current = scene;

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: "high-performance"
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    container.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // --- Camera & Orbit Controls ---
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.4, 500);
    camera.position.set(0, 12, 28);
    cameraRef.current = camera;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.04; // Don't clip below ground
    controls.minDistance = 3;
    controls.maxDistance = 180;
    controls.target.set(0, 1.0, 0);
    controlsRef.current = controls;

    // --- Beautiful Sky: Celestial Sun & Starfield ---
    const sunGeo = new THREE.SphereGeometry(3.5, 16, 16);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfff4aa });
    const sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunMesh.position.set(45, 65, 35);
    scene.add(sunMesh);

    // Starfield for night mode
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

    // --- Crisp Warm Sunlight (60-30-10 palette lighting) ---
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

    // --- MATHEMATICALLY ACCURATE THREE.JS ROAD SPLINES ---
    // In Three.js: X = East/West, Y = VERTICAL HEIGHT, Z = North/South (depth)!
    // Road surface is at Y = 0.05. Mountain pass climbs from Y = 0.4 up to Y = 3.2!
    
    // Circuit 1: Scenic Mountain Pass & City Highway (Endless Loop!)
    // Apex GT-90 (Car_BlueCoupe) drives on this panoramic mountain route!
    const mountainHighwayPoints = [
      new THREE.Vector3(0.0,  0.15,  16.0), // South highway cruising east
      new THREE.Vector3(14.0, 0.15,  16.0),
      new THREE.Vector3(20.0, 0.45,  14.0), // Mountain foot approach
      new THREE.Vector3(23.5, 1.15,   9.0), // Climbing mountain curve 1
      new THREE.Vector3(25.5, 1.95,   3.0), // Climbing mountain curve 2
      new THREE.Vector3(26.5, 3.25,  -3.0), // HIGHEST MOUNTAIN PASS OVERLOOK!
      new THREE.Vector3(24.0, 2.75,  -9.0), // Mountain switchback descent
      new THREE.Vector3(21.0, 1.45, -14.0),
      new THREE.Vector3(15.0, 0.45, -16.0), // Re-entering North Boulevard
      new THREE.Vector3(0.0,  0.15, -16.0),
      new THREE.Vector3(-18.0, 0.15, -16.0),
      new THREE.Vector3(-20.0, 0.15,  -8.0), // West Avenue
      new THREE.Vector3(-20.0, 0.15,   8.0),
      new THREE.Vector3(-18.0, 0.15,  16.0), // Turn into South highway
      new THREE.Vector3(0.0,  0.15,  16.0)  // Seamless Infinite Loop!
    ];
    const mountainHighwayCurve = new THREE.CatmullRomCurve3(mountainHighwayPoints, true, "catmullrom", 0.15);

    // Circuit 2: Downtown Avenue Loop (Sedan & Taxi)
    const downtownAvenuePoints = [
      new THREE.Vector3(-1.8, 0.15,  16.0),
      new THREE.Vector3(-1.8, 0.15,   0.0),
      new THREE.Vector3(-1.8, 0.15, -16.0),
      new THREE.Vector3( 1.8, 0.15, -16.0),
      new THREE.Vector3( 1.8, 0.15,   0.0),
      new THREE.Vector3( 1.8, 0.15,  16.0)
    ];
    const downtownAvenueCurve = new THREE.CatmullRomCurve3(downtownAvenuePoints, true, "catmullrom", 0.2);

    // Circuit 3: Outer Ring Road
    const outerRingPoints = [
      new THREE.Vector3( 16.0, 0.15,  16.0),
      new THREE.Vector3( 16.0, 0.15, -16.0),
      new THREE.Vector3(-16.0, 0.15, -16.0),
      new THREE.Vector3(-16.0, 0.15,  16.0)
    ];
    const outerRingCurve = new THREE.CatmullRomCurve3(outerRingPoints, true, "catmullrom", 0.15);

    // --- Load City GLB Asset ---
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

        // Car Configurations:
        // Car_BlueCoupe: Hero Orange Sports Car driving on the Mountain Pass!
        const carConfigs = [
          { name: "Car_BlueCoupe", curve: mountainHighwayCurve, progress: 0.05, speed: 0.00038 },
          { name: "Car_RedSedan",  curve: outerRingCurve,       progress: 0.35, speed: 0.00032 },
          { name: "Car_Taxi",      curve: downtownAvenueCurve,  progress: 0.65, speed: 0.00035 },
          { name: "Car_WhiteVan",  curve: mountainHighwayCurve, progress: 0.55, speed: 0.00028 }
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

          // Headlights Spotlight
          const spotLeft = new THREE.SpotLight(0xfffae0, 6.0, 24, Math.PI / 5, 0.4, 1.2);
          spotLeft.position.set(-0.6, 0.6, 2.0);
          const targetLeft = new THREE.Object3D();
          targetLeft.position.set(-0.6, 0.0, 16.0);
          carObj.add(targetLeft);
          spotLeft.target = targetLeft;
          carObj.add(spotLeft);

          const spotRight = new THREE.SpotLight(0xfffae0, 6.0, 24, Math.PI / 5, 0.4, 1.2);
          spotRight.position.set(0.6, 0.6, 2.0);
          const targetRight = new THREE.Object3D();
          targetRight.position.set(0.6, 0.0, 16.0);
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

        // Initialize Hero Car & Chase Camera immediately on load!
        if (carsRef.current.length > 0) {
          const hero = carsRef.current[0];
          const pt = hero.curve.getPointAt(hero.progress);
          const tangent = hero.curve.getTangentAt(hero.progress).normalize();
          hero.object.position.copy(pt);
          hero.object.lookAt(pt.clone().add(tangent));

          const initCam = pt.clone().add(tangent.clone().multiplyScalar(-7.5)).add(new THREE.Vector3(0, 3.2, 0));
          const initTarget = pt.clone().add(tangent.clone().multiplyScalar(4.5)).add(new THREE.Vector3(0, 1.0, 0));
          camera.position.copy(initCam);
          controls.target.copy(initTarget);
        }
        // Streetlights
        const lampPositions = [
          [-4.2, 3.2, -4.2], [4.2, 3.2, -4.2], [-4.2, 3.2, 4.2], [4.2, 3.2, 4.2],
          [-4.2, 3.2, -18.5], [4.2, 3.2, -18.5], [-4.2, 3.2, 18.5], [4.2, 3.2, 18.5]
        ];
        lampPositions.forEach(([lx, ly, lz]) => {
          const pLight = new THREE.PointLight(0xffeedd, 2.0, 14, 1.8);
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
        console.error("Error loading city GLB:", error);
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

    // --- ANIMATION & FLAWLESS CHASE CAMERA RENDER LOOP ---
    let animationFrameId: number;
    let lastTime = performance.now();

    const animate = (currentTime: number) => {
      animationFrameId = requestAnimationFrame(animate);

      const delta = Math.min((currentTime - lastTime) / 1000, 0.1);
      lastTime = currentTime;

      const {
        cameraPreset: curCamPreset,
        activeCarId: curActiveId,
        trafficSpeed: curSpeed,
        isPaused: curPaused
      } = propsRef.current;

      // Animate Cars along their road splines
      if (!curPaused) {
        carsRef.current.forEach((car) => {
          car.progress = (car.progress + car.speed * curSpeed * delta * 60) % 1.0;

          // In Three.js coordinates: Y is vertical UP!
          const pt = car.curve.getPointAt(car.progress);
          const tangent = car.curve.getTangentAt(car.progress).normalize();

          // Set car position directly on the road
          car.object.position.copy(pt);

          // Smooth forward heading along road tangent
          const lookTarget = pt.clone().add(tangent);
          car.object.lookAt(lookTarget);

          // Rotate wheels
          car.wheels.forEach((w) => {
            w.rotation.x += delta * 20 * curSpeed;
          });
        });
      }

      // ACTIVE HERO CAR CHASE CAMERA
      const heroCar = carsRef.current.find((c) => c.id === curActiveId) || carsRef.current[0];

      if (heroCar && curCamPreset === "chase") {
        // CHASE CAM: Positioned 8 meters behind the car along the road tangent, elevated 3.2m above road!
        const carPos = heroCar.object.position;
        const tangent = heroCar.curve.getTangentAt(heroCar.progress).normalize();

        // 8m behind along tangent + 3.2m above
        const behindOffset = tangent.clone().multiplyScalar(-8.0);
        const desiredCamPos = carPos.clone().add(behindOffset).add(new THREE.Vector3(0, 3.2, 0));

        camera.position.lerp(desiredCamPos, 0.08);

        // Look 4.5m ahead of the car for natural driving view
        const forwardLook = carPos.clone().add(tangent.clone().multiplyScalar(4.5)).add(new THREE.Vector3(0, 1.0, 0));
        controls.target.lerp(forwardLook, 0.1);
      } else if (heroCar && curCamPreset === "hood") {
        // HOOD CAM: Mounted on the car hood looking forward
        const carPos = heroCar.object.position;
        const tangent = heroCar.curve.getTangentAt(heroCar.progress).normalize();

        const hoodPos = carPos.clone().add(tangent.clone().multiplyScalar(0.8)).add(new THREE.Vector3(0, 1.1, 0));
        camera.position.lerp(hoodPos, 0.15);

        const hoodLook = carPos.clone().add(tangent.clone().multiplyScalar(16.0)).add(new THREE.Vector3(0, 0.8, 0));
        controls.target.lerp(hoodLook, 0.2);
      } else if (heroCar && curCamPreset === "drone") {
        // SIDE DRONE CAM: 8m side offset
        const carPos = heroCar.object.position;
        const dronePos = carPos.clone().add(new THREE.Vector3(-9.0, 6.5, 8.0));
        camera.position.lerp(dronePos, 0.06);
        controls.target.lerp(carPos, 0.08);
      } else if (curCamPreset === "mountain") {
        // MOUNTAIN OVERLOOK VIEW: High scenic vantage point
        const overlookPos = new THREE.Vector3(26.0, 8.0, 10.0);
        const mtnTarget = new THREE.Vector3(25.0, 2.5, 0.0);
        camera.position.lerp(overlookPos, 0.05);
        controls.target.lerp(mtnTarget, 0.05);
      } else if (curCamPreset === "street") {
        // STREET LEVEL VIEW: Low intersection cam
        const streetPos = new THREE.Vector3(0, 1.8, 8.0);
        const streetTarget = new THREE.Vector3(0, 4.0, -14.0);
        camera.position.lerp(streetPos, 0.04);
        controls.target.lerp(streetTarget, 0.04);
      } else if (curCamPreset === "topdown") {
        // TOPDOWN BIRD'S EYE VIEW
        camera.position.lerp(new THREE.Vector3(5, 55, 0.1), 0.04);
        controls.target.lerp(new THREE.Vector3(5, 0, 0), 0.04);
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

  // --- Dynamic Lighting & Atmosphere ---
  useEffect(() => {
    const scene = sceneRef.current;
    const lights = lightsRef.current;
    if (!scene || !lights) return;

    if (timeOfDay === "day") {
      scene.background = new THREE.Color(0xb5daf5); // Sunny clear azure sky
      scene.fog = new THREE.Fog(0xd4e9fa, 45, 160);

      lights.sun.intensity = 2.8;
      lights.sun.color.setHex(0xfffaec);
      lights.ambient.intensity = 1.1;
      lights.ambient.color.setHex(0xf0f6ff);
      lights.moon.intensity = 0;

      lights.sunMesh.visible = true;
      lights.sunMesh.position.set(45, 65, 35);
      (lights.sunMesh.material as THREE.MeshBasicMaterial).color.setHex(0xfff0aa);

      lights.streetlights.forEach((l) => (l.intensity = 0));
      carsRef.current.forEach((c) => c.headlights.forEach((h) => (h.intensity = 0)));

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 0.0));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.85;
      if (starsRef.current) starsRef.current.visible = false;
    } else if (timeOfDay === "sunset") {
      scene.background = new THREE.Color(0xf57c38); // Warm sunset amber/orange
      scene.fog = new THREE.Fog(0xc95232, 35, 125);

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
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 3.5;
          h.color.setHex(0xfff0cc);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 1.2));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.5));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.75;
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "night") {
      scene.background = new THREE.Color(0x0f172a); // Deep solid slate night
      scene.fog = new THREE.Fog(0x0f172a, 30, 115);

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
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 6.0;
          h.color.setHex(0xfffde8);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 2.5));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 4.5));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.8;
      if (starsRef.current) starsRef.current.visible = true;
    } else if (timeOfDay === "cyberpunk") {
      scene.background = new THREE.Color(0x1e1b4b);
      scene.fog = new THREE.Fog(0x311042, 25, 95);

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
      carsRef.current.forEach((c) =>
        c.headlights.forEach((h) => {
          h.intensity = 7.5;
          h.color.setHex(0xe0f2fe);
        })
      );

      windowMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 3.5));
      streetlampMaterialsRef.current.forEach((m) => (m.emissiveIntensity = 5.0));

      if (roadMaterialRef.current) roadMaterialRef.current.roughness = 0.15;
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
    <div className="relative w-full h-full select-none overflow-hidden bg-slate-100">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {loading && (
        <div className="absolute inset-0 z-30 flex flex-col items-center justify-center bg-white/95 backdrop-blur-md text-slate-800">
          <div className="relative flex items-center justify-center mb-5">
            <div className="w-14 h-14 border-4 border-orange-500/20 border-t-orange-500 rounded-full animate-spin" />
            <span className="absolute text-xs font-mono text-orange-600 font-bold">{loadProgress}%</span>
          </div>
          <h3 className="text-lg font-bold font-display tracking-wider text-slate-900">
            Đang tải Đô Thị & Cung Đường Núi...
          </h3>
          <p className="text-xs text-slate-500 mt-1 font-light">
            Blender 5.2 • Xe chạy vô tận • Camera bám đuôi thời gian thực
          </p>
        </div>
      )}
    </div>
  );
};
