with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update tStone and tRedTile repeat
code = code.replace(
    "const tStone = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 3, 1.2);",
    "const tStone = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 2);"
)

code = code.replace(
    "const tRedTile = loadTexture('textures/tex_authentic_red_tile.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 3);",
    "const tRedTile = loadTexture('textures/tex_authentic_red_tile.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 5, 4);"
)

# 2. Update firewood position: between concrete column (x=-6.4) and door (x=-4.8) as seen in 01:44 video & user screenshot
old_firewood_pos = """    // 西次间窗下堆叠柴火堆 (Firewood Stack beneath Bay 1 Window, 01:44 实景)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.85, 0.72, 0.45),
        mFirewood
    );
    firewoodMesh.position.set(-8.0, 0.18 + 0.36, 0.05);
    firewoodMesh.castShadow = true;
    firewoodMesh.receiveShadow = true;
    houseGroup.add(firewoodMesh);"""

new_firewood_pos = """    // 廊柱旁堆叠柴火堆 (Firewood Stack beside concrete pillar, 01:44 实景: 位于西次间立柱右侧)
    const firewoodMesh = new THREE.Mesh(
        new THREE.BoxGeometry(1.25, 0.46, 0.45),
        mFirewood
    );
    firewoodMesh.position.set(-5.65, 0.18 + 0.23, 0.05);
    firewoodMesh.castShadow = true;
    firewoodMesh.receiveShadow = true;
    houseGroup.add(firewoodMesh);"""

assert old_firewood_pos in code, "old_firewood_pos not found"
code = code.replace(old_firewood_pos, new_firewood_pos)

# 3. Update west_annex camera position to exactly match uploaded_media_1790322895646.png
old_annex_cam = """        west_annex: {
            pos: new THREE.Vector3(-5.2, 1.48, 7.0),
            target: new THREE.Vector3(-9.2, 1.65, 0.0),"""

new_annex_cam = """        west_annex: {
            pos: new THREE.Vector3(-8.8, 1.42, 6.2),
            target: new THREE.Vector3(-10.8, 1.65, -0.2),"""

assert old_annex_cam in code, "old_annex_cam not found"
code = code.replace(old_annex_cam, new_annex_cam)

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied annex and firewood fixes successfully")
