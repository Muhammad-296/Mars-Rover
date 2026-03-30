<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Mars Rover Mission Control — README</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap" rel="stylesheet"/>
<style>
  :root {
    --cyan: #00e6ff;
    --green: #00ff91;
    --amber: #ffb900;
    --red: #ff2d37;
    --violet: #b450ff;
    --bg: #020a14;
    --bg2: #040f1e;
    --bg3: #071828;
    --glass: rgba(0,230,255,0.04);
    --border: rgba(0,230,255,0.15);
    --text: #c8e8f8;
    --dim: #6a8fa8;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* ── starfield ── */
  #stars {
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
      radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,.5) 0%, transparent 100%),
      radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,.4) 0%, transparent 100%),
      radial-gradient(1px 1px at 55% 15%, rgba(255,255,255,.6) 0%, transparent 100%),
      radial-gradient(1px 1px at 75% 40%, rgba(255,255,255,.3) 0%, transparent 100%),
      radial-gradient(1px 1px at 90% 75%, rgba(255,255,255,.5) 0%, transparent 100%),
      radial-gradient(1px 1px at 20% 85%, rgba(255,255,255,.4) 0%, transparent 100%),
      radial-gradient(1px 1px at 65% 90%, rgba(255,255,255,.3) 0%, transparent 100%),
      radial-gradient(1px 1px at 45% 50%, rgba(255,255,255,.5) 0%, transparent 100%),
      radial-gradient(1px 1px at 80% 10%, rgba(255,255,255,.6) 0%, transparent 100%);
  }

  .wrap { max-width: 960px; margin: 0 auto; padding: 0 24px; position: relative; z-index: 1; }

  /* ── HERO ── */
  .hero {
    text-align: center;
    padding: 80px 24px 60px;
    position: relative;
  }
  .hero::before {
    content:'';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 700px;
    background: radial-gradient(ellipse, rgba(0,230,255,0.07) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 4px;
    color: var(--cyan);
    text-transform: uppercase;
    animation: fadeUp 0.8s ease both;
  }

  .hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(28px, 5vw, 56px);
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 40px rgba(0,230,255,0.5), 0 0 80px rgba(0,230,255,0.2);
    letter-spacing: 3px;
    line-height: 1.1;
    margin: 16px 0 8px;
    animation: fadeUp 0.8s 0.1s ease both;
  }
  .hero-title span { color: var(--cyan); }

  .hero-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 14px;
    color: var(--amber);
    letter-spacing: 2px;
    margin-bottom: 32px;
    animation: fadeUp 0.8s 0.2s ease both;
  }

  .badges {
    display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
    margin-bottom: 32px;
    animation: fadeUp 0.8s 0.3s ease both;
  }
  .badge {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 3px;
    letter-spacing: 1px;
    font-weight: 700;
    text-transform: uppercase;
    position: relative;
    overflow: hidden;
  }
  .badge::before {
    content:'';
    position:absolute; inset:0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    transform: translateX(-100%);
    animation: shimmer 3s infinite;
  }
  .badge-cyan   { background: rgba(0,230,255,0.1);  border:1px solid rgba(0,230,255,0.4);  color:var(--cyan);   }
  .badge-green  { background: rgba(0,255,145,0.1);  border:1px solid rgba(0,255,145,0.4);  color:var(--green);  }
  .badge-amber  { background: rgba(255,185,0,0.1);  border:1px solid rgba(255,185,0,0.4);  color:var(--amber);  }
  .badge-red    { background: rgba(255,45,55,0.1);  border:1px solid rgba(255,45,55,0.4);  color:var(--red);    }
  .badge-violet { background: rgba(180,80,255,0.1); border:1px solid rgba(180,80,255,0.4); color:var(--violet); }

  .hero-desc {
    max-width: 680px; margin: 0 auto;
    font-size: 17px; color: var(--text); line-height: 1.8;
    border-left: 3px solid var(--cyan);
    padding-left: 20px;
    text-align: left;
    animation: fadeUp 0.8s 0.4s ease both;
  }

  /* ── DIVIDER ── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--violet), transparent);
    margin: 48px 0;
    position: relative;
    animation: pulse-line 3s ease-in-out infinite;
  }

  /* ── SECTION ── */
  section { margin-bottom: 56px; }

  .section-head {
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 28px;
    animation: fadeUp 0.7s ease both;
  }
  .section-icon {
    width: 44px; height: 44px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }
  .icon-cyan   { background: rgba(0,230,255,0.12); border:1px solid rgba(0,230,255,0.3); }
  .icon-green  { background: rgba(0,255,145,0.12); border:1px solid rgba(0,255,145,0.3); }
  .icon-amber  { background: rgba(255,185,0,0.12); border:1px solid rgba(255,185,0,0.3); }
  .icon-violet { background: rgba(180,80,255,0.12);border:1px solid rgba(180,80,255,0.3);}
  .icon-red    { background: rgba(255,45,55,0.12); border:1px solid rgba(255,45,55,0.3); }

  .section-title {
    font-family: 'Orbitron', monospace;
    font-size: 20px; font-weight: 700;
    letter-spacing: 2px; color: #fff;
  }
  .section-title .accent-cyan   { color: var(--cyan); }
  .section-title .accent-green  { color: var(--green); }
  .section-title .accent-amber  { color: var(--amber); }
  .section-title .accent-violet { color: var(--violet); }
  .section-title .accent-red    { color: var(--red); }

  /* ── CARDS GRID ── */
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }
  .card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
    animation: fadeUp 0.6s ease both;
  }
  .card:hover {
    transform: translateY(-3px);
    border-color: var(--cyan);
    box-shadow: 0 8px 32px rgba(0,230,255,0.12);
  }
  .card::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    opacity:0; transition: opacity 0.3s;
  }
  .card:hover::before { opacity:1; }

  .card-title {
    font-family: 'Orbitron', monospace;
    font-size: 13px; font-weight: 700;
    color: var(--cyan); letter-spacing: 1px;
    margin-bottom: 8px;
    display: flex; align-items: center; gap: 8px;
  }
  .card-body { font-size: 15px; color: var(--text); }

  /* ── TABLE ── */
  .tbl-wrap { overflow-x: auto; border-radius: 8px; border: 1px solid var(--border); }
  table { width: 100%; border-collapse: collapse; }
  thead tr {
    background: linear-gradient(90deg, rgba(0,230,255,0.1), rgba(180,80,255,0.1));
  }
  th {
    font-family: 'Orbitron', monospace;
    font-size: 11px; letter-spacing: 2px;
    color: var(--cyan); text-align: left;
    padding: 12px 18px;
    border-bottom: 1px solid var(--border);
  }
  td {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px; color: var(--text);
    padding: 11px 18px;
    border-bottom: 1px solid rgba(0,230,255,0.06);
    vertical-align: top;
  }
  tr:last-child td { border-bottom: none; }
  tbody tr { transition: background 0.2s; }
  tbody tr:hover { background: rgba(0,230,255,0.04); }

  .pill {
    display: inline-block;
    padding: 2px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 700;
    font-family: 'Share Tech Mono', monospace;
  }
  .pill-cyan   { background:rgba(0,230,255,0.15);  color:var(--cyan); }
  .pill-green  { background:rgba(0,255,145,0.15);  color:var(--green); }
  .pill-amber  { background:rgba(255,185,0,0.15);  color:var(--amber); }
  .pill-violet { background:rgba(180,80,255,0.15); color:var(--violet); }
  .pill-red    { background:rgba(255,45,55,0.15);  color:var(--red); }

  /* ── CODE BLOCK ── */
  .code-block {
    background: #010810;
    border: 1px solid rgba(0,230,255,0.2);
    border-radius: 8px;
    overflow: hidden;
  }
  .code-header {
    background: rgba(0,230,255,0.06);
    border-bottom: 1px solid rgba(0,230,255,0.15);
    padding: 8px 16px;
    display: flex; align-items: center; gap: 8px;
  }
  .dot { width:10px;height:10px;border-radius:50%; }
  .dot-r{background:#ff5f57;} .dot-y{background:#febc2e;} .dot-g{background:#28c840;}
  .code-label { font-family:'Share Tech Mono',monospace; font-size:11px; color:var(--dim); margin-left:auto; letter-spacing:1px; }
  pre {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    line-height: 1.7;
    padding: 20px;
    overflow-x: auto;
    color: #a8d8f0;
  }
  .kw  { color: var(--cyan); }
  .str { color: var(--green); }
  .cmt { color: var(--dim); }
  .num { color: var(--amber); }

  /* ── ARCH DIAGRAM ── */
  .arch-diagram {
    background: #010810;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 28px;
    overflow-x: auto;
  }
  .arch-row {
    display: flex; gap: 12px; justify-content: center;
    flex-wrap: wrap; margin-bottom: 10px;
  }
  .arch-box {
    border-radius: 6px;
    padding: 10px 18px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    text-align: center;
    white-space: nowrap;
    position: relative;
    transition: transform 0.2s;
  }
  .arch-box:hover { transform: scale(1.05); }
  .ab-cyan   { background:rgba(0,230,255,0.1);  border:1px solid rgba(0,230,255,0.4);  color:var(--cyan); }
  .ab-green  { background:rgba(0,255,145,0.1);  border:1px solid rgba(0,255,145,0.4);  color:var(--green);}
  .ab-amber  { background:rgba(255,185,0,0.1);  border:1px solid rgba(255,185,0,0.4);  color:var(--amber);}
  .ab-violet { background:rgba(180,80,255,0.1); border:1px solid rgba(180,80,255,0.4); color:var(--violet);}
  .ab-red    { background:rgba(255,45,55,0.1);  border:1px solid rgba(255,45,55,0.4);  color:var(--red);  }
  .ab-label {
    font-family:'Orbitron',monospace; font-size:10px; font-weight:700;
    letter-spacing:1px; margin-bottom:8px; opacity:.7;
  }

  .arch-connector {
    text-align: center; color: var(--dim);
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px; margin: 4px 0;
    animation: blink 1.5s ease-in-out infinite;
  }
  .arch-layer-label {
    font-family: 'Orbitron', monospace;
    font-size: 10px; letter-spacing: 2px;
    text-align: center; margin-bottom: 14px;
  }
  .arch-sep {
    border: none;
    border-top: 1px dashed rgba(0,230,255,0.25);
    margin: 18px 0;
  }

  /* ── PROTOCOL TABLE ── */
  .dir-gui  { color: var(--cyan); }
  .dir-esp  { color: var(--amber); }

  /* ── KEY GRID ── */
  .key-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px,1fr));
    gap: 10px;
  }
  .key-row {
    display: flex; align-items: center; gap: 14px;
    background: var(--glass); border:1px solid var(--border);
    border-radius:6px; padding:10px 16px;
    transition: border-color 0.2s, background 0.2s;
  }
  .key-row:hover { border-color: var(--amber); background: rgba(255,185,0,0.04); }
  .key-chip {
    font-family:'Share Tech Mono',monospace;
    font-size:12px;
    background:rgba(255,185,0,0.15);
    border:1px solid rgba(255,185,0,0.4);
    color:var(--amber);
    padding:4px 10px; border-radius:4px;
    min-width:52px; text-align:center;
    flex-shrink:0;
  }
  .key-action { font-size:14px; color:var(--text); }

  /* ── SAFETY GRID ── */
  .safety-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px,1fr));
    gap: 14px;
  }
  .safety-card {
    border-radius:8px; padding:18px 20px;
    border-left: 3px solid;
    background: var(--glass);
  }
  .sc-red    { border-color:var(--red);   background:rgba(255,45,55,0.05); }
  .sc-amber  { border-color:var(--amber); background:rgba(255,185,0,0.05); }
  .sc-cyan   { border-color:var(--cyan);  background:rgba(0,230,255,0.05); }
  .sc-violet { border-color:var(--violet);background:rgba(180,80,255,0.05);}
  .safety-title {
    font-family:'Orbitron',monospace; font-size:12px; font-weight:700;
    letter-spacing:1px; margin-bottom:6px;
  }
  .safety-body { font-size:14px; color:var(--dim); }

  /* ── REPO TREE ── */
  .repo-tree {
    background:#010810;
    border:1px solid var(--border);
    border-radius:8px;
    padding:24px 28px;
    font-family:'Share Tech Mono',monospace;
    font-size:13px;
    line-height:2;
  }
  .rt-root  { color:var(--cyan); font-weight:700; }
  .rt-dir   { color:var(--green); }
  .rt-file  { color:var(--text); }
  .rt-img   { color:var(--amber); }
  .rt-comment { color:var(--dim); }
  .rt-branch { color: rgba(0,230,255,0.3); }

  /* ── FOOTER ── */
  footer {
    text-align: center;
    padding: 60px 24px 80px;
    position: relative;
  }
  footer::before {
    content:'';
    position:absolute; top:0; left:10%; right:10%; height:1px;
    background: linear-gradient(90deg, transparent, var(--violet), var(--cyan), var(--violet), transparent);
  }
  .footer-title {
    font-family:'Orbitron',monospace;
    font-size:18px; font-weight:700;
    color:#fff; letter-spacing:3px; margin-bottom:12px;
  }
  .footer-sub { font-size:15px; color:var(--dim); margin-bottom:24px; }
  .star-cta {
    display:inline-block;
    font-family:'Share Tech Mono',monospace;
    font-size:13px; letter-spacing:2px;
    color:var(--amber);
    border:1px solid rgba(255,185,0,0.4);
    padding:10px 28px; border-radius:4px;
    animation: pulse-amber 2s ease-in-out infinite;
  }

  /* ── ANIMATIONS ── */
  @keyframes fadeUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0);    }
  }
  @keyframes shimmer {
    0%   { transform:translateX(-100%); }
    60%  { transform:translateX(100%); }
    100% { transform:translateX(100%); }
  }
  @keyframes blink {
    0%,100% { opacity:.4; } 50% { opacity:1; }
  }
  @keyframes pulse-line {
    0%,100% { opacity:.4; } 50% { opacity:1; }
  }
  @keyframes pulse-amber {
    0%,100% { box-shadow:0 0 0 rgba(255,185,0,0); }
    50%      { box-shadow:0 0 16px rgba(255,185,0,0.3); }
  }
  @keyframes scan {
    0%   { top:-100%; } 100% { top:200%; }
  }
  .scan-line {
    position:fixed; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, rgba(0,230,255,0.15), transparent);
    animation: scan 6s linear infinite;
    pointer-events:none; z-index:100;
  }

  /* stagger children */
  .cards .card:nth-child(1)  { animation-delay:.05s }
  .cards .card:nth-child(2)  { animation-delay:.10s }
  .cards .card:nth-child(3)  { animation-delay:.15s }
  .cards .card:nth-child(4)  { animation-delay:.20s }
  .cards .card:nth-child(5)  { animation-delay:.25s }
  .cards .card:nth-child(6)  { animation-delay:.30s }
  .cards .card:nth-child(7)  { animation-delay:.35s }
  .cards .card:nth-child(8)  { animation-delay:.40s }
  .cards .card:nth-child(9)  { animation-delay:.45s }
  .cards .card:nth-child(10) { animation-delay:.50s }
  .cards .card:nth-child(11) { animation-delay:.55s }
  .cards .card:nth-child(12) { animation-delay:.60s }

  p { margin-bottom: 14px; }
  ul { padding-left: 24px; margin-bottom:14px; }
  li { margin-bottom: 6px; font-size:15px; }
