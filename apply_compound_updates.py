import re

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Texture Pipeline definitions
old_tex_block = """    const tDoorEast = loadTexture('textures/doorway_full_patch.jpg');
    const tDoorWest = loadTexture('textures/timber_door_leaves.jpg');
    const tPillar = loadTexture('textures/tex_pillar_patch.jpg');
    const tWindow = loadTexture('textures/win_casing_exact.jpg');
    const tStack = loadTexture('textures/tex_stack_patch.jpg');
    const tRoof = loadTexture('textures/tex_roof_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 12, 2);
    const tWing = loadTexture('textures/tex_wing_patch.jpg');
    const tStone = loadTexture('textures/tex_stonewall_horizontal.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 1.8);
    const tEarth = loadTexture('textures/tex_rammed_earth_clean.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tGround = loadTexture('textures/ground_seamless_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 16, 16);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tStackedBrick = loadTexture('textures/tex_video_stacked_brick_pillar.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 3);
    const tRedTile = loadTexture('textures/tex_red_roof_authentic.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 5, 3);
    const tAnnexWall = loadTexture('textures/tex_video_annex_earth_wall.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);
    const tFirewood = loadTexture('textures/tex_firewood_logs.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 1.5);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);"""

new_tex_block = """    const tDoorEast = loadTexture('textures/doorway_full_patch.jpg');
    const tDoorWest = loadTexture('textures/timber_door_leaves.jpg');
    const tPillar = loadTexture('textures/tex_pillar_patch.jpg');
    const tWindow = loadTexture('textures/win_casing_exact.jpg');
    const tStack = loadTexture('textures/tex_stack_patch.jpg');
    const tRoof = loadTexture('textures/tex_roof_patch.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 12, 2);
    const tWing = loadTexture('textures/tex_wing_patch.jpg');
    const tStone = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 3, 1.2);
    const tEarth = loadTexture('textures/tex_rammed_earth_authentic.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 3, 2);
    const tGround = loadTexture('textures/tex_authentic_courtyard_ground.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 14, 14);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tStackedBrick = loadTexture('textures/tex_video_stacked_brick_pillar.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 3);
    const tRedTile = loadTexture('textures/tex_authentic_red_tile.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 3);
    const tAnnexWall = loadTexture('textures/tex_rammed_earth_authentic.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);
    const tAnnexDoor = loadTexture('textures/tex_video_annex_door.jpg');
    const tFirewood = loadTexture('textures/tex_video_firewood_exact.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 1);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);"""

assert old_tex_block in code, "old_tex_block not found"
code = code.replace(old_tex_block, new_tex_block)

# 2. Update Lighting block
old_light_block = """    // Front Veranda Ambient Soft Fill Light (防止檐下死黑, 还原阴影通透感)
    const verandaFillLight = new THREE.DirectionalLight(0xffeedd, 0.85);
    verandaFillLight.position.set(-6, 8, 22);
    scene.add(verandaFillLight);"""

new_light_block = """    // Front Veranda Ambient Soft Fill Light (防止檐下死黑, 还原阴影通透感)
    const verandaFillLight = new THREE.DirectionalLight(0xffeedd, 0.90);
    verandaFillLight.position.set(-6, 10, 22);
    scene.add(verandaFillLight);

    // South Yard & Approach Road Fill Light (确保石围墙外壁与坡道通透自然)
    const southYardFillLight = new THREE.DirectionalLight(0xffeedd, 0.70);
    southYardFillLight.position.set(-15, 12, 35);
    scene.add(southYardFillLight);"""

assert old_light_block in code, "old_light_block not found"
code = code.replace(old_light_block, new_light_block)

