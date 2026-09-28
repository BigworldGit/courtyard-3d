import os

file_path = '/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update northSkyLight and mRoof
old_lights = '''    // Cool Northern Sky Ambient Light (Illuminates rear wall in alleyway)
    const northSkyLight = new THREE.DirectionalLight(0xdbe7f5, 0.85);
    northSkyLight.position.set(0, 25, -35);
    scene.add(northSkyLight);'''

new_lights = '''    // Cool Northern Sky Ambient Light (Illuminates rear wall & roof in alleyway and overview)
    const northSkyLight = new THREE.DirectionalLight(0xdfe8f2, 1.45);
    northSkyLight.position.set(0, 32, -35);
    scene.add(northSkyLight);

    const northFillLight = new THREE.DirectionalLight(0xdcd5c8, 0.85);
    northFillLight.position.set(-8, 16, -22);
    scene.add(northFillLight);'''

assert old_lights in content, 'old_lights not found'
content = content.replace(old_lights, new_lights)

old_mroof = '''    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        color: 0x52565c,
        roughness: 0.82,
        metalness: 0.10,
        side: THREE.DoubleSide
    });'''

new_mroof = '''    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        roughness: 0.86,
        metalness: 0.04,
        side: THREE.DoubleSide
    });'''

assert old_mroof in content, 'old_mroof not found'
content = content.replace(old_mroof, new_mroof)

# 2. Fix East Wing roof rotation order to ZXY
old_wing_roof = '''    // West Roof Slope (Pitching down toward yard / -X)
    const wRoofW = new THREE.Mesh(new THREE.PlaneGeometry(wRoofWidth, WL + 0.4), mRoof);
    wRoofW.rotation.set(-Math.PI / 2, 0, wRoofPitch);
    wRoofW.position.set(-WW/4, 0.18 + (WEaveH + WRidgeH)/2 + 0.05, 0);
    wRoofW.castShadow = true;
    wingGroup.add(wRoofW);

    // East Roof Slope (Pitching down toward east / +X)
    const wRoofE = new THREE.Mesh(new THREE.PlaneGeometry(wRoofWidth, WL + 0.4), mRoof);
    wRoofE.rotation.set(-Math.PI / 2, 0, -wRoofPitch);
    wRoofE.position.set(WW/4, 0.18 + (WEaveH + WRidgeH)/2 + 0.05, 0);
    wRoofE.castShadow = true;
    wingGroup.add(wRoofE);'''

new_wing_roof = '''    // West Roof Slope (Pitching down toward yard / -X)
    const wRoofW = new THREE.Mesh(new THREE.PlaneGeometry(wRoofWidth, WL + 0.4), mRoof);
    wRoofW.rotation.order = 'ZXY';
    wRoofW.rotation.set(-Math.PI / 2, 0, wRoofPitch);
    wRoofW.position.set(-WW/4, 0.18 + (WEaveH + WRidgeH)/2, 0);
    wRoofW.castShadow = true;
    wingGroup.add(wRoofW);

    // East Roof Slope (Pitching down toward east / +X)
    const wRoofE = new THREE.Mesh(new THREE.PlaneGeometry(wRoofWidth, WL + 0.4), mRoof);
    wRoofE.rotation.order = 'ZXY';
    wRoofE.rotation.set(-Math.PI / 2, 0, -wRoofPitch);
    wRoofE.position.set(WW/4, 0.18 + (WEaveH + WRidgeH)/2, 0);
    wRoofE.castShadow = true;
    wingGroup.add(wRoofE);'''

assert old_wing_roof in content, 'old_wing_roof not found'
content = content.replace(old_wing_roof, new_wing_roof)