</style>
</head>
<body>

<div id="stars"></div>
<div class="scan-line"></div>

<!-- ═══════════════ HERO ═══════════════ -->
<header class="hero">
  <div class="wrap">
    <div class="hero-tag">◈ Ground Control System · v5.1 Enhanced Edition ◈</div>
    <h1 class="hero-title">MARS<span> ROVER</span><br/>MISSION CONTROL</h1>
    <div class="hero-sub">ESP32 + PyQt5 · Real-Time Telemetry · Wi-Fi Command</div>

    <div class="badges">
      <span class="badge badge-cyan">🐍 Python 3.8+</span>
      <span class="badge badge-green">🖥 PyQt5 GUI</span>
      <span class="badge badge-amber">⚡ ESP32 WebSocket</span>
      <span class="badge badge-red">🔧 Arduino C++</span>
      <span class="badge badge-violet">📄 MIT License</span>
    </div>

    <p class="hero-desc">
      A full-featured, sci-fi styled real-time Mars Rover Mission Control interface.
      Control an ESP32-powered rover over Wi-Fi with live telemetry, obstacle detection,
      servo control, and animated OLED feedback — all from a slick PyQt5 desktop GUI.
    </p>
  </div>
</header>

<div class="wrap">

  <div class="divider"></div>

  <!-- ═══════════════ OVERVIEW ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-cyan">🛸</div>
      <h2 class="section-title"><span class="accent-cyan">PROJECT</span> OVERVIEW</h2>
    </div>
    <p>
      This project is a complete ground-control system for a 4-wheel ESP32 rover.
      The <strong style="color:var(--cyan)">Python PyQt5 GUI</strong> communicates with the
      <strong style="color:var(--amber)">ESP32 firmware</strong> over WebSocket (Wi-Fi), providing
      real-time sensor telemetry, keyboard-driven movement, camera pan and gripper servo control,
      live scrolling telemetry charts, proximity obstacle radar, dual OLED displays on the rover,
      and an animated boot sequence with a sci-fi HUD aesthetic.
    </p>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ FEATURES ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-green">✨</div>
      <h2 class="section-title"><span class="accent-green">FEATURE</span> SET</h2>
    </div>

    <h3 style="font-family:'Orbitron',monospace;font-size:14px;color:var(--cyan);letter-spacing:2px;margin-bottom:16px;">🖥 MISSION CONTROL GUI · PyQt5</h3>
    <div class="cards" style="margin-bottom:32px;">
      <div class="card"><div class="card-title">🎬 Animated Boot</div><div class="card-body">17-stage initialization animation with progress bar on startup.</div></div>
      <div class="card"><div class="card-title">🌐 Startup Config</div><div class="card-body">Enter your ESP32 WebSocket URL before launch via dialog.</div></div>
      <div class="card"><div class="card-title">📊 Live Charts</div><div class="card-body">Scrolling 80-sample history for Temp · Pressure · Altitude · Distance.</div></div>
      <div class="card"><div class="card-title">🎛 Arc Gauges</div><div class="card-body">Animated arc gauges for all 4 sensor channels.</div></div>
      <div class="card"><div class="card-title">🚨 Obstacle Radar</div><div class="card-body">Proximity radar with WARN @ 80 cm and CRITICAL @ 30 cm alerts.</div></div>
      <div class="card"><div class="card-title">📶 Ping Display</div><div class="card-body">Live ping bar chart with color-coded latency measurement.</div></div>
      <div class="card"><div class="card-title">🎮 D-Pad Visualizer</div><div class="card-body">On-screen directional pad showing active movement direction.</div></div>
      <div class="card"><div class="card-title">🤖 Rover Renderer</div><div class="card-body">Animated rover graphic with real-time wheel rotation.</div></div>
      <div class="card"><div class="card-title">⌨️ Keyboard Overlay</div><div class="card-body">Press <code style="color:var(--amber)">?</code> to toggle a semi-transparent shortcut reference.</div></div>
      <div class="card"><div class="card-title">🛑 Instant Stop</div><div class="card-body">Key-release triggers immediate motor stop command to rover.</div></div>
      <div class="card"><div class="card-title">🛡 Safety Watchdog</div><div class="card-body">Auto-stops rover after 3 s of no movement command received.</div></div>
      <div class="card"><div class="card-title">📋 Mission Log</div><div class="card-body">Timestamped scrolling event log with 50-line circular buffer.</div></div>
    </div>

    <h3 style="font-family:'Orbitron',monospace;font-size:14px;color:var(--amber);letter-spacing:2px;margin-bottom:16px;">🤖 ESP32 FIRMWARE · Arduino C++</h3>
    <div class="cards">
      <div class="card"><div class="card-title" style="color:var(--amber)">⚡ WebSocket Server</div><div class="card-body">Port 81 — receives commands, sends sensor data back to GUI.</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">🏎 L298N Control</div><div class="card-body">4-wheel drive via IN1–IN4 GPIO pins through H-bridge driver.</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">📷 Camera Pan Servo</div><div class="card-body">Smooth sweep on GPIO19 (0–180°, 10° incremental steps).</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">🦾 Gripper Servo</div><div class="card-body">Open/close on GPIO18 (10° closed / 90° open positions).</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">🌡 BMP280 Sensor</div><div class="card-body">Temperature · Pressure · Altitude over I²C bus.</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">📡 HC-SR04 Ultrasonic</div><div class="card-body">Distance measurement on GPIO17/16 (TRIG/ECHO).</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">🖥 Dual SSD1306 OLEDs</div><div class="card-body">Left: rover animation · Right: camera + live sensor data.</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">⏱ 500ms Watchdog</div><div class="card-body">Auto-stops motors if no command received (covers Wi-Fi drops).</div></div>
      <div class="card"><div class="card-title" style="color:var(--amber)">🎬 Boot Animation</div><div class="card-body">3-stage welcome sequence displayed on both OLED screens.</div></div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ HARDWARE ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-amber">⚙️</div>
      <h2 class="section-title"><span class="accent-amber">HARDWARE</span> REQUIREMENTS</h2>
    </div>

    <div class="tbl-wrap" style="margin-bottom:28px;">
      <table>
        <thead><tr><th>Component</th><th>Specification</th><th>Qty</th></tr></thead>
        <tbody>
          <tr><td><span class="pill pill-cyan">ESP32 DevKit</span></td><td>Any 38-pin variant</td><td>1</td></tr>
          <tr><td><span class="pill pill-amber">L298N H-Bridge</span></td><td>Dual motor driver</td><td>1</td></tr>
          <tr><td><span class="pill pill-green">DC Motors</span></td><td>5V DC geared motors</td><td>4</td></tr>
          <tr><td><span class="pill pill-violet">SG90 Servo</span></td><td>Camera pan</td><td>1</td></tr>
          <tr><td><span class="pill pill-violet">SG90 Servo</span></td><td>Gripper</td><td>1</td></tr>
          <tr><td><span class="pill pill-cyan">BMP280</span></td><td>Temp / Pressure / Altitude, I²C</td><td>1</td></tr>
          <tr><td><span class="pill pill-green">HC-SR04</span></td><td>Ultrasonic distance sensor</td><td>1</td></tr>
          <tr><td><span class="pill pill-amber">SSD1306 OLED</span></td><td>128×64, I²C (0x3C)</td><td>1</td></tr>
          <tr><td><span class="pill pill-amber">SSD1306 OLED</span></td><td>128×64, I²C (0x3D)</td><td>1</td></tr>
          <tr><td><span class="pill pill-red">Buck Converter</span></td><td>LM2596 12V → 5V, 3A</td><td>1</td></tr>
          <tr><td><span class="pill pill-red">Battery</span></td><td>12V LiPo or lead-acid</td><td>1</td></tr>
        </tbody>
      </table>
    </div>

    <h3 style="font-family:'Orbitron',monospace;font-size:13px;color:var(--cyan);letter-spacing:2px;margin-bottom:14px;">📌 GPIO PIN MAPPING</h3>
    <div class="code-block">
      <div class="code-header">
        <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
        <span class="code-label">esp32_pinmap.txt</span>
      </div>
      <pre><span class="cmt">── Motor Driver (L298N) ──────────────────</span>
  IN1  → <span class="num">GPIO 27</span>       IN2  → <span class="num">GPIO 26</span>
  IN3  → <span class="num">GPIO 25</span>       IN4  → <span class="num">GPIO 33</span>

