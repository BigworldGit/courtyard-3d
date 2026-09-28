import os

file_path = '/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update top bar subtitle
old_subtitle = '六开间双套正房 · 西侧低矮红瓦附房 · 西邻红砖院落高烟囱 · 东厢房残垣 · 东北门楼与第二栋农舍 · 后山翠柏夹道 · 梯田油菜花海'
new_subtitle = '六开间双套正房 · 西侧低矮红瓦附房 · 西邻红砖院落高烟囱 · 东厢房塌角残垣 · 后檐背风翠柏夹道 · 梯田油菜花海'
assert old_subtitle in content, 'old_subtitle not found'
content = content.replace(old_subtitle, new_subtitle)

# 2. Remove gateGroup and farm2Group completely, add rubble mound under wing breach
old_houses_section = '''    // --- 12. NORTHEAST CONNECTING GATEHOUSE (东北连接门楼, 05:20) ---
    const gateGroup = new THREE.Group();
    gateGroup.position.set(10.2, 0.18, -3.2);
    scene.add(gateGroup);

    const gateWallLeft = new THREE.Mesh(new THREE.BoxGeometry(0.45, 2.5, 0.4), mEarth);
    gateWallLeft.position.set(-0.6, 1.25, 0);
    gateWallLeft.castShadow = true;
    gateGroup.add(gateWallLeft);

    const gateWallRight = new THREE.Mesh(new THREE.BoxGeometry(0.45, 2.5, 0.4), mEarth);
    gateWallRight.position.set(0.6, 1.25, 0);
    gateWallRight.castShadow = true;
    gateGroup.add(gateWallRight);

    const gateLintel = new THREE.Mesh(new THREE.BoxGeometry(1.65, 0.35, 0.42), mWood);
    gateLintel.position.set(0, 2.3, 0);
    gateLintel.castShadow = true;
    gateGroup.add(gateLintel);

    const gateDoorLeaf = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.95, 0.06), mDoorWest);
    gateDoorLeaf.position.set(0, 1.0, 0);
    gateDoorLeaf.castShadow = true;
    gateGroup.add(gateDoorLeaf);

    const gateRoofHipped = new THREE.Mesh(new THREE.ConeGeometry(1.4, 0.6, 4), mRoof);
    gateRoofHipped.rotation.y = Math.PI / 4;
    gateRoofHipped.position.set(0, 2.75, 0);
    gateRoofHipped.castShadow = true;
    gateGroup.add(gateRoofHipped);

    // --- 13. SECOND NORTHEAST FARMHOUSE ON UPPER TERRACE (东北第二栋山腰农舍, 05:20) ---
    const farm2Group = new THREE.Group();
    farm2Group.position.set(18.2, 2.2, -9.2);
    scene.add(farm2Group);

    const F2W = 8.4;
    const F2L = 4.4;
    const F2H = 2.8;

    const farm2Body = new THREE.Mesh(new THREE.BoxGeometry(F2W, F2H, F2L), mEarth);
    farm2Body.position.y = F2H/2;
    farm2Body.castShadow = true;
    farm2Body.receiveShadow = true;
    farm2Group.add(farm2Body);

    // Grey Tiled Dual Pitch Roof with White Ridge
    const f2RoofFront = new THREE.Mesh(new THREE.PlaneGeometry(F2W + 0.4, 2.8), mRoof);
    f2RoofFront.rotation.x = -Math.PI / 2 + 0.48;
    f2RoofFront.position.set(0, F2H + 0.9, F2L/4);
    f2RoofFront.castShadow = true;
    farm2Group.add(f2RoofFront);

    const f2RoofRear = new THREE.Mesh(new THREE.PlaneGeometry(F2W + 0.4, 2.8), mRoof);
    f2RoofRear.rotation.x = -Math.PI / 2 - 0.48;
    f2RoofRear.position.set(0, F2H + 0.9, -F2L/4);
    f2RoofRear.castShadow = true;
    farm2Group.add(f2RoofRear);

    const f2Ridge = new THREE.Mesh(new THREE.BoxGeometry(F2W + 0.5, 0.22, 0.28), new THREE.MeshStandardMaterial({ color: 0xdfdad2, roughness: 0.8 }));
    f2Ridge.position.set(0, F2H + 1.85, 0);
    f2Ridge.castShadow = true;
    farm2Group.add(f2Ridge);'''

new_houses_section = '''    // Collapsed adobe debris mound under the breach (视频01:05实景残土堆)
    const moundGeo = new THREE.ConeGeometry(0.85, 0.38, 12);
    const moundMesh = new THREE.Mesh(moundGeo, mEarth);
    moundMesh.position.set(-WW/2 + 0.35, 0.18 + 0.19, 1.8);
    moundMesh.castShadow = true;
    moundMesh.receiveShadow = true;
    wingGroup.add(moundMesh);

    // Notice: As verified directly from video frame 01:05 and user correction,
    // the corner/gap between the main house and east wing is an open corridor
    // with NO connecting gatehouse and NO second farmhouse behind it.
    // Behind the gap are only the natural hillside slope, green evergreen cypresses, poplars, and open sky.'''

assert old_houses_section in content, 'old_houses_section not found'
content = content.replace(old_houses_section, new_houses_section)

# 3. Update east_wing viewpoint to match user uploaded frame 01:05 exactly
old_east_wing_view = '''        east_wing: {
            pos: new THREE.Vector3(6.5, 1.75, 5.8),
            target: new THREE.Vector3(11.8, 1.85, 1.2),
            refImg: "ref_images/ref_070s_east_wing.jpg",
            refTag: "M2U00577.MPG · 01:10",
            title: "东厢房侧立面与塌角残垣 (01:10)",
            body: "展示东厢房土坯墙体、直棂木窗、入口木门以及西南角大面积残损塌落的断口，显露内部草筋与土坯分层细节。"
        },'''

new_east_wing_view = '''        east_wing: {
            pos: new THREE.Vector3(4.2, 1.55, 6.8),
            target: new THREE.Vector3(9.8, 1.65, 0.8),
            refImg: "ref_images/ref_065s_wing_corner.jpg",
            refTag: "M2U00577.MPG · 01:05",
            title: "主房与东厢房转折夹角全景 (01:05)",
            body: "严格对应视频1分05秒实景：主房东侧与东厢房转折夹角，夹角后方开阔通透，直接呈现北山林木与蓝天，无任何多余房舍阻挡；东厢房呈现土坯墙体、木门白灰套、直棂窗与塌角残垣。"
        },'''

assert old_east_wing_view in content, 'old_east_wing_view not found'
content = content.replace(old_east_wing_view, new_east_wing_view)

# 4. Also update bottom navigation button label
old_nav_btn = '5. 东厢房塌角残垣'
new_nav_btn = '5. 房舍夹角与东厢房'
content = content.replace(old_nav_btn, new_nav_btn)

old_nav_sub = '01:10 土坯分层与破口'
new_nav_sub = '01:05 夹角通透无它房'
content = content.replace(old_nav_sub, new_nav_sub)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated build_complete_compound.py: Removed extra houses behind gap, added debris mound, and aligned camera to frame 01:05!')