# 3. Update Material definitions
old_mat_block = """    const mEarth = new THREE.MeshStandardMaterial({
        map: tEarth,
        color: 0xba9e74,
        roughness: 0.96,
        metalness: 0.01,
        side: THREE.DoubleSide
    });

    const mWindow = new THREE.MeshStandardMaterial({
        map: tWindow,
        roughness: 0.86,
        metalness: 0.02
    });

    const mDoorEast = new THREE.MeshStandardMaterial({
        map: tDoorEast,
        roughness: 0.88,
        metalness: 0.02
    });

    const mDoorWest = new THREE.MeshStandardMaterial({
        map: tDoorWest,
        roughness: 0.88,
        metalness: 0.02
    });

    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        color: 0x625e5a,
        roughness: 0.94,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mRedTile = new THREE.MeshStandardMaterial({
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
    });

    const mPillar = new THREE.MeshStandardMaterial({
        map: tPillar,
        roughness: 0.88,
        metalness: 0.05
    });

    const mStone = new THREE.MeshStandardMaterial({
        map: tStone,
        color: 0x9e9890,
        roughness: 0.92,
        metalness: 0.04,
        side: THREE.DoubleSide
    });"""

new_mat_block = """    const mEarth = new THREE.MeshStandardMaterial({
        map: tEarth,
        roughness: 0.92,
        metalness: 0.01,
        side: THREE.DoubleSide
    });

    const mWindow = new THREE.MeshStandardMaterial({
        map: tWindow,
        roughness: 0.86,
        metalness: 0.02
    });

    const mDoorEast = new THREE.MeshStandardMaterial({
        map: tDoorEast,
        roughness: 0.88,
        metalness: 0.02
    });

    const mDoorWest = new THREE.MeshStandardMaterial({
        map: tDoorWest,
        roughness: 0.88,
        metalness: 0.02
    });

    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        color: 0x625e5a,
        roughness: 0.94,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mRedTile = new THREE.MeshStandardMaterial({
        map: tRedTile,
        roughness: 0.82,
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
        roughness: 0.92,
        metalness: 0.01,
        side: THREE.DoubleSide
    });

    const mAnnexDoor = new THREE.MeshStandardMaterial({
        map: tAnnexDoor,
        roughness: 0.85
    });

    const mFirewood = new THREE.MeshStandardMaterial({
        map: tFirewood,
        roughness: 0.92
    });

    const mPillar = new THREE.MeshStandardMaterial({
        map: tPillar,
        roughness: 0.88,
        metalness: 0.05
    });

    const mStone = new THREE.MeshStandardMaterial({
        map: tStone,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });"""

assert old_mat_block in code, "old_mat_block not found"
code = code.replace(old_mat_block, new_mat_block)

# 4. Update Stone Wall Points
old_wall_points = """    // 1. South Courtyard Perimeter Wall (南侧通长石围墙, 完整环抱大院坝, 00:20-00:55视频实景)
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
    addGatepost(-7.5, 14.0); // 东门垛"""