<span class="cmt">── Servos ────────────────────────────────</span>
  Camera  → <span class="num">GPIO 19</span>     Gripper → <span class="num">GPIO 18</span>

<span class="cmt">── I²C Bus (BMP280 + OLEDs) ─────────────</span>
  SDA → <span class="num">GPIO 21</span>          SCL → <span class="num">GPIO 22</span>

<span class="cmt">── Ultrasonic (HC-SR04) ─────────────────</span>
  TRIG → <span class="num">GPIO 17</span>         ECHO → <span class="num">GPIO 16</span>

<span class="cmt">── I²C Addresses ────────────────────────</span>
  BMP280 → <span class="str">0x76</span> or <span class="str">0x77</span>
  OLED L → <span class="str">0x3C</span>
  OLED R → <span class="str">0x3D</span></pre>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ SOFTWARE ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-cyan">💻</div>
      <h2 class="section-title"><span class="accent-cyan">SOFTWARE</span> REQUIREMENTS</h2>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;flex-wrap:wrap;">
      <div class="code-block">
        <div class="code-header">
          <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
          <span class="code-label">Python GUI</span>
        </div>
        <pre><span class="cmt"># Python 3.8+</span>
<span class="kw">pip install</span> <span class="str">PyQt5</span> <span class="str">websocket-client</span></pre>
      </div>
      <div class="code-block">
        <div class="code-header">
          <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
          <span class="code-label">Arduino Libraries</span>
        </div>
        <pre><span class="str">WebSocketsServer</span>   <span class="cmt"># Markus Sattler</span>
