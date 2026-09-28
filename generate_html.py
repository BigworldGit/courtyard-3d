# -*- coding: utf-8 -*-
import os

html_content = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>陕北/北方传统民居院落高精3D数字孪生与视频对比系统</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
            background-color: #111;
            color: #eee;
        }
        #webgl-container {
            width: 100%;
            height: 100%;
            position: absolute;
            left: 0;
            top: 0;
            z-index: 1;
        }

        /* Top Header UI */
        .top-bar {
            position: absolute;
            top: 16px;
            left: 20px;
            right: 20px;
            z-index: 10;
            display: flex;
            justify-content: space-between;
            align-items: center;
            pointer-events: none;
        }
        .title-badge {
            background: rgba(18, 20, 24, 0.88);
            backdrop-filter: blur(12px);
            padding: 12px 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
            pointer-events: auto;
        }
        .title-badge h1 {
            font-size: 18px;
            font-weight: 600;
            color: #f3efe6;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .title-badge .subtitle {
            font-size: 12px;
            color: #a49e93;
            margin-top: 4px;
        }
        .status-tag {
            background: #2b7a4b;
            color: #e5ffed;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 6px;
            font-weight: 500;
        }

        /* Top Right Control Pill */
        .top-controls {
            display: flex;
            gap: 10px;
            pointer-events: auto;
        }
        .glass-btn {
            background: rgba(22, 25, 31, 0.85);
            backdrop-filter: blur(10px);
            color: #e2ded5;
            border: 1px solid rgba(255, 255, 255, 0.14);
            padding: 9px 15px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }
        .glass-btn:hover {
            background: rgba(45, 52, 65, 0.95);
            border-color: rgba(255, 215, 0, 0.4);
            color: #fff;
            transform: translateY(-1px);
        }
        .glass-btn.active {
            background: #8b5e34;
            color: #fff;
            border-color: #d4a373;
            box-shadow: 0 0 12px rgba(212, 163, 115, 0.5);
        }

        /* Bottom Floating Viewpoint Selector */
        .bottom-nav {
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;
            background: rgba(18, 20, 24, 0.88);
            backdrop-filter: blur(16px);
            padding: 8px 12px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
            display: flex;
            gap: 6px;
            max-width: 95vw;
            overflow-x: auto;
        }
        .view-btn {
            background: transparent;
            border: 1px solid transparent;
            color: #b5b0a5;
            padding: 8px 14px;
            border-radius: 10px;
            font-size: 12.5px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            white-space: nowrap;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }
        .view-btn span.label {
            font-size: 12.5px;
            color: #f1ede4;
        }
        .view-btn span.time {
            font-size: 10px;
            color: #888277;
        }
        .view-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
        }
        .view-btn.active {
            background: #4a3728;
            border-color: #c99355;
            color: #fff;
        }
        .view-btn.active span.time {
            color: #e5b982;
        }

        /* Side Comparison Drawer */
        .comparison-drawer {
            position: absolute;
            top: 80px;
            right: 20px;
            width: 360px;
            max-height: calc(100vh - 180px);
            background: rgba(18, 20, 24, 0.92);
            backdrop-filter: blur(16px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: 0 16px 48px rgba(0,0,0,0.6);
            z-index: 15;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), opacity 0.3s;
        }
        .comparison-drawer.collapsed {
            transform: translateX(390px);
            opacity: 0;
            pointer-events: none;
        }
        .drawer-header {
            padding: 14px 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(30, 34, 40, 0.6);
        }
        .drawer-header h3 {
            font-size: 14px;
            font-weight: 600;
            color: #f4ede1;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .close-drawer-btn {
            background: transparent;
            border: none;
            color: #8c867c;
            font-size: 18px;
            cursor: pointer;
            padding: 2px 6px;
            border-radius: 6px;
        }
        .close-drawer-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.1);
        }
        .drawer-content {
            padding: 16px;
            overflow-y: auto;
            font-size: 13px;
            color: #ccc5b9;
            line-height: 1.6;
        }
        .ref-image-wrapper {
            width: 100%;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.15);
            margin-bottom: 12px;
            background: #000;
            position: relative;
        }
        .ref-image-wrapper img {
            width: 100%;
            height: auto;
            display: block;
        }
        .ref-image-tag {
            position: absolute;
            bottom: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.75);
            font-size: 11px;
            color: #f7d794;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
        }
        .detail-card {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .detail-card h4 {
            font-size: 13px;
            color: #e5b982;
            margin-bottom: 6px;
        }
        .detail-card ul {
            padding-left: 18px;
            font-size: 12px;
            color: #b5b0a5;
        }
        .detail-card li {
            margin-bottom: 4px;
        }

        /* Hotspot Pins in 3D Scene */
        .hotspot-pin {
            position: absolute;
            transform: translate(-50%, -50%);
            width: 28px;
            height: 28px;
            background: rgba(212, 163, 115, 0.85);
            border: 2px solid #fff;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 16px rgba(212, 163, 115, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: bold;
            color: #2b1d0c;
            transition: transform 0.2s, background 0.2s;
            pointer-events: auto;
            z-index: 5;
        }
        .hotspot-pin:hover {
            transform: translate(-50%, -50%) scale(1.25);
            background: #ffd166;
        }
        .hotspot-label {
            position: absolute;
            left: 34px;
            top: 2px;
            background: rgba(18, 20, 24, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 11px;
            white-space: nowrap;
            color: #eee;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }
        .hotspot-pin:hover .hotspot-label {
            opacity: 1;
        }

        /* Instruction Overlay */
        .help-overlay {
            position: absolute;
            left: 20px;
            bottom: 24px;
            z-index: 10;
            background: rgba(18, 20, 24, 0.82);
            backdrop-filter: blur(10px);
            padding: 10px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 11.5px;
            color: #9e978c;
            line-height: 1.5;
            pointer-events: none;
        }
        .help-overlay b {
            color: #e5d7c3;
        }

        /* First Person Reticle */
        #crosshair {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 8px;
            height: 8px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            display: none;
            z-index: 20;
        }
    </style>
</head>
<body>
    <div id="webgl-container"></div>
    <div id="crosshair"></div>

    <!-- Top UI Bar -->
    <div class="top-bar">
        <div class="title-badge">
            <h1>
                <span>三开间北方传统夯土民居院落 · 3D高精重构</span>
                <span class="status-tag">视频精确还原 (M2U00577.MPG)</span>
            </h1>
            <div class="subtitle">包含正房三开间、水泥空心立柱、青瓦堆、木梯、东厢房残破土墙、干砌块石围墙、高耸古树与山林环境</div>
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

    <!-- Help HUD -->
    <div class="help-overlay">
        <div>视角操作: <b>鼠标左键</b>旋转 · <b>右键</b>平移 · <b>滚轮</b>缩放</div>
        <div>建筑细节: <b>点击场景中的发光金球</b>即可聚焦对应建筑部件与视频对比</div>
    </div>

    <!-- Three.js and OrbitControls -->
    <script src="libs/three.min.js"></script>
    <script src="libs/OrbitControls.js"></script>

    <script>
    // --- Procedural Texture Generators using HTML5 Canvas ---
    // Generates rich PBR-like textures without external image file latency

    function createRammedEarthTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 1024;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Base earthen background
        const grad = ctx.createLinearGradient(0, 0, 0, 1024);
        grad.addColorStop(0, '#b88958');
        grad.addColorStop(0.3, '#9d7345');
        grad.addColorStop(0.6, '#a87c4c');
        grad.addColorStop(1, '#8e6439');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 1024, 1024);

        // Horizontal ramming layers (夯层纹理)
        for (let y = 0; y < 1024; y += 32) {
            ctx.fillStyle = `rgba(60, 40, 20, ${0.12 + Math.random() * 0.15})`;
            ctx.fillRect(0, y + (Math.random() * 4 - 2), 1024, 3 + Math.random() * 4);

            ctx.fillStyle = `rgba(230, 200, 160, ${0.08 + Math.random() * 0.1})`;
            ctx.fillRect(0, y + 8, 1024, 2);
        }

        // Noise, clay clumps and fine straw fiber
        const imgData = ctx.getImageData(0, 0, 1024, 1024);
        const d = imgData.data;
        for (let i = 0; i < d.length; i += 4) {
            const noise = (Math.random() - 0.5) * 45;
            d[i] = Math.min(255, Math.max(0, d[i] + noise));
            d[i+1] = Math.min(255, Math.max(0, d[i+1] + noise * 0.9));
            d[i+2] = Math.min(255, Math.max(0, d[i+2] + noise * 0.7));
        }
        ctx.putImageData(imgData, 0, 0);

        // Straw specks (麦草纤维)
        ctx.strokeStyle = 'rgba(230, 210, 140, 0.45)';
        ctx.lineWidth = 1.2;
        for (let j = 0; j < 600; j++) {
            const sx = Math.random() * 1024;
            const sy = Math.random() * 1024;
            const len = 4 + Math.random() * 12;
            const ang = (Math.random() - 0.5) * 1.5;
            ctx.beginPath();
            ctx.moveTo(sx, sy);
            ctx.lineTo(sx + Math.cos(ang) * len, sy + Math.sin(ang) * len);
            ctx.stroke();
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
    }

    function createPeelingPlasterTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 1024;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Earthen mud base
        ctx.fillStyle = '#a17849';
        ctx.fillRect(0, 0, 1024, 1024);

        // Whitewash plaster patches with peeling edges (白灰脱落斑驳效果)
        ctx.fillStyle = '#e8e5dc';
        for (let k = 0; k < 45; k++) {
            const px = 200 + Math.random() * 624;
            const py = 150 + Math.random() * 724;
            const r = 40 + Math.random() * 120;
            ctx.beginPath();
            ctx.arc(px, py, r, 0, Math.PI * 2);
            ctx.fill();
        }

        // Flaked edge noise
        ctx.fillStyle = 'rgba(245, 242, 235, 0.85)';
        for (let k = 0; k < 300; k++) {
            const px = 100 + Math.random() * 824;
            const py = 100 + Math.random() * 824;
            ctx.fillRect(px, py, 10 + Math.random() * 35, 10 + Math.random() * 35);
        }

        // Dirt stains running down
        ctx.fillStyle = 'rgba(70, 50, 30, 0.15)';
        for (let k = 0; k < 80; k++) {
            const sx = Math.random() * 1024;
            ctx.fillRect(sx, 100 + Math.random() * 200, 2 + Math.random() * 4, 150 + Math.random() * 350);
        }

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
    }

    function createRoofTileTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Base grey tile tone
        ctx.fillStyle = '#424548';
        ctx.fillRect(0, 0, 512, 512);

        // Vertical corrugation grooves (仰瓦与筒瓦的瓦垄沟)
        const colW = 32;
        for (let x = 0; x < 512; x += colW) {
            // Shadow side
            const g = ctx.createLinearGradient(x, 0, x + colW, 0);
            g.addColorStop(0, '#222426');
            g.addColorStop(0.3, '#5c6066');
            g.addColorStop(0.7, '#6b7077');
            g.addColorStop(1, '#25272a');
            ctx.fillStyle = g;
            ctx.fillRect(x, 0, colW, 512);

            // Shingle overlap lines (横向搭接阴影)
            for (let y = 0; y < 512; y += 40) {
                ctx.fillStyle = 'rgba(15, 16, 18, 0.6)';
                ctx.fillRect(x, y, colW, 4);
                ctx.fillStyle = 'rgba(180, 185, 195, 0.25)';
                ctx.fillRect(x, y + 4, colW, 2);
            }
        }

        // Weathering patina and lichen
        for (let i = 0; i < 400; i++) {
            ctx.fillStyle = Math.random() > 0.5 ? 'rgba(90, 85, 75, 0.2)' : 'rgba(30, 32, 35, 0.3)';
            ctx.fillRect(Math.random() * 512, Math.random() * 512, 4 + Math.random() * 12, 3 + Math.random() * 8);
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
    }

    function createCinderBlockTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Concrete grey background
        ctx.fillStyle = '#8f9296';
        ctx.fillRect(0, 0, 256, 512);

        // 11 distinct block layers matching the video column!
        const blockH = 512 / 11;
        for (let i = 0; i < 11; i++) {
            const y = i * blockH;
            // Block texture variation
            ctx.fillStyle = (i % 2 === 0) ? '#96999e' : '#888b8f';
            ctx.fillRect(4, y + 2, 248, blockH - 4);

            // Mortar joint (灰缝阴影与白线)
            ctx.fillStyle = '#4a4d52';
            ctx.fillRect(0, y, 256, 4);
            ctx.fillStyle = '#b8bbc0';
            ctx.fillRect(0, y + 4, 256, 1.5);
        }

        // Noise
        const imgData = ctx.getImageData(0, 0, 256, 512);
        const d = imgData.data;
        for (let i = 0; i < d.length; i += 4) {
            const n = (Math.random() - 0.5) * 30;
            d[i] = Math.min(255, Math.max(0, d[i] + n));
            d[i+1] = Math.min(255, Math.max(0, d[i+1] + n));
            d[i+2] = Math.min(255, Math.max(0, d[i+2] + n));
        }
        ctx.putImageData(imgData, 0, 0);

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
    }

    function createRedBrickTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 128;
        const ctx = canvas.getContext('2d');

        ctx.fillStyle = '#8f3c2c';
        ctx.fillRect(0, 0, 256, 128);

        // Brick courses and mortar joints
        ctx.fillStyle = '#dcd8cf';
        ctx.fillRect(0, 60, 256, 6);
        ctx.fillRect(124, 0, 6, 60);
        ctx.fillRect(60, 66, 6, 62);
        ctx.fillRect(190, 66, 6, 62);

        // Brick noise
        const imgData = ctx.getImageData(0, 0, 256, 128);
        const d = imgData.data;
        for (let i = 0; i < d.length; i += 4) {
            const n = (Math.random() - 0.5) * 40;
            d[i] = Math.min(255, Math.max(0, d[i] + n));
            d[i+1] = Math.min(255, Math.max(0, d[i+1] + n * 0.6));
            d[i+2] = Math.min(255, Math.max(0, d[i+2] + n * 0.5));
        }
        ctx.putImageData(imgData, 0, 0);

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
    }

    function createWoodDoorTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Dark aged cedar wood (老杉木板)
        ctx.fillStyle = '#423223';
        ctx.fillRect(0, 0, 512, 1024);

        // Vertical grain and board joints (对开两扇板门垂直拼缝)
        const boardW = 64;
        for (let x = 0; x < 512; x += boardW) {
            ctx.fillStyle = (x === 256) ? '#18120c' : 'rgba(25, 18, 12, 0.4)';
            ctx.fillRect(x - 2, 0, (x === 256) ? 5 : 2, 1024);

            // Fine vertical grains
            for (let g = 0; g < boardW; g += 4) {
                ctx.fillStyle = `rgba(20, 14, 9, ${0.1 + Math.random() * 0.15})`;
                ctx.fillRect(x + g, 0, 1.5, 1024);
            }
        }

        // Two diamond spring festival paper sheets (斗方/门神纸)
        function drawDiamond(cx, cy, size, color) {
            ctx.save();
            ctx.translate(cx, cy);
            ctx.rotate(Math.PI / 4);
            ctx.fillStyle = color;
            ctx.fillRect(-size/2, -size/2, size, size);
            ctx.strokeStyle = 'rgba(50, 10, 10, 0.4)';
            ctx.lineWidth = 2;
            ctx.strokeRect(-size/2, -size/2, size, size);
            // Ink traces
            ctx.fillStyle = 'rgba(20, 20, 20, 0.7)';
            ctx.beginPath();
            ctx.arc(0, 0, size * 0.25, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }

        // Left door diamond
        drawDiamond(128, 380, 85, 'rgba(225, 215, 195, 0.85)');
        // Right door diamond
        drawDiamond(384, 380, 85, 'rgba(225, 215, 195, 0.85)');

        // Weathered door headers (横批纸条)
        ctx.fillStyle = 'rgba(230, 220, 200, 0.9)';
        ctx.fillRect(160, 80, 192, 45);

        // Side couplet strips (对联)
        ctx.fillRect(15, 180, 32, 600);
        ctx.fillRect(465, 180, 32, 600);

        const texture = new THREE.CanvasTexture(canvas);
        return texture;
    }

    function createDryStoneWallTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 1024;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');

        // Dark deep mortarless shadow base
        ctx.fillStyle = '#222325';
        ctx.fillRect(0, 0, 1024, 512);

        // Dry masonry irregular stones (乱石干砌)
        const rows = 12;
        const cols = 20;
        const rh = 512 / rows;
        const cw = 1024 / cols;

        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const ox = (r % 2 === 0 ? 0 : cw / 2) + c * cw + (Math.random() - 0.5) * 8;
                const oy = r * rh + (Math.random() - 0.5) * 4;
                const sw = cw * (0.8 + Math.random() * 0.35);
                const sh = rh * (0.75 + Math.random() * 0.3);

                // Varied stone hue: grey granite, ochre sandstone, weathered limestone
                const stoneColors = ['#6e7072', '#7d7a75', '#888075', '#5a5c5f', '#8f8c85', '#635d56'];
                ctx.fillStyle = stoneColors[Math.floor(Math.random() * stoneColors.length)];

                // Rounded irregular polygon
                ctx.beginPath();
                ctx.roundRect ? ctx.roundRect(ox, oy, sw, sh, 4 + Math.random() * 4) : ctx.rect(ox, oy, sw, sh);
                ctx.fill();

                // Chiseled edge highlight
                ctx.strokeStyle = 'rgba(220, 220, 225, 0.18)';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
    }

    function createCourtyardDirtTexture() {
        const canvas = document.createElement('canvas');
        canvas.width = 1024;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        // Warm North China yellow loess earth (黄土硬院坪)
        ctx.fillStyle = '#c5a06c';
        ctx.fillRect(0, 0, 1024, 1024);

        // Trampled paths and sandy variations
        for (let i = 0; i < 60; i++) {
            const rx = Math.random() * 1024;
            const ry = Math.random() * 1024;
            const rad = 60 + Math.random() * 180;
            const g = ctx.createRadialGradient(rx, ry, 10, rx, ry, rad);
            g.addColorStop(0, Math.random() > 0.5 ? 'rgba(175, 135, 88, 0.45)' : 'rgba(215, 185, 135, 0.35)');
            g.addColorStop(1, 'transparent');
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.arc(rx, ry, rad, 0, Math.PI * 2);
            ctx.fill();
        }

        // Dry grass / weed tufts
        for (let j = 0; j < 350; j++) {
            const gx = Math.random() * 1024;
            const gy = Math.random() * 1024;
            ctx.fillStyle = Math.random() > 0.3 ? 'rgba(155, 135, 75, 0.4)' : 'rgba(105, 130, 65, 0.4)';
            ctx.fillRect(gx, gy, 4 + Math.random() * 12, 2 + Math.random() * 5);
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.wrapS = THREE.RepeatWrapping;
        texture.wrapT = THREE.RepeatWrapping;
        return texture;
    }

    // --- Scene Initialization ---
    const container = document.getElementById('webgl-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbddaf0);
    scene.fog = new THREE.FogExp2(0xd6e5f2, 0.012);

    const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 400);
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.02; // Prevent going underground
    controls.minDistance = 2.0;
    controls.maxDistance = 120.0;

    // --- Textures Pool ---
    const rammedEarthTex = createRammedEarthTexture();
    rammedEarthTex.repeat.set(4, 2);

    const plasterTex = createPeelingPlasterTexture();
    const tileTex = createRoofTileTexture();
    tileTex.repeat.set(12, 6);

    const pillarTex = createCinderBlockTexture();
    const brickTex = createRedBrickTexture();
    brickTex.repeat.set(2, 1);

    const doorTex = createWoodDoorTexture();
    const stoneWallTex = createDryStoneWallTexture();
    stoneWallTex.repeat.set(4, 2);

    const groundTex = createCourtyardDirtTexture();
    groundTex.repeat.set(8, 8);

    // --- Common Materials ---
    const earthMat = new THREE.MeshStandardMaterial({
        map: rammedEarthTex,
        roughness: 0.95,
        metalness: 0.05,
        bumpMap: rammedEarthTex,
        bumpScale: 0.04
    });

    const plasterMat = new THREE.MeshStandardMaterial({
        map: plasterTex,
        roughness: 0.88,
        metalness: 0.02
    });

    const roofTileMat = new THREE.MeshStandardMaterial({
        map: tileTex,
        roughness: 0.75,
        metalness: 0.12,
        bumpMap: tileTex,
        bumpScale: 0.06
    });

    const pillarMat = new THREE.MeshStandardMaterial({
        map: pillarTex,
        roughness: 0.82,
        metalness: 0.05
    });

    const brickMat = new THREE.MeshStandardMaterial({
        map: brickTex,
        roughness: 0.85,
        metalness: 0.04
    });

    const woodMat = new THREE.MeshStandardMaterial({
        color: 0x4a3725,
        roughness: 0.8,
        metalness: 0.08
    });

    const doorMat = new THREE.MeshStandardMaterial({
        map: doorTex,
        roughness: 0.78,
        metalness: 0.06
    });

    const stoneWallMat = new THREE.MeshStandardMaterial({
        map: stoneWallTex,
        roughness: 0.92,
        metalness: 0.08,
        bumpMap: stoneWallTex,
        bumpScale: 0.08
    });

    const groundMat = new THREE.MeshStandardMaterial({
        map: groundTex,
        roughness: 0.96,
        metalness: 0.02
    });

    // --- Lighting ---
    const hemiLight = new THREE.HemisphereLight(0xfff5e6, 0x8a927d, 0.75);
    scene.add(hemiLight);

    const sunLight = new THREE.DirectionalLight(0xfffaed, 1.8);
    sunLight.position.set(-25, 45, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 150;
    sunLight.shadow.camera.left = -25;
    sunLight.shadow.camera.right = 25;
    sunLight.shadow.camera.top = 25;
    sunLight.shadow.camera.bottom = -25;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    // --- Ground & Terraced Terrain Modeling ---
    const groundGeo = new THREE.PlaneGeometry(80, 80, 64, 64);
    // Add subtle elevation: rising at the back (North), slight dip to the southwest
    const pos = groundGeo.attributes.position;
    for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i);
        const y = pos.getY(i);
        // y in plane geometry maps to z in 3D scene after rotation
        let zElev = 0;
        if (y < -3) { // Back hillside
            zElev = Math.pow(Math.abs(y + 3) * 0.18, 1.3);
        } else if (x < -8 && y > 8) { // Southwest path slope
            zElev = -(y - 8) * 0.12;
        }
        pos.setZ(i, zElev + (Math.sin(x*0.4) * Math.cos(y*0.4) * 0.08));
    }
    groundGeo.computeVertexNormals();
    const groundMesh = new THREE.Mesh(groundGeo, groundMat);
    groundMesh.rotation.x = -Math.PI / 2;
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // Distant mountain backdrop
    const mountainGeo = new THREE.CylinderGeometry(180, 220, 50, 48, 8, true);
    const mountainMat = new THREE.MeshBasicMaterial({
        color: 0x98a8b8,
        side: THREE.BackSide,
        fog: true
    });
    const mountainMesh = new THREE.Mesh(mountainGeo, mountainMat);
    mountainMesh.position.y = 10;
    scene.add(mountainMesh);

    // Blue ground marker stake (as seen in video frame 60s)
    const stakeGeo = new THREE.BoxGeometry(0.08, 0.45, 0.08);
    const stakeMat = new THREE.MeshStandardMaterial({ color: 0x2277bb, roughness: 0.5 });
    const stake = new THREE.Mesh(stakeGeo, stakeMat);
    stake.position.set(1.5, 0.22, 4.2);
    stake.castShadow = true;
    scene.add(stake);

    // --- 1. Main House (正房/上房) Modeling ---
    const houseGroup = new THREE.Group();
    scene.add(houseGroup);

    // Coordinate Origin of Main House: centered at (0, 0, -2.5)
    const H_WIDTH = 11.2;
    const H_DEPTH = 4.8;
    const H_EAVES_H = 2.85;
    const H_RIDGE_H = 4.65;
    const PORCH_DEPTH = 0.95;

    // Raised Foundation Plinth (台基与散水)
    const plinthGeo = new THREE.BoxGeometry(H_WIDTH + 0.8, 0.2, H_DEPTH + PORCH_DEPTH + 0.6);
    const plinthMat = new THREE.MeshStandardMaterial({ color: 0x7c7873, roughness: 0.9 });
    const plinthMesh = new THREE.Mesh(plinthGeo, plinthMat);
    plinthMesh.position.set(0, 0.1, -2.5 + PORCH_DEPTH * 0.35);
    plinthMesh.receiveShadow = true;
    plinthMesh.castShadow = true;
    houseGroup.add(plinthMesh);

    // Main Earthen Walls (Rear, Gable West, Gable East)
    // Rear Wall
    const rearWallGeo = new THREE.BoxGeometry(H_WIDTH, H_EAVES_H, 0.45);
    const rearWall = new THREE.Mesh(rearWallGeo, earthMat);
    rearWall.position.set(0, 0.2 + H_EAVES_H / 2, -2.5 - H_DEPTH / 2);
    rearWall.castShadow = true;
    rearWall.receiveShadow = true;
    houseGroup.add(rearWall);

    // West Gable Wall
    const westGable = new THREE.Mesh(new THREE.BoxGeometry(0.45, H_EAVES_H, H_DEPTH), earthMat);
    westGable.position.set(-H_WIDTH / 2 + 0.22, 0.2 + H_EAVES_H / 2, -2.5);
    westGable.castShadow = true;
    houseGroup.add(westGable);

    // East Gable Wall
    const eastGable = new THREE.Mesh(new THREE.BoxGeometry(0.45, H_EAVES_H, H_DEPTH), earthMat);
    eastGable.position.set(H_WIDTH / 2 - 0.22, 0.2 + H_EAVES_H / 2, -2.5);
    eastGable.castShadow = true;
    houseGroup.add(eastGable);

    // Gable Triangular Tops (山墙三角形山花)
    const gableTriShape = new THREE.Shape();
    gableTriShape.moveTo(-H_DEPTH / 2, 0);
    gableTriShape.lineTo(H_DEPTH / 2, 0);
    gableTriShape.lineTo(0, H_RIDGE_H - H_EAVES_H);
    gableTriShape.closePath();
    const gableExtrudeSettings = { depth: 0.42, bevelEnabled: false };
    const gableTriGeo = new THREE.ExtrudeGeometry(gableTriShape, gableExtrudeSettings);

    const westTriMesh = new THREE.Mesh(gableTriGeo, earthMat);
    westTriMesh.rotation.y = Math.PI / 2;
    westTriMesh.position.set(-H_WIDTH / 2 + 0.42, 0.2 + H_EAVES_H, -2.5);
    houseGroup.add(westTriMesh);

    const eastTriMesh = new THREE.Mesh(gableTriGeo, earthMat);
    eastTriMesh.rotation.y = Math.PI / 2;
    eastTriMesh.position.set(H_WIDTH / 2, 0.2 + H_EAVES_H, -2.5);
    houseGroup.add(eastTriMesh);

    // Front Wall (南立面夯土墙 - 留出门窗开口)
    const frontWallZ = -2.5 + H_DEPTH / 2 - 0.25;

    // West Bay Front Wall
    const westWallGeo = new THREE.BoxGeometry(3.6, H_EAVES_H, 0.4);
    const westFrontWall = new THREE.Mesh(westWallGeo, earthMat);
    westFrontWall.position.set(-3.5, 0.2 + H_EAVES_H / 2, frontWallZ);
    westFrontWall.castShadow = true;
    westFrontWall.receiveShadow = true;
    houseGroup.add(westFrontWall);

    // East Bay Front Wall
    const eastWallGeo = new THREE.BoxGeometry(3.6, H_EAVES_H, 0.4);
    const eastFrontWall = new THREE.Mesh(eastWallGeo, earthMat);
    eastFrontWall.position.set(3.5, 0.2 + H_EAVES_H / 2, frontWallZ);
    eastFrontWall.castShadow = true;
    eastFrontWall.receiveShadow = true;
    houseGroup.add(eastFrontWall);

    // Center Bay Wall Over Lintel
    const lintelWallGeo = new THREE.BoxGeometry(2.4, H_EAVES_H - 2.2, 0.4);
    const lintelWall = new THREE.Mesh(lintelWallGeo, earthMat);
    lintelWall.position.set(0, 0.2 + 2.2 + (H_EAVES_H - 2.2) / 2, frontWallZ);
    houseGroup.add(lintelWall);

    // Central Main Doorway & Arched Peeling Plaster Surround (堂屋拱形白石灰门套与对开木门)
    const doorSurroundGeo = new THREE.BoxGeometry(1.8, 2.35, 0.42);
    const doorSurround = new THREE.Mesh(doorSurroundGeo, plasterMat);
    doorSurround.position.set(0, 0.2 + 2.35 / 2, frontWallZ);
    houseGroup.add(doorSurround);

    // Double Wooden Door Leaves
    const doorLeafGeo = new THREE.BoxGeometry(1.22, 2.1, 0.08);
    const doorMesh = new THREE.Mesh(doorLeafGeo, doorMat);
    doorMesh.position.set(0, 0.2 + 2.1 / 2, frontWallZ + 0.12);
    doorMesh.castShadow = true;
    houseGroup.add(doorMesh);

    // Raised Stone Door Sill (石门槛)
    const sillGeo = new THREE.BoxGeometry(1.35, 0.12, 0.25);
    const sillMat = new THREE.MeshStandardMaterial({ color: 0x6e6a64, roughness: 0.9 });
    const doorSill = new THREE.Mesh(sillGeo, sillMat);
    doorSill.position.set(0, 0.2 + 0.06, frontWallZ + 0.15);
    doorSill.castShadow = true;
    houseGroup.add(doorSill);

    // Windows with Painted White Plaster Frame (东西次间白灰包边木窗)
    function createWindow(xPos) {
        const winGroup = new THREE.Group();
        winGroup.position.set(xPos, 0.2 + 1.45, frontWallZ + 0.18);

        // White plaster surround
        const borderGeo = new THREE.BoxGeometry(1.25, 1.35, 0.08);
        const borderMat = new THREE.MeshStandardMaterial({ color: 0xefedea, roughness: 0.85 });
        const borderMesh = new THREE.Mesh(borderGeo, borderMat);
        winGroup.add(borderMesh);

        // Dark window frame and recessed opening
        const innerGeo = new THREE.BoxGeometry(0.85, 0.95, 0.14);
        const innerMat = new THREE.MeshStandardMaterial({ color: 0x181716, roughness: 0.8 });
        const innerMesh = new THREE.Mesh(innerGeo, innerMat);
        innerMesh.position.z = 0.02;
        winGroup.add(innerMesh);

        // Wooden cross muntins
        const muntinMat = new THREE.MeshStandardMaterial({ color: 0x2b221a, roughness: 0.7 });
        const vertBar = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.95, 0.16), muntinMat);
        const horizBar = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.04, 0.16), muntinMat);
        winGroup.add(vertBar);
        winGroup.add(horizBar);

        return winGroup;
    }
    const westWindow = createWindow(-3.4);
    const eastWindow = createWindow(3.4);
    houseGroup.add(westWindow);
    houseGroup.add(eastWindow);

    // West Bay Roof Tile Stack (西次间窗下规整堆叠的青瓦垛)
    const tileStackGroup = new THREE.Group();
    tileStackGroup.position.set(-3.4, 0.2, frontWallZ + 0.45);
    const tileStackMat = new THREE.MeshStandardMaterial({
        color: 0x484b50,
        roughness: 0.85,
        bumpMap: tileTex,
        bumpScale: 0.05
    });

    // 4 neatly stacked tiers of curved roof tiles
    for (let row = 0; row < 4; row++) {
        for (let col = 0; col < 6; col++) {
            const tileBlock = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.18, 0.42), tileStackMat);
            tileBlock.position.set(-0.75 + col * 0.3, 0.09 + row * 0.18, 0);
            tileBlock.castShadow = true;
            tileBlock.receiveShadow = true;
            tileStackGroup.add(tileBlock);
        }
    }
    houseGroup.add(tileStackGroup);

    // East Bay Wooden Ladder (东次间斜靠在檐梁上的老木梯)
    const ladderGroup = new THREE.Group();
    ladderGroup.position.set(3.8, 0.2, frontWallZ + 0.9);
    ladderGroup.rotation.x = -0.32; // leaning against eave beam
    ladderGroup.rotation.y = 0.08;

    const railGeo = new THREE.BoxGeometry(0.07, 3.1, 0.09);
    const leftRail = new THREE.Mesh(railGeo, woodMat);
    leftRail.position.set(-0.25, 1.5, 0);
    leftRail.castShadow = true;
    ladderGroup.add(leftRail);

    const rightRail = new THREE.Mesh(railGeo, woodMat);
    rightRail.position.set(0.25, 1.5, 0);
    rightRail.castShadow = true;
    ladderGroup.add(rightRail);

    // 8 rungs
    for (let r = 0; r < 8; r++) {
        const rung = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.5, 8), woodMat);
        rung.rotation.z = Math.PI / 2;
        rung.position.set(0, 0.35 + r * 0.36, 0);
        rung.castShadow = true;
        ladderGroup.add(rung);
    }
    houseGroup.add(ladderGroup);

    // Rustic Wooden Bench under East Window (木凳)
    const benchGroup = new THREE.Group();
    benchGroup.position.set(2.8, 0.2, frontWallZ + 0.45);
    const benchTop = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.06, 0.3), woodMat);
    benchTop.position.y = 0.45;
    benchTop.castShadow = true;
    benchGroup.add(benchTop);
    for (let lx of [-0.55, 0.55]) {
        for (let lz of [-0.1, 0.1]) {
            const leg = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.45, 0.06), woodMat);
            leg.position.set(lx, 0.225, lz);
            leg.castShadow = true;
            benchGroup.add(leg);
        }
    }
    houseGroup.add(benchGroup);

    // 4 Front Veranda Pillars (前廊水泥空心砌块柱与红砖基座)
    const pillarPositionsX = [-4.8, -1.6, 1.6, 4.8];
    const pillarZ = -2.5 + H_DEPTH / 2 + PORCH_DEPTH - 0.15;

    pillarPositionsX.forEach(px => {
        // Red brick base (双层红砖底座)
        const baseMesh = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.16, 0.46), brickMat);
        baseMesh.position.set(px, 0.2 + 0.08, pillarZ);
        baseMesh.castShadow = true;
        baseMesh.receiveShadow = true;
        houseGroup.add(baseMesh);

        // Concrete cinder block column shaft (11 tiers of stacked blocks)
        const shaftMesh = new THREE.Mesh(new THREE.BoxGeometry(0.36, 2.35, 0.36), pillarMat);
        shaftMesh.position.set(px, 0.2 + 0.16 + 2.35 / 2, pillarZ);
        shaftMesh.castShadow = true;
        shaftMesh.receiveShadow = true;
        houseGroup.add(shaftMesh);
    });

    // Longitudinal Wooden Lintel Beam (贯通大木枋)
    const beamGeo = new THREE.BoxGeometry(H_WIDTH + 0.6, 0.22, 0.28);
    const eaveBeam = new THREE.Mesh(beamGeo, woodMat);
    eaveBeam.position.set(0, 0.2 + 2.58, pillarZ);
    eaveBeam.castShadow = true;
    houseGroup.add(eaveBeam);

    // Transverse Tie Beams (穿插枋)
    pillarPositionsX.forEach(px => {
        const tieBeam = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.2, PORCH_DEPTH + 0.2), woodMat);
        tieBeam.position.set(px, 0.2 + 2.55, (frontWallZ + pillarZ) / 2);
        tieBeam.castShadow = true;
        houseGroup.add(tieBeam);
    });

    // Exposed Eave Rafter Tails (檐口椽木序列)
    const numRafters = 40;
    const rafterSpacing = (H_WIDTH + 0.6) / numRafters;
    for (let i = 0; i <= numRafters; i++) {
        const rx = -H_WIDTH / 2 - 0.3 + i * rafterSpacing;
        const rafter = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.08, 0.6), woodMat);
        rafter.rotation.x = 0.32;
        rafter.position.set(rx, 0.2 + 2.72, pillarZ + 0.15);
        rafter.castShadow = true;
        houseGroup.add(rafter);
    }

    // Double-Pitched Roof (硬山双坡青瓦屋顶)
    // Front Roof Slope (南坡)
    const roofHalfDepth = (H_DEPTH / 2 + PORCH_DEPTH) / Math.cos(0.35);
    const frontRoofGeo = new THREE.PlaneGeometry(H_WIDTH + 1.0, roofHalfDepth + 0.4, 24, 12);
    const frontRoof = new THREE.Mesh(frontRoofGeo, roofTileMat);
    frontRoof.rotation.x = -Math.PI / 2 + 0.35;
    frontRoof.position.set(0, 0.2 + (H_EAVES_H + H_RIDGE_H) / 2 + 0.08, -2.5 + (PORCH_DEPTH - 0.1) / 2);
    frontRoof.castShadow = true;
    frontRoof.receiveShadow = true;
    houseGroup.add(frontRoof);

    // Rear Roof Slope (北坡)
    const rearRoofGeo = new THREE.PlaneGeometry(H_WIDTH + 1.0, (H_DEPTH / 2) / Math.cos(0.35) + 0.4, 24, 12);
    const rearRoof = new THREE.Mesh(rearRoofGeo, roofTileMat);
    rearRoof.rotation.x = -Math.PI / 2 - 0.35;
    rearRoof.position.set(0, 0.2 + (H_EAVES_H + H_RIDGE_H) / 2 + 0.12, -2.5 - H_DEPTH / 4);
    rearRoof.castShadow = true;
    rearRoof.receiveShadow = true;
    houseGroup.add(rearRoof);

    // Roof Ridge with Whitewashed Mortar Cresting & Ornamental Finials (白灰正脊与起翘脊头)
    const ridgeGeo = new THREE.BoxGeometry(H_WIDTH + 1.1, 0.22, 0.35);
    const ridgeMat = new THREE.MeshStandardMaterial({ color: 0xdfdad2, roughness: 0.8 });
    const ridgeMesh = new THREE.Mesh(ridgeGeo, ridgeMat);
    ridgeMesh.position.set(0, 0.2 + H_RIDGE_H + 0.1, -2.5);
    ridgeMesh.castShadow = true;
    houseGroup.add(ridgeMesh);

    // Upturned Finials at East and West Ends (正脊两端翘角)
    for (let endX of [-H_WIDTH / 2 - 0.55, H_WIDTH / 2 + 0.55]) {
        const finial = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.45, 4), ridgeMat);
        finial.position.set(endX, 0.2 + H_RIDGE_H + 0.28, -2.5);
        finial.rotation.z = endX < 0 ? 0.4 : -0.4;
        houseGroup.add(finial);
    }

    // --- 2. East Wing Outbuilding (东厢房 / 倒座房) Modeling ---
    const wingGroup = new THREE.Group();
    wingGroup.position.set(6.4, 0, 1.8);
    scene.add(wingGroup);

    const W_W = 3.6;
    const W_L = 6.4;
    const W_EH = 2.45;
    const W_RH = 3.45;

    // Wing Adobe Walls
    // North Wall
    const wingNorthWall = new THREE.Mesh(new THREE.BoxGeometry(W_W, W_EH, 0.4), earthMat);
    wingNorthWall.position.set(0, 0.2 + W_EH / 2, -W_L / 2);
    wingGroup.add(wingNorthWall);

    // East Back Wall
    const wingEastWall = new THREE.Mesh(new THREE.BoxGeometry(0.4, W_EH, W_L), earthMat);
    wingEastWall.position.set(W_W / 2 - 0.2, 0.2 + W_EH / 2, 0);
    wingGroup.add(wingEastWall);

    // West Front Wall (Facing Courtyard) with Door, Barred Window & Broken Breach
    const wingFrontNorth = new THREE.Mesh(new THREE.BoxGeometry(0.4, W_EH, 2.2), earthMat);
    wingFrontNorth.position.set(-W_W / 2 + 0.2, 0.2 + W_EH / 2, -W_L / 2 + 1.1);
    wingGroup.add(wingFrontNorth);

    // Wing Wooden Door
    const wingDoor = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.9, 0.95), doorMat);
    wingDoor.position.set(-W_W / 2 + 0.2, 0.2 + 0.95, -W_L / 2 + 1.1);
    wingDoor.castShadow = true;
    wingGroup.add(wingDoor);

    // Window with Vertical Security Bars (直棂木栏窗)
    const barredWinGroup = new THREE.Group();
    barredWinGroup.position.set(-W_W / 2 + 0.2, 0.2 + 1.35, 0.5);
    const winHole = new THREE.Mesh(new THREE.BoxGeometry(0.35, 1.0, 1.1), new THREE.MeshStandardMaterial({ color: 0x111, roughness: 0.9 }));
    barredWinGroup.add(winHole);
    // Vertical wooden bars
    for (let b = -4; b <= 4; b++) {
        const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 0.98, 8), woodMat);
        bar.position.set(0.12, 0, b * 0.11);
        barredWinGroup.add(bar);
    }
    wingGroup.add(barredWinGroup);

    // Partially Collapsed Corner Breach (残破豁口 - 对应视频70s/90s特写)
    const brokenChunk = new THREE.Mesh(new THREE.DodecahedronGeometry(0.7, 1), earthMat);
    brokenChunk.position.set(-W_W / 2 + 0.2, 0.2 + 0.6, 2.2);
    brokenChunk.scale.set(0.6, 1.2, 0.8);
    wingGroup.add(brokenChunk);

    // Wing Roof
    const wingRoofW = new THREE.Mesh(new THREE.PlaneGeometry(W_L + 0.6, (W_W / 2) / Math.cos(0.3) + 0.3), roofTileMat);
    wingRoofW.rotation.y = -Math.PI / 2;
    wingRoofW.rotation.x = -Math.PI / 2 + 0.3;
    wingRoofW.position.set(-W_W / 4, 0.2 + (W_EH + W_RH) / 2, 0);
    wingGroup.add(wingRoofW);

    const wingRoofE = new THREE.Mesh(new THREE.PlaneGeometry(W_L + 0.6, (W_W / 2) / Math.cos(0.3) + 0.3), roofTileMat);
    wingRoofE.rotation.y = -Math.PI / 2;
    wingRoofE.rotation.x = -Math.PI / 2 - 0.3;
    wingRoofE.position.set(W_W / 4, 0.2 + (W_EH + W_RH) / 2, 0);
    wingGroup.add(wingRoofE);

    // --- 3. Connecting Gatehouse / Back Wall (后院连接门楼 - 见视频320s) ---
    const gateWall = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.4, 0.35), earthMat);
    gateWall.position.set(5.5, 0.2 + 1.2, -2.5);
    scene.add(gateWall);

    const smallGateDoor = new THREE.Mesh(new THREE.BoxGeometry(0.85, 1.75, 0.08), doorMat);
    smallGateDoor.position.set(5.5, 0.2 + 0.88, -2.5);
    scene.add(smallGateDoor);

    const gateRoof = new THREE.Mesh(new THREE.ConeGeometry(1.2, 0.5, 4), roofTileMat);
    gateRoof.position.set(5.5, 0.2 + 2.55, -2.5);
    gateRoof.rotation.y = Math.PI / 4;
    scene.add(gateRoof);

    // --- 4. Perimeter Dry Stone Retaining Wall & Entrance (干砌块石护坡围墙与大石门墩) ---
    const stoneWallGroup = new THREE.Group();
    scene.add(stoneWallGroup);

    // Front Courtyard Retaining Wall (南侧护坡石墙)
    const frontWallPoints = [
        new THREE.Vector3(-12, 0, 10),
        new THREE.Vector3(-7, 0, 9.5),
        new THREE.Vector3(-5, 0, 8.5),
        new THREE.Vector3(-4.5, 0, 6.8),
        new THREE.Vector3(2.5, 0, 7.2),
        new THREE.Vector3(7.5, 0, 7.0)
    ];

    for (let p = 0; p < frontWallPoints.length - 1; p++) {
        // Skip entry gap
        if (p === 2) continue;

        const p1 = frontWallPoints[p];
        const p2 = frontWallPoints[p+1];
        const segLen = p1.distanceTo(p2);
        const wallH = 1.35;
        const wallSeg = new THREE.Mesh(new THREE.BoxGeometry(segLen, wallH, 0.55), stoneWallMat);
        const mid = p1.clone().add(p2).multiplyScalar(0.5);
        wallSeg.position.set(mid.x, wallH / 2, mid.z);
        wallSeg.rotation.y = Math.atan2(p2.x - p1.x, p2.z - p1.z) - Math.PI / 2;
        wallSeg.castShadow = true;
        wallSeg.receiveShadow = true;
        stoneWallGroup.add(wallSeg);
    }

    // Large Stacked Boulders at Entrance Pier (入口处巨石门墩 - 见视频20s/50s)
    const pierBoulderMat = new THREE.MeshStandardMaterial({ color: 0x6e685f, roughness: 0.95 });
    for (let b = 0; b < 4; b++) {
        const boulder = new THREE.Mesh(new THREE.DodecahedronGeometry(0.48 + Math.random() * 0.25, 1), pierBoulderMat);
        boulder.scale.set(1.1, 0.8, 1.2);
        boulder.position.set(-4.6 + (Math.random() - 0.5) * 0.3, 0.3 + b * 0.45, 7.2 + (Math.random() - 0.5) * 0.3);
        boulder.castShadow = true;
        stoneWallGroup.add(boulder);
    }

    // --- 5. Haystacks & Brushwood Bundles on Hillside (后山干柴垛与草堆 - 见视频320s) ---
    const haystackMat = new THREE.MeshStandardMaterial({ color: 0x8a6a3b, roughness: 0.95 });
    function createHaystack(x, z, r, h) {
        const stackGeo = new THREE.CylinderGeometry(r * 0.7, r, h, 14);
        const stackMesh = new THREE.Mesh(stackGeo, haystackMat);
        stackMesh.position.set(x, 1.5 + h / 2, z);
        stackMesh.castShadow = true;
        scene.add(stackMesh);

        const capGeo = new THREE.ConeGeometry(r * 0.85, h * 0.6, 14);
        const capMesh = new THREE.Mesh(capGeo, haystackMat);
        capMesh.position.set(x, 1.5 + h + h * 0.3, z);
        capMesh.castShadow = true;
        scene.add(capMesh);
    }
    createHaystack(1.8, -7.5, 1.2, 1.1);
    createHaystack(-1.5, -8.2, 1.5, 1.3);

    // --- 6. Vegetation & Trees System (高精度树木群) ---
    const treeGroup = new THREE.Group();
    scene.add(treeGroup);

    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x483e35, roughness: 0.9 });
    const cypressMat = new THREE.MeshStandardMaterial({ color: 0x1f3824, roughness: 0.85 });
    const blossomMat = new THREE.MeshStandardMaterial({ color: 0xebb8c6, roughness: 0.75 });

    // Procedural Bare Spring Tree (高大杨树/杂木 - 枯枝细密)
    function createBareTree(x, z, height, branchLevels) {
        const group = new THREE.Group();
        group.position.set(x, 0, z);

        // Main trunk
        const trunkGeo = new THREE.CylinderGeometry(0.18, 0.35, height * 0.5, 8);
        const trunk = new THREE.Mesh(trunkGeo, trunkMat);
        trunk.position.y = height * 0.25;
        trunk.castShadow = true;
        group.add(trunk);

        // Recursive branches
        function addBranches(startX, startY, startZ, len, thick, level) {
            if (level <= 0) return;
            const numB = 2 + Math.floor(Math.random() * 3);
            for (let b = 0; b < numB; b++) {
                const angleY = (b / numB) * Math.PI * 2 + (Math.random() - 0.5);
                const angleTilt = 0.35 + Math.random() * 0.5;
                const bLen = len * (0.65 + Math.random() * 0.25);

                const bGeo = new THREE.CylinderGeometry(thick * 0.6, thick, bLen, 6);
                const branch = new THREE.Mesh(bGeo, trunkMat);
                branch.position.set(startX, startY + bLen * 0.45 * Math.cos(angleTilt), startZ);
                branch.rotation.y = angleY;
                branch.rotation.z = angleTilt;
                branch.castShadow = true;
                group.add(branch);

                const tipX = startX + Math.sin(angleTilt) * Math.sin(angleY) * bLen;
                const tipY = startY + Math.cos(angleTilt) * bLen;
                const tipZ = startZ + Math.sin(angleTilt) * Math.cos(angleY) * bLen;

                addBranches(tipX, tipY, tipZ, bLen * 0.7, thick * 0.65, level - 1);
            }
        }
        addBranches(0, height * 0.48, 0, height * 0.45, 0.16, branchLevels);
        return group;
    }

    // Procedural Coniferous Cypress Tree (高耸尖塔状翠柏)
    function createCypressTree(x, z, height) {
        const group = new THREE.Group();
        group.position.set(x, 0, z);

        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.25, height * 0.3, 8), trunkMat);
        trunk.position.y = height * 0.15;
        group.add(trunk);

        // Tiered slender cones
        const tiers = 5;
        for (let t = 0; t < tiers; t++) {
            const coneH = height * 0.32;
            const coneR = 0.85 * (1 - t / tiers * 0.65);
            const cone = new THREE.Mesh(new THREE.ConeGeometry(coneR, coneH, 10), cypressMat);
            cone.position.y = height * 0.25 + t * (height * 0.15);
            cone.castShadow = true;
            group.add(cone);
        }
        return group;
    }

    // Procedural Flowering Peach Tree (盛开山桃花 - 见视频480s)
    function createPeachBlossomTree(x, z, height) {
        const group = new THREE.Group();
        group.position.set(x, 1.2, z);

        const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.22, height * 0.45, 8), trunkMat);
        trunk.position.y = height * 0.22;
        group.add(trunk);

        // Blossom clusters
        for (let k = 0; k < 35; k++) {
            const bx = (Math.random() - 0.5) * 2.8;
            const by = height * 0.4 + Math.random() * (height * 0.55);
            const bz = (Math.random() - 0.5) * 2.8;
            const cluster = new THREE.Mesh(new THREE.DodecahedronGeometry(0.35 + Math.random() * 0.25, 1), blossomMat);
            cluster.position.set(bx, by, bz);
            cluster.castShadow = true;
            group.add(cluster);
        }
        return group;
    }

    // Populate Trees matching the actual video layout!
    // Behind Main House (North Side): tall poplars & evergreen cypresses
    treeGroup.add(createBareTree(-4.2, -6.5, 11, 3));
    treeGroup.add(createBareTree(0.5, -7.2, 13, 3));
    treeGroup.add(createBareTree(4.6, -6.8, 10.5, 3));
    treeGroup.add(createCypressTree(-2.2, -6.0, 7.5));
    treeGroup.add(createCypressTree(2.4, -6.2, 8.2));
    treeGroup.add(createCypressTree(6.2, -5.8, 7.0));

    // Hillside terrace: Spring Blossom Tree
    treeGroup.add(createPeachBlossomTree(9.5, -4.5, 4.2));

    // South approach grove
    treeGroup.add(createBareTree(-7.5, 11.0, 9.5, 2));
    treeGroup.add(createCypressTree(-8.8, 9.2, 6.8));

    // Courtyard perimeter bushes
    const bushMat = new THREE.MeshStandardMaterial({ color: 0x556038, roughness: 0.9 });
    for (let b = 0; b < 24; b++) {
        const bush = new THREE.Mesh(new THREE.DodecahedronGeometry(0.4 + Math.random() * 0.35, 1), bushMat);
        bush.scale.set(1.2, 0.7, 1.2);
        const bx = -10 + Math.random() * 20;
        const bz = 4 + Math.random() * 6;
        bush.position.set(bx, 0.25, bz);
        bush.castShadow = true;
        scene.add(bush);
    }

    // --- Interactive 3D Hotspot Pins ---
    const hotspots = [
        {
            id: "door",
            name: "堂屋大门与春联",
            pos: new THREE.Vector3(0, 1.4, -2.5 + H_DEPTH/2 + 0.3),
            view: "door",
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋对开门与拱门白灰套",
            body: "深色老杉木竖向拼板门，表面贴有泛白退色的春联横批、两侧门联与门扇中央两张菱形斗方/门神。外围为具有地方特色的拱券形白石灰抹灰套，呈现真实的自然剥落露土肌理。"
        },
        {
            id: "west_stack",
            name: "西间整齐瓦堆",
            pos: new THREE.Vector3(-3.4, 0.8, -2.5 + H_DEPTH/2 + 0.7),
            view: "west",
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "西次间窗下堆叠青瓦",
            body: "西次间泥墙窗台下整齐码放着数百片传统灰青色弧形屋瓦，垛高约0.8米，呈规整排列。上方为白石灰饰边方形木窗，内含深色木质窗框。"
        },
        {
            id: "east_ladder",
            name: "东间靠墙木梯",
            pos: new THREE.Vector3(3.8, 1.6, -2.5 + H_DEPTH/2 + 0.9),
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
            pos: new THREE.Vector3(6.4 - W_W/2, 1.2, 3.8),
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
            pos: new THREE.Vector3(0, H_RIDGE_H + 0.6, -2.5),
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
            // Check if in front of camera
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

    // --- Camera Viewpoint Definitions ---
    const viewpoints = {
        facade: {
            pos: new THREE.Vector3(0, 1.8, 9.5),
            target: new THREE.Vector3(0, 2.2, -1.8),
            refImg: "ref_images/ref_060s_main_facade.jpg",
            refTag: "M2U00577.MPG · 01:00",
            title: "正房正立面构型 (01:00)",
            body: "三开间硬山顶夯土正房立面，4根水泥空心砌块柱清晰可见，西侧摆放整齐瓦堆，东侧靠有杉木梯子，右侧连接东厢房。"
        },
        door: {
            pos: new THREE.Vector3(0, 1.5, 1.5),
            target: new THREE.Vector3(0, 1.5, -2.5 + H_DEPTH/2),
            refImg: "ref_images/ref_180s_door_close.jpg",
            refTag: "M2U00577.MPG · 03:00",
            title: "堂屋大门特写 (03:00)",
            body: "双扇木板门、泛黄褪色春联纸符、拱形石灰白边抹灰门套与门前条石门槛特写。"
        },
        west: {
            pos: new THREE.Vector3(-3.4, 1.4, 2.2),
            target: new THREE.Vector3(-3.4, 1.3, -2.5 + H_DEPTH/2),
            refImg: "ref_images/ref_150s_tiles_stack.jpg",
            refTag: "M2U00577.MPG · 02:30",
            title: "西次间瓦堆与白框木窗 (02:30)",
            body: "紧靠黄土墙脚下堆码的大量青瓦片，与上方带白石灰饰边的木窗构成鲜明而朴实的生活生产印记。"
        },
        east: {
            pos: new THREE.Vector3(3.8, 1.6, 2.6),
            target: new THREE.Vector3(3.8, 1.8, -2.5 + H_DEPTH/2),
            refImg: "ref_images/ref_190s_ladder_wall.jpg",
            refTag: "M2U00577.MPG · 03:10",
            title: "东次间靠墙木梯 (03:10)",
            body: "木质长梯搭靠在廊枋处，梯底摆放长木凳，右侧近景为东厢房山墙夹道。"
        },
        wing: {
            pos: new THREE.Vector3(2.5, 1.6, 2.8),
            target: new THREE.Vector3(6.4, 1.6, 2.8),
            refImg: "ref_images/ref_070s_east_wing.jpg",
            refTag: "M2U00577.MPG · 01:10",
            title: "东厢房侧立面与破口 (01:10)",
            body: "展示东厢房土坯墙体、木板小门、直棂木栅窗以及西南角大面积残损塌落的断口细节。"
        },
        aerial: {
            pos: new THREE.Vector3(-1.0, 10.5, -15.5),
            target: new THREE.Vector3(1.5, 2.5, 0),
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
    }

    function updateDrawer(info) {
        document.getElementById('ref-img').src = info.refImg;
        document.getElementById('ref-tag').textContent = info.refTag;
        document.getElementById('drawer-title').textContent = info.name || info.title;
        document.getElementById('detail-card-title').textContent = info.title;
        document.getElementById('detail-card-body').innerHTML = `<p>${info.body}</p>`;
    }

    // Set initial camera
    camera.position.copy(viewpoints.facade.pos);
    controls.target.copy(viewpoints.facade.target);
    controls.update();

    // --- UI Event Listeners ---
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            switchView(btn.dataset.view);
        });
    });

    const drawer = document.getElementById('comparison-drawer');
    document.getElementById('btn-toggle-drawer').addEventListener('click', () => {
        drawer.classList.toggle('collapsed');
    });
    document.getElementById('close-drawer-btn').addEventListener('click', () => {
        drawer.classList.add('collapsed');
    });

    // Lighting Presets
    const lightModes = [
        { name: "晴朗正午", sunPos: [-25, 45, 30], sunColor: 0xfffaed, sunInt: 1.8, hemiSky: 0xfff5e6, bg: 0xbddaf0 },
        { name: "清晨柔光", sunPos: [-45, 18, 20], sunColor: 0xffe2b8, sunInt: 1.4, hemiSky: 0xd9e5f5, bg: 0xa9cce8 },
        { name: "金色黄昏", sunPos: [-45, 12, 10], sunColor: 0xff9944, sunInt: 1.9, hemiSky: 0xf5ccaa, bg: 0xd99566 },
        { name: "阴天漫射", sunPos: [0, 50, 0], sunColor: 0xdbe0e5, sunInt: 1.0, hemiSky: 0xcfd5db, bg: 0xc2ccd4 }
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

    // First Person Walkthrough Mode (WASD + Mouse)
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
            // Eye level height
            camera.position.y = 1.68;
        } else {
            btnToggleWalk.classList.remove('active');
            modeLabel.textContent = "漫游漫步视角";
            crosshair.style.display = 'none';
            controls.enabled = true;
            controls.target.set(0, 1.8, 0);
        }
    });

    // Keyboard state
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

    // Walk mode mouse look
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

    // --- Main Render & Animation Loop ---
    const clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);
        const dt = clock.getDelta();

        // Smooth camera transition between viewpoints
        if (isTransitioning) {
            camera.position.lerp(targetCamPos, 0.06);
            controls.target.lerp(targetLookAt, 0.06);
            controls.update();
            if (camera.position.distanceTo(targetCamPos) < 0.05) {
                isTransitioning = false;
            }
        } else if (controls.enabled) {
            controls.update();
        }

        // Walk Mode update
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

            // Ground height clamping
            let groundH = 0;
            if (camera.position.z < -3) {
                groundH = Math.pow(Math.abs(camera.position.z + 3) * 0.18, 1.3);
            }
            camera.position.y = groundH + 1.68;
        }

        updateHotspotsScreenPosition();
        renderer.render(scene, camera);
    }
    animate();

    // Window Resize Handler
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
    f.write(html_content)

print("Successfully written index.html! File size:", len(html_content), "bytes")