new_wall_points = """    // 1. South Courtyard Perimeter Wall (南侧通长石围墙, 完整环抱大院坝, 00:20-00:55视频实景)
    const southWallPoints = [
        new THREE.Vector3(-7.8, 0.0, 14.2),
        new THREE.Vector3(-1.5, 0.0, 14.5),
        new THREE.Vector3(4.5, 0.0, 14.8),
        new THREE.Vector3(10.5, 0.0, 15.0),
        new THREE.Vector3(16.2, 0.0, 14.8)
    ];
    buildWallRun(southWallPoints, 1.15, 0.65, 1.55);

    // 2. East Courtyard Boundary Wall (东侧石围墙/阶梯护坎, 连接东厢房)
    const eastWallPoints = [
        new THREE.Vector3(16.2, 0.0, 14.8),
        new THREE.Vector3(16.2, 0.0, 8.0),
        new THREE.Vector3(15.8, 0.0, 2.0),
        new THREE.Vector3(15.2, 0.0, -3.5)
    ];
    buildWallRun(eastWallPoints, 1.15, 0.65, 1.40);

    // 3. West Courtyard Boundary Wall (西侧院墙, 围护大院西边界)
    const westWallPoints = [
        new THREE.Vector3(-10.0, 0.0, 14.2),
        new THREE.Vector3(-14.5, 0.0, 14.0),
        new THREE.Vector3(-14.8, 0.0, 7.5),
        new THREE.Vector3(-14.5, 0.0, 2.5)
    ];
    buildWallRun(westWallPoints, 1.15, 0.65, 1.35);

    // 4. Southwest Approach Retaining Wall (西南斜坡步道护坡墙)
    const approachWallPoints = [
        new THREE.Vector3(-10.0, 0.0, 14.2),
        new THREE.Vector3(-15.5, -0.6, 17.5),
        new THREE.Vector3(-21.5, -1.2, 20.5),
        new THREE.Vector3(-27.0, -1.8, 23.5)
    ];
    buildWallRun(approachWallPoints, 1.35, 0.70, 1.60);

    // Courtyard Entrance Boulder Gateposts (-10.0 & -7.8 at z = 14.2)
    function addGatepost(gx, gz) {
        const post = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.85, 1.0), mStone);
        post.position.set(gx, 0.925, gz);
        post.castShadow = true;
        post.receiveShadow = true;
        stoneWallGroup.add(post);

        const cap = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.20, 1.20), mStone);
        cap.position.set(gx, 1.85 + 0.10, gz);
        cap.castShadow = true;
        stoneWallGroup.add(cap);

        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.68, 1), mStone);
        boulder.scale.set(1.25, 0.8, 1.15);
        boulder.position.set(gx + (gx < -8.5 ? -0.45 : 0.45), 0.35, gz + 0.4);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }
    addGatepost(-10.0, 14.2); // 西门垛 (00:30 实景大毛石门垛)
    addGatepost(-7.8, 14.2);  // 东门垛"""

assert old_wall_points in code, "old_wall_points not found"
code = code.replace(old_wall_points, new_wall_points)

# 5. Update Firewood Mesh definition
old_firewood = """    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        new THREE.MeshStandardMaterial({ map: tFirewood, roughness: 0.95, color: 0x7a634e })
    );"""

new_firewood = """    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        mFirewood
    );"""

assert old_firewood in code, "old_firewood not found"
code = code.replace(old_firewood, new_firewood)

# 6. Update Annex Architecture to true Hipped Roof & seamless attachment
old_annex_section = """    // --- 9. WEST LOW RED-TILED ANNEX SHED (西侧低矮红瓦附房/柴火房, 紧邻正房 01:44 实景) ---
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

    // Red Clay Tile Roof with Realistic Thickness & Terracotta Hue (01:44 实景: 烧结红陶机瓦坡顶)
    const eaveOverhangZ = 0.65;
    const roofLen = Math.sqrt((AH_rear - AH_front)**2 + (AL + eaveOverhangZ)**2) + 0.45;
    const roofAngle = Math.atan2(AH_rear - AH_front, AL + eaveOverhangZ);

    const annexRoof = new THREE.Mesh(new THREE.BoxGeometry(AW + 0.65, 0.10, roofLen), mRedTile);
    annexRoof.rotation.x = roofAngle;
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
    annexGroup.add(annexEaveBeam);"""

