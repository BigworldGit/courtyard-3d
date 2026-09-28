import os

file_path = '/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update mRoof roughness & metalness, and mEarth color
old_mats = '''    const mEarth = new THREE.MeshStandardMaterial({
        map: tEarth,
        color: 0xc4a678,
        roughness: 0.94,
        metalness: 0.02,
        side: THREE.DoubleSide
    });'''

new_mats = '''    const mEarth = new THREE.MeshStandardMaterial({
        map: tEarth,
        color: 0xba9e74,
        roughness: 0.96,
        metalness: 0.01,
        side: THREE.DoubleSide
    });'''

assert old_mats in content, 'old_mats not found'
content = content.replace(old_mats, new_mats)

old_mroof = '''    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        roughness: 0.86,
        metalness: 0.04,
        side: THREE.DoubleSide
    });'''

new_mroof = '''    const mRoof = new THREE.MeshStandardMaterial({
        map: tRoof,
        roughness: 0.96,
        metalness: 0.0,
        side: THREE.DoubleSide
    });'''

assert old_mroof in content, 'old_mroof not found'
content = content.replace(old_mroof, new_mroof)

# 2. Update East Wing position to x = 12.8 to leave a natural ~1.3m gap between houses
old_wing_pos = 'wingGroup.position.set(11.8, 0, 3.4);'
new_wing_pos = 'wingGroup.position.set(12.8, 0, 3.2);'
assert old_wing_pos in content, 'old_wing_pos not found'
content = content.replace(old_wing_pos, new_wing_pos)

# 3. Add diagonal wood strut on main house east corner as seen in user photo
old_wing_start = '''    // --- 11. EAST WING OUTBUILDING (东厢房 / 侧屋, 01:05-01:50, 04:15) ---'''
new_wing_start = '''    // Diagonal wood prop leaning at main house east corner (视频01:05实景主房东侧斜撑木)
    const strutGeo = new THREE.CylinderGeometry(0.06, 0.08, 3.2, 8);
    const strutMesh = new THREE.Mesh(strutGeo, mWood);
    strutMesh.position.set(9.65, 1.35, -0.2);
    strutMesh.rotation.z = -0.38;
    strutMesh.rotation.x = 0.22;
    strutMesh.castShadow = true;
    scene.add(strutMesh);

    // --- 11. EAST WING OUTBUILDING (东厢房 / 侧屋, 01:05-01:50, 04:15) ---'''

assert old_wing_start in content, 'old_wing_start not found'
content = content.replace(old_wing_start, new_wing_start)

# 4. Update east_wing viewpoint camera
old_view = '''        east_wing: {
            pos: new THREE.Vector3(4.2, 1.55, 6.8),
            target: new THREE.Vector3(9.8, 1.65, 0.8),'''

new_view = '''        east_wing: {
            pos: new THREE.Vector3(2.5, 1.60, 9.8),
            target: new THREE.Vector3(11.2, 1.65, 1.8),'''

if old_view in content:
    content = content.replace(old_view, new_view)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated build_complete_compound.py successfully!')