# 3. Fix cypresses along alley and poplars
old_cypresses_block = '''    // Prominent foreground haystacks on northern hillside directly as framed in frame 320s / 05:20
    addHaystack(3.2, -10.5, 1.35, 1.55);
    addHaystack(0.2, -11.2, 1.25, 1.45);
    addHaystack(14.5, -7.5, 1.30, 1.50);

    // --- 14. REAR ALLEY DENSE CYPRESS WINDBREAK HEDGE (后墙背风防风柏树绿篱, 08:15) ---
    const cypressGroup = new THREE.Group();
    scene.add(cypressGroup);

    const matCypress = new THREE.MeshStandardMaterial({
        map: tTreeCypress,
        alphaTest: 0.35,
        roughness: 0.85,
        side: THREE.DoubleSide
    });

    function addDenseCypress(x, z, w, h) {
        const baseY = getTerrainY(x, z);
        const pGeo = new THREE.PlaneGeometry(w, h);
        const m1 = new THREE.Mesh(pGeo, matCypress);
        m1.position.set(x, baseY + h/2, z);
        m1.castShadow = true;
        cypressGroup.add(m1);

        const m2 = new THREE.Mesh(pGeo, matCypress);
        m2.position.set(x, baseY + h/2, z);
        m2.rotation.y = Math.PI / 2;
        m2.castShadow = true;
        cypressGroup.add(m2);
    }

    // Continuous Dense Cypress Windbreak Row immediately along Rear Alley (z = -6.45m, rear wall is at z = -5.05m)
    for (let c = -10.5; c <= 10.5; c += 0.9) {
        addDenseCypress(c, -6.45, 2.3, 4.8 + Math.sin(c)*0.35);
    }

    // --- 15. TALL POPLARS & PEACH ORCHARD TREES (高大杨树与桃花果林) ---
    const treeGroup = new THREE.Group();
    scene.add(treeGroup);

    const matPoplar = new THREE.MeshStandardMaterial({
        map: tTreePoplar,
        alphaTest: 0.28,
        roughness: 0.9,
        side: THREE.DoubleSide
    });

    const matPeach = new THREE.MeshStandardMaterial({
        map: tTreePeach,
        alphaTest: 0.28,
        roughness: 0.8,
        side: THREE.DoubleSide
    });

    function addPoplarTree(x, z, width, height) {
        const baseY = getTerrainY(x, z);
        const planeGeo = new THREE.PlaneGeometry(width, height);
        // Star pattern with 3 planes for 360-degree volumetric look from any angle
        for (let a = 0; a < 3; a++) {
            const m = new THREE.Mesh(planeGeo, matPoplar);
            m.position.set(x, baseY + height/2, z);
            m.rotation.y = (a * Math.PI) / 3;
            m.castShadow = true;
            treeGroup.add(m);
        }
    }

    function addPeachTree(x, z, width, height) {
        const baseY = getTerrainY(x, z);
        const planeGeo = new THREE.PlaneGeometry(width, height);
        for (let a = 0; a < 3; a++) {
            const p = new THREE.Mesh(planeGeo, matPeach);
            p.position.set(x, baseY + height/2, z);
            p.rotation.y = (a * Math.PI) / 3;
            p.castShadow = true;
            treeGroup.add(p);
        }
    }

    // Tall Towering Poplars on Hillside (Flanking the rear overview corridor)
    addPoplarTree(-13.5, -12.5, 9.5, 18);
    addPoplarTree(-6.5, -14.5, 9.0, 18);
    addPoplarTree(8.5, -14.5, 9.0, 18);
    addPoplarTree(15.0, -12.5, 8.5, 16);'''