new_annex_section = """    // --- 9. WEST LOW RED-TILED ANNEX SHED (西侧低矮红瓦附房/柴火房, 紧邻正房 01:44 实景) ---
    const annexGroup = new THREE.Group();
    scene.add(annexGroup);

    // 附房紧挨正房西山墙 (x = -9.6), 无任何缝隙隔道
    const AW = 4.2;
    const annexX_east = -9.6;
    const annexX_west = annexX_east - AW; // -13.8
    const annexZ_north = -4.5;
    const annexZ_southWall = -0.35; // 凹进的前墙
    const annexZ_eaveSouth = 0.85;  // 前檐挑檐
    const annexZ_eaveNorth = -4.75;
    const annexX_eaveWest = -14.05;

    const annexEaveH = 2.15;
    const annexRidgeH = 3.20;
    const annexRidgeZ = (annexZ_eaveSouth + annexZ_eaveNorth) / 2; // -1.95m
    const annexHipX = -12.4; // 西侧四坡斜脊起点

    // 1. South Wall (凹进的土坯前墙, z = annexZ_southWall)
    const annexSouthWallMesh = new THREE.Mesh(
        new THREE.BoxGeometry(AW, annexEaveH, 0.35),
        mAnnexEarth
    );
    annexSouthWallMesh.position.set((annexX_east + annexX_west)/2, 0.18 + annexEaveH/2, annexZ_southWall);
    annexSouthWallMesh.castShadow = true;
    annexSouthWallMesh.receiveShadow = true;
    annexGroup.add(annexSouthWallMesh);

    // 2. North Rear Wall
    const annexNorthWallMesh = new THREE.Mesh(
        new THREE.BoxGeometry(AW, annexEaveH, 0.35),
        mAnnexEarth
    );
    annexNorthWallMesh.position.set((annexX_east + annexX_west)/2, 0.18 + annexEaveH/2, annexZ_north);
    annexNorthWallMesh.castShadow = true;
    annexNorthWallMesh.receiveShadow = true;
    annexGroup.add(annexNorthWallMesh);

    // 3. West Wall (x = annexX_west)
    const annexWestWallMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.35, annexEaveH, Math.abs(annexZ_north - annexZ_southWall)),
        mAnnexEarth
    );
    annexWestWallMesh.position.set(annexX_west, 0.18 + annexEaveH/2, (annexZ_north + annexZ_southWall)/2);
    annexWestWallMesh.castShadow = true;
    annexWestWallMesh.receiveShadow = true;
    annexGroup.add(annexWestWallMesh);

    // 4. East Wall flush against main house west gable
    const annexEastWallMesh = new THREE.Mesh(
        new THREE.BoxGeometry(0.35, annexEaveH, Math.abs(annexZ_north - annexZ_southWall)),
        mAnnexEarth
    );
    annexEastWallMesh.position.set(annexX_east, 0.18 + annexEaveH/2, (annexZ_north + annexZ_southWall)/2);
    annexEastWallMesh.castShadow = true;
    annexGroup.add(annexEastWallMesh);

    // 5. Recessed Timber Door with Paper Poster (01:44 实景: 紧靠主房砖叠柱与西山墙)
    const annexDoor = new THREE.Mesh(new THREE.BoxGeometry(0.88, 1.80, 0.06), mAnnexDoor);
    annexDoor.position.set(-10.25, 0.18 + 0.90, annexZ_southWall + 0.18);
    annexDoor.castShadow = true;
    annexGroup.add(annexDoor);

    // 6. Southwest Eave Corner Support Column (01:44 实景: 附房左前角立柱支撑挑檐)
    const annexPost = new THREE.Mesh(new THREE.BoxGeometry(0.18, annexEaveH, 0.18), mStone);
    annexPost.position.set(annexX_west + 0.15, 0.18 + annexEaveH/2, annexZ_eaveSouth - 0.15);
    annexPost.castShadow = true;
    annexGroup.add(annexPost);

    // Front eave fascia beam connecting corner post to main house column
    const annexEaveBeam = new THREE.Mesh(new THREE.BoxGeometry(AW + 0.35, 0.16, 0.16), mWood);
    annexEaveBeam.position.set((annexX_east + annexX_west)/2, 0.18 + annexEaveH, annexZ_eaveSouth - 0.15);
    annexEaveBeam.castShadow = true;
    annexGroup.add(annexEaveBeam);

    // 7. HIPPED RED TILE ROOF (真实烧结红陶平瓦四坡顶, 与视频实景完全一致)
    // South Slope (Trapezoid from ridge to south eave)
    const southSlopeGeo = new THREE.BufferGeometry();
    const s_vertices = new Float32Array([
        // Triangle 1: (RE, SW, SE)
        annexX_east, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_eaveWest, 0.18 + annexEaveH, annexZ_eaveSouth,
        annexX_east, 0.18 + annexEaveH, annexZ_eaveSouth,
        // Triangle 2: (RE, RW, SW)
        annexX_east, 0.18 + annexRidgeH, annexRidgeZ,
        annexHipX, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_eaveWest, 0.18 + annexEaveH, annexZ_eaveSouth,
    ]);
    const s_uvs = new Float32Array([
        0, 3,
        4, 0,
        0, 0,
        0, 3,
        2.5, 3,
        4, 0
    ]);
    southSlopeGeo.setAttribute('position', new THREE.BufferAttribute(s_vertices, 3));
    southSlopeGeo.setAttribute('uv', new THREE.BufferAttribute(s_uvs, 2));
    southSlopeGeo.computeVertexNormals();
    const southSlopeMesh = new THREE.Mesh(southSlopeGeo, mRedTile);
    southSlopeMesh.castShadow = true;
    southSlopeMesh.receiveShadow = true;
    annexGroup.add(southSlopeMesh);

    // West Hip Slope (Triangle from hip apex to west eave)
    const westSlopeGeo = new THREE.BufferGeometry();
    const w_vertices = new Float32Array([
        annexHipX, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_eaveWest, 0.18 + annexEaveH, annexZ_eaveNorth,
        annexX_eaveWest, 0.18 + annexEaveH, annexZ_eaveSouth,
    ]);
    const w_uvs = new Float32Array([
        2, 3,
        4, 0,
        0, 0
    ]);
    westSlopeGeo.setAttribute('position', new THREE.BufferAttribute(w_vertices, 3));
    westSlopeGeo.setAttribute('uv', new THREE.BufferAttribute(w_uvs, 2));
    westSlopeGeo.computeVertexNormals();
    const westSlopeMesh = new THREE.Mesh(westSlopeGeo, mRedTile);
    westSlopeMesh.castShadow = true;
    westSlopeMesh.receiveShadow = true;
    annexGroup.add(westSlopeMesh);

    // North Slope (Trapezoid from ridge to north eave)
    const northSlopeGeo = new THREE.BufferGeometry();
    const n_vertices = new Float32Array([
        // Triangle 1: (RW, NE, NW)
        annexHipX, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_east, 0.18 + annexEaveH, annexZ_eaveNorth,
        annexX_eaveWest, 0.18 + annexEaveH, annexZ_eaveNorth,
        // Triangle 2: (RW, RE, NE)
        annexHipX, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_east, 0.18 + annexRidgeH, annexRidgeZ,
        annexX_east, 0.18 + annexEaveH, annexZ_eaveNorth,
    ]);
    const n_uvs = new Float32Array([
        2.5, 3,
        0, 0,
        4, 0,
        2.5, 3,
        0, 3,
        0, 0
    ]);
    northSlopeGeo.setAttribute('position', new THREE.BufferAttribute(n_vertices, 3));
    northSlopeGeo.setAttribute('uv', new THREE.BufferAttribute(n_uvs, 2));
    northSlopeGeo.computeVertexNormals();
    const northSlopeMesh = new THREE.Mesh(northSlopeGeo, mRedTile);
    northSlopeMesh.castShadow = true;
    northSlopeMesh.receiveShadow = true;
    annexGroup.add(northSlopeMesh);

    // White Plaster Ridge Cap
    const ridgeCapMesh = new THREE.Mesh(
        new THREE.BoxGeometry(Math.abs(annexX_east - annexHipX) + 0.2, 0.12, 0.24),
        new THREE.MeshStandardMaterial({ color: 0xdfdcd5, roughness: 0.8 })
    );
    ridgeCapMesh.position.set((annexX_east + annexHipX)/2, 0.18 + annexRidgeH + 0.06, annexRidgeZ);
    ridgeCapMesh.castShadow = true;
    annexGroup.add(ridgeCapMesh);"""

