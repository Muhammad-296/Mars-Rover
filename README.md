<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Mars Rover Mission Control v5.1</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;700;900&family=Exo+2:wght@300;400;600&display=swap" rel="stylesheet"/>
<style>
:root {
  --bg:       #02040A;
  --bg2:      #060D14;
  --bg3:      #0A1520;
  --cyan:     #00E6FF;
  --cyan2:    #00B8CC;
  --cyan3:    #006680;
  --green:    #00FF91;
  --amber:    #FFB900;
  --red:      #FF2D37;
  --blue:     #3776AB;
  --white:    #E8F4F8;
  --muted:    #4A7A8A;
  --border:   #0D3040;
  --border2:  #1A4A60;
  --card:     #07111A;
  --card2:    #0C1D2A;
  --glow:     0 0 20px rgba(0,230,255,0.15);
  --glow2:    0 0 40px rgba(0,230,255,0.08);
  --font-mono: 'Share Tech Mono', monospace;
  --font-display: 'Orbitron', sans-serif;
  --font-body: 'Exo 2', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--white);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.7;
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── BACKGROUND GRID ── */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(0,230,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,230,255,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

body::after {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, rgba(0,60,80,0.5) 0%, transparent 70%),
    radial-gradient(ellipse 40% 40% at 100% 100%, rgba(0,30,50,0.4) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.content { position: relative; z-index: 1; }

/* ── HEADER ── */
.hero {
  padding: 72px 24px 60px;
  text-align: center;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(0,40,60,0.6) 0%, transparent 100%);
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--cyan), var(--green), var(--cyan), transparent);
}

.hero-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--cyan3);
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.hero h1 {
  font-family: var(--font-display);
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 900;
  color: var(--cyan);
  letter-spacing: 4px;
  text-transform: uppercase;
  line-height: 1;
  margin-bottom: 12px;
  text-shadow: 0 0 60px rgba(0,230,255,0.4), 0 0 120px rgba(0,230,255,0.15);
}

.hero-sub {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--cyan2);
  letter-spacing: 3px;
  margin-bottom: 40px;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 36px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 16px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  border: 1px solid;
  font-weight: 600;
}
.badge-green  { color: var(--green); border-color: rgba(0,255,145,0.3); background: rgba(0,255,145,0.06); }
.badge-cyan   { color: var(--cyan);  border-color: rgba(0,230,255,0.3); background: rgba(0,230,255,0.06); }
.badge-amber  { color: var(--amber); border-color: rgba(255,185,0,0.3);  background: rgba(255,185,0,0.06); }
.badge-red    { color: var(--red);   border-color: rgba(255,45,55,0.3);  background: rgba(255,45,55,0.06); }
.badge-blue   { color: #64B5F6;      border-color: rgba(55,118,171,0.35);background: rgba(55,118,171,0.06); }
.badge-orange { color: #FF9944;      border-color: rgba(255,136,0,0.3);  background: rgba(255,136,0,0.06); }

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
  margin-top: 8px;
}

.tech-pill {
  padding: 6px 18px;
  border: 1px solid var(--border2);
  border-radius: 2px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--muted);
  letter-spacing: 2px;
  background: rgba(0,230,255,0.03);
}

/* ── MAIN LAYOUT ── */
.main {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px 80px;
}

/* ── SECTION ── */
section {
  margin-top: 64px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 28px;
}

.section-label::before {
  content: '';
  display: block;
  width: 4px;
  height: 28px;
  background: linear-gradient(180deg, var(--cyan), var(--cyan3));
  border-radius: 2px;
  flex-shrink: 0;
}

.section-label h2 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--cyan);
  letter-spacing: 3px;
  text-transform: uppercase;
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--border2), transparent);
}

/* ── OVERVIEW BLOCK ── */
.overview-box {
  background: var(--card);
  border: 1px solid var(--border2);
  border-left: 3px solid var(--cyan);
  padding: 24px 28px;
  border-radius: 4px;
  font-size: 14.5px;
  color: #9ECAD5;
  line-height: 1.8;
  box-shadow: var(--glow2);
}

.overview-box strong { color: var(--cyan); }

/* ── FEATURE GRID ── */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.feature-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 20px 22px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.feature-card:hover { border-color: var(--border2); background: var(--card2); }

.feature-icon {
  font-size: 22px;
  flex-shrink: 0;
  margin-top: 2px;
}

.feature-title {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  color: var(--cyan);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 5px;
}

.feature-desc {
  font-size: 13px;
  color: #7AAABB;
  line-height: 1.6;
}

/* ── TABLES ── */
.table-wrap {
  overflow-x: auto;
  border-radius: 4px;
  border: 1px solid var(--border);
  box-shadow: var(--glow2);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

thead tr {
  background: #060F18;
  border-bottom: 1px solid var(--border2);
}

thead th {
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  color: var(--cyan2);
  letter-spacing: 2.5px;
  text-transform: uppercase;
  padding: 13px 18px;
  text-align: left;
  white-space: nowrap;
}

thead th:first-child { width: 40px; text-align: center; }

tbody tr {
  border-bottom: 1px solid rgba(13,48,64,0.6);
  background: var(--card);
}

tbody tr:nth-child(even) { background: #060E17; }
tbody tr:last-child { border-bottom: none; }

tbody td {
  padding: 11px 18px;
  color: #8CBFCC;
  vertical-align: middle;
}

tbody td:first-child { text-align: center; font-size: 16px; }

code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--cyan);
  background: rgba(0,230,255,0.08);
  padding: 2px 7px;
  border-radius: 3px;
  border: 1px solid rgba(0,230,255,0.15);
}