new_cypresses_block = '''    // Prominent foreground haystacks on northern hillside directly as framed in frame 320s / 05:20
    addHaystack(3.8, -11.5, 1.35, 1.55);
    addHaystack(-2.2, -12.2, 1.25, 1.45);
    addHaystack(14.5, -7.5, 1.30, 1.50);

    // --- 14. REAR ALLEY DENSE CYPRESS WINDBREAK HEDGE (后墙背风防风柏树绿篱, 08:15) ---
    const cypressGroup = new THREE.Group();
    scene.add(cypressGroup);

    const matCypress = new THREE.MeshStandardMaterial({
        map: tTreeCypress,
        alphaTest: 0.35,
        roughness: 0.85,
        side: THREE.DoubleSide
    });

    function addDenseCypress(x, z, w, h) {
        const baseY = getTerrainY(x, z);
        const pGeo = new THREE.PlaneGeometry(w, h);
        const m1 = new THREE.Mesh(pGeo, matCypress);
        m1.position.set(x, baseY + h/2, z);
        m1.castShadow = true;
        cypressGroup.add(m1);

        const m2 = new THREE.Mesh(new THREE.PlaneGeometry(w * 0.55, h), matCypress);
        m2.position.set(x, baseY + h/2, z);
        m2.rotation.y = Math.PI / 2;
        m2.castShadow = true;
        cypressGroup.add(m2);
    }

    // Continuous Dense Cypress Windbreak Row set on north slope bank (z = -6.85m, walkway is at z = -5.65m)
    for (let c = -10.5; c <= 10.5; c += 0.9) {
        addDenseCypress(c, -6.85, 2.2, 4.8 + Math.sin(c)*0.35);
    }

    // --- 15. TALL POPLARS & PEACH ORCHARD TREES (高大杨树与桃花果林) ---
    const treeGroup = new THREE.Group();
    scene.add(treeGroup);

    const matPoplar = new THREE.MeshStandardMaterial({
        map: tTreePoplar,
        alphaTest: 0.28,
        roughness: 0.9,
        side: THREE.DoubleSide
    });

    const matPeach = new THREE.MeshStandardMaterial({
        map: tTreePeach,
        alphaTest: 0.28,
        roughness: 0.8,
        side: THREE.DoubleSide
    });

    function addPoplarTree(x, z, width, height) {
        const baseY = getTerrainY(x, z);
        const planeGeo = new THREE.PlaneGeometry(width, height);
        // Star pattern with 3 planes for 360-degree volumetric look from any angle
        for (let a = 0; a < 3; a++) {
            const m = new THREE.Mesh(planeGeo, matPoplar);
            m.position.set(x, baseY + height/2, z);
            m.rotation.y = (a * Math.PI) / 3;
            m.castShadow = true;
            treeGroup.add(m);
        }
    }

    function addPeachTree(x, z, width, height) {
        const baseY = getTerrainY(x, z);
        const planeGeo = new THREE.PlaneGeometry(width, height);
        for (let a = 0; a < 3; a++) {
            const p = new THREE.Mesh(planeGeo, matPeach);
            p.position.set(x, baseY + height/2, z);
            p.rotation.y = (a * Math.PI) / 3;
            p.castShadow = true;
            treeGroup.add(p);
        }
    }

    // Tall Towering Poplars on Hillside (Kept to far flanks to avoid obstructing rear overview)
    addPoplarTree(-14.5, -15.5, 9.5, 18);
    addPoplarTree(14.5, -15.5, 8.5, 16);'''

assert old_cypresses_block in content, 'old_cypresses_block not found'
content = content.replace(old_cypresses_block, new_cypresses_block)

# 4. Viewpoint rear_overview pos
old_rear_overview = '''        rear_overview: {
            pos: new THREE.Vector3(5.5, 7.5, -17.5),
            target: new THREE.Vector3(-3.0, 2.6, -1.0),
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "后山俯瞰双坡顶与全景聚落 (05:20)",
            body: "从北侧后山坡地俯瞰双坡青瓦大屋顶与白灰正脊，近景为麦秸草垛，左侧为门楼与东厢房，右侧远景为西邻红砖房高烟囱与苍翠山峦。"
        },'''

new_rear_overview = '''        rear_overview: {
            pos: new THREE.Vector3(3.2, 7.2, -16.5),
            target: new THREE.Vector3(-1.5, 2.7, -1.0),
            refImg: "ref_images/ref_320s_rear_overview.jpg",
            refTag: "M2U00577.MPG · 05:20",
            title: "后山俯瞰双坡顶与全景聚落 (05:20)",
            body: "从北侧后山坡地俯瞰双坡青瓦大屋顶与白灰正脊，近景为麦秸草垛，左侧为门楼与东厢房，右侧远景为西邻红砖房高烟囱与苍翠山峦。"
        },'''

assert old_rear_overview in content, 'old_rear_overview not found'
content = content.replace(old_rear_overview, new_rear_overview)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated build_complete_compound.py with ZXY roof, clear alley, and balanced lighting!')
