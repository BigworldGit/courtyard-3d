with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Tone mapping exposure and lighting calibration
code = code.replace(
    "renderer.toneMappingExposure = 1.08;",
    "renderer.toneMappingExposure = 0.98;"
)

code = code.replace(
    "const hemiLight = new THREE.HemisphereLight(0xfff7ed, 0x8a927e, 1.10);",
    "const hemiLight = new THREE.HemisphereLight(0xfff7ed, 0x7a826e, 0.85);"
)

code = code.replace(
    "const sunLight = new THREE.DirectionalLight(0xfffaec, 1.85);",
    "const sunLight = new THREE.DirectionalLight(0xfffaec, 1.50);"
)

code = code.replace(
    "const verandaFillLight = new THREE.DirectionalLight(0xffeedd, 0.90);",
    "const verandaFillLight = new THREE.DirectionalLight(0xffeedd, 0.70);"
)

code = code.replace(
    "const southYardFillLight = new THREE.DirectionalLight(0xffeedd, 0.70);",
    "const southYardFillLight = new THREE.DirectionalLight(0xffeedd, 0.60);"
)

# 2. Add dedicated stone materials for wall, gatepost, coping, and boulder
old_tex_stone = "    const tStone = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 4, 2);"
new_tex_stone = """    const tStoneWall = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 8, 2);
    const tGatepost = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1.2, 2.2);
    const tCoping = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 6, 1);
    const tStoneBoulder = loadTexture('textures/tex_authentic_dry_stone.jpg', THREE.RepeatWrapping, THREE.RepeatWrapping, 1.5, 1.5);
    const tStone = tStoneWall;"""

assert old_tex_stone in code, "old_tex_stone not found"
code = code.replace(old_tex_stone, new_tex_stone)

old_mat_stone = """    const mStone = new THREE.MeshStandardMaterial({
        map: tStone,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });"""

new_mat_stone = """    const mStoneWall = new THREE.MeshStandardMaterial({
        map: tStoneWall,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mGatepost = new THREE.MeshStandardMaterial({
        map: tGatepost,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mCoping = new THREE.MeshStandardMaterial({
        map: tCoping,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mStoneBoulder = new THREE.MeshStandardMaterial({
        map: tStoneBoulder,
        roughness: 0.88,
        metalness: 0.02,
        side: THREE.DoubleSide
    });

    const mStone = mStoneWall;"""

assert old_mat_stone in code, "old_mat_stone not found"
code = code.replace(old_mat_stone, new_mat_stone)

# 3. Clean up buildWallRun to use mStoneWall, mCoping, mStoneBoulder directly without texture cloning
old_wall_func = """    function buildWallRun(pts, wallH = 1.15, wallThick = 0.65, extraDown = 1.45) {
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

new_wall_func = """    function buildWallRun(pts, wallH = 1.15, wallThick = 0.65, extraDown = 1.45) {
        for (let p = 0; p < pts.length - 1; p++) {
            const p1 = pts[p];
            const p2 = pts[p+1];
            const segLen = p1.distanceTo(p2);
            const mid = p1.clone().add(p2).multiplyScalar(0.5);
            const rotY = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;

            const totalH = wallH + extraDown;
            const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, totalH, wallThick), mStoneWall);
            wallSeg.position.set(mid.x, mid.y - extraDown + totalH/2, mid.z);
            wallSeg.rotation.y = rotY;
            wallSeg.castShadow = true;
            wallSeg.receiveShadow = true;
            stoneWallGroup.add(wallSeg);

            // Rustic Stone Coping Slabs on top (条石/毛石压顶)
            const coping = new THREE.Mesh(new THREE.BoxGeometry(segLen + 0.1, 0.14, wallThick + 0.16), mCoping);
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
                const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.36 + (b % 2) * 0.12, 1), mStoneBoulder);
                boulder.scale.set(1.2, 0.75, 1.15);
                boulder.position.set(bx, mid.y + 0.15, bz);
                boulder.castShadow = true;
                stoneWallGroup.add(boulder);
            }
        }
    }"""

assert old_wall_func in code, "old_wall_func not found"
code = code.replace(old_wall_func, new_wall_func)

# 4. Clean up addGatepost to use mGatepost, mCoping, mStoneBoulder directly without texture cloning
old_gate_func = """    // Courtyard Entrance Boulder Gateposts (-10.0 & -7.8 at z = 14.2)
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

new_gate_func = """    // Courtyard Entrance Boulder Gateposts (-10.0 & -7.8 at z = 14.2)
    function addGatepost(gx, gz) {
        const post = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.85, 1.0), mGatepost);
        post.position.set(gx, 0.925, gz);
        post.castShadow = true;
        post.receiveShadow = true;
        stoneWallGroup.add(post);

        const cap = new THREE.Mesh(new THREE.BoxGeometry(1.20, 0.18, 1.20), mCoping);
        cap.position.set(gx, 1.85 + 0.09, gz);
        cap.castShadow = true;
        stoneWallGroup.add(cap);

        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.55, 1), mStoneBoulder);
        boulder.scale.set(1.25, 0.75, 1.15);
        boulder.position.set(gx + (gx < -8.5 ? -0.45 : 0.45), 0.22, gz + 0.4);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }"""

assert old_gate_func in code, "old_gate_func not found"
code = code.replace(old_gate_func, new_gate_func)

# 5. Make annex timber post and beam dark weathered timber
code = code.replace(
    "const annexPost = new THREE.Mesh(new THREE.BoxGeometry(0.18, annexEaveH, 0.18), mStone);",
    "const annexPost = new THREE.Mesh(new THREE.BoxGeometry(0.18, annexEaveH, 0.18), new THREE.MeshStandardMaterial({ color: 0x2b1e16, roughness: 0.88 }));"
)

code = code.replace(
    "const annexEaveBeam = new THREE.Mesh(new THREE.BoxGeometry(AW + 0.35, 0.16, 0.16), mWood);",
    "const annexEaveBeam = new THREE.Mesh(new THREE.BoxGeometry(AW + 0.35, 0.16, 0.16), new THREE.MeshStandardMaterial({ color: 0x2b1e16, roughness: 0.88 }));"
)

# 6. Set mRedTile color to rich terracotta red so sunlight doesn't wash it out
code = code.replace(
    "const mRedTile = new THREE.MeshStandardMaterial({\n        map: tRedTile,\n        roughness: 0.82,\n        metalness: 0.02,\n        side: THREE.DoubleSide\n    });",
    "const mRedTile = new THREE.MeshStandardMaterial({\n        map: tRedTile,\n        color: 0xbb4a34,\n        roughness: 0.85,\n        metalness: 0.01,\n        side: THREE.DoubleSide\n    });"
)

with open('/Users/roy/Documents/workspace/courtyard_3d/build_complete_compound.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied definitive fix successfully")