.gpio { color: var(--amber); font-family: var(--font-mono); font-weight: 600; font-size: 13px; }
.tag-fw { color: var(--green);; font-family: var(--font-mono); font-size: 11px; }
.tag-bk { color: var(--amber); font-family: var(--font-mono); font-size: 11px; }
.tag-st { color: var(--red);   font-family: var(--font-mono); font-size: 11px; }

/* ── ARCHITECTURE ── */
.arch-grid {
  display: grid;
  grid-template-columns: 1fr 160px 1fr;
  gap: 0;
  align-items: center;
}

.arch-col {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px;
}

.arch-node {
  background: var(--card2);
  border: 1px solid var(--border2);
  border-radius: 3px;
  padding: 11px 14px;
  margin: 4px;
  font-size: 12px;
}

.arch-node-title {
  font-family: var(--font-display);
  font-size: 9px;
  letter-spacing: 2px;
  color: var(--cyan2);
  text-transform: uppercase;
  margin-bottom: 4px;
}

.arch-node-body { color: #7AAABB; font-family: var(--font-mono); font-size: 11px; }

.arch-col-header {
  font-family: var(--font-display);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--white);
  text-transform: uppercase;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.arch-middle {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
  padding: 8px;
}

.ws-box {
  background: #060F18;
  border: 1px solid var(--border2);
  border-radius: 4px;
  padding: 18px 10px;
  text-align: center;
  width: 100%;
}

.ws-title {
  font-family: var(--font-display);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--cyan);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.ws-arrow {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--muted);
  margin: 4px 0;
}

.ws-cmd { color: var(--green); font-family: var(--font-mono); font-size: 10px; }
.ws-tel { color: var(--amber); font-family: var(--font-mono); font-size: 10px; }

/* ── CMD PROTOCOL ── */
.cmd-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.cmd-group {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.cmd-group-header {
  background: #060F18;
  border-bottom: 1px solid var(--border2);
  padding: 10px 16px;
  font-family: var(--font-display);
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--cyan2);
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cmd-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 16px;
  border-bottom: 1px solid rgba(13,48,64,0.5);
}

.cmd-row:last-child { border-bottom: none; }

.cmd-key {
  font-family: var(--font-mono);
  font-size: 13px;
  font-weight: 700;
  color: var(--cyan);
  background: rgba(0,230,255,0.1);
  border: 1px solid rgba(0,230,255,0.25);
  border-radius: 3px;
  padding: 2px 10px;
  min-width: 48px;
  text-align: center;
  flex-shrink: 0;
}

.cmd-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.dot-g { background: var(--green); }
.dot-y { background: var(--amber); }
.dot-b { background: #64B5F6; }
.dot-r { background: var(--red); }
.dot-c { background: var(--cyan); }

.cmd-desc { font-size: 13px; color: #7AAABB; }

/* ── SOFTWARE STACK ── */
.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
}

.stack-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 18px 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.stack-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }

.stack-layer {
  font-family: var(--font-display);
  font-size: 10px;
  font-weight: 700;
  color: var(--amber);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.stack-tech { font-size: 14px; font-weight: 600; color: var(--white); margin-bottom: 3px; }
.stack-detail { font-size: 12px; color: #6A9EAC; }

/* ── SAFETY ── */
.safety-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 14px;
}

.safety-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 16px 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.safety-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 5px;
}

.ind-green { background: var(--green); box-shadow: 0 0 8px rgba(0,255,145,0.5); }
.ind-amber { background: var(--amber); box-shadow: 0 0 8px rgba(255,185,0,0.5); }
.ind-red   { background: var(--red);   box-shadow: 0 0 8px rgba(255,45,55,0.5); }
.ind-cyan  { background: var(--cyan);  box-shadow: 0 0 8px rgba(0,230,255,0.5); }

