with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update tRedTile to use tex_terracotta_tiles_crisp.jpg
code = code.replace(
    "const tRedTile = loadTexture('textures/tex_authentic_red_tile.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 5, 4);",
    "const tRedTile = loadTexture('textures/tex_terracotta_tiles_crisp.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1, 1);"
)

# 2. Update buildWallRun to dynamically calculate texture repeat based on segLen and height!
old_buildWallRun = """    function buildWallRun(pts, wallH = 1.20, wallThick = 0.65, extraDown = 1.35) {
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
    }"""

new_buildWallRun = """    function buildWallRun(pts, wallH = 1.15, wallThick = 0.65, extraDown = 1.45) {
        for (let p = 0; p < pts.length - 1; p++) {
            const p1 = pts[p];
            const p2 = pts[p+1];
            const segLen = p1.distanceTo(p2);
            const mid = p1.clone().add(p2).multiplyScalar(0.5);
            const rotY = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;

            const totalH = wallH + extraDown;
            const segTex = tStone.clone();
            segTex.needsUpdate = true;
            segTex.wrapS = THREE.RepeatWrapping;
            segTex.wrapT = THREE.RepeatWrapping;
            segTex.repeat.set(Math.max(1.0, segLen / 1.5), totalH / 1.0);

            const segMat = new THREE.MeshStandardMaterial({
                map: segTex,
                roughness: 0.88,
                metalness: 0.02,
                side: THREE.DoubleSide
            });

            const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, totalH, wallThick), segMat);
            wallSeg.position.set(mid.x, mid.y - extraDown + totalH/2, mid.z);
            wallSeg.rotation.y = rotY;
            wallSeg.castShadow = true;
            wallSeg.receiveShadow = true;
            stoneWallGroup.add(wallSeg);

            // Rustic Stone Coping Slabs on top (条石/毛石压顶)
            const coping = new THREE.Mesh(new THREE.BoxGeometry(segLen + 0.1, 0.14, wallThick + 0.16), segMat);
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
                const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.36 + (b % 2) * 0.12, 1), segMat);
                boulder.scale.set(1.2, 0.75, 1.15);
                boulder.position.set(bx, mid.y + 0.15, bz);
                boulder.castShadow = true;
                stoneWallGroup.add(boulder);
            }
        }
    }"""

assert old_buildWallRun in code, "old_buildWallRun not found"
code = code.replace(old_buildWallRun, new_buildWallRun)

# 3. Update addGatepost with proper stone texture repeat and natural boulder base
old_gatepost = """    // Courtyard Entrance Boulder Gateposts (-10.0 & -7.8 at z = 14.2)
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
    }"""

new_gatepost = """    // Courtyard Entrance Boulder Gateposts (-10.0 & -7.8 at z = 14.2)
    function addGatepost(gx, gz) {
        const postTex = tStone.clone();
        postTex.needsUpdate = true;
        postTex.wrapS = THREE.RepeatWrapping;
        postTex.wrapT = THREE.RepeatWrapping;
        postTex.repeat.set(1.0, 1.8);
        const postMat = new THREE.MeshStandardMaterial({ map: postTex, roughness: 0.88, metalness: 0.02, side: THREE.DoubleSide });

        const post = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.85, 1.0), postMat);
        post.position.set(gx, 0.925, gz);
        post.castShadow = true;
        post.receiveShadow = true;
        stoneWallGroup.add(post);

        const cap = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.18, 1.20), postMat);
        cap.position.set(gx, 1.85 + 0.09, gz);
        cap.castShadow = true;
        stoneWallGroup.add(cap);

        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.55, 1), postMat);
        boulder.scale.set(1.25, 0.75, 1.15);
        boulder.position.set(gx + (gx < -8.5 ? -0.45 : 0.45), 0.22, gz + 0.4);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }"""

assert old_gatepost in code, "old_gatepost not found"
code = code.replace(old_gatepost, new_gatepost)

# 4. Update Annex Roof Height & UV Mapping
old_annex_heights = """    const annexEaveH = 2.15;
    const annexRidgeH = 3.20;
    const annexRidgeZ = (annexZ_eaveSouth + annexZ_eaveNorth) / 2; // -1.95m
    const annexHipX = -12.4; // 西侧四坡斜脊起点"""

new_annex_heights = """    const annexEaveH = 2.05;
    const annexRidgeH = 3.45;
    const annexRidgeZ = (annexZ_eaveSouth + annexZ_eaveNorth) / 2; // -1.95m
    const annexHipX = -12.3; // 西侧四坡斜脊起点"""

assert old_annex_heights in code, "old_annex_heights not found"
code = code.replace(old_annex_heights, new_annex_heights)

old_annex_uvs = """    const s_uvs = new Float32Array([
        0, 3,
        4, 0,
        0, 0,
        0, 3,
        2.5, 3,
        4, 0
    ]);"""

new_annex_uvs = """    const s_uvs = new Float32Array([
        0, 6.0,
        8.0, 0,
        0, 0,
        0, 6.0,
        5.2, 6.0,
        8.0, 0
    ]);"""

assert old_annex_uvs in code, "old_annex_uvs not found"
code = code.replace(old_annex_uvs, new_annex_uvs)

old_w_uvs = """    const w_uvs = new Float32Array([
        2, 3,
        4, 0,
        0, 0
    ]);"""

new_w_uvs = """    const w_uvs = new Float32Array([
        4.0, 6.0,
        8.0, 0,
        0, 0
    ]);"""

assert old_w_uvs in code, "old_w_uvs not found"
code = code.replace(old_w_uvs, new_w_uvs)

old_n_uvs = """    const n_uvs = new Float32Array([
        2.5, 3,
        0, 0,
        4, 0,
        2.5, 3,
        0, 3,
        0, 0
    ]);"""

new_n_uvs = """    const n_uvs = new Float32Array([
        5.2, 6.0,
        0, 0,
        8.0, 0,
        5.2, 6.0,
        0, 6.0,
        0, 0
    ]);"""

assert old_n_uvs in code, "old_n_uvs not found"
code = code.replace(old_n_uvs, new_n_uvs)

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied stone and roof polish successfully")
