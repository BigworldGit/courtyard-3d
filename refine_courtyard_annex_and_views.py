import re

with open('build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Texture Pipeline & Materials for authentic textures
old_tex_block = '''    const tStone = loadTexture('textures/tex_stonewall_seamless.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 1.5);
    const tEarth = loadTexture('textures/tex_rammed_earth_clean.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tGround = loadTexture('textures/ground_seamless_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 18, 18);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tStackedBrick = loadTexture('textures/tex_video_stacked_brick_pillar.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 3);
    const tRedTile = loadTexture('textures/tex_redtile_seamless.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 3);
    const tAnnexWall = loadTexture('textures/tex_video_annex_earth_wall.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);'''

new_tex_block = '''    const tStone = loadTexture('textures/tex_stonewall_horizontal.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 1.8);
    const tEarth = loadTexture('textures/tex_rammed_earth_clean.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 2);
    const tGround = loadTexture('textures/ground_seamless_real.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 16, 16);
    const tBrick = loadTexture('textures/brick_authentic_red.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 4);
    const tStackedBrick = loadTexture('textures/tex_video_stacked_brick_pillar.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 3);
    const tRedTile = loadTexture('textures/tex_red_roof_authentic.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 5, 3);
    const tAnnexWall = loadTexture('textures/tex_video_annex_earth_wall.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);
    const tFirewood = loadTexture('textures/tex_firewood_logs.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 1.5);
    const tRapeseed = loadTexture('textures/rapeseed_field.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 10, 6);
    const tStraw = loadTexture('textures/tex_straw_haystack.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 2, 2);'''

assert old_tex_block in code, "old_tex_block not found!"
code = code.replace(old_tex_block, new_tex_block)

# 2. Update Firewood Mesh under Bay 1 Window
old_firewood = '''    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        new THREE.MeshStandardMaterial({ map: tStraw, roughness: 0.94, color: 0x9e7f58 })
    );
    firewoodMesh.position.set(-8.0, 0.18 + 0.36, 0.05);
    firewoodMesh.castShadow = true;
    firewoodMesh.receiveShadow = true;
    houseGroup.add(firewoodMesh);'''

new_firewood = '''    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        new THREE.MeshStandardMaterial({ map: tFirewood, roughness: 0.95, color: 0x7a634e })
    );
    firewoodMesh.position.set(-8.0, 0.18 + 0.36, 0.05);
    firewoodMesh.castShadow = true;
    firewoodMesh.receiveShadow = true;
    houseGroup.add(firewoodMesh);'''

assert old_firewood in code, "old_firewood not found!"
code = code.replace(old_firewood, new_firewood)

# 3. Update Annex Roof to 3D BoxGeometry with realistic overhang and thickness
old_annex_sec = '''    // Single-Pitch Red Clay Tile Roof (单坡红瓦顶, 覆压红机瓦, 前挑出檐)
    const eaveOverhangZ = 0.65;
    const roofLen = Math.sqrt((AH_rear - AH_front)**2 + (AL + eaveOverhangZ)**2) + 0.45;
    const roofAngle = Math.atan2(AH_rear - AH_front, AL + eaveOverhangZ);

    const annexRoof = new THREE.Mesh(new THREE.PlaneGeometry(AW + 0.6, roofLen), mRedTile);
    annexRoof.rotation.x = -Math.PI / 2 + roofAngle;
    annexRoof.position.set(0, 0.18 + (AH_front + AH_rear)/2 + 0.16, eaveOverhangZ/2);
    annexRoof.castShadow = true;
    annexRoof.receiveShadow = true;
    annexGroup.add(annexRoof);'''

new_annex_sec = '''    // Red Clay Tile Roof with Realistic Thickness & Terracotta Hue (01:44 实景: 烧结红陶机瓦坡顶)
    const eaveOverhangZ = 0.65;
    const roofLen = Math.sqrt((AH_rear - AH_front)**2 + (AL + eaveOverhangZ)**2) + 0.45;
    const roofAngle = Math.atan2(AH_rear - AH_front, AL + eaveOverhangZ);

    const annexRoof = new THREE.Mesh(new THREE.BoxGeometry(AW + 0.65, 0.10, roofLen), mRedTile);
    annexRoof.rotation.x = -Math.PI / 2 + roofAngle;
    annexRoof.position.set(0, 0.18 + (AH_front + AH_rear)/2 + 0.16, eaveOverhangZ/2);
    annexRoof.castShadow = true;
    annexRoof.receiveShadow = true;
    annexGroup.add(annexRoof);'''

assert old_annex_sec in code, "old_annex_sec not found!"
code = code.replace(old_annex_sec, new_annex_sec)

# 4. Move blocking poplar tree away from approach viewpoint
old_poplar = '''    addPoplarTree(-19.5, 18.0, 4.5, 10.0);'''
new_poplar = '''    addPoplarTree(-22.5, 21.0, 4.5, 10.0);'''
assert old_poplar in code, "old_poplar not found!"
code = code.replace(old_poplar, new_poplar)

# 5. Perfect the viewpoints for facade, west_annex, and approach
old_facade_vp = '''        facade: {
            pos: new THREE.Vector3(-1.0, 2.8, 20.8),
            target: new THREE.Vector3(0.5, 1.8, 0.0),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房与石围墙大院 (00:56)",
            body: "近景为南侧环抱院落的干砌毛石围墙与石垛，开阔平整的泥土院场（打谷晒场），后方为完整的双联六开间夯土正房立面，7根立柱与中段青瓦垛整齐排列，西侧紧挨低矮红瓦附房，东侧连接东厢房。"
        },'''

new_facade_vp = '''        facade: {
            pos: new THREE.Vector3(-8.2, 1.68, 13.2),
            target: new THREE.Vector3(1.2, 1.90, -0.4),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 00:56",
            title: "双联六开间正房与石围墙大院 (00:56)",
            body: "严格对应00:56实景机位：左侧为院落西南毛石门垛与石围墙，中心为开阔平整的泥土大院落（晒场/院场），后方为完整的双联六开间夯土正房立面，左侧紧挨低矮红瓦附房，右侧紧密连接东厢房，北坡翠柏林木苍翠。"
        },'''

assert old_facade_vp in code, "old_facade_vp not found!"
code = code.replace(old_facade_vp, new_facade_vp)

old_annex_vp = '''        west_annex: {
            pos: new THREE.Vector3(-6.8, 1.55, 9.2),
            target: new THREE.Vector3(-10.8, 1.85, -0.5),
            refImg: "ref_images/ref_104s_west_annex.jpg",
            refTag: "M2U00577.MPG · 01:44",
            title: "西侧红瓦附房与紧邻正房实景 (01:44)",
            body: "严格对应用户指出的实景对比：西侧低矮红瓦附房紧挨正房西山墙与立柱，红瓦单坡屋顶、左下角立柱支护出檐；正房西角采用烧结砖叠砌柱体，窗下堆码柴草堆，正房开间白灰门套与木门清晰可见，前方为开阔平整的泥土大院落与围墙环抱。"
        },'''

new_annex_vp = '''        west_annex: {
            pos: new THREE.Vector3(-6.2, 1.48, 8.6),
            target: new THREE.Vector3(-10.6, 1.75, -0.5),
            refImg: "ref_images/ref_104s_west_annex.jpg",
            refTag: "M2U00577.MPG · 01:44",
            title: "西侧红瓦附房与紧邻正房实景 (01:44)",
            body: "严格对应用户指出的实景对比（01:44实景）：西侧低矮红瓦附房紧挨正房西山墙与立柱，红瓦坡屋顶、左前角木柱支护挑檐；正房西角采用烧结砖叠砌柱体，白石灰门套与木门清晰可见，窗下整齐堆码柴草堆，前方为开阔平整的泥土大院落与石围墙环抱。"
        },'''

assert old_annex_vp in code, "old_annex_vp not found!"
code = code.replace(old_annex_vp, new_annex_vp)

old_approach_vp = '''        approach: {
            pos: new THREE.Vector3(-18.5, 1.35, 19.5),
            target: new THREE.Vector3(-7.5, 1.8, 8.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南斜坡步道与毛石围墙 (00:20)",
            body: "从西南坡道步入主院的沿途视角，左侧为毛石垒砌的护坡矮墙与巨石门墩，前方露出正房柱廊、红瓦附房与大院落围墙。"
        }'''

new_approach_vp = '''        approach: {
            pos: new THREE.Vector3(-15.8, 1.35, 17.5),
            target: new THREE.Vector3(-6.8, 1.8, 7.0),
            refImg: "ref_images/ref_020s_approach.jpg",
            refTag: "M2U00577.MPG · 00:20",
            title: "西南坡道步道与毛石围墙 (00:20)",
            body: "从西南斜坡步道步入主院的沿途视角，左侧为干砌片石垒砌的护坡矮墙与巨石门墩，前方展现开阔大院坝与正房柱廊、红瓦附房。"
        }'''

assert old_approach_vp in code, "old_approach_vp not found!"
code = code.replace(old_approach_vp, new_approach_vp)

with open('build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully refined build_complete_compound.py!')
