# -*- coding: utf-8 -*-
import os

html_code = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>传统北方夯土民居院落 · 高精3D数字孪生系统</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
        body, html {
            width: 100%; height: 100%; overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            background-color: #0c0e12; color: #f2eee6;
        }
        #webgl-container { width: 100%; height: 100%; position: absolute; left: 0; top: 0; z-index: 1; }

        /* Top HUD */
        .top-bar {
            position: absolute; top: 16px; left: 20px; right: 20px; z-index: 10;
            display: flex; justify-content: space-between; align-items: center; pointer-events: none;
        }
        .title-badge {
            background: rgba(18, 20, 24, 0.92); backdrop-filter: blur(14px);
            padding: 12px 22px; border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 36px rgba(0, 0, 0, 0.55); pointer-events: auto;
        }
        .title-badge h1 {
            font-size: 17.5px; font-weight: 600; color: #f6f2e9;
            display: flex; align-items: center; gap: 10px;
        }
        .title-badge .subtitle {
            font-size: 12px; color: #a8a092; margin-top: 4px;
        }
        .status-tag {
            background: #2b7a4b; color: #e5ffed; font-size: 11px;
            padding: 2px 8px; border-radius: 6px; font-weight: 500;
        }

        .top-controls { display: flex; gap: 10px; pointer-events: auto; }
        .glass-btn {
            background: rgba(22, 25, 31, 0.9); backdrop-filter: blur(12px);
            color: #e2ded5; border: 1px solid rgba(255, 255, 255, 0.16);
            padding: 9px 16px; border-radius: 10px; font-size: 13px; font-weight: 500;
            cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex; align-items: center; gap: 6px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
        .glass-btn:hover {
            background: rgba(45, 52, 65, 0.95); border-color: rgba(255, 215, 0, 0.4);
            color: #fff; transform: translateY(-1px);
        }
        .glass-btn.active {
            background: #8b5e34; color: #fff; border-color: #d4a373;
            box-shadow: 0 0 12px rgba(212, 163, 115, 0.5);
        }

        /* Bottom Floating Viewpoint Bar */
        .bottom-nav {
            position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
            z-index: 10; background: rgba(18, 20, 24, 0.92); backdrop-filter: blur(16px);
            padding: 8px 12px; border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
            display: flex; gap: 6px; max-width: 95vw; overflow-x: auto;
        }
        .view-btn {
            background: transparent; border: 1px solid transparent; color: #b5b0a5;
            padding: 8px 14px; border-radius: 10px; font-size: 12.5px; font-weight: 500;
            cursor: pointer; transition: all 0.2s ease; white-space: nowrap;
            display: flex; flex-direction: column; align-items: center; gap: 2px;
        }
        .view-btn span.label { font-size: 12.5px; color: #f1ede4; }
        .view-btn span.time { font-size: 10px; color: #888277; }
        .view-btn:hover { background: rgba(255, 255, 255, 0.08); color: #fff; }
        .view-btn.active { background: #4a3728; border-color: #c99355; color: #fff; }
        .view-btn.active span.time { color: #e5b982; }

        /* Side Drawer */
        .comparison-drawer {
            position: absolute; top: 80px; right: 20px; width: 375px;
            max-height: calc(100vh - 180px); background: rgba(18, 20, 24, 0.95);
            backdrop-filter: blur(18px); border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 16px 48px rgba(0,0,0,0.7); z-index: 15;
            display: flex; flex-direction: column; overflow: hidden;
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.3s;
        }
        .comparison-drawer.collapsed { transform: translateX(410px); opacity: 0; pointer-events: none; }
        .drawer-header {
            padding: 14px 18px; border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(30, 34, 40, 0.7);
        }
        .drawer-header h3 { font-size: 14px; font-weight: 600; color: #f4ede1; }
        .close-drawer-btn {
            background: transparent; border: none; color: #8c867c; font-size: 20px;
            cursor: pointer; padding: 2px 6px; border-radius: 6px; line-height: 1;
        }
        .close-drawer-btn:hover { color: #fff; background: rgba(255, 255, 255, 0.1); }
        .drawer-content { padding: 16px; overflow-y: auto; font-size: 13px; color: #ccc5b9; line-height: 1.6; }
        .ref-image-wrapper {
            width: 100%; border-radius: 10px; overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15); margin-bottom: 12px;
            background: #000; position: relative;
        }
        .ref-image-wrapper img { width: 100%; height: auto; display: block; }
        .ref-image-tag {
            position: absolute; bottom: 8px; left: 8px; background: rgba(0, 0, 0, 0.78);
            font-size: 11px; color: #f7d794; padding: 2px 8px; border-radius: 4px; font-family: monospace;
        }
        .detail-card {
            background: rgba(255, 255, 255, 0.04); border-radius: 8px; padding: 12px;
            margin-bottom: 12px; border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .detail-card h4 { font-size: 13px; color: #e5b982; margin-bottom: 6px; }
        .detail-card ul { padding-left: 18px; font-size: 12px; color: #b5b0a5; }
        .detail-card li { margin-bottom: 4px; }

        /* Hotspot Pins */
        .hotspot-pin {
            position: absolute; transform: translate(-50%, -50%);
            width: 26px; height: 26px; background: rgba(212, 163, 115, 0.9);
            border: 2px solid #fff; border-radius: 50%; cursor: pointer;
            box-shadow: 0 0 16px rgba(212, 163, 115, 0.9);
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: bold; color: #2b1d0c;
            transition: transform 0.2s, background 0.2s; pointer-events: auto; z-index: 5;
        }
        .hotspot-pin:hover { transform: translate(-50%, -50%) scale(1.25); background: #ffd166; }
        .hotspot-label {
            position: absolute; left: 32px; top: 2px; background: rgba(18, 20, 24, 0.92);
            border: 1px solid rgba(255, 255, 255, 0.15); padding: 3px 8px; border-radius: 6px;
            font-size: 11px; white-space: nowrap; color: #eee; opacity: 0; pointer-events: none; transition: opacity 0.2s ease;
        }
        .hotspot-pin:hover .hotspot-label { opacity: 1; }

        /* Help Overlay */
        .help-overlay {
            position: absolute; left: 20px; bottom: 24px; z-index: 10;
            background: rgba(18, 20, 24, 0.88); backdrop-filter: blur(10px);
            padding: 10px 16px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 11.5px; color: #9e978c; line-height: 1.5; pointer-events: none;
        }
        .help-overlay b { color: #e5d7c3; }

        #crosshair {
            position: absolute; top: 50%; left: 50%; width: 8px; height: 8px;
            background: rgba(255, 255, 255, 0.7); border-radius: 50%;
            transform: translate(-50%, -50%); pointer-events: none; display: none; z-index: 20;
        }
    </style>
</head>
<body>
    <div id="webgl-container"></div>
    <div id="crosshair"></div>

    <div class="top-bar">
        <div class="title-badge">
            <h1>
                <span>三开间北方传统夯土民居院落 · 3D高精重构</span>
                <span class="status-tag">视频去隔行逐帧贴图</span>
            </h1>
            <div class="subtitle">正房三开间、水泥砌块廊柱、青瓦大屋顶、瓦垛、木梯、东厢房残破土墙、干砌石护坡</div>
        </div>

        <div class="top-controls">
            <button class="glass-btn" id="btn-toggle-drawer">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="15" y1="3" x2="15" y2="21"/></svg>
                <span>实景视频对照</span>
            </button>
            <button class="glass-btn" id="btn-light-mode">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
                <span id="light-label">晴朗正午</span>
            </button>
            <button class="glass-btn" id="btn-toggle-walk">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 4v16"/><path d="M17 8l-4-4-4 4"/></svg>
                <span id="mode-label">漫游漫步视角</span>
            </button>
        </div>
    </div>

    <!-- Bottom Viewpoints Floating Bar -->
    <div class="bottom-nav">
        <button class="view-btn active" data-view="facade">
            <span class="label">1. 正房立面全景</span>
            <span class="time">01:00 原视频正视</span>
        </button>
        <button class="view-btn" data-view="door">
            <span class="label">2. 堂屋大门特写</span>
            <span class="time">03:00 斑驳门套与春联</span>
        </button>
        <button class="view-btn" data-view="west">
            <span class="label">3. 西间瓦堆与窗</span>
            <span class="time">02:30 整齐瓦堆细节</span>
        </button>
        <button class="view-btn" data-view="east">
            <span class="label">4. 东间木梯与板凳</span>
            <span class="time">03:10 靠墙斜梯</span>
        </button>
        <button class="view-btn" data-view="wing">
            <span class="label">5. 东厢房残破土墙</span>
            <span class="time">01:10 土坯分层与破口</span>
        </button>
        <button class="view-btn" data-view="aerial">
            <span class="label">6. 后山俯瞰村落</span>
            <span class="time">05:20 青瓦屋脊全景</span>
        </button>
        <button class="view-btn" data-view="approach">
            <span class="label">7. 入口土坡石墙</span>
            <span class="time">00:20 干砌石护坡</span>
        </button>
    </div>

    <!-- Comparison Drawer -->
    <div class="comparison-drawer" id="comparison-drawer">
        <div class="drawer-header">
            <h3 id="drawer-title">原视频关键帧与建筑特征解析</h3>
            <button class="close-drawer-btn" id="close-drawer-btn">&times;</button>
        </div>
        <div class="drawer-content">
            <div class="ref-image-wrapper">
                <img id="ref-img" src="ref_images/ref_060s_main_facade.jpg" alt="Video Reference Frame">
                <div class="ref-image-tag" id="ref-tag">M2U00577.MPG · 01:00</div>
            </div>
            <div class="detail-card">
                <h4 id="detail-card-title">正房正立面构型 (01:00)</h4>
                <div id="detail-card-body">
                    <ul>
                        <li><b>建筑开间：</b>标准三开间硬山双坡顶，面宽约11.2米，进深约4.8米。</li>
                        <li><b>前廊立柱：</b>4根水泥空心砌块柱，每根由11层砌块拼砌，底部设双层烧结红砖基座。</li>
                        <li><b>墙面材质：</b>传统夯土/黄土泥坯墙，抹面风化露出黄土底色。</li>
                        <li><b>窗框工艺：</b>东西次间各一扇木窗，外框刷有一圈极具地域特色的白色石灰装饰边。</li>
                    </ul>
                </div>
            </div>
            <div class="detail-card">
                <h4>3D模型操作指南</h4>
                <ul style="color:#a8a29e;">
                    <li><b>旋转观察：</b>按住鼠标左键拖动</li>
                    <li><b>平移视角：</b>按住鼠标右键拖动</li>
                    <li><b>缩放视图：</b>滑动鼠标滚轮</li>
                    <li><b>进入第一人称漫游：</b>点击右上角“漫游漫步视角”或按键 [V]</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="help-overlay">
        <div>视角操作: <b>鼠标左键</b>旋转 · <b>右键</b>平移 · <b>滚轮</b>缩放</div>
        <div>细节考证: <b>点击场景金色图钉</b>自动平滑运镜并弹出视频对比</div>
    </div>

    <script src="libs/three.min.js"></script>
    <script src="libs/OrbitControls.js"></script>

    <script>
    // --- Texture Loader with Direct Video Extracts ---
    const texLoader = new THREE.TextureLoader();

    function loadTexture(path, wrapS = THREE.ClampToEdgeWrapping, wrapT = THREE.ClampToEdgeWrapping, repeatX = 1, repeatY = 1) {
        const tex = texLoader.load(path);
        tex.wrapS = wrapS;
        tex.wrapT = wrapT;
        tex.repeat.set(repeatX, repeatY);
        tex.encoding = THREE.sRGBEncoding;
        return tex;
    }

    const tDoor = loadTexture('textures/tex_door_patch.jpg');
    const tPillar = loadTexture('textures/tex_pillar_patch.jpg');
    const tWindow = loadTexture('textures/tex_window_patch.jpg');
    const tStack = loadTexture('textures/tex_stack_patch.jpg');
    const tRoof = loadTexture('textures/tex_roof_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tWing = loadTexture('textures/tex_wing_patch.jpg');
    const tStone = loadTexture('textures/tex_stone_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 3, 1);
    const tEarth = loadTexture('textures/tex_earth_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 2);
    const tGround = loadTexture('textures/tex_ground_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 8, 8);

    const tTreePoplar = loadTexture('textures/tree_real_alpha.png');
    const tTreeCypress = loadTexture('textures/cypress_real_alpha.png');
    const tTreePeach = loadTexture('textures/tree_peach.png');

    // --- Scene Setup ---
    const container = document.getElementById('webgl-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xaecce6);
    scene.fog = new THREE.FogExp2(0xc5daf0, 0.009);

    const camera = new THREE.PerspectiveCamera(46, window.innerWidth / window.innerHeight, 0.1, 400);
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.01;
    controls.minDistance = 2.0;
    controls.maxDistance = 120.0;

    // --- Warm Sunny Lighting matching Video ---
    const hemiLight = new THREE.HemisphereLight(0xfff5e6, 0x828a76, 0.85);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfffaec, 1.85);
    sunLight.position.set(-28, 42, 32);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 140;
    sunLight.shadow.camera.left = -22;
    sunLight.shadow.camera.right = 22;
    sunLight.shadow.camera.top = 22;
    sunLight.shadow.camera.bottom = -22;
    sunLight.shadow.bias = -0.0004;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xffdfb8, 0.35);
    fillLight.position.set(22, 16, -20);
    scene.add(fillLight);

    // --- Materials with Real Photo Textures ---
    const mEarth = new THREE.MeshStandardMaterial({
        map: tEarth,
        color: 0xaa8254,
        roughness: 0.94,
        metalness: 0.02
    });

    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        color: 0x5a5e64,
        roughness: 0.82,
        metalness: 0.12
    });

    const mPillar = new THREE.MeshStandardMaterial({
        map: tPillar,
        roughness: 0.88,
        metalness: 0.05
    });

    const mStone = new THREE.MeshStandardMaterial({
        map: tStone,
        roughness: 0.92,
        metalness: 0.05
    });

    const mGround = new THREE.MeshStandardMaterial({
        map: tGround,
        roughness: 0.96,
        metalness: 0.02
    });

    const mWood = new THREE.MeshStandardMaterial({
        color: 0x3d3023,
        roughness: 0.82,
        metalness: 0.05
    });

    const mRedBrick = new THREE.MeshStandardMaterial({
        color: 0x8a3828,
        roughness: 0.85,
        metalness: 0.03
    });

    // --- Ground & Mountain Backdrop ---
    const groundGeo = new THREE.PlaneGeometry(90, 90, 48, 48);
    const gPos = groundGeo.attributes.position;
    for (let i = 0; i < gPos.count; i++) {
        const x = gPos.getX(i);
        const y = gPos.getY(i);
        let zElev = 0;
        if (y < -3) { // Hillside rising behind house
            zElev = Math.pow(Math.abs(y + 3) * 0.18, 1.25);
        } else if (x < -6 && y > 8) { // Southwest path slope
            zElev = -(y - 8) * 0.12;
        }
        gPos.setZ(i, zElev + Math.sin(x*0.3)*Math.cos(y*0.3)*0.06);
    }
    groundGeo.computeVertexNormals();
    const groundMesh = new THREE.Mesh(groundGeo, mGround);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // Distant mountain cylinder
    const mountainGeo = new THREE.CylinderGeometry(160, 200, 45, 48, 1, true);
    const mountainMat = new THREE.MeshBasicMaterial({ color: 0x92a2b2, side: THREE.BackSide, fog: true });
    const mountainMesh = new THREE.Mesh(mountainGeo, mountainMat);
    mountainMesh.position.y = 8;
    scene.add(mountainMesh);

    // Blue ground survey marker (seen in frame 60s)
    const marker = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.45, 0.08), new THREE.MeshStandardMaterial({ color: 0x2277bb, roughness: 0.4 }));
    marker.position.set(1.5, 0.22, 4.2);
    marker.castShadow = true;
    scene.add(marker);

    // --- 1. Main House (正房/上房) Accurate Solid Modeling ---
    const houseGroup = new THREE.Group();
    scene.add(houseGroup);

    // Coordinates:
    // Front wall: z = -0.45
    // Porch columns: z = 0.55
    // Roof front eave: z = 0.95, y = 2.75
    // Roof ridge: z = -2.25, y = 4.65
    // Roof rear eave: z = -5.45, y = 2.75
    // Back wall: z = -5.05
    // Width: 11.2m (-5.6 to +5.6)
    const wallHeight = 2.75;

    // Raised Earthen Porch Plinth (黄土台基与散水)
    const plinthMesh = new THREE.Mesh(
        new THREE.BoxGeometry(11.8, 0.18, 6.4),
        new THREE.MeshStandardMaterial({ map: tGround, roughness: 0.96 })
    );
    plinthMesh.position.set(0, 0.09, -2.2);
    plinthMesh.receiveShadow = true;
    plinthMesh.castShadow = true;
    houseGroup.add(plinthMesh);

    // Back Solid Wall
    const rearWall = new THREE.Mesh(new THREE.BoxGeometry(11.2, wallHeight, 0.45), mEarth);
    rearWall.position.set(0, 0.18 + wallHeight/2, -5.05);
    rearWall.castShadow = true;
    rearWall.receiveShadow = true;
    houseGroup.add(rearWall);

    // Solid Gable Walls with Seamless Triangular Top to Ridge
    const gableShape = new THREE.Shape();
    gableShape.moveTo(0.55, 0); // front eave line
    gableShape.lineTo(-5.05, 0); // rear wall
    gableShape.lineTo(-5.05, wallHeight); // rear eave
    gableShape.lineTo(-2.25, 4.47); // ridge apex
    gableShape.lineTo(0.55, wallHeight); // front eave
    gableShape.closePath();

    const gableGeo = new THREE.ExtrudeGeometry(gableShape, { depth: 0.45, bevelEnabled: false });

    const westGable = new THREE.Mesh(gableGeo, mEarth);
    westGable.rotation.y = Math.PI / 2;
    westGable.position.set(-5.6, 0.18, 0);
    westGable.castShadow = true;
    westGable.receiveShadow = true;
    houseGroup.add(westGable);

    const eastGable = new THREE.Mesh(gableGeo, mEarth);
    eastGable.rotation.y = Math.PI / 2;
    eastGable.position.set(5.15, 0.18, 0);
    eastGable.castShadow = true;
    eastGable.receiveShadow = true;
    houseGroup.add(eastGable);

    // Front Wall (南立面夯土墙 at z = -0.45)
    const westFrontWall = new THREE.Mesh(new THREE.BoxGeometry(3.6, wallHeight, 0.4), mEarth);
    westFrontWall.position.set(-3.5, 0.18 + wallHeight/2, -0.45);
    westFrontWall.castShadow = true;
    westFrontWall.receiveShadow = true;
    houseGroup.add(westFrontWall);

    const eastFrontWall = new THREE.Mesh(new THREE.BoxGeometry(3.6, wallHeight, 0.4), mEarth);
    eastFrontWall.position.set(3.5, 0.18 + wallHeight/2, -0.45);
    eastFrontWall.castShadow = true;
    eastFrontWall.receiveShadow = true;
    houseGroup.add(eastFrontWall);

    const lintelWall = new THREE.Mesh(new THREE.BoxGeometry(2.4, wallHeight - 2.3, 0.4), mEarth);
    lintelWall.position.set(0, 0.18 + 2.3 + (wallHeight - 2.3)/2, -0.45);
    houseGroup.add(lintelWall);

    // Central Bay Doorway (堂屋大门与拱形白石灰套)
    const doorPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(2.0, 2.32),
        new THREE.MeshStandardMaterial({ map: tDoor, roughness: 0.85, metalness: 0.05 })
    );
    doorPlane.position.set(0, 0.18 + 2.32/2, -0.24);
    doorPlane.castShadow = true;
    houseGroup.add(doorPlane);

    // Raised Stone Door Sill (石门槛)
    const doorSill = new THREE.Mesh(
        new THREE.BoxGeometry(1.4, 0.12, 0.28),
        new THREE.MeshStandardMaterial({ color: 0x5e5a54, roughness: 0.9 })
    );
    doorSill.position.set(0, 0.18 + 0.06, -0.22);
    doorSill.castShadow = true;
    houseGroup.add(doorSill);

    // Windows with Real Video Texture (东西次间白灰框木窗)
    const mWindowReal = new THREE.MeshStandardMaterial({ map: tWindow, roughness: 0.8, metalness: 0.05 });
    const westWin = new THREE.Mesh(new THREE.PlaneGeometry(1.22, 1.22), mWindowReal);
    westWin.position.set(-3.4, 0.18 + 1.48, -0.24);
    houseGroup.add(westWin);

    const eastWin = new THREE.Mesh(new THREE.PlaneGeometry(1.22, 1.22), mWindowReal);
    eastWin.position.set(3.4, 0.18 + 1.48, -0.24);
    houseGroup.add(eastWin);

    // West Bay Stack of Roof Tiles (西次间窗下青瓦垛)
    const tileStackGroup = new THREE.Group();
    tileStackGroup.position.set(-3.4, 0.18, 0.05);

    const mainStack = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.82, 0.48),
        new THREE.MeshStandardMaterial({ map: tStack, roughness: 0.88, metalness: 0.08 })
    );
    mainStack.position.y = 0.41;
    mainStack.castShadow = true;
    mainStack.receiveShadow = true;
    tileStackGroup.add(mainStack);

    // Loose curved tiles leaning against stack
    for (let lt = 0; lt < 10; lt++) {
        const looseTile = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.18, 0.04), mRoof);
        looseTile.rotation.y = 0.18;
        looseTile.rotation.x = -0.32;
        looseTile.position.set(-0.88 + lt * 0.11, 0.11 + lt * 0.04, 0.22);
        looseTile.castShadow = true;
        tileStackGroup.add(looseTile);
    }
    houseGroup.add(tileStackGroup);

    // East Bay Wooden Ladder & Bench (东次间木梯与长条凳)
    const ladderGroup = new THREE.Group();
    ladderGroup.position.set(3.85, 0.18, 0.38);
    ladderGroup.rotation.x = -0.34;
    ladderGroup.rotation.y = 0.08;

    const railGeo = new THREE.BoxGeometry(0.08, 3.2, 0.1);
    const leftRail = new THREE.Mesh(railGeo, mWood);
    leftRail.position.set(-0.26, 1.55, 0);
    leftRail.castShadow = true;
    ladderGroup.add(leftRail);

    const rightRail = new THREE.Mesh(railGeo, mWood);
    rightRail.position.set(0.26, 1.55, 0);
    rightRail.castShadow = true;
    ladderGroup.add(rightRail);

    for (let r = 0; r < 8; r++) {
        const rung = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.52, 8), mWood);
        rung.rotation.z = Math.PI / 2;
        rung.position.set(0, 0.35 + r * 0.36, 0);
        rung.castShadow = true;
        ladderGroup.add(rung);
    }
    houseGroup.add(ladderGroup);

    // Rustic Long Bench (长条木凳)
    const benchGroup = new THREE.Group();
    benchGroup.position.set(2.8, 0.18, -0.15);
    const benchTop = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.06, 0.32), mWood);
    benchTop.position.y = 0.42;
    benchTop.castShadow = true;
    benchGroup.add(benchTop);
    for (let bx of [-0.55, 0.55]) {
        for (let bz of [-0.1, 0.1]) {
            const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.42, 0.06), mWood);
            leg.position.set(bx, 0.21, bz);
            leg.castShadow = true;
            benchGroup.add(leg);
        }
    }
    houseGroup.add(benchGroup);

    // 4 Veranda Columns (水泥空心砖柱与红砖基座)
    const pillarPositionsX = [-4.8, -1.6, 1.6, 4.8];
    const pillarZ = 0.55;

    pillarPositionsX.forEach(px => {
        const brickBase = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.16, 0.44), mRedBrick);
        brickBase.position.set(px, 0.18 + 0.08, pillarZ);
        brickBase.castShadow = true;
        brickBase.receiveShadow = true;
        houseGroup.add(brickBase);

        const shaftMesh = new THREE.Mesh(new THREE.BoxGeometry(0.36, 2.35, 0.36), mPillar);
        shaftMesh.position.set(px, 0.18 + 0.16 + 2.35/2, pillarZ);
        shaftMesh.castShadow = true;
        shaftMesh.receiveShadow = true;
        houseGroup.add(shaftMesh);
    });

    // Longitudinal Timber Tie-Beam (贯通大木枋)
    const eaveBeam = new THREE.Mesh(new THREE.BoxGeometry(11.6, 0.22, 0.28), mWood);
    eaveBeam.position.set(0, 0.18 + 2.58, pillarZ);
    eaveBeam.castShadow = true;
    houseGroup.add(eaveBeam);

    pillarPositionsX.forEach(px => {
        const tie = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.2, 1.05), mWood);
        tie.position.set(px, 0.18 + 2.55, 0.02);
        tie.castShadow = true;
        houseGroup.add(tie);
    });

    // Exposed Eave Rafter Tails (檐口椽木序列)
    const numRafters = 42;
    const rSpacing = 11.6 / numRafters;
    for (let i = 0; i <= numRafters; i++) {
        const rx = -5.8 + i * rSpacing;
        const rafter = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.08, 0.75), mWood);
        rafter.rotation.x = 0.54;
        rafter.position.set(rx, 0.18 + 2.68, pillarZ + 0.22);
        rafter.castShadow = true;
        houseGroup.add(rafter);
    }

    // CONTINUOUS WATERTIGHT ROOF GEOMETRY (双坡青瓦大屋顶)
    // Front Slope
    const frontRoofGeo = new THREE.PlaneGeometry(11.8, 3.75, 16, 8);
    const frontRoof = new THREE.Mesh(frontRoofGeo, mRoof);
    frontRoof.rotation.x = -Math.PI / 2 + 0.54;
    frontRoof.position.set(0, 0.18 + 3.7, -0.65);
    frontRoof.castShadow = true;
    frontRoof.receiveShadow = true;
    houseGroup.add(frontRoof);

    // Rear Slope
    const rearRoofGeo = new THREE.PlaneGeometry(11.8, 3.75, 16, 8);
    const rearRoof = new THREE.Mesh(rearRoofGeo, mRoof);
    rearRoof.rotation.x = -Math.PI / 2 - 0.54;
    rearRoof.position.set(0, 0.18 + 3.7, -3.85);
    rearRoof.castShadow = true;
    rearRoof.receiveShadow = true;
    houseGroup.add(rearRoof);

    // Dark Eaves Fascia Board (檐口封檐木板)
    const fasciaBoard = new THREE.Mesh(
        new THREE.BoxGeometry(11.8, 0.14, 0.08),
        new THREE.MeshStandardMaterial({ color: 0x221a12, roughness: 0.9 })
    );
    fasciaBoard.position.set(0, 0.18 + 2.76, 0.96);
    fasciaBoard.castShadow = true;
    houseGroup.add(fasciaBoard);

    // Under-Roof Soffit
    const underRoof = new THREE.Mesh(
        new THREE.PlaneGeometry(11.6, 1.4),
        new THREE.MeshStandardMaterial({ color: 0x261e14, roughness: 0.9 })
    );
    underRoof.rotation.x = Math.PI / 2 - 0.54;
    underRoof.position.set(0, 0.18 + 2.82, 0.15);
    houseGroup.add(underRoof);

    // Whitewashed Lime Mortar Ridge Cresting (白灰正脊)
    const ridgeMesh = new THREE.Mesh(
        new THREE.BoxGeometry(11.9, 0.26, 0.38),
        new THREE.MeshStandardMaterial({ color: 0xe5dfd7, roughness: 0.8 })
    );
    ridgeMesh.position.set(0, 0.18 + 4.65 + 0.12, -2.25);
    ridgeMesh.castShadow = true;
    houseGroup.add(ridgeMesh);

    for (let endX of [-5.95, 5.95]) {
        const finial = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.48, 4), new THREE.MeshStandardMaterial({ color: 0xdfd9ce, roughness: 0.8 }));
        finial.position.set(endX, 0.18 + 4.88, -2.25);
        finial.rotation.z = endX < 0 ? 0.38 : -0.38;
        houseGroup.add(finial);
    }

    // --- 2. East Wing Outbuilding (东厢房 / 侧屋) ---
    const wingGroup = new THREE.Group();
    wingGroup.position.set(6.4, 0, 1.8);
    scene.add(wingGroup);

    const W_W = 3.6;
    const W_L = 6.4;
    const W_EH = 2.45;
    const W_RH = 3.45;

    const wingNorthWall = new THREE.Mesh(new THREE.BoxGeometry(W_W, W_EH, 0.4), mEarth);
    wingNorthWall.position.set(0, 0.18 + W_EH/2, -W_L/2);
    wingGroup.add(wingNorthWall);

    const wingEastWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, W_EH, W_L), mEarth);
    wingEastWall.position.set(W_W/2 - 0.2, 0.18 + W_EH/2, 0);
    wingGroup.add(wingEastWall);

    const wingFrontWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, W_EH, 4.2), mEarth);
    wingFrontWall.position.set(-W_W/2 + 0.2, 0.18 + W_EH/2, -0.6);
    wingGroup.add(wingFrontWall);

    // Broken adobe breach patch
    const wingBrokenPlane = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.8), new THREE.MeshStandardMaterial({
        map: tWing,
        roughness: 0.9,
        metalness: 0.05
    }));
    wingBrokenPlane.rotation.y = -Math.PI / 2;
    wingBrokenPlane.position.set(-W_W/2 + 0.02, 0.18 + 1.1, 1.8);
    wingGroup.add(wingBrokenPlane);

    // Wing Roof
    const wingRoofW = new THREE.Mesh(new THREE.PlaneGeometry(W_L + 0.4, (W_W/2)/Math.cos(0.3) + 0.3), mRoof);
    wingRoofW.rotation.y = -Math.PI / 2;
    wingRoofW.rotation.x = -Math.PI / 2 + 0.3;
    wingRoofW.position.set(-W_W/4, 0.18 + (W_EH + W_RH)/2, 0);
    wingRoofW.castShadow = true;
    wingGroup.add(wingRoofW);

    const wingRoofE = new THREE.Mesh(new THREE.PlaneGeometry(W_L + 0.4, (W_W/2)/Math.cos(0.3) + 0.3), mRoof);
    wingRoofE.rotation.y = -Math.PI / 2;
    wingRoofE.rotation.x = -Math.PI / 2 - 0.3;
    wingRoofE.position.set(W_W/4, 0.18 + (W_EH + W_RH)/2, 0);
    wingRoofE.castShadow = true;
    wingGroup.add(wingRoofE);

    // --- 3. Connecting Gatehouse / Back Wall ---
    const gateWall = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.4, 0.35), mEarth);
    gateWall.position.set(5.5, 0.18 + 1.2, -2.5);
    scene.add(gateWall);

    const gateDoor = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.75, 0.08), mWood);
    gateDoor.position.set(5.5, 0.18 + 0.88, -2.5);
    scene.add(gateDoor);

    const gateRoof = new THREE.Mesh(new THREE.ConeGeometry(1.2, 0.5, 4), mRoof);
    gateRoof.position.set(5.5, 0.18 + 2.55, -2.5);
    gateRoof.rotation.y = Math.PI / 4;
    scene.add(gateRoof);

    // --- 4. Perimeter Dry Stone Retaining Wall & Entrance ---
    const stoneWallGroup = new THREE.Group();
    scene.add(stoneWallGroup);

    const wallPoints = [
        new THREE.Vector3(-14, 0, 11),
        new THREE.Vector3(-8, 0, 9.5),
        new THREE.Vector3(-5, 0, 8.5),
        new THREE.Vector3(-4.5, 0, 6.8),
        new THREE.Vector3(2.5, 0, 7.2),
        new THREE.Vector3(8.5, 0, 7.0)
    ];

    for (let p = 0; p < wallPoints.length - 1; p++) {
        if (p === 2) continue;
        const p1 = wallPoints[p];
        const p2 = wallPoints[p+1];
        const segLen = p1.distanceTo(p2);
        const wallH = 1.35;
        const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, wallH, 0.6), mStone);
        const mid = p1.clone().add(p2).multiplyScalar(0.5);
        wallSeg.position.set(mid.x, wallH/2, mid.z);
        wallSeg.rotation.y = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;
        wallSeg.castShadow = true;
        wallSeg.receiveShadow = true;
        stoneWallGroup.add(wallSeg);
    }

    const pierMat = new THREE.MeshStandardMaterial({ color: 0x68645c, roughness: 0.95 });
    for (let b = 0; b < 4; b++) {
        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.52 + Math.random()*0.2, 1), pierMat);
        boulder.scale.set(1.15, 0.85, 1.15);
        boulder.position.set(-4.6 + (Math.random()-0.5)*0.2, 0.35 + b * 0.45, 7.2);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }

    // --- 5. Haystacks / Straw Bundles on Hillside ---
    const haystackMat = new THREE.MeshStandardMaterial({ color: 0x82643a, roughness: 0.95 });
    function createHaystack(x, z, r, h) {
        const stackGeo = new THREE.CylinderGeometry(r * 0.75, r, h, 14);
        const stackMesh = new THREE.Mesh(stackGeo, haystackMat);
        stackMesh.position.set(x, 1.5 + h/2, z);
        stackMesh.castShadow = true;
        scene.add(stackMesh);

        const capGeo = new THREE.ConeGeometry(r * 0.88, h * 0.6, 14);
        const capMesh = new THREE.Mesh(capGeo, haystackMat);
        capMesh.position.set(x, 1.5 + h + h * 0.3, z);
        capMesh.castShadow = true;
        scene.add(capMesh);
    }
    createHaystack(1.8, -7.8, 1.3, 1.1);
    createHaystack(-1.5, -8.5, 1.6, 1.35);

    // --- 6. REALISTIC TREES & VEGETATION (真实行道树与翠柏) ---
    const treeGroup = new THREE.Group();
    scene.add(treeGroup);

    function addPoplarTree(x, z, width, height, groundBaseY = 1.5) {
        const planeGeo = new THREE.PlaneGeometry(width, height);
        const mat = new THREE.MeshStandardMaterial({
            map: tTreePoplar,
            transparent: true,
            alphaTest: 0.15,
            roughness: 0.9,
            side: THREE.DoubleSide
        });
        const t1 = new THREE.Mesh(planeGeo, mat);
        t1.position.set(x, groundBaseY + height/2, z);
        t1.castShadow = true;
        treeGroup.add(t1);

        const t2 = new THREE.Mesh(planeGeo, mat);
        t2.position.set(x, groundBaseY + height/2, z);
        t2.rotation.y = Math.PI / 2;
        t2.castShadow = true;
        treeGroup.add(t2);
    }

    function addCypressTree(x, z, width, height, groundBaseY = 1.5) {
        const planeGeo = new THREE.PlaneGeometry(width, height);
        const mat = new THREE.MeshStandardMaterial({
            map: tTreeCypress,
            transparent: true,
            alphaTest: 0.2,
            roughness: 0.85,
            side: THREE.DoubleSide
        });
        const c1 = new THREE.Mesh(planeGeo, mat);
        c1.position.set(x, groundBaseY + height/2, z);
        c1.castShadow = true;
        treeGroup.add(c1);

        const c2 = new THREE.Mesh(planeGeo, mat);
        c2.position.set(x, groundBaseY + height/2, z);
        c2.rotation.y = Math.PI / 2;
        c2.castShadow = true;
        treeGroup.add(c2);
    }

    function addPeachTree(x, z, width, height) {
        const planeGeo = new THREE.PlaneGeometry(width, height);
        const mat = new THREE.MeshStandardMaterial({
            map: tTreePeach,
            transparent: true,
            alphaTest: 0.15,
            roughness: 0.8,
            side: THREE.DoubleSide
        });
        const p1 = new THREE.Mesh(planeGeo, mat);
        p1.position.set(x, 1.2 + height/2, z);
        p1.castShadow = true;
        treeGroup.add(p1);

        const p2 = new THREE.Mesh(planeGeo, mat);
        p2.position.set(x, 1.2 + height/2, z);
        p2.rotation.y = Math.PI / 2;
        p2.castShadow = true;
        treeGroup.add(p2);
    }

    // Tall towering poplars on the hillside behind house
    addPoplarTree(-4.2, -8.2, 8.5, 17, 2.2);
    addPoplarTree(0.8, -8.6, 9.0, 18, 2.5);
    addPoplarTree(5.0, -8.2, 8.0, 16.5, 2.2);
    addPoplarTree(-7.5, 11.0, 6.5, 13, 0.0);

    // Cypress trees
    addCypressTree(-2.4, -7.6, 3.2, 9.5, 2.0);
    addCypressTree(2.6, -7.8, 3.4, 10.0, 2.0);
    addCypressTree(6.8, -7.4, 3.0, 8.8, 2.0);
    addCypressTree(-8.8, 9.2, 3.0, 8.2, 0.0);

    addPeachTree(9.5, -4.5, 4.5, 4.5);

    // Wild bushes & weed tufts
    const bushMat = new THREE.MeshStandardMaterial({ color: 0x5a5c3c, roughness: 0.95 });
    for (let b = 0; b < 28; b++) {
        const bush = new THREE.Mesh(new THREE.DodecahedronGeometry(0.38 + Math.random()*0.3, 1), bushMat);
        bush.scale.set(1.2, 0.65, 1.2);
        const bx = -11 + Math.random() * 22;
        const bz = 4.5 + Math.random() * 5.5;
        bush.position.set(bx, 0.25, bz);
        bush.castShadow = true;
        scene.add(bush);
    }

    // --- Interactive 3D Hotspot Pins ---
    const hotspots = [
        {
            id: "door",
            name: "堂屋大门与春联",
            pos: new THREE.Vector3(0, 1.4, -0.2),
            view: "door",
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋对开门与拱门白灰套",
            body: "深色老杉木竖向拼板门，表面贴有泛白退色的春联横批、两侧门联与门扇中央两张菱形斗方/门神。外围为具有地方特色的拱券形白石灰抹灰套，呈现真实的自然剥落露土肌理。"
        },
        {
            id: "west_stack",
            name: "西间整齐瓦堆",
            pos: new THREE.Vector3(-3.4, 0.8, 0.2),
            view: "west",
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "西次间窗下堆叠青瓦",
            body: "西次间泥墙窗台下整齐码放着数百片传统灰青色弧形屋瓦，垛高约0.8米，呈规整排列。上方为白石灰饰边方形木窗，内含深色木质窗框。"
        },
        {
            id: "east_ladder",
            name: "东间靠墙木梯",
            pos: new THREE.Vector3(3.8, 1.6, 0.4),
            view: "east",
            refImg: "ref_images/ref_190s_ladder_wall.jpg",
            refTag: "M2U00577.MPG · 03:10",
            title: "东次间斜靠杉木直梯",
            body: "一把双侧木梁、多横档的老木梯斜靠在前廊大木枋与夯土墙上，下方摆放有一张传统实木长条矮凳。"
        },
        {
            id: "pillars",
            name: "水泥空心立柱",
            pos: new THREE.Vector3(-1.6, 1.4, pillarZ),
            view: "facade",
            refImg: "ref_images/ref_165s_main_door.jpg",
            refTag: "M2U00577.MPG · 02:45",
            title: "预制水泥砌块廊柱",
            body: "4根方形廊柱支撑前廊屋檐，精准还原自视频中11层灰水泥空心砖自下而上砌筑的结构，柱底以双层烧结实心红砖作为防潮基础，柱顶承托贯通木质挑梁与椽条。"
        },
        {
            id: "wing_wall",
            name: "东厢房残破土墙",
            pos: new THREE.Vector3(6.4 - W_W/2, 1.2, 3.6),
            view: "wing",
            refImg: "ref_images/ref_070s_east_wing.jpg",
            refTag: "M2U00577.MPG · 01:10",
            title: "东厢房夯土砖层与残损破口",
            body: "东侧厢房墙面清晰显露横向夯土层次与掺杂草筋的土坯构造。墙角处有因自然风化坍塌形成的大缺口，直观展现了黄土民居原生的厚重质感。"
        },
        {
            id: "stone_retaining",
            name: "干砌块石护坡",
            pos: new THREE.Vector3(-4.5, 0.9, 7.8),
            view: "approach",
            refImg: "ref_images/ref_050s_gate_view.jpg",
            refTag: "M2U00577.MPG · 00:50",
            title: "院前干砌毛石挡土墙与巨石门墩",
            body: "院落地势高于外侧坡道，南侧与西南侧由天然乱石干砌成阶梯状护坡挡墙，入口处堆垒大块花岗岩原石作为门墩标志。"
        },
        {
            id: "roof_overview",
            name: "双坡青瓦屋脊",
            pos: new THREE.Vector3(0, 4.8, -2.25),
            view: "aerial",
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "北方青瓦垄沟与白灰正脊",
            body: "双坡屋面铺覆深灰青瓦，瓦垄排列严密，正脊抹白灰砂浆勾缝，东西两端做出微起翘的传统脊头造型。"
        }
    ];

    const hotspotElements = [];
    hotspots.forEach(h => {
        const pin = document.createElement('div');
        pin.className = 'hotspot-pin';
        pin.innerHTML = '✦<div class="hotspot-label">' + h.name + '</div>';
        container.appendChild(pin);

        pin.addEventListener('click', () => {
            switchView(h.view);
            updateDrawer(h);
        });

        hotspotElements.push({ el: pin, pos: h.pos });
    });

    function updateHotspotsScreenPosition() {
        const tempV = new THREE.Vector3();
        hotspotElements.forEach(item => {
            tempV.copy(item.pos).project(camera);
            if (tempV.z < 1) {
                const x = (tempV.x * 0.5 + 0.5) * window.innerWidth;
                const y = (-(tempV.y * 0.5) + 0.5) * window.innerHeight;
                item.el.style.display = 'flex';
                item.el.style.left = `${x}px`;
                item.el.style.top = `${y}px`;
            } else {
                item.el.style.display = 'none';
            }
        });
    }

    // --- Camera Viewpoint Definitions (Aligned with Video Frame Framing) ---
    const viewpoints = {
        facade: {
            pos: new THREE.Vector3(0.5, 1.8, 12.8),
            target: new THREE.Vector3(0.5, 2.25, -1.2),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 01:00",
            title: "正房正立面构型 (01:00)",
            body: "三开间硬山顶夯土正房立面，4根水泥空心砌块柱清晰可见，西侧摆放整齐瓦堆，东侧靠有杉木梯子，右侧连接东厢房。"
        },
        door: {
            pos: new THREE.Vector3(0, 1.5, 2.2),
            target: new THREE.Vector3(0, 1.45, -0.4),
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋大门特写 (03:00)",
            body: "双扇木板门、泛黄褪色春联纸符、拱形石灰白边抹灰门套与门前条石门槛特写。"
        },
        west: {
            pos: new THREE.Vector3(-3.4, 1.35, 2.6),
            target: new THREE.Vector3(-3.4, 1.25, -0.4),
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "西次间瓦堆与白框木窗 (02:30)",
            body: "紧靠黄土墙脚下堆码的大量青瓦片，与上方带白石灰饰边的木窗构成鲜明而朴实的生活生产印记。"
        },
        east: {
            pos: new THREE.Vector3(3.8, 1.6, 2.8),
            target: new THREE.Vector3(3.8, 1.7, -0.4),
            refImg: "ref_images/ref_190s_ladder_wall.jpg",
            refTag: "M2U00577.MPG · 03:10",
            title: "东次间靠墙木梯 (03:10)",
            body: "木质长梯搭靠在廊枋处，梯底摆放长木凳，右侧近景为东厢房山墙夹道。"
        },
        wing: {
            pos: new THREE.Vector3(2.5, 1.6, 2.8),
            target: new THREE.Vector3(6.4, 1.6, 2.6),
            refImg: "ref_images/ref_070s_east_wing.jpg",
            refTag: "M2U00577.MPG · 01:10",
            title: "东厢房侧立面与破口 (01:10)",
            body: "展示东厢房土坯墙体、木板小门、直棂木栅窗以及西南角大面积残损塌落的断口细节。"
        },
        aerial: {
            pos: new THREE.Vector3(-1.0, 10.5, -15.5),
            target: new THREE.Vector3(1.2, 2.2, 0),
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "后山俯瞰院落与村落远山 (05:20)",
            body: "站在北侧山坡上俯瞰双坡瓦顶、连接门楼、草堆柴垛与远处隐约可见的山峦村舍。"
        },
        approach: {
            pos: new THREE.Vector3(-9.5, 0.8, 15.0),
            target: new THREE.Vector3(-2.0, 1.8, 4.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "入口斜坡与干砌石护坡 (00:20)",
            body: "从西南坡道步入主院的沿途视角，左侧为毛石垒砌的护坡矮墙，前方露出院内瓦顶与大树。"
        }
    };

    let targetCamPos = viewpoints.facade.pos.clone();
    let targetLookAt = viewpoints.facade.target.clone();
    let isTransitioning = false;

    function switchView(viewKey) {
        const v = viewpoints[viewKey];
        if (!v) return;

        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewKey);
        });

        targetCamPos = v.pos.clone();
        targetLookAt = v.target.clone();
        isTransitioning = true;

        updateDrawer(v);
        location.hash = viewKey;
    }

    function updateDrawer(info) {
        document.getElementById('ref-img').src = info.refImg;
        document.getElementById('ref-tag').textContent = info.refTag;
        document.getElementById('drawer-title').textContent = info.name || info.title;
        document.getElementById('detail-card-title').textContent = info.title;
        document.getElementById('detail-card-body').innerHTML = `<p>${info.body}</p>`;
    }

    const initialHash = location.hash.replace('#', '');
    if (initialHash && viewpoints[initialHash]) {
        switchView(initialHash);
        camera.position.copy(viewpoints[initialHash].pos);
        controls.target.copy(viewpoints[initialHash].target);
    } else {
        camera.position.copy(viewpoints.facade.pos);
        controls.target.copy(viewpoints.facade.target);
    }
    controls.update();

    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    const drawer = document.getElementById('comparison-drawer');
    document.getElementById('btn-toggle-drawer').addEventListener('click', () => {
        drawer.classList.toggle('collapsed');
    });
    document.getElementById('close-drawer-btn').addEventListener('click', () => {
        drawer.classList.add('collapsed');
    });

    const lightModes = [
        { name: "晴朗正午", sunPos: [-28, 42, 32], sunColor: 0xfffaed, sunInt: 1.85, hemiSky: 0xfff5e6, bg: 0xaecce6 },
        { name: "清晨柔光", sunPos: [-45, 18, 25], sunColor: 0xffe2b8, sunInt: 1.5, hemiSky: 0xd9e5f5, bg: 0xa9cce8 },
        { name: "金色黄昏", sunPos: [-45, 12, 12], sunColor: 0xff9944, sunInt: 2.1, hemiSky: 0xf5ccaa, bg: 0xd99566 },
        { name: "阴天漫射", sunPos: [0, 50, 0], sunColor: 0xdbe0e5, sunInt: 1.1, hemiSky: 0xcfd5db, bg: 0xc2ccd4 }
    ];
    let curLightIdx = 0;
    document.getElementById('btn-light-mode').addEventListener('click', () => {
        curLightIdx = (curLightIdx + 1) % lightModes.length;
        const mode = lightModes[curLightIdx];
        document.getElementById('light-label').textContent = mode.name;

        sunLight.position.set(mode.sunPos[0], mode.sunPos[1], mode.sunPos[2]);
        sunLight.color.setHex(mode.sunColor);
        sunLight.intensity = mode.sunInt;
        hemiLight.color.setHex(mode.hemiSky);
        scene.background.setHex(mode.bg);
        scene.fog.color.setHex(mode.bg);
    });

    // Walk Mode
    let isWalkMode = false;
    const btnToggleWalk = document.getElementById('btn-toggle-walk');
    const modeLabel = document.getElementById('mode-label');
    const crosshair = document.getElementById('crosshair');

    btnToggleWalk.addEventListener('click', () => {
        isWalkMode = !isWalkMode;
        if (isWalkMode) {
            btnToggleWalk.classList.add('active');
            modeLabel.textContent = "返回轨道视角";
            crosshair.style.display = 'block';
            controls.enabled = false;
            camera.position.y = 1.68;
        } else {
            btnToggleWalk.classList.remove('active');
            modeLabel.textContent = "漫游漫步视角";
            crosshair.style.display = 'none';
            controls.enabled = true;
            controls.target.set(0, 1.8, 0);
        }
    });

    const keys = { w: false, a: false, s: false, d: false };
    window.addEventListener('keydown', (e) => {
        const k = e.key.toLowerCase();
        if (k in keys) keys[k] = true;
        if (k === 'v') btnToggleWalk.click();
    });
    window.addEventListener('keyup', (e) => {
        const k = e.key.toLowerCase();
        if (k in keys) keys[k] = false;
    });

    let isMouseDown = false;
    let prevMouseX = 0, prevMouseY = 0;
    let walkYaw = 0, walkPitch = 0;

    window.addEventListener('mousedown', (e) => {
        isMouseDown = true;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
    });
    window.addEventListener('mouseup', () => { isMouseDown = false; });
    window.addEventListener('mousemove', (e) => {
        if (!isWalkMode || !isMouseDown) return;
        const dx = e.clientX - prevMouseX;
        const dy = e.clientY - prevMouseY;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;

        walkYaw -= dx * 0.003;
        walkPitch = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, walkPitch - dy * 0.003));

        const lookDir = new THREE.Vector3(
            Math.sin(walkYaw) * Math.cos(walkPitch),
            Math.sin(walkPitch),
            -Math.cos(walkYaw) * Math.cos(walkPitch)
        );
        camera.lookAt(camera.position.clone().add(lookDir));
    });

    const clock = new THREE.Clock();
    function animate() {
        requestAnimationFrame(animate);
        const dt = clock.getDelta();

        if (isTransitioning) {
            camera.position.lerp(targetCamPos, 0.07);
            controls.target.lerp(targetLookAt, 0.07);
            controls.update();
            if (camera.position.distanceTo(targetCamPos) < 0.05) {
                isTransitioning = false;
            }
        } else if (controls.enabled) {
            controls.update();
        }

        if (isWalkMode) {
            const moveSpeed = 4.5 * dt;
            const forward = new THREE.Vector3();
            camera.getWorldDirection(forward);
            forward.y = 0;
            forward.normalize();
            const right = new THREE.Vector3(-forward.z, 0, forward.x);

            if (keys.w) camera.position.addScaledVector(forward, moveSpeed);
            if (keys.s) camera.position.addScaledVector(forward, -moveSpeed);
            if (keys.a) camera.position.addScaledVector(right, -moveSpeed);
            if (keys.d) camera.position.addScaledVector(right, moveSpeed);

            let groundH = 0;
            if (camera.position.z < -3) {
                groundH = Math.pow(Math.abs(camera.position.z + 3) * 0.18, 1.25);
            }
            camera.position.y = groundH + 1.68;
        }

        updateHotspotsScreenPosition();
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    </script>
</body>
</html>
'''

with open('/Users/roy/Documents/workspace/courtyard_3d/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("Successfully updated index.html to v3!")
