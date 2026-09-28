import re, sys

with open('build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update HTML bottom-nav buttons
old_nav = '''    <!-- Bottom Viewpoints Floating Bar -->
    <div class="bottom-nav">
        <button class="view-btn active" data-view="facade">
            <span class="label">1. 双联正房全貌</span>
            <span class="time">00:56 原视频全景</span>
        </button>
        <button class="view-btn" data-view="door">
            <span class="label">2. 堂屋拱券大门</span>
            <span class="time">03:00 斑驳门套与门神</span>
        </button>
        <button class="view-btn" data-view="west_stack">
            <span class="label">3. 西套木门与瓦垛</span>
            <span class="time">02:30 青瓦整齐堆码</span>
        </button>
        <button class="view-btn" data-view="east_ladder">
            <span class="label">4. 东次间木梯条凳</span>
            <span class="time">03:10 靠墙斜梯</span>
        </button>
        <button class="view-btn" data-view="east_wing">
            <span class="label">5. 房舍夹角与东厢房</span>
            <span class="time">01:05 夹角通透无它房</span>
        </button>
        <button class="view-btn" data-view="west_compound">
            <span class="label">6. 西邻红砖院落</span>
            <span class="time">02:20 烟囱与果园</span>
        </button>
        <button class="view-btn" data-view="rear_alley">
            <span class="label">7. 后檐翠柏夹道</span>
            <span class="time">08:15 背风防风绿篱</span>
        </button>
        <button class="view-btn" data-view="rear_overview">
            <span class="label">8. 后山俯瞰双坡顶</span>
            <span class="time">05:20 草垛与聚落全景</span>
        </button>
        <button class="view-btn" data-view="approach">
            <span class="label">9. 西南斜坡门墩</span>
            <span class="time">00:20 干砌石护坡</span>
        </button>
    </div>'''

new_nav = '''    <!-- Bottom Viewpoints Floating Bar -->
    <div class="bottom-nav">
        <button class="view-btn active" data-view="facade">
            <span class="label">1. 双联正房与石围墙大院</span>
            <span class="time">00:56 院落全貌</span>
        </button>
        <button class="view-btn" data-view="door">
            <span class="label">2. 堂屋拱券大门</span>
            <span class="time">03:00 斑驳门套与门神</span>
        </button>
        <button class="view-btn" data-view="west_stack">
            <span class="label">3. 西套木门与瓦垛</span>
            <span class="time">02:30 青瓦整齐堆码</span>
        </button>
        <button class="view-btn" data-view="west_annex">
            <span class="label">4. 西侧红瓦附房紧邻</span>
            <span class="time">01:44 紧挨正房/砖叠柱/柴堆</span>
        </button>
        <button class="view-btn" data-view="east_ladder">
            <span class="label">5. 东次间木梯条凳</span>
            <span class="time">03:10 靠墙斜梯</span>
        </button>
        <button class="view-btn" data-view="east_wing">
            <span class="label">6. 房舍夹角与东厢房</span>
            <span class="time">01:05 夹角通透无它房</span>
        </button>
        <button class="view-btn" data-view="west_compound">
            <span class="label">7. 西邻红砖院落</span>
            <span class="time">02:20 烟囱与果园</span>
        </button>
        <button class="view-btn" data-view="rear_alley">
            <span class="label">8. 后檐翠柏夹道</span>
            <span class="time">08:15 背风防风绿篱</span>
        </button>
        <button class="view-btn" data-view="rear_overview">
            <span class="label">9. 后山俯瞰双坡顶</span>
            <span class="time">05:20 草垛与聚落全景</span>
        </button>
        <button class="view-btn" data-view="approach">
            <span class="label">10. 西南坡道与毛石围墙</span>
            <span class="time">00:20 干砌石护坡门墩</span>
        </button>
    </div>'''

assert old_nav in code, "old_nav not found!"
code = code.replace(old_nav, new_nav)

# 2. Update Texture Pipeline (Section 1)
old_tex = '''    const tDoorEast = loadTexture('textures/doorway_full_patch.jpg');
    const tDoorWest = loadTexture('textures/timber_door_leaves.jpg');
    const tPillar = loadTexture('textures/tex_pillar_patch.jpg');
    const tWindow = loadTexture('textures/window_clean_authentic.jpg');
    const tStack = loadTexture('textures/tex_stack_patch.jpg');
    const tRoof = loadTexture('textures/tex_roof_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 12, 2);
    const tWing = loadTexture('textures/tex_wing_patch.jpg');
    const tStone = loadTexture('textures/tex_stone_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tEarth = loadTexture('textures/tex_earth_clean_pure.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 8, 2);
    const tGround = loadTexture('textures/tex_ground_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 20, 20);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);'''

new_tex = '''    const tDoorEast = loadTexture('textures/doorway_full_patch.jpg');
    const tDoorWest = loadTexture('textures/timber_door_leaves.jpg');
    const tPillar = loadTexture('textures/tex_pillar_patch.jpg');
    const tWindow = loadTexture('textures/window_clean_authentic.jpg');
    const tStack = loadTexture('textures/tex_stack_patch.jpg');
    const tRoof = loadTexture('textures/tex_roof_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 12, 2);
    const tWing = loadTexture('textures/tex_wing_patch.jpg');
    const tStone = loadTexture('textures/tex_stonewall_seamless.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 1.5);
    const tEarth = loadTexture('textures/tex_rammed_earth_clean.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tGround = loadTexture('textures/ground_seamless_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 18, 18);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tStackedBrick = loadTexture('textures/tex_video_stacked_brick_pillar.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 3);
    const tRedTile = loadTexture('textures/tex_redtile_seamless.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 3);
    const tAnnexWall = loadTexture('textures/tex_video_annex_earth_wall.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);'''

assert old_tex in code, "old_tex not found!"
code = code.replace(old_tex, new_tex)

# 3. Update Materials (Section 4)
old_mat = '''    const mRedTile = new THREE.MeshStandardMaterial({
        map: tRoof,
        color: 0x9a3e2e,
        roughness: 0.85,
        metalness: 0.06,
        side: THREE.DoubleSide
    });'''

new_mat = '''    const mRedTile = new THREE.MeshStandardMaterial({
        map: tRedTile,
        roughness: 0.84,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mStackedBrick = new THREE.MeshStandardMaterial({
        map: tStackedBrick,
        roughness: 0.88,
        metalness: 0.03,
        side: THREE.DoubleSide
    });

    const mAnnexEarth = new THREE.MeshStandardMaterial({
        map: tAnnexWall,
        color: 0xba9e74,
        roughness: 0.96,
        metalness: 0.01,
        side: THREE.DoubleSide
    });'''

assert old_mat in code, "old_mat not found!"
code = code.replace(old_mat, new_mat)

# 4. Update Terrain Elevation Function getTerrainY
old_terrain = '''    // Terrain Elevation Function
    function getTerrainY(x, z) {
        if (z < -4.5) {
            const dist = -z - 4.5;
            let elev = Math.pow(dist * 0.18, 1.25);
            if (x > 10.5 && z < -5.5) {
                elev = Math.max(elev, 2.3 + (x - 10.5) * 0.04);
            }
            return elev;
        } else if (z > 9.5 && x < -6) {
            return -(z - 9.5) * 0.16;
        } else if (z > 12.0) {
            const valleyDist = z - 12.0;
            return -1.2 - valleyDist * 0.10 + Math.sin(x * 0.15) * 0.12;
        } else {
            return Math.sin(x * 0.3) * Math.cos(z * 0.3) * 0.02;
        }
    }'''

new_terrain = '''    // Terrain Elevation Function (平整大院落与阶梯梯田护坎)
    function getTerrainY(x, z) {
        if (z < -4.5) {
            const dist = -z - 4.5;
            let elev = Math.pow(dist * 0.18, 1.25);
            if (x > 10.5 && z < -5.5) {
                elev = Math.max(elev, 2.3 + (x - 10.5) * 0.04);
            }
            return elev;
        } else if (z > 13.8 && x < -8.5) {
            // Southwest descending approach road
            const dist = (z - 13.8) * 0.16 + Math.max(0, -x - 8.5) * 0.07;
            return -Math.min(2.2, dist);
        } else if (z > 14.2) {
            // South terrace drop below courtyard stone retaining wall
            const valleyDist = z - 14.2;
            return -1.35 - valleyDist * 0.12 + Math.sin(x * 0.15) * 0.12;
        } else if (x < -16.0 && z > 0) {
            // West orchard slope
            return -(Math.abs(x) - 16.0) * 0.14;
        } else {
            // Expansive flat courtyard drying ground (院坝/打谷场, x: -14 to +16, z: 0 to 14)
            return Math.sin(x * 0.3) * Math.cos(z * 0.3) * 0.02;
        }
    }'''

assert old_terrain in code, "old_terrain not found!"
code = code.replace(old_terrain, new_terrain)

# 5. Update Section 7: Courtyard Dry Stone Perimeter Wall
old_sec7 = '''    // --- 7. Southwest Dry Stone Retaining Wall & Boulder Gatepost ---
    const stoneWallGroup = new THREE.Group();
    scene.add(stoneWallGroup);

    const wallPoints = [
        new THREE.Vector3(-26, -1.8, 22),
        new THREE.Vector3(-20, -1.2, 18),
        new THREE.Vector3(-14, -0.6, 15),
        new THREE.Vector3(-9.6, 0.0, 11.8)
    ];

    for (let p = 0; p < wallPoints.length - 1; p++) {
        const p1 = wallPoints[p];
        const p2 = wallPoints[p+1];
        const segLen = p1.distanceTo(p2);
        const wallH = 1.45;
        const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, wallH, 0.65), mStone);
        const mid = p1.clone().add(p2).multiplyScalar(0.5);
        wallSeg.position.set(mid.x, mid.y + wallH/2, mid.z);
        wallSeg.rotation.y = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;
        wallSeg.castShadow = true;
        wallSeg.receiveShadow = true;
        stoneWallGroup.add(wallSeg);

        // Stone Wall Coping Caps
        const coping = new THREE.Mesh(new THREE.BoxGeometry(segLen + 0.1, 0.12, 0.75), mStone);
        coping.position.set(mid.x, mid.y + wallH + 0.06, mid.z);
        coping.rotation.y = wallSeg.rotation.y;
        coping.castShadow = true;
        stoneWallGroup.add(coping);
    }

    // Natural Granite Gatepost Pillar at Courtyard Entrance (-9.6, 0, 11.8)
    const gatepostPillar = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.8, 0.85), mStone);
    gatepostPillar.position.set(-9.6, 0.9, 11.8);
    gatepostPillar.castShadow = true;
    gatepostPillar.receiveShadow = true;
    stoneWallGroup.add(gatepostPillar);

    const gatepostCap = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.22, 1.05), mStone);
    gatepostCap.position.set(-9.6, 1.8 + 0.11, 11.8);
    gatepostCap.castShadow = true;
    stoneWallGroup.add(gatepostCap);

    // Natural rough boulders flanking the entrance base
    const baseBoulder1 = new THREE.Mesh(new THREE.DodecahedronGeometry(0.65, 1), mStone);
    baseBoulder1.scale.set(1.2, 0.8, 1.1);
    baseBoulder1.position.set(-10.4, 0.35, 12.5);
    baseBoulder1.castShadow = true;
    stoneWallGroup.add(baseBoulder1);

    const baseBoulder2 = new THREE.Mesh(new THREE.DodecahedronGeometry(0.55, 1), mStone);
    baseBoulder2.scale.set(1.1, 0.75, 1.2);
    baseBoulder2.position.set(-9.2, 0.30, 12.7);
    baseBoulder2.castShadow = true;
    stoneWallGroup.add(baseBoulder2);'''

new_sec7 = '''    // --- 7. Courtyard Dry Stone Perimeter Wall & Boulder Gateposts (院子周围石头垒砌围墙与门垛, 视频实景还原) ---
    const stoneWallGroup = new THREE.Group();
    scene.add(stoneWallGroup);

    function buildWallRun(pts, wallH = 1.20, wallThick = 0.65, extraDown = 1.35) {
        for (let p = 0; p < pts.length - 1; p++) {
            const p1 = pts[p];
            const p2 = pts[p+1];
            const segLen = p1.distanceTo(p2);
            const mid = p1.clone().add(p2).multiplyScalar(0.5);
            const rotY = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;

            const totalH = wallH + extraDown;
            const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, totalH, wallThick), mStone);
            wallSeg.position.set(mid.x, mid.y - extraDown + totalH/2, mid.z);
            wallSeg.rotation.y = rotY;
            wallSeg.castShadow = true;
            wallSeg.receiveShadow = true;
            stoneWallGroup.add(wallSeg);

            // Rustic Stone Coping Slabs on top (条石/毛石压顶)
            const coping = new THREE.Mesh(new THREE.BoxGeometry(segLen + 0.1, 0.14, wallThick + 0.16), mStone);
            coping.position.set(mid.x, mid.y + wallH + 0.07, mid.z);
            coping.rotation.y = rotY;
            coping.castShadow = true;
            coping.receiveShadow = true;
            stoneWallGroup.add(coping);

            // Natural base boulders along wall rim
            const count = Math.max(1, Math.floor(segLen / 2.8));
            for (let b = 0; b < count; b++) {
                const t = (b + 0.5) / count;
                const bx = p1.x + (p2.x - p1.x) * t;
                const bz = p1.z + (p2.z - p1.z) * t;
                const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.36 + (b % 2) * 0.12, 1), mStone);
                boulder.scale.set(1.2, 0.75, 1.15);
                boulder.position.set(bx, mid.y + 0.15, bz);
                boulder.castShadow = true;
                stoneWallGroup.add(boulder);
            }
        }
    }

    // 1. South Courtyard Perimeter Wall (南侧通长石围墙, 完整环抱大院坝, 00:20-00:55视频实景)
    const southWallPoints = [
        new THREE.Vector3(-7.5, 0.0, 14.0),
        new THREE.Vector3(-1.5, 0.0, 14.5),
        new THREE.Vector3(4.5, 0.0, 14.8),
        new THREE.Vector3(10.5, 0.0, 15.0),
        new THREE.Vector3(16.0, 0.0, 14.8)
    ];
    buildWallRun(southWallPoints, 1.20, 0.65, 1.45);

    // 2. East Courtyard Boundary Wall (东侧石围墙/阶梯护坎, 连接东厢房)
    const eastWallPoints = [
        new THREE.Vector3(16.0, 0.0, 14.8),
        new THREE.Vector3(16.0, 0.0, 8.0),
        new THREE.Vector3(15.5, 0.0, 2.0),
        new THREE.Vector3(15.0, 0.0, -3.5)
    ];
    buildWallRun(eastWallPoints, 1.15, 0.65, 1.35);

    // 3. West Courtyard Boundary Wall (西侧院墙, 围护大院西边界)
    const westWallPoints = [
        new THREE.Vector3(-9.6, 0.0, 14.0),
        new THREE.Vector3(-14.2, 0.0, 13.8),
        new THREE.Vector3(-14.6, 0.0, 7.5),
        new THREE.Vector3(-14.2, 0.0, 2.5)
    ];
    buildWallRun(westWallPoints, 1.15, 0.65, 1.25);

    // 4. Southwest Approach Retaining Wall (西南斜坡步道护坡墙)
    const approachWallPoints = [
        new THREE.Vector3(-9.6, 0.0, 14.0),
        new THREE.Vector3(-15.0, -0.6, 17.0),
        new THREE.Vector3(-21.0, -1.2, 20.0),
        new THREE.Vector3(-27.0, -1.8, 23.0)
    ];
    buildWallRun(approachWallPoints, 1.35, 0.70, 1.50);

    // Courtyard Entrance Boulder Gateposts (-9.6 & -7.5 at z = 14.0)
    function addGatepost(gx, gz) {
        const post = new THREE.Mesh(new THREE.BoxGeometry(0.95, 1.85, 0.95), mStone);
        post.position.set(gx, 0.925, gz);
        post.castShadow = true;
        post.receiveShadow = true;
        stoneWallGroup.add(post);

        const cap = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.22, 1.15), mStone);
        cap.position.set(gx, 1.85 + 0.11, gz);
        cap.castShadow = true;
        stoneWallGroup.add(cap);

        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.65, 1), mStone);
        boulder.scale.set(1.25, 0.8, 1.15);
        boulder.position.set(gx + (gx < -8.5 ? -0.4 : 0.4), 0.35, gz + 0.4);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }
    addGatepost(-9.6, 14.0); // 西门垛
    addGatepost(-7.5, 14.0); // 东门垛'''

assert old_sec7 in code, "old_sec7 not found!"
code = code.replace(old_sec7, new_sec7)

# 6. Update Section 8: Veranda Pillars and Firewood Stack
old_pillars = '''    // 7 Veranda Columns: Concrete Cinder Blocks & Red Brick Footings (7根水泥空心砌块柱)
    const pillarPositionsX = [-9.6, -6.4, -3.2, 0.0, 3.2, 6.4, 9.6];
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
    });'''

new_pillars = '''    // 7 Veranda Columns: Concrete Cinder Blocks & Red Brick Footings
    // 西端立柱 (px = -9.6) 为烧结砖/泥土砖叠砌柱体 (01:44 实景)
    const pillarPositionsX = [-9.6, -6.4, -3.2, 0.0, 3.2, 6.4, 9.6];
    pillarPositionsX.forEach(px => {
        const brickBase = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.16, 0.44), mRedBrick);
        brickBase.position.set(px, 0.18 + 0.08, pillarZ);
        brickBase.castShadow = true;
        brickBase.receiveShadow = true;
        houseGroup.add(brickBase);

        const colMat = (px === -9.6) ? mStackedBrick : mPillar;
        const shaftMesh = new THREE.Mesh(new THREE.BoxGeometry(0.36, 2.35, 0.36), colMat);
        shaftMesh.position.set(px, 0.18 + 0.16 + 2.35/2, pillarZ);
        shaftMesh.castShadow = true;
        shaftMesh.receiveShadow = true;
        houseGroup.add(shaftMesh);
    });

    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        new THREE.MeshStandardMaterial({ map: tStraw, roughness: 0.94, color: 0x9e7f58 })
    );
    firewoodMesh.position.set(-8.0, 0.18 + 0.36, 0.05);
    firewoodMesh.castShadow = true;
    firewoodMesh.receiveShadow = true;
    houseGroup.add(firewoodMesh);'''

assert old_pillars in code, "old_pillars not found!"
code = code.replace(old_pillars, new_pillars)

# 7. Update Section 9: Attached West Low Red-Tiled Annex Shed
old_sec9 = '''    // --- 9. WEST LOW RED-TILED ANNEX SHED (西侧低矮红瓦附房/柴火房, 00:45, 07:10) ---
    const annexGroup = new THREE.Group();
    annexGroup.position.set(-halfWidth - 2.8, 0, -2.8);
    scene.add(annexGroup);

    const AW = 3.6;
    const AL = 4.2;
    const AH_front = 2.15;
    const AH_rear = 2.95;

    // Solid Rammed Earth Walls
    const annexNorth = new THREE.Mesh(new THREE.BoxGeometry(AW, AH_rear, 0.35), mEarth);
    annexNorth.position.set(0, 0.18 + AH_rear/2, -AL/2);
    annexNorth.castShadow = true;
    annexGroup.add(annexNorth);

    const annexSouth = new THREE.Mesh(new THREE.BoxGeometry(AW, AH_front, 0.35), mEarth);
    annexSouth.position.set(0, 0.18 + AH_front/2, AL/2);
    annexSouth.castShadow = true;
    annexGroup.add(annexSouth);

    const annexWest = new THREE.Mesh(new THREE.BoxGeometry(0.35, (AH_front + AH_rear)/2, AL), mEarth);
    annexWest.position.set(-AW/2, 0.18 + (AH_front + AH_rear)/4, 0);
    annexWest.castShadow = true;
    annexGroup.add(annexWest);

    const annexEast = new THREE.Mesh(new THREE.BoxGeometry(0.35, (AH_front + AH_rear)/2, AL), mEarth);
    annexEast.position.set(AW/2, 0.18 + (AH_front + AH_rear)/4, 0);
    annexEast.castShadow = true;
    annexGroup.add(annexEast);

    // Weathered Timber Door on South Wall
    const annexDoor = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.75, 0.05), mDoorWest);
    annexDoor.position.set(0.4, 0.18 + 0.875, AL/2 + 0.18);
    annexDoor.castShadow = true;
    annexGroup.add(annexDoor);

    // Single-Pitch Red Clay Tile Roof (单坡红瓦顶)
    const annexSlopeAngle = Math.atan2(AH_rear - AH_front, AL);
    const annexRoofLen = Math.sqrt((AH_rear - AH_front)**2 + AL**2) + 0.6;
    const annexRoof = new THREE.Mesh(new THREE.PlaneGeometry(AW + 0.5, annexRoofLen), mRedTile);
    annexRoof.rotation.x = -Math.PI / 2 + annexSlopeAngle;
    annexRoof.position.set(0, 0.18 + (AH_front + AH_rear)/2 + 0.12, 0);
    annexRoof.castShadow = true;
    annexRoof.receiveShadow = true;
    annexGroup.add(annexRoof);

    // Stone Slab Pavers in West Alley Walkway (西侧石板夹道小径)
    for (let sp = 0; sp < 8; sp++) {
        const paver = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.08, 0.6), mStone);
        paver.position.set(-halfWidth - 0.9, 0.06, -5.2 + sp * 0.9);
        paver.receiveShadow = true;
        scene.add(paver);
    }'''

new_sec9 = '''    // --- 9. WEST LOW RED-TILED ANNEX SHED (西侧低矮红瓦附房/柴火房, 紧邻正房 01:44 实景) ---
    const annexGroup = new THREE.Group();
    // 附房紧挨正房西山墙 (x = -9.6), 无任何缝隙隔道
    const AW = 4.2;
    const AL = 4.6;
    const AH_front = 2.20;
    const AH_rear = 3.25;

    // 附房东墙与主房西山墙完全重合贴紧: 中心 x = -9.6 - AW/2 = -11.7
    annexGroup.position.set(-halfWidth - AW/2, 0, 0.1 - AL/2);
    scene.add(annexGroup);

    // Solid Rammed Earth / Adobe Walls (真实土坯夯土墙)
    const annexNorth = new THREE.Mesh(new THREE.BoxGeometry(AW, AH_rear, 0.35), mAnnexEarth);
    annexNorth.position.set(0, 0.18 + AH_rear/2, -AL/2);
    annexNorth.castShadow = true;
    annexGroup.add(annexNorth);

    const annexSouth = new THREE.Mesh(new THREE.BoxGeometry(AW, AH_front, 0.35), mAnnexEarth);
    annexSouth.position.set(0, 0.18 + AH_front/2, AL/2);
    annexSouth.castShadow = true;
    annexGroup.add(annexSouth);

    const annexWest = new THREE.Mesh(new THREE.BoxGeometry(0.35, (AH_front + AH_rear)/2, AL), mAnnexEarth);
    annexWest.position.set(-AW/2, 0.18 + (AH_front + AH_rear)/4, 0);
    annexWest.castShadow = true;
    annexGroup.add(annexWest);

    // East Wall directly flush against main house west gable
    const annexEast = new THREE.Mesh(new THREE.BoxGeometry(0.35, (AH_front + AH_rear)/2, AL), mAnnexEarth);
    annexEast.position.set(AW/2, 0.18 + (AH_front + AH_rear)/4, 0);
    annexEast.castShadow = true;
    annexGroup.add(annexEast);

    // Weathered Timber Door on South Wall (紧靠主房砖叠柱与西山墙, x ~ -10.2)
    const annexDoor = new THREE.Mesh(new THREE.BoxGeometry(0.88, 1.80, 0.05), mDoorWest);
    annexDoor.position.set(AW/2 - 0.65, 0.18 + 0.90, AL/2 + 0.18);
    annexDoor.castShadow = true;
    annexGroup.add(annexDoor);

    // Single-Pitch Red Clay Tile Roof (单坡红瓦顶, 覆压红机瓦, 前挑出檐)
    const eaveOverhangZ = 0.65;
    const roofLen = Math.sqrt((AH_rear - AH_front)**2 + (AL + eaveOverhangZ)**2) + 0.45;
    const roofAngle = Math.atan2(AH_rear - AH_front, AL + eaveOverhangZ);

    const annexRoof = new THREE.Mesh(new THREE.PlaneGeometry(AW + 0.6, roofLen), mRedTile);
    annexRoof.rotation.x = -Math.PI / 2 + roofAngle;
    annexRoof.position.set(0, 0.18 + (AH_front + AH_rear)/2 + 0.16, eaveOverhangZ/2);
    annexRoof.castShadow = true;
    annexRoof.receiveShadow = true;
    annexGroup.add(annexRoof);

    // Front-West Corner Support Post (01:44 实景: 附房左前角立柱支撑挑檐)
    const annexPost = new THREE.Mesh(new THREE.BoxGeometry(0.14, AH_front, 0.14), mWood);
    annexPost.position.set(-AW/2 + 0.12, 0.18 + AH_front/2, AL/2 + eaveOverhangZ - 0.10);
    annexPost.castShadow = true;
    annexGroup.add(annexPost);

    // Front eave fascia beam connecting corner post to main house column
    const annexEaveBeam = new THREE.Mesh(new THREE.BoxGeometry(AW + eaveOverhangZ*0.5, 0.16, 0.16), mWood);
    annexEaveBeam.position.set(0.1, 0.18 + AH_front, AL/2 + eaveOverhangZ - 0.10);
    annexEaveBeam.castShadow = true;
    annexGroup.add(annexEaveBeam);

    // Stone Slab Pavers in West Lane Walkway (西侧外道石板小径, 位于附房西侧外)
    for (let sp = 0; sp < 8; sp++) {
        const paver = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.08, 0.6), mStone);
        paver.position.set(-halfWidth - AW - 0.85, 0.06, -4.5 + sp * 0.95);
        paver.receiveShadow = true;
        scene.add(paver);
    }'''

assert old_sec9 in code, "old_sec9 not found!"
code = code.replace(old_sec9, new_sec9)

# 8. Update Viewpoints (Section 16)
old_vp = '''    const viewpoints = {
        facade: {
            pos: new THREE.Vector3(-1.8, 2.4, 17.5),
            target: new THREE.Vector3(-0.4, 2.0, -1.0),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房全貌 (00:56)",
            body: "完整展现双联六开间硬山顶夯土正房立面，7根水泥空心砌块柱贯通排列，中段摆放整齐长瓦垛与红砖压顶，东侧拱门与靠墙木梯清晰可见，右侧连接东厢房。"
        },
        door: {
            pos: new THREE.Vector3(3.6, 1.5, 3.8),
            target: new THREE.Vector3(4.8, 1.45, -0.4),
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋拱券大门特写 (03:00)",
            body: "双扇老杉木门、泛黄褪色春联纸符、拱形石灰白边抹灰门套与门前条石门槛特写，左侧立柱与檐下挑梁结构。"
        },
        west_stack: {
            pos: new THREE.Vector3(-2.8, 1.6, 5.5),
            target: new THREE.Vector3(-1.6, 1.35, -0.4),
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "中次间长瓦垛与西套木门 (02:30)",
            body: "紧靠黄土墙脚下堆码的大量青瓦片与红砖压顶，与西套住宅木板门、白石灰饰边木窗构成鲜明而朴实的生活印记。"
        },
        east_ladder: {
            pos: new THREE.Vector3(5.6, 1.6, 5.2),
            target: new THREE.Vector3(7.4, 1.6, -0.4),
            refImg: "ref_images/ref_190s_ladder_wall.jpg",
            refTag: "M2U00577.MPG · 03:10",
            title: "东次间靠墙木梯与条凳 (03:10)",
            body: "木质长梯斜靠在前廊檐枋处，梯底摆放长木凳，左侧可见拱券大门，右侧近景为东厢房山墙夹道。"
        },
        east_wing: {
            pos: new THREE.Vector3(2.5, 1.60, 9.8),
            target: new THREE.Vector3(10.8, 1.70, 1.2),
            refImg: "ref_images/ref_065s_wing_corner.jpg",
            refTag: "M2U00577.MPG · 01:05",
            title: "主房与东厢房转折夹角全景 (01:05)",
            body: "严格对应视频1分05秒实景：主房东侧与东厢房转折夹角，夹角后方开阔通透，直接呈现北山林木与蓝天，无任何多余房舍阻挡；东厢房呈现土坯墙体、木门白灰套、直棂窗与塌角残垣。"
        },
        west_compound: {
            pos: new THREE.Vector3(-12.0, 1.65, 5.5),
            target: new THREE.Vector3(-24.5, 2.2, 1.0),
            refImg: "ref_images/ref_140s_west_neighbor.jpg",
            refTag: "M2U00577.MPG · 02:20",
            title: "西邻红砖院落与果园 (02:20)",
            body: "正房西侧隔道相邻的烧结红砖院落，高耸的红砖方形烟囱、围墙以及春日盛开的粉色桃花果园。"
        },
        rear_alley: {
            pos: new THREE.Vector3(-6.5, 1.40, -5.65),
            target: new THREE.Vector3(7.0, 1.40, -5.65),
            refImg: "ref_images/ref_495s_rear_alley.jpg",
            refTag: "M2U00577.MPG · 08:15",
            title: "后檐背风夹道与翠柏绿篱 (08:15)",
            body: "正房后檐下1.2米宽的窄长夹道，右侧为夯土后墙与石基，左侧为密植成排的翠绿侧柏防风林。"
        },
        rear_overview: {
            pos: new THREE.Vector3(3.2, 7.2, -16.5),
            target: new THREE.Vector3(-1.5, 2.7, -1.0),
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "后山俯瞰双坡顶与全景聚落 (05:20)",
            body: "从北侧后山坡地俯瞰双坡青瓦大屋顶与白灰正脊，近景为麦秸草垛，左侧为门楼与东厢房，右侧远景为西邻红砖房高烟囱与苍翠山峦。"
        },
        approach: {
            pos: new THREE.Vector3(-16.0, 1.35, 18.5),
            target: new THREE.Vector3(-5.0, 1.8, 4.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南斜坡步道与毛石门墩 (00:20)",
            body: "从西南坡道步入主院的沿途视角，左侧为毛石垒砌的护坡矮墙与巨石门墩，前方露出正房柱廊与远处林木。"
        }
    };'''

new_vp = '''    const viewpoints = {
        facade: {
            pos: new THREE.Vector3(-1.0, 2.8, 20.8),
            target: new THREE.Vector3(0.5, 1.8, 0.0),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房与石围墙大院 (00:56)",
            body: "近景为南侧环抱院落的干砌毛石围墙与石垛，开阔平整的泥土院场（打谷晒场），后方为完整的双联六开间夯土正房立面，7根立柱与中段青瓦垛整齐排列，西侧紧挨低矮红瓦附房，东侧连接东厢房。"
        },
        door: {
            pos: new THREE.Vector3(3.6, 1.5, 3.8),
            target: new THREE.Vector3(4.8, 1.45, -0.4),
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋拱券大门特写 (03:00)",
            body: "双扇老杉木门、泛黄褪色春联纸符、拱形石灰白边抹灰门套与门前条石门槛特写，左侧立柱与檐下挑梁结构。"
        },
        west_stack: {
            pos: new THREE.Vector3(-2.8, 1.6, 5.5),
            target: new THREE.Vector3(-1.6, 1.35, -0.4),
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "中次间长瓦垛与西套木门 (02:30)",
            body: "紧靠黄土墙脚下堆码的大量青瓦片与红砖压顶，与西套住宅木板门、白石灰饰边木窗构成鲜明而朴实的生活印记。"
        },
        west_annex: {
            pos: new THREE.Vector3(-6.8, 1.55, 9.2),
            target: new THREE.Vector3(-10.8, 1.85, -0.5),
            refImg: "ref_images/ref_104s_west_annex.jpg",
            refTag: "M2U00577.MPG · 01:44",
            title: "西侧红瓦附房与紧邻正房实景 (01:44)",
            body: "严格对应用户指出的实景对比：西侧低矮红瓦附房紧挨正房西山墙与立柱，红瓦单坡屋顶、左下角立柱支护出檐；正房西角采用烧结砖叠砌柱体，窗下堆码柴草堆，正房开间白灰门套与木门清晰可见，前方为开阔平整的泥土大院落与围墙环抱。"
        },
        east_ladder: {
            pos: new THREE.Vector3(5.6, 1.6, 5.2),
            target: new THREE.Vector3(7.4, 1.6, -0.4),
            refImg: "ref_images/ref_190s_ladder_wall.jpg",
            refTag: "M2U00577.MPG · 03:10",
            title: "东次间靠墙木梯与条凳 (03:10)",
            body: "木质长梯斜靠在前廊檐枋处，梯底摆放长木凳，左侧可见拱券大门，右侧近景为东厢房山墙夹道。"
        },
        east_wing: {
            pos: new THREE.Vector3(2.5, 1.60, 9.8),
            target: new THREE.Vector3(10.8, 1.70, 1.2),
            refImg: "ref_images/ref_065s_wing_corner.jpg",
            refTag: "M2U00577.MPG · 01:05",
            title: "主房与东厢房转折夹角全景 (01:05)",
            body: "严格对应视频1分05秒实景：主房东侧与东厢房转折夹角，夹角后方开阔通透，直接呈现北山林木与蓝天，无任何多余房舍阻挡；东厢房呈现土坯墙体、木门白灰套、直棂窗与塌角残垣。"
        },
        west_compound: {
            pos: new THREE.Vector3(-12.5, 1.65, 5.5),
            target: new THREE.Vector3(-24.5, 2.2, 1.0),
            refImg: "ref_images/ref_140s_west_neighbor.jpg",
            refTag: "M2U00577.MPG · 02:20",
            title: "西邻红砖院落与果园 (02:20)",
            body: "正房西侧隔道相邻的烧结红砖院落，高耸的红砖方形烟囱、围墙以及春日盛开的粉色桃花果园。"
        },
        rear_alley: {
            pos: new THREE.Vector3(-6.5, 1.40, -5.65),
            target: new THREE.Vector3(7.0, 1.40, -5.65),
            refImg: "ref_images/ref_495s_rear_alley.jpg",
            refTag: "M2U00577.MPG · 08:15",
            title: "后檐翠柏夹道与防风绿篱 (08:15)",
            body: "正房后檐下1.2米宽的窄长夹道，右侧为夯土后墙与石基，左侧为密植成排的翠绿侧柏防风林。"
        },
        rear_overview: {
            pos: new THREE.Vector3(3.2, 7.2, -16.5),
            target: new THREE.Vector3(-1.5, 2.7, -1.0),
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "后山俯瞰双坡顶与全景聚落 (05:20)",
            body: "从北侧后山坡地俯瞰双坡青瓦大屋顶与白灰正脊，近景为麦秸草垛，左侧为门楼与东厢房，右侧远景为西邻红砖房高烟囱与苍翠山峦。"
        },
        approach: {
            pos: new THREE.Vector3(-18.5, 1.35, 19.5),
            target: new THREE.Vector3(-7.5, 1.8, 8.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南斜坡步道与毛石围墙 (00:20)",
            body: "从西南坡道步入主院的沿途视角，左侧为毛石垒砌的护坡矮墙与巨石门墩，前方露出正房柱廊、红瓦附房与大院落围墙。"
        }
    };'''

assert old_vp in code, "old_vp not found!"
code = code.replace(old_vp, new_vp)

with open('build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully updated build_complete_compound.py with attached annex and courtyard stone wall!')