.safety-title { font-family: var(--font-display); font-size: 11px; letter-spacing: 1.5px; color: var(--white); text-transform: uppercase; margin-bottom: 4px; }
.safety-desc { font-size: 12.5px; color: #7AAABB; }
.safety-trigger { font-family: var(--font-mono); font-size: 11px; color: var(--cyan2); margin-top: 4px; }

/* ── CODE BLOCK ── */
.code-block {
  background: #030810;
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.code-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #060F18;
  border-bottom: 1px solid var(--border);
}

.code-dot { width: 10px; height: 10px; border-radius: 50%; }
.cd-r { background: #FF5F56; }
.cd-y { background: #FFBD2E; }
.cd-g { background: #27C93F; }

.code-lang {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--muted);
  margin-left: auto;
  letter-spacing: 1px;
}

pre {
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.7;
  padding: 20px 24px;
  color: #8ECCD8;
  overflow-x: auto;
}

.kw { color: #FF79C6; }
.str { color: var(--green); }
.cm { color: #4A7A8A; font-style: italic; }
.fn { color: var(--cyan); }
.num { color: var(--amber); }

/* ── GETTING STARTED ── */
.steps { display: flex; flex-direction: column; gap: 24px; }

.step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.step-num {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(0,230,255,0.08);
  border: 1px solid rgba(0,230,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 14px;
  font-weight: 700;
  color: var(--cyan);
}

.step-content { flex: 1; }

.step-title {
  font-family: var(--font-display);
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--white);
  text-transform: uppercase;
  margin-bottom: 10px;
}

/* ── FILE TREE ── */
.tree {
  background: #030810;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 20px 24px;
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 2;
  color: #7AAABB;
}

.tree-dir   { color: var(--cyan); }
.tree-file  { color: #8ECCD8; }
.tree-arrow { color: var(--muted); }
.tree-note  { color: var(--muted); font-style: italic; }

/* ── OLED DISPLAY ── */
.oled-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.oled-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
}

.oled-screen {
  background: #000A06;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border);
  font-family: var(--font-mono);
  font-size: 13px;
  color: #00FF77;
  letter-spacing: 2px;
  text-align: center;
  padding: 12px;
}

.oled-info { padding: 14px 16px; }
.oled-addr { font-family: var(--font-mono); font-size: 11px; color: var(--cyan); margin-bottom: 5px; }
.oled-desc { font-size: 12px; color: #7AAABB; }

/* ── PIN MAP ── */
.pin-visual {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 10px;
}

.pin-row {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.pin-num {
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  min-width: 38px;
  padding: 3px 8px;
  text-align: center;
  border-radius: 3px;
  border: 1px solid;
}

.pin-cyan  { color: var(--cyan); border-color: rgba(0,230,255,0.4); background: rgba(0,230,255,0.08); }
.pin-amber { color: var(--amber);border-color: rgba(255,185,0,0.4);  background: rgba(255,185,0,0.08); }
.pin-green { color: var(--green);border-color: rgba(0,255,145,0.4);  background: rgba(0,255,145,0.08); }

.pin-label { font-size: 12px; color: #7AAABB; font-family: var(--font-mono); }
.pin-type  { font-size: 10px; color: var(--muted); margin-top: 2px; }

/* ── STATS BAR ── */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 64px;
}

.stat-cell {
  background: var(--card);
  padding: 24px;
  text-align: center;
}

.stat-num {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 900;
  color: var(--cyan);
  line-height: 1;
  margin-bottom: 6px;
  text-shadow: 0 0 30px rgba(0,230,255,0.3);
}

.stat-label { font-size: 11px; color: var(--muted); letter-spacing: 2px; text-transform: uppercase; font-family: var(--font-mono); }

/* ── FOOTER ── */
footer {
  border-top: 1px solid var(--border);
  padding: 40px 24px;
  text-align: center;
  position: relative;
}

footer::before {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan3), transparent);
}

.footer-title {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 900;
  color: var(--cyan);
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.footer-sub { font-family: var(--font-mono); font-size: 12px; color: var(--muted); letter-spacing: 2px; }

/* ── RESPONSIVE ── */
@media (max-width: 760px) {
  .arch-grid, .cmd-grid, .oled-grid { grid-template-columns: 1fr; }
  .stats-bar { grid-template-columns: 1fr 1fr; }
  .arch-middle { flex-direction: row; }
}
</style>
</head>
<body>
<div class="content">

<!-- ── HERO ── -->
<header class="hero">
  <div class="hero-tag">◈ MISSION CONTROL SYSTEM ◈ ESP32 PLATFORM ◈ v5.1</div>
  <h1>🚀 MARS ROVER</h1>
  <div class="hero-sub">MISSION CONTROL v5.1 &nbsp;|&nbsp; ESP32 &nbsp;|&nbsp; PYTHON GUI &nbsp;|&nbsp; WEBSOCKET</div>

  <div class="badges">
    <span class="badge badge-green">🟢 STATUS · OPERATIONAL</span>
    <span class="badge badge-cyan">📡 VERSION · v5.1</span>
    <span class="badge badge-amber">⚖️ LICENSE · MIT</span>
    <span class="badge badge-red">🔧 PLATFORM · ESP32</span>
    <span class="badge badge-blue">🐍 GUI · PYQT5</span>
    <span class="badge badge-orange">📶 PROTOCOL · WEBSOCKET</span>
  </div>

  <div class="tech-stack">
    <span class="tech-pill">PYTHON</span>
    <span class="tech-pill">C++ / ARDUINO</span>
    <span class="tech-pill">ESP32</span>
    <span class="tech-pill">GITHUB</span>
    <span class="tech-pill">VS CODE</span>
  </div>
</header>

<div class="main">

  <!-- ── OVERVIEW ── -->
  <section>
    <div class="section-label"><h2>🛸 Mission Overview</h2></div>
    <div class="overview-box">
      <strong>Mars Rover Mission Control</strong> is a full-stack robotics project combining a custom
      <strong>ESP32-powered 6-wheel rover chassis</strong> with a <strong>Python PyQt5 GUI</strong> for
      real-time telemetry, remote driving, camera panning, and gripper control — all over Wi-Fi via
      <strong>WebSocket</strong>.
    </div>
  </section>

  <!-- ── FEATURES ── -->
  <section>
    <div class="section-label"><h2>⚡ Core Features</h2></div>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <div>
          <div class="feature-title">6 DC Motors</div>
          <div class="feature-desc">Paired as 3 channels for tank-style differential drive. No PWM needed — direction only.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📷</div>
        <div>
          <div class="feature-title">ESP32-CAM on Servo</div>
          <div class="feature-desc">Live camera with 0°–180° pan control. Step 10° per command via GPIO 19.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🌡️</div>
        <div>
          <div class="feature-title">BMP280 Sensor</div>
          <div class="feature-desc">Real-time temperature, pressure &amp; altitude over I²C bus at 0x76 / 0x77.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📡</div>
        <div>
          <div class="feature-title">HC-SR04 Radar</div>
          <div class="feature-desc">Ultrasonic proximity with WARN @ 80 cm and CRIT @ 30 cm threshold alerts.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🦾</div>
        <div>
          <div class="feature-title">Servo Gripper</div>
          <div class="feature-desc">Object manipulation via GPIO 18. Open: 90° · Close: 10° with state confirmation.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🟣</div>
        <div>
          <div class="feature-title">Custom PCB</div>
          <div class="feature-desc">ESP32 breakout with all motor, servo &amp; sensor headers fully populated.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🎮</div>
        <div>
          <div class="feature-title">Sci-Fi GUI</div>
          <div class="feature-desc">PyQt5 Mission Control with live charts, arc gauges, radar display &amp; safety watchdog.</div>
        </div>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🖥️</div>
        <div>
          <div class="feature-title">Dual OLED Display</div>
          <div class="feature-desc">128×64 panels at 0x3C and 0x3D — drive state left, sensors &amp; camera right.</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── ARCHITECTURE ── -->
  <section>
    <div class="section-label"><h2>🗺️ System Architecture</h2></div>
    <div class="arch-grid">
      <!-- PC -->
      <div class="arch-col">
        <div class="arch-col-header">🖥️ MISSION CONTROL — Python PyQt5</div>
        <div class="arch-node">
          <div class="arch-node-title">🎮 PyQt5 GUI v5.1</div>
          <div class="arch-node-body">Boot Sequence · Key Overlay · Startup Config</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">📊 Arc Gauges</div>
          <div class="arch-node-body">Temp · Press · Alt · Dist · Servo</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">📈 Telemetry Charts</div>
          <div class="arch-node-body">4 Scrolling Streams · 80-point History</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">🔴 Proximity Radar</div>
          <div class="arch-node-body">WARN @ 80 cm · CRIT @ 30 cm</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">📶 Latency Monitor</div>
          <div class="arch-node-body">Live Ping Graph · Auto-Reconnect</div>
        </div>
      </div>

      <!-- WS -->
      <div class="arch-middle">
        <div class="ws-box">
          <div class="ws-title">📡 WebSocket</div>
          <div class="ws-cmd">ws://ESP32_IP:81</div>
          <div class="ws-arrow">▼ Commands ▼</div>
          <div class="ws-cmd">F B L R S A D O C SENSOR PING</div>
          <div class="ws-arrow">▲ Telemetry ▲</div>
          <div class="ws-tel">t,p,alt,d · angle · GRIPPER_STATE</div>
        </div>
      </div>

      <!-- ESP32 -->
      <div class="arch-col">
        <div class="arch-col-header">⚡ ESP32 — Arduino Firmware</div>
        <div class="arch-node">
          <div class="arch-node-title">🔧 Motor Driver</div>
          <div class="arch-node-body">L298D × 2 · 6 DC Motors · IN1:27 IN2:26 IN3:25 IN4:33</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">📷 Camera Servo</div>
          <div class="arch-node-body">GPIO 19 · 0°–180°</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">🦾 Gripper Servo</div>
          <div class="arch-node-body">GPIO 18 · Open 90° / Close 10°</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">🌡️ BMP280 + HC-SR04</div>
          <div class="arch-node-body">I²C · Trig:17 · Echo:16</div>
        </div>
        <div class="arch-node">
          <div class="arch-node-title">🖥️ Dual OLED</div>
          <div class="arch-node-body">0x3C Left · 0x3D Right</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── HARDWARE ── -->
  <section>
    <div class="section-label"><h2>🔩 Hardware Components</h2></div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Component</th>
            <th>Qty</th>
            <th>GPIO / Bus</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>🔵</td><td><strong>ESP32</strong> DevKit / WROOM</td><td>1</td><td>—</td><td>Wi-Fi · WebSocket server port <code>81</code></td></tr>
          <tr><td>📷</td><td><strong>ESP32-CAM</strong></td><td>1</td><td><span class="gpio">GPIO 19</span></td><td>Mounted on pan servo · 0°–180°</td></tr>
          <tr><td>⚙️</td><td><strong>DC Gear Motors</strong></td><td>6</td><td>IN1–IN4</td><td>Paired 3+3 wired as 2 channels</td></tr>
          <tr><td>🔌</td><td><strong>L298D Motor Driver</strong></td><td>2</td><td><span class="gpio">27·26·25·33</span></td><td>No Enable pin · direction only</td></tr>
          <tr><td>🦾</td><td><strong>Servo — Camera Pan</strong></td><td>1</td><td><span class="gpio">GPIO 19</span></td><td>Range 0°–180° · Step 10°</td></tr>
          <tr><td>🤖</td><td><strong>Servo — Gripper</strong></td><td>1</td><td><span class="gpio">GPIO 18</span></td><td>Open: 90° · Close: 10°</td></tr>
          <tr><td>📡</td><td><strong>HC-SR04 Ultrasonic</strong></td><td>1</td><td><span class="gpio">Trig 17 · Echo 16</span></td><td>Proximity radar 0–500 cm</td></tr>
          <tr><td>🌡️</td><td><strong>BMP280</strong></td><td>1</td><td>I²C · 0x76/0x77</td><td>Temperature · Pressure · Altitude</td></tr>
          <tr><td>🖥️</td><td><strong>SSD1306 OLED 128×64</strong></td><td>2</td><td>I²C · 0x3C · 0x3D</td><td>Left: Drive state · Right: Cam + Sensors</td></tr>
          <tr><td>🟣</td><td><strong>Custom PCB</strong></td><td>1</td><td>—</td><td>ESP32 breakout · all headers populated</td></tr>
        </tbody>
      </table>
    </div>

    <div style="margin-top:20px">
      <div class="section-label" style="margin-top:0"><h2>⚡ Motor Channel Wiring</h2></div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr><th style="text-align:center">Channel</th><th>IN+</th><th>IN−</th><th>Side</th><th>Motors</th></tr>
          </thead>
          <tbody>
            <tr><td><strong>CH 1</strong></td><td><span class="gpio">GPIO 27</span></td><td><span class="gpio">GPIO 26</span></td><td>◀ Left</td><td>3 × DC motor (parallel)</td></tr>
            <tr><td><strong>CH 2</strong></td><td><span class="gpio">GPIO 25</span></td><td><span class="gpio">GPIO 33</span></td><td>Right ▶</td><td>3 × DC motor (parallel)</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- ── PIN MAP ── -->
  <section>
    <div class="section-label"><h2>🗃️ Pin Mapping</h2></div>
    <div class="pin-visual">
      <div class="pin-row"><span class="pin-num pin-amber">27</span><div><div class="pin-label">IN1 — Left Motor FWD</div><div class="pin-type">Digital Output</div></div></div>
      <div class="pin-row"><span class="pin-num pin-amber">26</span><div><div class="pin-label">IN2 — Left Motor REV</div><div class="pin-type">Digital Output</div></div></div>
      <div class="pin-row"><span class="pin-num pin-amber">25</span><div><div class="pin-label">IN3 — Right Motor FWD</div><div class="pin-type">Digital Output</div></div></div>
      <div class="pin-row"><span class="pin-num pin-amber">33</span><div><div class="pin-label">IN4 — Right Motor REV</div><div class="pin-type">Digital Output</div></div></div>
      <div class="pin-row"><span class="pin-num pin-cyan">19</span><div><div class="pin-label">Camera Servo Signal</div><div class="pin-type">PWM · 0°–180°</div></div></div>
      <div class="pin-row"><span class="pin-num pin-cyan">18</span><div><div class="pin-label">Gripper Servo Signal</div><div class="pin-type">PWM · 10° / 90°</div></div></div>
      <div class="pin-row"><span class="pin-num pin-green">17</span><div><div class="pin-label">Ultrasonic TRIG</div><div class="pin-type">Digital Output</div></div></div>
      <div class="pin-row"><span class="pin-num pin-green">16</span><div><div class="pin-label">Ultrasonic ECHO</div><div class="pin-type">Digital Input</div></div></div>
      <div class="pin-row"><span class="pin-num pin-cyan">SDA</span><div><div class="pin-label">BMP280 + OLED Data</div><div class="pin-type">I²C Bus</div></div></div>
      <div class="pin-row"><span class="pin-num pin-cyan">SCL</span><div><div class="pin-label">BMP280 + OLED Clock</div><div class="pin-type">I²C Bus</div></div></div>
    </div>
  </section>

  <!-- ── SOFTWARE ── -->
  <section>
    <div class="section-label"><h2>💻 Software Stack</h2></div>
    <div class="stack-grid">
      <div class="stack-card">
        <div class="stack-icon">🎮</div>
        <div>
          <div class="stack-layer">GUI Layer</div>
          <div class="stack-tech">Python 3 + PyQt5 v5.1</div>
          <div class="stack-detail">Sci-fi Mission Control · Boot animation · Keyboard overlay</div>
        </div>
      </div>
      <div class="stack-card">
        <div class="stack-icon">📡</div>
        <div>
          <div class="stack-layer">Communication</div>
          <div class="stack-tech">WebSocket</div>
          <div class="stack-detail"><code>websocket-client</code> ↔ <code>WebSocketsServer</code> port 81</div>
        </div>
      </div>
      <div class="stack-card">
        <div class="stack-icon">⚡</div>
        <div>
          <div class="stack-layer">Firmware</div>
          <div class="stack-tech">Arduino C++ / ESP32</div>
          <div class="stack-detail">Motor · Servo · Sensor · OLED control loop</div>
        </div>
      </div>
      <div class="stack-card">
        <div class="stack-icon">🌡️</div>
        <div>
          <div class="stack-layer">Sensor Library</div>
          <div class="stack-tech">Adafruit BMP280</div>
          <div class="stack-detail">Temperature · Pressure · Altitude</div>
        </div>
      </div>
      <div class="stack-card">
        <div class="stack-icon">🖥️</div>
        <div>
          <div class="stack-layer">Display Library</div>
          <div class="stack-tech">Adafruit SSD1306 + GFX</div>
          <div class="stack-detail">Dual OLED panels with animated states</div>
        </div>
      </div>
      <div class="stack-card">
        <div class="stack-icon">🦾</div>
        <div>
          <div class="stack-layer">Servo Library</div>
          <div class="stack-tech">ESP32Servo</div>
          <div class="stack-detail">Smooth sweep movement · PWM control</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── KEYBOARD ── -->
  <section>
    <div class="section-label"><h2>⌨️ Keyboard Controls</h2></div>
    <div class="cmd-grid">
      <div class="cmd-group">
        <div class="cmd-group-header">🚗 Movement</div>
        <div class="cmd-row"><span class="cmd-key">↑</span><span class="cmd-dot dot-g"></span><span class="cmd-desc">Drive <strong>Forward</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">↓</span><span class="cmd-dot dot-y"></span><span class="cmd-desc">Drive <strong>Backward</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">←</span><span class="cmd-dot dot-b"></span><span class="cmd-desc">Turn <strong>Left</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">→</span><span class="cmd-dot dot-b"></span><span class="cmd-desc">Turn <strong>Right</strong></span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:10px">REL</span><span class="cmd-dot dot-r"></span><span class="cmd-desc">⚡ <strong>Instant Stop</strong></span></div>
      </div>
      <div class="cmd-group">
        <div class="cmd-group-header">📷 Camera &amp; Gripper</div>
        <div class="cmd-row"><span class="cmd-key">A</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Camera pan <strong>Left</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">D</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Camera pan <strong>Right</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">O</span><span class="cmd-dot dot-g"></span><span class="cmd-desc"><strong>Open</strong> gripper</span></div>
        <div class="cmd-row"><span class="cmd-key">C</span><span class="cmd-dot dot-r"></span><span class="cmd-desc"><strong>Close</strong> gripper</span></div>
        <div class="cmd-row"><span class="cmd-key">?</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Toggle keyboard overlay</span></div>
        <div class="cmd-row"><span class="cmd-key">ESC</span><span class="cmd-dot dot-r"></span><span class="cmd-desc">Exit application</span></div>
      </div>
    </div>
  </section>

  <!-- ── PROTOCOL ── -->
  <section>
    <div class="section-label"><h2>📡 WebSocket Command Protocol</h2></div>
    <div class="cmd-grid">
      <div class="cmd-group">
        <div class="cmd-group-header">→ GUI to ESP32</div>
        <div class="cmd-row"><span class="cmd-key">F</span><span class="cmd-dot dot-g"></span><span class="cmd-desc">Move Forward</span></div>
        <div class="cmd-row"><span class="cmd-key">B</span><span class="cmd-dot dot-y"></span><span class="cmd-desc">Move Backward</span></div>
        <div class="cmd-row"><span class="cmd-key">L</span><span class="cmd-dot dot-b"></span><span class="cmd-desc">Turn Left</span></div>
        <div class="cmd-row"><span class="cmd-key">R</span><span class="cmd-dot dot-b"></span><span class="cmd-desc">Turn Right</span></div>
        <div class="cmd-row"><span class="cmd-key">S</span><span class="cmd-dot dot-r"></span><span class="cmd-desc"><strong>INSTANT STOP</strong></span></div>
        <div class="cmd-row"><span class="cmd-key">A</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Camera pan left</span></div>
        <div class="cmd-row"><span class="cmd-key">D</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Camera pan right</span></div>
        <div class="cmd-row"><span class="cmd-key">O</span><span class="cmd-dot dot-g"></span><span class="cmd-desc">Open gripper</span></div>
        <div class="cmd-row"><span class="cmd-key">C</span><span class="cmd-dot dot-r"></span><span class="cmd-desc">Close gripper</span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:9px">SENSOR</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Request sensor reading</span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:9px">PING</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Latency measurement</span></div>
      </div>
      <div class="cmd-group">
        <div class="cmd-group-header">← ESP32 to GUI</div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:9px">t,p,alt,d</span><span class="cmd-dot dot-y"></span><span class="cmd-desc">Sensor telemetry (CSV)</span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:9px">&lt;angle&gt;</span><span class="cmd-dot dot-c"></span><span class="cmd-desc">Camera position (integer)</span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:8px">GR_OPEN</span><span class="cmd-dot dot-g"></span><span class="cmd-desc">Gripper state confirm</span></div>
        <div class="cmd-row"><span class="cmd-key" style="font-size:8px">GR_CLOSE</span><span class="cmd-dot dot-r"></span><span class="cmd-desc">Gripper state confirm</span></div>
      </div>
    </div>
  </section>

  <!-- ── SAFETY ── -->
  <section>
    <div class="section-label"><h2>🛡️ Safety Features</h2></div>
    <div class="safety-grid">
      <div class="safety-card">
        <div class="safety-indicator ind-green"></div>
        <div>
          <div class="safety-title">⚡ Instant Stop</div>
          <div class="safety-desc">S sent immediately on key release — bypasses all async queues.</div>
          <div class="safety-trigger">Trigger: Any arrow key released</div>
        </div>
      </div>
      <div class="safety-card">
        <div class="safety-indicator ind-amber"></div>
        <div>
          <div class="safety-title">⏱️ GUI Watchdog</div>
          <div class="safety-desc">Auto-sends Stop command after 3 s of no key input. Resets state to IDLE.</div>
          <div class="safety-trigger">Trigger: No input &gt; 3 seconds</div>
        </div>
      </div>
      <div class="safety-card">
        <div class="safety-indicator ind-amber"></div>
        <div>
          <div class="safety-title">⏱️ ESP32 Watchdog</div>
          <div class="safety-desc">Hardware-level motor cutoff independent of GUI state.</div>
          <div class="safety-trigger">Trigger: No command &gt; 500 ms</div>
        </div>
      </div>
      <div class="safety-card">
        <div class="safety-indicator ind-cyan"></div>
        <div>
          <div class="safety-title">🔄 Auto-Reconnect</div>
          <div class="safety-desc">GUI automatically retries WebSocket connection on link drop.</div>
          <div class="safety-trigger">Trigger: Link dropped → retry every 2 s</div>
        </div>
      </div>
      <div class="safety-card">
        <div class="safety-indicator ind-amber"></div>
        <div>
          <div class="safety-title">⚠️ Obstacle Warning</div>
          <div class="safety-desc">Yellow pulsing alert with log entry when proximity threshold breached.</div>
          <div class="safety-trigger">Trigger: Distance &lt; 80 cm</div>
        </div>
      </div>
      <div class="safety-card">
        <div class="safety-indicator ind-red"></div>
        <div>
          <div class="safety-title">🚫 Obstacle Critical</div>
          <div class="safety-desc">Red pulsing alert with log entry for imminent collision risk.</div>
          <div class="safety-trigger">Trigger: Distance &lt; 30 cm</div>
        </div>
      </div>
    </div>
  </section>

  <!-- ── OLED ── -->
  <section>
    <div class="section-label"><h2>🖥️ OLED Display Panels</h2></div>
    <div class="oled-grid">
      <div class="oled-card">
        <div class="oled-screen">[ IDLE ]<br/>&gt; ROVER STANDBY</div>
        <div class="oled-info">
          <div class="oled-addr">I²C 0x3C &nbsp;·&nbsp; LEFT PANEL</div>
          <div class="oled-desc">Drive state: IDLE / FWD / REV / TURN L / TURN R. Pulse rings, motion lines, turn arcs on state change.</div>
        </div>
      </div>
      <div class="oled-card">
        <div class="oled-screen">CAM: 90°<br/>T:25°C P:1013hPa<br/>DIST: 150cm</div>
        <div class="oled-info">
          <div class="oled-addr">I²C 0x3D &nbsp;·&nbsp; RIGHT PANEL</div>
          <div class="oled-desc">Camera servo arc gauge, BMP280 readings, HC-SR04 distance &amp; gripper status with sweeping scan line.</div>
        </div>
      </div>
    </div>
    <div class="overview-box" style="margin-top:14px; font-size:13px;">
      Both OLEDs run a <strong>welcome animation</strong> on boot: border reveal → particle burst → countdown → <strong>GO!</strong> splash.
    </div>
  </section>

  <!-- ── GETTING STARTED ── -->
  <section>
    <div class="section-label"><h2>🚀 Getting Started</h2></div>
    <div class="steps">

      <div class="step">
        <div class="step-num">1</div>
        <div class="step-content">
          <div class="step-title">Flash the ESP32</div>
          <p style="font-size:13px;color:#7AAABB;margin-bottom:14px;">Install these Arduino libraries via the Library Manager:</p>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Library</th><th>Purpose</th></tr></thead>
              <tbody>
                <tr><td><code>ESP32Servo</code></td><td>Servo motor control</td></tr>
                <tr><td><code>WebSockets</code> by Markus Sattler</td><td>WebSocket server</td></tr>
                <tr><td><code>Adafruit BMP280</code></td><td>Temperature &amp; pressure</td></tr>
                <tr><td><code>Adafruit SSD1306</code></td><td>OLED display driver</td></tr>
                <tr><td><code>Adafruit GFX Library</code></td><td>Graphics primitives</td></tr>
              </tbody>
            </table>
          </div>
          <div style="margin-top:14px">
          <div class="code-block">
            <div class="code-header">
              <span class="code-dot cd-r"></span><span class="code-dot cd-y"></span><span class="code-dot cd-g"></span>
              <span class="code-lang">mars_rover_esp32.ino</span>
            </div>
            <pre><span class="cm">// Update Wi-Fi credentials before flashing</span>
<span class="kw">const char*</span> ssid     = <span class="str">"YOUR_WIFI_SSID"</span>;
<span class="kw">const char*</span> password = <span class="str">"YOUR_WIFI_PASSWORD"</span>;</pre>
          </div>
          </div>
          <p style="font-size:12px;color:#6A9EAC;margin-top:10px;">Flash via Arduino IDE. The IP address appears on the <strong>left OLED</strong> after connecting to Wi-Fi.</p>
        </div>
      </div>

      <div class="step">
        <div class="step-num">2</div>
        <div class="step-content">
          <div class="step-title">Run the Python GUI</div>
          <div class="code-block">
            <div class="code-header">
              <span class="code-dot cd-r"></span><span class="code-dot cd-y"></span><span class="code-dot cd-g"></span>
              <span class="code-lang">bash</span>
            </div>
            <pre><span class="cm"># Install Python dependencies</span>
pip install PyQt5 websocket-client

<span class="cm"># Launch Mission Control</span>
python mars_rover_gui.py</pre>
          </div>
          <div class="code-block" style="margin-top:12px">
            <div class="code-header">
              <span class="code-dot cd-r"></span><span class="code-dot cd-y"></span><span class="code-dot cd-g"></span>
              <span class="code-lang">startup dialog</span>
            </div>
            <pre>ws://<span class="num">192.168.x.x</span>:<span class="num">81</span></pre>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- ── FILE STRUCTURE ── -->
  <section>
    <div class="section-label"><h2>📁 Project Structure</h2></div>
    <div class="tree">
      <span class="tree-dir">mars-rover/</span><br/>
      &nbsp;&nbsp;├── <span class="tree-dir">📁 firmware/</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-file">mars_rover_esp32.ino</span>&nbsp;&nbsp;&nbsp;<span class="tree-note">← ESP32 Arduino firmware</span><br/>
      &nbsp;&nbsp;├── <span class="tree-dir">📁 gui/</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-file">mars_rover_gui.py</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-note">← Python PyQt5 Mission Control v5.1</span><br/>
      &nbsp;&nbsp;├── <span class="tree-dir">📁 hardware/</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-dir">pcb/</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-note">← KiCad PCB design files</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-dir">cad/</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="tree-note">← SolidWorks 3D model files</span><br/>
      &nbsp;&nbsp;├── <span class="tree-dir">📁 docs/</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <span class="tree-file">pcb_layout.png</span><br/>
      &nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <span class="tree-file">rover_3d.png</span><br/>
      &nbsp;&nbsp;└── <span class="tree-file">README.md</span>
    </div>
  </section>

  <!-- ── CONTRIBUTING ── -->
  <section>
    <div class="section-label"><h2>🤝 Contributing</h2></div>
    <div class="code-block">
      <div class="code-header">
        <span class="code-dot cd-r"></span><span class="code-dot cd-y"></span><span class="code-dot cd-g"></span>
        <span class="code-lang">bash</span>
      </div>
      <pre>git checkout -b <span class="str">feature/my-feature</span>
git commit -m <span class="str">"Add my feature"</span>
git push origin <span class="str">feature/my-feature</span>
<span class="cm"># Then open a Pull Request on GitHub</span></pre>
    </div>
  </section>

  <!-- ── STATS ── -->
  <div class="stats-bar">
    <div class="stat-cell">
      <div class="stat-num">10</div>
      <div class="stat-label">Components</div>
    </div>
    <div class="stat-cell">
      <div class="stat-num">15</div>
      <div class="stat-label">WebSocket Cmds</div>
    </div>
    <div class="stat-cell">
      <div class="stat-num">6</div>
      <div class="stat-label">Safety Guards</div>
    </div>
    <div class="stat-cell">
      <div class="stat-num">v5.1</div>
      <div class="stat-label">Current Version</div>
    </div>
  </div>

</div><!-- /main -->

<!-- ── FOOTER ── -->
<footer>
  <div class="footer-title">🚀 MARS ROVER MISSION CONTROL</div>
  <div class="footer-sub">◈ v5.1 ENHANCED EDITION &nbsp;·&nbsp; ESP32 · PYTHON · WEBSOCKET · REAL-TIME TELEMETRY ◈</div>
  <div style="margin-top:12px; font-size:11px; color:#1A4A60; font-family:var(--font-mono);">MIT LICENSE &nbsp;·&nbsp; BUILT FOR EXPLORATION</div>
</footer>

</div><!-- /content -->
</body>
</html>