assert old_annex_section in code, "old_annex_section not found"
code = code.replace(old_annex_section, new_annex_section)

# 7. Update Viewpoint Camera Coordinates
old_views_code = """        facade: {
            pos: new THREE.Vector3(-1.0, 3.60, 21.0),
            target: new THREE.Vector3(0.5, 1.80, -0.5),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房与石围墙大院 (00:56)",
            body: "严格对应00:56实景机位：左侧为院落西南毛石门垛与石围墙，中心为开阔平整的泥土大院落（晒场/院场），后方为完整的双联六开间夯土正房立面，左侧紧挨低矮红瓦附房，右侧紧密连接东厢房，北坡翠柏林木苍翠。"
        },"""

new_views_code = """        facade: {
            pos: new THREE.Vector3(-1.0, 4.20, 23.5),
            target: new THREE.Vector3(0.0, 1.80, 0.0),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房与石围墙大院 (00:56)",
            body: "严格对应00:56实景机位：近景为院坝边缘干砌毛石围墙与西南门垛，中心为开阔平整的泥土大院落（晒场/院坝），后方为完整的双联六开间夯土正房立面，左侧紧挨低矮红瓦四坡附房，右侧连接东厢房，北坡翠柏林木苍翠。"
        },"""

assert old_views_code in code, "old_views_code not found"
code = code.replace(old_views_code, new_views_code)

