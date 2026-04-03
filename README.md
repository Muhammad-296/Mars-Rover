<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Mars Rover Mission Control | ESP32 Telemetry Hub</title>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <!-- Google Fonts: Share Tech Mono & Orbitron for sci-fi feel -->
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
        }

        body {
            background: radial-gradient(circle at 20% 30%, #02040A, #000000);
            font-family: 'Share Tech Mono', monospace;
            color: #00E6FF;
            overflow-x: hidden;
            min-height: 100vh;
            padding: 20px;
        }

        /* Animated hex-grid background */
        .grid-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 230, 255, 0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 230, 255, 0.08) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
            animation: gridShift 20s linear infinite;
        }

        @keyframes gridShift {
            0% { transform: translate(0,0); }
            100% { transform: translate(50px, 50px); }
        }

        .main-container {
            position: relative;
            z-index: 2;
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Header wavy animation (replaces typing svg error) */
        .header-badge {
            text-align: center;
            margin-bottom: 30px;
        }
        .glow-text {
            font-family: 'Orbitron', monospace;
            font-size: 3.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00E6FF, #007799);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 15px rgba(0,230,255,0.6);
            letter-spacing: 4px;
            animation: pulseGlow 2.5s ease-in-out infinite;
        }
        @keyframes pulseGlow {
            0% { opacity: 0.9; text-shadow: 0 0 5px #00E6FF; }
            50% { opacity: 1; text-shadow: 0 0 25px #00E6FF, 0 0 10px #00B8CC; }
            100% { opacity: 0.9; text-shadow: 0 0 5px #00E6FF; }
        }
        .sub-mission {
            font-size: 1rem;
            letter-spacing: 3px;
            color: #00B8CC;
            border-top: 1px solid #00E6FF30;
            border-bottom: 1px solid #00E6FF30;
            display: inline-block;
            padding: 8px 20px;
            backdrop-filter: blur(4px);
            animation: borderPulse 3s infinite;
        }
        @keyframes borderPulse {
            0% { border-color: #00E6FF30; }
            50% { border-color: #00E6FFAA; }
            100% { border-color: #00E6FF30; }
        }

        /* Status chips */
        .status-row {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 18px;
            margin: 25px 0;
        }
        .chip {
            background: rgba(0, 24, 34, 0.7);
            backdrop-filter: blur(8px);
            border: 1px solid #00E6FF60;
            border-radius: 60px;
            padding: 8px 20px;
            font-weight: bold;
            font-size: 0.9rem;
            font-family: 'Share Tech Mono', monospace;
            transition: all 0.2s;
            box-shadow: 0 0 8px rgba(0,230,255,0.2);
        }
        .chip i {
            margin-right: 8px;
            color: #00ff91;
        }

        /* Dashboard grid */
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 24px;
            margin-top: 20px;
        }
        .card {
            background: rgba(2, 4, 10, 0.65);
            backdrop-filter: blur(12px);
            border: 1px solid #00E6FF40;
            border-radius: 28px;
            padding: 18px;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        .card:hover {
            border-color: #00E6FF;
            box-shadow: 0 0 20px rgba(0,230,255,0.3);
            transform: translateY(-3px);
        }
        .card-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            border-left: 4px solid #00E6FF;
            padding-left: 12px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        /* Gauges & Telemetry */
        .gauge-group {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 18px;
        }
        .gauge {
            text-align: center;
            width: 110px;
        }
        .gauge canvas {
            width: 100px;
            height: 100px;
        }
        .gauge-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00ffcc;
        }
        .gauge-label {
            font-size: 0.7rem;
            text-transform: uppercase;
        }

        /* Radar (proximity) */
        .radar-container {
            position: relative;
            display: flex;
            justify-content: center;
            margin: 15px 0;
        }
        .radar-ring {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, #001822, #000c12);
            border: 2px solid #00E6FF;
            position: relative;
            animation: radarPulse 1.5s infinite;
        }
        @keyframes radarPulse {
            0% { box-shadow: 0 0 0 0 rgba(0,230,255,0.4); }
            70% { box-shadow: 0 0 0 12px rgba(0,230,255,0); }
            100% { box-shadow: 0 0 0 0 rgba(0,230,255,0); }
        }
        .distance-badge {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #02040A;
            padding: 15px;
            border-radius: 60px;
            font-size: 2rem;
            font-weight: bold;
            border: 1px solid cyan;
        }
        .warning-led {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 6px;
            animation: blink 0.8s infinite;
        }
        @keyframes blink {
            0% { opacity: 0.3; }
            100% { opacity: 1; background-color: #ffaa00; box-shadow: 0 0 8px orange; }
        }

        /* Live Chart canvas */
        .chart-canvas {
            background: #010a0f;
            border-radius: 16px;
            width: 100%;
            height: 150px;
            margin-top: 10px;
            border: 1px solid #00E6FF40;
        }

        /* D-Pad + virtual keys */
        .dpad {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        .dpad-row {
            display: flex;
            gap: 18px;
            justify-content: center;
        }
        .dpad-btn {
            background: #00151e;
            border: 1px solid #00E6FF;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            border-radius: 20px;
            transition: 0.1s linear;
            cursor: pointer;
            color: #00E6FF;
        }
        .dpad-btn:active {
            background: #00E6FF;
            color: #000;
            transform: scale(0.95);
        }
        .key-hint {
            font-size: 0.7rem;
            margin-top: 8px;
            text-align: center;
        }
        .log-area {
            background: #010a0fcc;
            border-radius: 16px;
            padding: 10px;
            height: 140px;
            overflow-y: auto;
            font-size: 0.7rem;
            font-family: monospace;
        }
        .footer-wave {
            margin-top: 40px;
            text-align: center;
            font-size: 0.75rem;
            opacity: 0.7;
        }

        button, .dpad-btn {
            cursor: pointer;
        }

        @media (max-width: 700px) {
            .glow-text { font-size: 2rem; }
        }
    </style>
</head>
<body>
<div class="grid-bg"></div>
<div class="main-container">
    <div class="header-badge">
        <div class="glow-text">🚀 MARS ROVER MISSION CONTROL</div>
        <div class="sub-mission">◈ DRIVE · CAMERA · GRIPPER · TELEMETRY ◈</div>
        <div class="status-row">
            <div class="chip"><i class="fas fa-circle" style="color:#00ff91;"></i> STATUS: OPERATIONAL</div>
            <div class="chip"><i class="fas fa-microchip"></i> VERSION: v5.1 ENHANCED</div>
            <div class="chip"><i class="fab fa-python"></i> GUI: PyQt5 STYLE</div>
            <div class="chip"><i class="fas fa-wifi"></i> WEBSOCKET: ACTIVE</div>
        </div>
    </div>

    <div class="dashboard">
        <!-- Telemetry Gauges Card -->
        <div class="card">
            <div class="card-title"><i class="fas fa-chart-line"></i> REAL-TIME TELEMETRY</div>
            <div class="gauge-group">
                <div class="gauge"><canvas id="tempGauge" width="100" height="100"></canvas><div class="gauge-value" id="tempVal">24.5°C</div><div class="gauge-label">TEMP</div></div>
                <div class="gauge"><canvas id="pressGauge" width="100" height="100"></canvas><div class="gauge-value" id="pressVal">1013 hPa</div><div class="gauge-label">PRESSURE</div></div>
                <div class="gauge"><canvas id="altGauge" width="100" height="100"></canvas><div class="gauge-value" id="altVal">120 m</div><div class="gauge-label">ALTITUDE</div></div>
                <div class="gauge"><canvas id="distGauge" width="100" height="100"></canvas><div class="gauge-value" id="distVal">45 cm</div><div class="gauge-label">DISTANCE</div></div>
            </div>
            <div class="radar-container">
                <div class="radar-ring"></div>
                <div class="distance-badge" id="radarDist">45cm</div>
            </div>
            <div class="key-hint" style="margin-top:5px;"><span id="proxWarning" style="color:#ffaa00;">⚠️ WARN >80cm</span>  |  <span id="proxCrit" style="color:#ff3355;">🔴 CRIT <30cm</span></div>
        </div>

        <!-- Live Scrolling Chart Card (simulated) -->
        <div class="card">
            <div class="card-title"><i class="fas fa-chart-scatter"></i> TELEMETRY HISTORY (4 streams)</div>
            <canvas id="liveChart" class="chart-canvas" width="500" height="150" style="width:100%; height:150px;"></canvas>
            <div class="key-hint">📈 scrolling 80-point history | Temp · Pressure · Alt · Dist</div>
        </div>

        <!-- Rover Control Panel (D-Pad + Gripper + Camera) -->
        <div class="card">
            <div class="card-title"><i class="fas fa-gamepad"></i> MISSION CONTROL & SHORTCUTS</div>
            <div class="dpad">
                <div class="dpad-row"><div class="dpad-btn" data-cmd="F"><i class="fas fa-arrow-up"></i></div></div>
                <div class="dpad-row">
                    <div class="dpad-btn" data-cmd="L"><i class="fas fa-arrow-left"></i></div>
                    <div class="dpad-btn" data-cmd="S"><i class="fas fa-stop"></i></div>
                    <div class="dpad-btn" data-cmd="R"><i class="fas fa-arrow-right"></i></div>
                </div>
                <div class="dpad-row"><div class="dpad-btn" data-cmd="B"><i class="fas fa-arrow-down"></i></div></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 20px;">
                <div><i class="fas fa-camera"></i> CAM PAN: 
                    <button id="camLeft" class="dpad-btn" style="width:50px; height:40px; font-size:1rem;">A</button>
                    <button id="camRight" class="dpad-btn" style="width:50px; height:40px; font-size:1rem;">D</button>
                    <span id="camAngle"> 90°</span>
                </div>
                <div><i class="fas fa-hand-peace"></i> GRIPPER:
                    <button id="gripOpen" class="dpad-btn" style="width:50px; height:40px;">O</button>
                    <button id="gripClose" class="dpad-btn" style="width:50px; height:40px;">C</button>
                    <span id="gripState">CLOSED</span>
                </div>
            </div>
            <div class="key-hint" style="margin-top: 15px;">⌨️ Keyboard: ↑ ↓ ← → (drive) | A/D pan | O/C gripper | S=STOP | ESC to quit (simulated)</div>
            <div class="log-area" id="eventLog">
                [●] SYSTEM READY | WEBSOCKET SIMULATED<br>
                [●] MISSION CONTROL v5.1 ACTIVE<br>
            </div>
        </div>
    </div>

    <div class="footer-wave">
        <i class="fas fa-satellite-dish"></i> ESP32 · WebSocket · BMP280 · Ultrasonic · Dual OLED | 🔒 Safety Watchdog: Auto-Stop after 3s idle
    </div>
</div>

<script>
    // ------------------- SIMULATED TELEMETRY + ANIMATED GAUGES ------------------
    // We simulate ESP32-like telemetry values changing over time (temp, pressure, alt, distance)
    // Also produce camera/gripper commands simulation + rover movement logs.
    // Fix Typing SVG error by removing external dependency, instead we use CSS + JS internal animation.
    
    // Canvas Gauges initialization (simple arc drawing)
    function drawGauge(canvasId, value, minVal, maxVal, color) {
        const canvas = document.getElementById(canvasId);
        if(!canvas) return;
        const ctx = canvas.getContext('2d');
        const w = canvas.width, h = canvas.height;
        ctx.clearRect(0,0,w,h);
        const startAngle = -0.5 * Math.PI;
        const endAngle = startAngle + (Math.PI * 1.8);
        const percent = (value - minVal) / (maxVal - minVal);
        const angle = startAngle + (Math.PI * 1.8) * Math.min(1, Math.max(0, percent));
        ctx.beginPath();
        ctx.arc(w/2, h/2, 38, startAngle, endAngle);
        ctx.strokeStyle = '#225566';
        ctx.lineWidth = 8;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(w/2, h/2, 38, startAngle, angle);
        ctx.strokeStyle = color;
        ctx.stroke();
        ctx.fillStyle = '#00E6FF';
        ctx.font = "bold 18px 'Share Tech Mono'";
        ctx.fillText(Math.floor(value), w/2-12, h/2+8);
    }

    let temp = 24.5, pressure = 1013, altitude = 120, distance = 75;
    let cameraAngle = 90;
    let gripperOpen = false; // false=closed
    let lastCommandTime = Date.now();
    let watchdogInterval;
    let roverMoving = false;
    let currentDir = "IDLE";

    // Event log
    const logDiv = document.getElementById('eventLog');
    function addLog(msg, type="info") {
        const prefix = type==="warn"? "⚠️" : (type==="crit"? "🔴" : "🟢");
        const time = new Date().toLocaleTimeString();
        logDiv.innerHTML += `<div>[${time}] ${prefix} ${msg}</div>`;
        logDiv.scrollTop = logDiv.scrollHeight;
        if(logDiv.children.length > 40) logDiv.removeChild(logDiv.children[0]);
    }

    // Update UI gauges and radar
    function updateTelemetryUI() {
        drawGauge('tempGauge', temp, -10, 60, '#ff884d');
        drawGauge('pressGauge', pressure, 980, 1050, '#88ffaa');
        drawGauge('altGauge', altitude, 0, 500, '#55ccff');
        drawGauge('distGauge', distance, 0, 200, '#ffaa66');
        document.getElementById('tempVal').innerHTML = temp.toFixed(1)+'°C';
        document.getElementById('pressVal').innerHTML = Math.floor(pressure)+' hPa';
        document.getElementById('altVal').innerHTML = Math.floor(altitude)+' m';
        document.getElementById('distVal').innerHTML = Math.floor(distance)+' cm';
        document.getElementById('radarDist').innerHTML = Math.floor(distance)+'cm';
        
        let warnSpan = document.getElementById('proxWarning');
        let critSpan = document.getElementById('proxCrit');
        if(distance < 80 && distance >=30) { warnSpan.innerHTML = '⚠️ WARN obstacle!'; warnSpan.style.color='#ffaa00'; }
        else if(distance < 30) { warnSpan.innerHTML = '🚫 CRITICAL!'; warnSpan.style.color='#ff3355'; addLog(`Obstacle critical! ${distance}cm`, 'crit');}
        else { warnSpan.innerHTML = '✅ CLEAR >80cm'; warnSpan.style.color='#88ff88';}
    }

    // Simulate sensor variation (random walk)
    setInterval(() => {
        temp += (Math.random() - 0.5) * 0.3;
        temp = Math.min(45, Math.max(18, temp));
        pressure += (Math.random() - 0.5) * 1.2;
        pressure = Math.min(1045, Math.max(990, pressure));
        altitude += (Math.random() - 0.5) * 1.5;
        altitude = Math.min(350, Math.max(80, altitude));
        // distance simulation based on rover movement ? but add dynamic changes + random walk
        distance += (Math.random() - 0.5) * 4;
        distance = Math.min(180, Math.max(12, distance));
        updateTelemetryUI();
        addChartData(temp, pressure, altitude, distance);
    }, 1200);

    // ---- LIVE CHART (scrolling) ----
    const chartCanvas = document.getElementById('liveChart');
    const ctxChart = chartCanvas.getContext('2d');
    let chartWidth = chartCanvas.clientWidth, chartHeight = 150;
    function resizeCanvas() { chartCanvas.width = chartCanvas.clientWidth; chartCanvas.height = 150; chartWidth=chartCanvas.width; }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    let dataHistory = []; // store {t,p,alt,d}
    function addChartData(t,p,alt,d) {
        dataHistory.push({t,p,alt,d});
        if(dataHistory.length > 80) dataHistory.shift();
        drawChart();
    }
    function drawChart() {
        if(!ctxChart) return;
        ctxChart.clearRect(0,0,chartWidth,150);
        if(dataHistory.length < 2) return;
        // draw 4 lines normalized: Temp:0-50, Press:980-1050, Alt:0-400, Dist:0-200
        const wStep = chartWidth / (dataHistory.length-1);
        const colors = ['#ff6666','#66ffcc','#ffcc44','#ff9966'];
        const datasets = [
            dataHistory.map(d=> (d.t - 10)/50 * 130),
            dataHistory.map(d=> ((d.p - 980)/70) * 130),
            dataHistory.map(d=> (d.alt / 400) * 130),
            dataHistory.map(d=> (d.dist / 200) * 130)
        ];
        for(let idx=0; idx<4; idx++) {
            ctxChart.beginPath();
            let points = datasets[idx];
            for(let i=0; i<points.length; i++) {
                let x = i * wStep;
                let y = 140 - points[i];
                if(i===0) ctxChart.moveTo(x,y);
                else ctxChart.lineTo(x,y);
            }
            ctxChart.strokeStyle = colors[idx];
            ctxChart.lineWidth = 1.8;
            ctxChart.stroke();
        }
        ctxChart.fillStyle = "#00E6CC";
        ctxChart.font = "8px monospace";
        ctxChart.fillText("Temp|Press|Alt|Dist", 5, 12);
    }
    for(let i=0;i<30;i++) addChartData(24,1013,120,55);
    
    // Rover movement simulation (via keyboard/dpad)
    function sendCommand(cmd) {
        lastCommandTime = Date.now();
        let logMsg = "";
        switch(cmd) {
            case 'F': logMsg = "DRIVE FORWARD"; roverMoving=true; currentDir="FORWARD"; break;
            case 'B': logMsg = "DRIVE BACKWARD"; roverMoving=true; currentDir="BACKWARD"; break;
            case 'L': logMsg = "TURN LEFT"; roverMoving=true; currentDir="LEFT TURN"; break;
            case 'R': logMsg = "TURN RIGHT"; roverMoving=true; currentDir="RIGHT TURN"; break;
            case 'S': logMsg = "INSTANT STOP"; roverMoving=false; currentDir="IDLE"; addLog("Emergency stop triggered", "warn"); break;
            case 'A': cameraAngle = Math.max(0, cameraAngle-15); document.getElementById('camAngle').innerHTML = cameraAngle+"°"; logMsg=`Camera pan LEFT → ${cameraAngle}°`; break;
            case 'D': cameraAngle = Math.min(180, cameraAngle+15); document.getElementById('camAngle').innerHTML = cameraAngle+"°"; logMsg=`Camera pan RIGHT → ${cameraAngle}°`; break;
            case 'O': gripperOpen=true; document.getElementById('gripState').innerHTML="OPEN"; logMsg="Gripper OPENED"; break;
            case 'C': gripperOpen=false; document.getElementById('gripState').innerHTML="CLOSED"; logMsg="Gripper CLOSED"; break;
            default: return;
        }
        if(cmd === 'S') roverMoving=false;
        if(['F','B','L','R'].includes(cmd)) addLog(`Movement: ${logMsg}`, "info");
        else addLog(`${logMsg}`, "info");
        if(['F','B','L','R'].includes(cmd)) {
            // small effect: modify distance while moving? just simulation touch
            setTimeout(() => { if(roverMoving) distance = Math.min(180, distance+ (cmd==='F'? -2 : (cmd==='B'? 3 : 1))); updateTelemetryUI(); }, 100);
        }
        updateRoverVisual();
    }

    function updateRoverVisual() {
        // visual feedback on dpad highlight (no external animation heavy)
        const btns = document.querySelectorAll('.dpad-btn');
        btns.forEach(btn=>btn.style.background='#00151e');
        if(currentDir === 'FORWARD') document.querySelector('[data-cmd="F"]').style.background='#006688';
        if(currentDir === 'BACKWARD') document.querySelector('[data-cmd="B"]').style.background='#006688';
        if(currentDir === 'LEFT TURN') document.querySelector('[data-cmd="L"]').style.background='#006688';
        if(currentDir === 'RIGHT TURN') document.querySelector('[data-cmd="R"]').style.background='#006688';
    }
    
    // Watchdog: auto-stop after 3s inactivity
    watchdogInterval = setInterval(() => {
        if(roverMoving && (Date.now() - lastCommandTime) > 3000) {
            sendCommand('S');
            addLog("🛡️ Safety Watchdog: No command for 3s -> Auto STOP", "warn");
            roverMoving=false;
            currentDir="IDLE";
            updateRoverVisual();
        }
    }, 1000);

    // Attach event listeners to dpad and buttons
    document.querySelectorAll('.dpad-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            let cmd = btn.getAttribute('data-cmd');
            if(cmd) sendCommand(cmd);
        });
    });
    document.getElementById('camLeft').addEventListener('click',()=>sendCommand('A'));
    document.getElementById('camRight').addEventListener('click',()=>sendCommand('D'));
    document.getElementById('gripOpen').addEventListener('click',()=>sendCommand('O'));
    document.getElementById('gripClose').addEventListener('click',()=>sendCommand('C'));
    
    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
        const key = e.key;
        e.preventDefault();
        switch(key) {
            case 'ArrowUp': sendCommand('F'); break;
            case 'ArrowDown': sendCommand('B'); break;
            case 'ArrowLeft': sendCommand('L'); break;
            case 'ArrowRight': sendCommand('R'); break;
            case 's': case 'S': sendCommand('S'); break;
            case 'a': case 'A': sendCommand('A'); break;
            case 'd': case 'D': sendCommand('D'); break;
            case 'o': case 'O': sendCommand('O'); break;
            case 'c': case 'C': sendCommand('C'); break;
            case 'Escape': addLog("ESC pressed - GUI close (simulated)","info"); break;
            default: break;
        }
        // extra for stop on key up? we just implement stop only on S, but also safety watch.
        if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(key)) {
            // for instant stop on key release we add separate listener
        }
    });
    window.addEventListener('keyup', (e) => {
        if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) {
            sendCommand('S');
            addLog("Key released → Instant STOP", "warn");
        }
    });
    
    // simulated telemetry ping and boot animation effect
    addLog("[BOOT] Mission Control v5.1 Enhanced | WebSocket Simulated", "info");
    addLog("[POST] ESP32-CAM online · BMP280 ok · Dual OLED ready", "info");
    setInterval(() => {
        addLog(`[TELEM] T:${temp.toFixed(1)}°C  P:${Math.floor(pressure)}hPa  Dist:${Math.floor(distance)}cm`, "info");
    }, 8000);
    
    // additional animated ring effect for radar (JS pulse)
    setInterval(() => {
        const ring = document.querySelector('.radar-ring');
        if(ring) ring.style.animation = 'none';
        setTimeout(()=> { if(ring) ring.style.animation = 'radarPulse 1.5s infinite'; }, 10);
    }, 2000);
    
    // initial gauge draw
    updateTelemetryUI();
    drawChart();
    document.getElementById('camAngle').innerHTML = "90°";
    document.getElementById('gripState').innerHTML = "CLOSED";
    // show rover idle animation
    setInterval(() => {
        if(!roverMoving && currentDir!="IDLE") { currentDir="IDLE"; updateRoverVisual(); }
    }, 500);
</script>
</body>
</html>
