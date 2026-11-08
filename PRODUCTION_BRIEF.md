# Production Brief: Touge Mountain Canyon & Right-Side Environment Props

**Type:** Environment / Modular Touge Road & Canyon Props
**Target:** WebGL (Three.js) & Real-time Game Engine via Cloudflare Workers
**Style:** Stylized AAA Low-Poly / PBR Hybrid (60-30-10 Palette, solid materials, clean facet topology)
**Poly Budget:** Under 65,000 triangles total scene (Fast 60fps load on mobile & desktop WebGL)
**Texture Budget:** PBR Vertex Materials & Material Slot Colors (0 external texture files for zero-latency instant loading)
**Export:** GLTF / GLB (`mountain.glb` < 1.2 MB)
**Pivot:** Road centerline origin $(0, 0, 0)$, $Y$-Up coordinate system for Three.js compatibility
**Animation:** Procedural spline curve driving with accurate lane offset (+1.65m right-hand traffic)

### Active Skills
1. **blender-director** — Production pipeline orchestration, architectural scale, review verification
2. **blender-modeler** — Precision Edit Mode modeling, non-destructive modifiers, collection hierarchy (`COL_`)
3. **environment-artist** — Canyon geological terraces, rock spires, observation deck belvédère, scree formations
4. **asset-optimization** — Vertex sharing, low draw-call batching, clean normal recalculation

### Pipeline Phases
- [x] Reference & Planning (User request: right-hand lane driving & rich right-side canyon details)
- [ ] Scene Structure Setup (`COL_Road`, `COL_Canyon_Abyss`, `COL_ObservationDeck`, `COL_Nature_Forest`, `COL_Props_Highway`)
- [ ] Detail Modeling:
  - Observation Deck Belvédère (curved stone terrace, iron safety railings, tourist viewpoint binoculars, warning sign)
  - Canyon Rock Spires & Cliff Monoliths (vertical jagged geological needles rising from depth)
  - Roadside Highway Furniture (Yellow/Black Chevron curve warning arrows, Km milestones, delineator posts)
  - Mountain Cascade Waterfall & Rocky River Gorge
  - Triple-Layer Atmospheric Mist Volumes ($Z = -6m, -12m, -18m$)
  - Dense Forest Expansion (80+ alpine pine trees, shrub clusters along ledges)
- [ ] Cleanup & Normal Recalculation (Shared vertices, watertight geometry)
- [ ] GLB Export (`mountain.glb`) & Validation Renders in Blender
- [ ] Three.js Lane Driving Update (`CityCanvas.tsx` right lane offset +1.65m)
- [ ] Build & Cloudflare Deployment Verification via Browser Automation

### MCP Execution Plan
1. Construct script `build_clean_world.py` / `render_realistic_mountain.py` with expanded collections and props.
2. Run Blender to generate high-resolution close and wide verification renders.
3. Update Three.js car trajectory and camera tracking to lock into the right lane.
4. Deploy to Cloudflare Workers and execute headless browser QA verification.