<span class="str">ESP32Servo</span>
<span class="str">Adafruit GFX</span>
<span class="str">Adafruit SSD1306</span>
<span class="str">Adafruit BMP280</span></pre>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ GETTING STARTED ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-green">🚀</div>
      <h2 class="section-title"><span class="accent-green">GETTING</span> STARTED</h2>
    </div>

    <div style="display:flex;flex-direction:column;gap:20px;">
      <div class="code-block">
        <div class="code-header">
          <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
          <span class="code-label">Step 1 · Flash ESP32</span>
        </div>
        <pre><span class="cmt">// Update your Wi-Fi credentials in esp32_firmware.ino</span>
<span class="kw">const char*</span> ssid     = <span class="str">"YOUR_WIFI_SSID"</span>;
<span class="kw">const char*</span> password = <span class="str">"YOUR_WIFI_PASSWORD"</span>;

<span class="cmt">// Flash via Arduino IDE → OLED shows assigned IP address</span></pre>
      </div>

      <div class="code-block">
        <div class="code-header">
          <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
          <span class="code-label">Step 2 · Launch GUI</span>
        </div>
        <pre><span class="kw">git</span> clone https://github.com/Muhammad-296/Mars-Rover.git
<span class="kw">cd</span> Mars-Rover
<span class="kw">pip install</span> PyQt5 websocket-client
<span class="kw">python</span> main.py