old_annex_cam = """        west_annex: {
            pos: new THREE.Vector3(-6.2, 1.48, 8.6),
            target: new THREE.Vector3(-10.6, 1.75, -0.5),
            refImg: "ref_images/ref_104s_west_annex.jpg",
            refTag: "M2U00577.MPG · 01:44",
            title: "西侧红瓦附房与紧邻正房实景 (01:44)",
            body: "严格对应用户指出的实景对比（01:44实景）：西侧低矮红瓦附房紧挨正房西山墙与立柱，红瓦坡屋顶、左前角木柱支护挑檐；正房西角采用烧结砖叠砌柱体，白石灰门套与木门清晰可见，窗下整齐堆码柴草堆，前方为开阔平整的泥土大院落与石围墙环抱。"
        },"""

new_annex_cam = """        west_annex: {
            pos: new THREE.Vector3(-5.2, 1.48, 7.0),
            target: new THREE.Vector3(-9.2, 1.65, 0.0),
            refImg: "ref_images/ref_104s_west_annex.jpg",
            refTag: "M2U00577.MPG · 01:44",
            title: "西侧红瓦附房与紧邻正房实景 (01:44)",
            body: "严格对应用户截图标注的真实建筑关系：西侧低矮红机瓦四坡顶附房紧挨正房西山墙（共享墙体无空隙），挑檐由左前角立柱支撑；正房西角为烧结砖叠砌柱体，白石灰抹灰窗套与暗窗、窗下切面柴木堆整齐堆码，前侧为开阔院落与石围墙。"
        },"""

assert old_annex_cam in code, "old_annex_cam not found"
code = code.replace(old_annex_cam, new_annex_cam)

old_approach_cam = """        approach: {
            pos: new THREE.Vector3(-15.8, 1.35, 17.5),
            target: new THREE.Vector3(-6.8, 1.8, 7.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南坡道步道与毛石围墙 (00:20)",
            body: "从西南斜坡步道步入主院的沿途视角，左侧为干砌片石垒砌的护坡矮墙与巨石门墩，前方展现开阔大院坝与正房柱廊、红瓦附房。"
        }"""

new_approach_cam = """        approach: {
            pos: new THREE.Vector3(-13.0, 0.70, 21.0),
            target: new THREE.Vector3(-4.5, 1.80, 4.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南坡道步道与毛石围墙 (00:20)",
            body: "严格对应视频00:20-00:30实景视角：从西南斜坡步道步入大院，左侧为巨石门垛与干砌石护坡墙，右侧为横贯大院南缘的干砌毛石围墙，前方展现开阔大院坝与正房柱廊、紧挨的红瓦附房。"
        }"""

assert old_approach_cam in code, "old_approach_cam not found"
code = code.replace(old_approach_cam, new_approach_cam)

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied all compound updates to build_complete_compound.py successfully")