<span class="cmt"># In Startup Dialog, enter WebSocket URL:</span>
<span class="str">ws://192.168.x.x:81</span>

<span class="cmt"># Click ▶ INITIATE UPLINK — enjoy boot sequence!</span></pre>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ KEYBOARD CONTROLS ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-amber">⌨️</div>
      <h2 class="section-title"><span class="accent-amber">KEYBOARD</span> CONTROLS</h2>
    </div>
    <div class="key-grid">
      <div class="key-row"><div class="key-chip">↑  UP</div><div class="key-action">Drive Forward</div></div>
      <div class="key-row"><div class="key-chip">↓  DOWN</div><div class="key-action">Drive Backward</div></div>
      <div class="key-row"><div class="key-chip">←  LEFT</div><div class="key-action">Turn Left</div></div>
      <div class="key-row"><div class="key-chip">→  RIGHT</div><div class="key-action">Turn Right</div></div>
      <div class="key-row"><div class="key-chip">A</div><div class="key-action">Pan Camera Right</div></div>
      <div class="key-row"><div class="key-chip">D</div><div class="key-action">Pan Camera Left</div></div>
      <div class="key-row"><div class="key-chip">O</div><div class="key-action">Open Gripper</div></div>
      <div class="key-row"><div class="key-chip">C</div><div class="key-action">Close Gripper</div></div>
      <div class="key-row"><div class="key-chip">?</div><div class="key-action">Toggle Keyboard Overlay</div></div>
      <div class="key-row"><div class="key-chip">ESC</div><div class="key-action">Exit Application</div></div>
    </div>
    <p style="margin-top:16px;font-size:14px;color:var(--dim);">
      ⚡ Releasing any movement key immediately sends a STOP command. A 3-second watchdog auto-stops the rover if the GUI freezes or disconnects.
    </p>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ ARCHITECTURE ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-violet">🏗️</div>
      <h2 class="section-title"><span class="accent-violet">SYSTEM</span> ARCHITECTURE</h2>
    </div>
    <div class="arch-diagram">
      <div class="arch-layer-label" style="color:var(--cyan);">▸ PyQt5 MISSION CONTROL</div>
      <div class="arch-row">
        <div class="arch-box ab-cyan"><div class="ab-label">TELEMETRY</div>Arc Gauges</div>
        <div class="arch-box ab-cyan"><div class="ab-label">HISTORY</div>Live Charts</div>
        <div class="arch-box ab-cyan"><div class="ab-label">VISUAL</div>Rover Renderer</div>
      </div>
      <div class="arch-row" style="margin-top:8px;">
        <div class="arch-box ab-violet" style="width:100%;max-width:500px;margin:0 auto;">
          <div class="ab-label">CONTROL</div>Keyboard Handler + Safety Watchdog
        </div>
      </div>
      <div class="arch-connector">│<br/>WebSocket Client<br/>│</div>
      <div class="arch-connector" style="color:var(--cyan);font-size:14px;letter-spacing:2px;">
        ━━━━━━━━  Wi-Fi  ·  ws://rover-ip:81  ━━━━━━━━
      </div>
      <div class="arch-connector">│</div>
      <hr class="arch-sep"/>
      <div class="arch-layer-label" style="color:var(--amber);">▸ ESP32 FIRMWARE</div>
      <div class="arch-row">
        <div class="arch-box ab-amber"><div class="ab-label">MOTORS</div>L298N Drive</div>
        <div class="arch-box ab-amber"><div class="ab-label">SERVER</div>WebSocket :81</div>
        <div class="arch-box ab-amber"><div class="ab-label">SENSORS</div>BMP280 + HC-SR04</div>
      </div>
      <div class="arch-row" style="margin-top:12px;">
        <div class="arch-box ab-green"><div class="ab-label">CAMERA</div>Pan Servo</div>
        <div class="arch-box ab-green"><div class="ab-label">GRIP</div>Gripper Servo</div>
        <div class="arch-box ab-green"><div class="ab-label">DISPLAY</div>Dual OLEDs</div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ PROTOCOL ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-cyan">📡</div>
      <h2 class="section-title"><span class="accent-cyan">WEBSOCKET</span> PROTOCOL</h2>
    </div>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Command</th><th>Direction</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td><code style="color:var(--green)">F</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Drive Forward</td></tr>
          <tr><td><code style="color:var(--green)">B</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Drive Backward</td></tr>
          <tr><td><code style="color:var(--green)">L</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Turn Left</td></tr>
          <tr><td><code style="color:var(--green)">R</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Turn Right</td></tr>
          <tr><td><code style="color:var(--green)">S</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Instant Stop</td></tr>
          <tr><td><code style="color:var(--green)">A</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Camera Pan Right</td></tr>
          <tr><td><code style="color:var(--green)">D</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Camera Pan Left</td></tr>
          <tr><td><code style="color:var(--green)">O</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Open Gripper</td></tr>
          <tr><td><code style="color:var(--green)">C</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Close Gripper</td></tr>
          <tr><td><code style="color:var(--cyan)">SENSOR</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Request sensor data</td></tr>
          <tr><td><code style="color:var(--cyan)">PING</code></td><td><span class="dir-gui">GUI → ESP32</span></td><td>Latency measurement</td></tr>
          <tr><td><code style="color:var(--amber)">T,P,A,D</code></td><td><span class="dir-esp">ESP32 → GUI</span></td><td>Sensor CSV: temp · pressure · altitude · distance</td></tr>
          <tr><td><code style="color:var(--amber)">&lt;angle&gt;</code></td><td><span class="dir-esp">ESP32 → GUI</span></td><td>Camera servo position in degrees</td></tr>
          <tr><td><code style="color:var(--amber)">GRIPPER_OPEN</code></td><td><span class="dir-esp">ESP32 → GUI</span></td><td>Gripper state confirmation</td></tr>
          <tr><td><code style="color:var(--amber)">GRIPPER_CLOSE</code></td><td><span class="dir-esp">ESP32 → GUI</span></td><td>Gripper state confirmation</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ SAFETY ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-red">🔒</div>
      <h2 class="section-title"><span class="accent-red">SAFETY</span> FEATURES</h2>
    </div>
    <div class="safety-grid">
      <div class="safety-card sc-red">
        <div class="safety-title" style="color:var(--red)">🛑 Instant Stop</div>
        <div class="safety-body">No key held = no movement. Key release immediately sends STOP command to rover.</div>
      </div>
      <div class="safety-card sc-amber">
        <div class="safety-title" style="color:var(--amber)">⏱ GUI Watchdog — 3s</div>
        <div class="safety-body">GUI-side timer halts rover if movement command stalls or GUI freezes.</div>
      </div>
      <div class="safety-card sc-cyan">
        <div class="safety-title" style="color:var(--cyan)">⚡ ESP32 Watchdog — 500ms</div>
        <div class="safety-body">Firmware stops motors if no command received — covers Wi-Fi drops.</div>
      </div>
      <div class="safety-card sc-violet">
        <div class="safety-title" style="color:var(--violet)">🚨 Obstacle Alerts</div>
        <div class="safety-body">Visual + log warning: CAUTION &lt; 80 cm · CRITICAL &lt; 30 cm distance.</div>
      </div>
      <div class="safety-card sc-green" style="border-color:var(--green);background:rgba(0,255,145,0.05);">
        <div class="safety-title" style="color:var(--green)">🔄 Auto-Reconnect</div>
        <div class="safety-body">GUI automatically retries WebSocket connection on failure or timeout.</div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ REPO ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-violet">🗂️</div>
      <h2 class="section-title"><span class="accent-violet">REPOSITORY</span> STRUCTURE</h2>
    </div>
    <div class="repo-tree">
      <span class="rt-root">Mars-Rover/</span><br/>
      <span class="rt-branch">│</span><br/>
      <span class="rt-branch">├── </span><span class="rt-file">📄 main.py</span>  <span class="rt-comment"># PyQt5 Mission Control GUI (v5.1)</span><br/>
      <span class="rt-branch">├── </span><span class="rt-file">📄 esp32_firmware.ino</span>  <span class="rt-comment"># ESP32 Arduino firmware</span><br/>
      <span class="rt-branch">│</span><br/>
      <span class="rt-branch">├── </span><span class="rt-img">📸 Robot_Wiring.png</span>  <span class="rt-comment"># Full wiring diagram</span><br/>
      <span class="rt-branch">├── </span><span class="rt-img">📸 Station.png</span>  <span class="rt-comment"># Software architecture diagram</span><br/>
      <span class="rt-branch">│</span><br/>
      <span class="rt-branch">└── </span><span class="rt-file">📄 README.md</span>  <span class="rt-comment"># This file</span>
    </div>
  </section>

  <div class="divider"></div>

  <!-- ═══════════════ CONTRIBUTING ═══════════════ -->
  <section>
    <div class="section-head">
      <div class="section-icon icon-green">🤝</div>
      <h2 class="section-title"><span class="accent-green">CONTRIBUTING</span></h2>
    </div>
    <p>Pull requests are welcome! Please open an issue first to discuss major changes.</p>
    <div class="code-block">
      <div class="code-header">
        <div class="dot dot-r"></div><div class="dot dot-y"></div><div class="dot dot-g"></div>
        <span class="code-label">git workflow</span>
      </div>
      <pre><span class="cmt"># 1. Fork the repo, then:</span>
<span class="kw">git checkout</span> -b <span class="str">feature/amazing-feature</span>
<span class="kw">git commit</span>  -m <span class="str">'Add amazing feature'</span>
<span class="kw">git push</span>    origin <span class="str">feature/amazing-feature</span>
<span class="cmt"># 2. Open a Pull Request</span></pre>
    </div>
  </section>

</div><!-- /wrap -->

<!-- ═══════════════ FOOTER ═══════════════ -->
<footer>
  <div class="footer-title">MIT LICENSE</div>
  <div class="footer-sub">This project is licensed under the MIT License.</div>
  <div style="margin-bottom:20px;font-family:'Share Tech Mono',monospace;font-size:13px;color:var(--dim);">
    Built with ❤️ for robotics enthusiasts
  </div>
  <div class="star-cta">⭐ STAR THIS REPO IF IT HELPED YOU BUILD SOMETHING AWESOME ⭐</div>
</footer>

</body>
</html>
