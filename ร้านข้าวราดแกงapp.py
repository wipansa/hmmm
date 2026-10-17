import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="เกมร้านข้าวราดแกงลุงสมชาย", layout="wide")

game_html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ร้านข้าวราดแกงลุงสมชาย</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Charm:wght@700&family=Kalam:wght@700&family=Mali:ital,wght@0,500;0,700;1,500&family=Prompt:wght@400;500;600;700&family=Srisakdi:wght@700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Prompt', sans-serif;
            background-color: #f7f3ed;
            margin: 0;
            padding: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: background-color 1s;
        }

        body.morning { background-color: #f7f3ed; }
        body.midday { background-color: #fffde7; }
        body.evening { background-color: #fbe9e7; }
        body.rainy { background-color: #eceff1; }

        /* Login Screen Overlay */
        .login-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
        }
        .login-card {
            background: #fffefb;
            border: 3px solid #8d6e63;
            border-radius: 16px;
            padding: 25px 35px;
            width: 320px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .login-card h2 { color: #5d4037; margin-top: 0; margin-bottom: 15px; font-size: 22px; }
        .login-input {
            width: 100%;
            padding: 10px;
            font-family: 'Prompt', sans-serif;
            font-size: 14px;
            border: 1px solid #d7ccc8;
            border-radius: 8px;
            margin-bottom: 15px;
            box-sizing: border-box;
            text-align: center;
        }
        .login-btn {
            width: 100%;
            padding: 10px;
            background: #81c784;
            color: #1b5e20;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        .login-btn:hover { background: #66bb6a; }

        /* Header & Top Bar */
        .header-container {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 12px;
            width: 1080px;
            justify-content: space-between;
        }

        .shop-title-box {
            border: 2px solid #8d6e63;
            background: #fff8f0;
            padding: 8px 30px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(141, 110, 99, 0.15);
            display: flex;
            align-items: center;
            gap: 12px;
        }
        h1 { color: #5d4037; margin: 0; font-size: 22px; font-weight: 700; }
        .player-tag { font-size: 12px; color: #8d6e63; background: #efebe9; padding: 3px 8px; border-radius: 6px; cursor: pointer; }

        .env-badge {
            background: #ffffff;
            border: 1px solid #d7ccc8;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            color: #5d4037;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .action-btns {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
        }

        .btn-main {
            padding: 8px 18px;
            font-size: 13px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            transition: 0.2s;
        }
        .btn-shop-status.close { background: #e57373; color: white; }
        .btn-shop-status.open { background: #81c784; color: #1b5e20; }
        .btn-store { background: #ffb74d; color: #e65100; }
        .btn-store:hover { background: #ffa726; }

        .game-container {
            display: flex;
            gap: 15px;
            width: 1080px;
            position: relative;
        }

        /* 1. ออเดอร์ (ซ้าย) */
        .orders-area {
            display: flex;
            flex-direction: column;
            gap: 12px;
            width: 230px;
        }

        .order-box {
            background: #fffdf7;
            border: 1px solid #e0d7c6;
            padding: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border-radius: 12px;
            position: relative;
        }
        .order-box.active-box {
            border: 2px solid #a1887f;
            background: #fffaf0;
        }
        .order-box h3 { margin-top: 0; color: #6d4c41; font-size: 14px; font-weight: 600; margin-bottom: 8px; }
        .order-list { list-style: none; padding: 0; margin: 0 0 10px 0; }
        
        .order-item { 
            font-size: 15px; 
            margin-bottom: 4px; 
            color: #3e2723; 
            line-height: 1.2;
        }
        
        .handwrite-1 { font-family: 'Mali', cursive; font-weight: 700; }
        .handwrite-2 { font-family: 'Charm', cursive; font-size: 16px; }
        .handwrite-3 { font-family: 'Srisakdi', cursive; font-size: 16px; }
        .handwrite-4 { font-family: 'Kalam', cursive; font-size: 16px; }

        .order-item.done { text-decoration: line-through; color: #81c784; opacity: 0.8; }

        .timer-bar-container {
            width: 100%;
            background: #efebe9;
            height: 7px;
            border-radius: 4px;
            margin-bottom: 8px;
            overflow: hidden;
        }
        .timer-bar {
            height: 100%;
            background: #dce775;
            width: 100%;
            transition: width 1s linear;
        }

        .serve-btn {
            width: 100%;
            padding: 6px;
            background: #cfd8dc;
            color: #fff;
            border: none;
            font-size: 12px;
            font-weight: 600;
            border-radius: 6px;
            cursor: not-allowed;
        }
        .serve-btn.active {
            background: #81c784;
            color: #1b5e20;
            cursor: pointer;
            box-shadow: 0 3px 6px rgba(129, 199, 132, 0.4);
        }

        .order-alert {
            font-size: 11px;
            color: #e57373;
            margin-top: 4px;
            font-weight: 500;
            text-align: center;
        }

        /* 2. พื้นที่ทำอาหาร (กลาง) */
        .kitchen-area {
            flex: 1;
            background: #ffffff;
            padding: 18px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
        }
        .kitchen-area h3 { margin-top: 0; color: #4e342e; font-size: 14px; font-weight: 600; margin-bottom: 10px; }

        .top-kitchen-row {
            display: flex;
            gap: 10px;
            margin-bottom: 12px;
            width: 100%;
            align-items: center;
        }

        .plate-box {
            width: 75px;
            height: 75px;
            border: 2px dashed #bcaaa4;
            border-radius: 50%;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            background: #fff8e1;
            padding: 4px;
            box-sizing: border-box;
            text-align: center;
            position: relative;
        }

        .smoke-effect {
            position: absolute;
            top: -15px;
            font-size: 15px;
            animation: floatUp 1s infinite alternate;
            display: none;
        }
        @keyframes floatUp {
            0% { transform: translateY(0) scale(0.9); opacity: 0.6; }
            100% { transform: translateY(-8px) scale(1.2); opacity: 1; }
        }

        .dish-box {
            flex: 1;
            background: #fafafa;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #eee;
            min-height: 45px;
            font-size: 12px;
        }

        .cooking-alert {
            width: 100%;
            background: #f1f8e9;
            color: #558b2f;
            padding: 6px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
            text-align: center;
            margin-bottom: 8px;
            display: none;
        }

        .ing-tabs {
            display: flex;
            gap: 6px;
            width: 100%;
            margin-bottom: 10px;
        }
        .tab-btn {
            flex: 1;
            padding: 6px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid #d7ccc8;
            background: #f5f5f5;
            color: #6d4c41;
            border-radius: 6px;
            cursor: pointer;
        }
        .tab-btn.active {
            background: #8d6e63;
            color: white;
            border-color: #8d6e63;
        }

        .ingredients-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            width: 100%;
            margin-bottom: 12px;
            max-height: 220px;
            overflow-y: auto;
        }
        .ing-btn {
            padding: 6px;
            background: #a1887f;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 500;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            transition: 0.1s;
        }
        .ing-btn:hover { background: #8d6e63; }
        .ing-btn span { font-size: 9px; opacity: 0.85; }

        .selected-item-tag {
            display: inline-block;
            background: #ffe0b2;
            color: #e65100;
            padding: 2px 6px;
            margin: 2px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 10px;
            font-weight: 500;
        }
        .selected-item-tag:hover { text-decoration: line-through; }

        .cook-btn {
            width: 100%;
            padding: 9px;
            background: #d7ccc8;
            color: #4e342e;
            border: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 4px;
            transition: 0.2s;
        }
        .cook-btn:hover { background: #bcaaa4; }

        /* 3. หนังสือสูตรอาหาร (ขวา) */
        .recipe-book {
            width: 270px;
            background: #fffde7;
            border: 1px solid #fff59d;
            padding: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            border-radius: 12px;
            height: fit-content;
            font-family: 'Mali', cursive;
        }
        .recipe-book h3 { margin-top: 0; color: #f57f17; font-size: 15px; font-weight: 700; margin-bottom: 8px; }
        .recipe-book ul { padding-left: 0; list-style: none; margin: 0; font-size: 11px; color: #5d4037; }
        .recipe-book li { 
            margin-bottom: 5px; 
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Dashboard เลเวล & เงิน */
        .status-panel {
            position: absolute;
            bottom: -55px;
            right: 0;
            display: flex;
            gap: 10px;
        }
        .stat-box {
            color: white;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .level-box { background: #7e57c2; }
        .fame-box { background: #ffb74d; }
        .money-box { background: #81c784; }

        /* Modals */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(3px);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal-card {
            background: #fffefb;
            border: 3px solid #8d6e63;
            border-radius: 16px;
            padding: 20px 28px;
            width: 360px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            font-family: 'Prompt', sans-serif;
        }
        .modal-card h2 { color: #5d4037; margin-top: 0; margin-bottom: 12px; font-size: 20px; text-align: center; }

        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 13px;
            color: #4e342e;
            border-bottom: 1px dashed #efebe9;
            padding-bottom: 4px;
        }
        .summary-total {
            font-size: 15px;
            font-weight: bold;
            color: #2e7d32;
            margin-top: 10px;
            border-bottom: none;
        }

        .shop-items-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 280px;
            overflow-y: auto;
            margin-bottom: 12px;
        }
        .shop-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #fdfbf7;
            border: 1px solid #e0d7c6;
            padding: 8px 12px;
            border-radius: 8px;
        }
        .shop-item-info strong { display: block; font-size: 13px; color: #4e342e; }
        .shop-item-info span { font-size: 10px; color: #8d6e63; }
        .buy-btn {
            padding: 5px 12px;
            font-size: 11px;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            background: #81c784;
            color: #1b5e20;
        }
        .buy-btn:disabled {
            background: #e0e0e0;
            color: #9e9e9e;
            cursor: not-allowed;
        }

        .close-modal-btn {
            width: 100%;
            padding: 7px;
            background: #8d6e63;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body class="morning">

    <!-- หน้าต่าง Login / ใส่ชื่อผู้เล่น -->
    <div class="login-overlay" id="loginModal">
        <div class="login-card">
            <h2>🍳 เข้าสู่ระบบร้านข้าวแกง</h2>
            <p style="font-size: 12px; color: #795548; margin-bottom: 15px;">ใส่ชื่อของคุณเพื่อบันทึกความก้าวหน้าและเลเวล</p>
            <input type="text" id="usernameInput" class="login-input" placeholder="พิมพ์ชื่อผู้เล่น..." maxlength="15">
            <button class="login-btn" onclick="handleLogin()">เริ่มเปิดร้าน!</button>
        </div>
    </div>

    <div class="header-container">
        <div class="shop-title-box">
            <h1>ร้านข้าวราดแกงลุงสมชาย</h1>
            <span class="player-tag" id="playerTagDisplay" onclick="logout()" title="คลิกเพื่อเปลี่ยนผู้เล่น">👤 ผู้เล่น: -</span>
        </div>
        <div class="env-badge" id="envBadge">🌅 เช้าสดใส | ☀️ แดดอบอุ่น</div>
    </div>

    <div class="action-btns">
        <button id="shopBtn" class="btn-main btn-shop-status close" onclick="toggleShopStatus()">CLOSE (ร้านปิด)</button>
        <button class="btn-main btn-store" onclick="openShopModal()">🛒 ร้านค้าอุปกรณ์</button>
    </div>

    <div class="game-container">
        <!-- 1. ออเดอร์ (ซ้าย) -->
        <div class="orders-area" id="ordersArea"></div>

        <!-- 2. พื้นที่ทำอาหาร (กลาง) -->
        <div class="kitchen-area">
            <h3>🍳 เลือกวัตถุดิบลงจาน (ทำคิวบนสุดก่อน)</h3>
            
            <div class="cooking-alert" id="cookingAlert">แจ้งเตือน</div>

            <div class="ing-tabs">
                <button class="tab-btn active" onclick="switchTab('food')">🍚 ข้าวแกง</button>
                <button class="tab-btn" onclick="switchTab('drink')">🥤 เครื่องดื่ม</button>
                <button class="tab-btn" onclick="switchTab('dessert')">🍰 ขนมหวาน</button>
            </div>

            <div class="ingredients-grid" id="ingredientsGrid"></div>

            <div class="top-kitchen-row" style="width: 100%;">
                <div class="plate-box" id="plateBox" title="จานข้าว">
                    <div class="smoke-effect" id="smokeEffect">♨️</div>
                    <span id="plateEmojis">🍽️</span>
                </div>
                <div class="dish-box">
                    <strong>วัตถุดิบที่เลือก:</strong> <span id="currentSelection" style="color: #a1887f;">- คลิกเลือกวัตถุดิบ -</span><br>
                    <div id="selectedTagsContainer" style="margin-top: 4px;"></div>
                </div>
            </div>

            <button class="cook-btn" onclick="cookDish()">🔥 COOK (ยืนยันทำเมนู)</button>
        </div>

        <!-- 3. หนังสือสูตรอาหาร (ขวา) -->
        <div class="recipe-book">
            <h3>📖 สมุดสูตรอาหาร</h3>
            <ul id="recipeList"></ul>
        </div>

        <!-- Dashboard เลเวล & เงิน -->
        <div class="status-panel">
            <div class="stat-box level-box" id="levelDisplay">🎖️ Lv.1 (0/100 EXP)</div>
            <div class="stat-box fame-box" id="fameDisplay">⭐ 5.0 (100%)</div>
            <div class="stat-box money-box">💰 <span id="score">150</span> บาท</div>
        </div>
    </div>

    <!-- Modal สรุปยอด -->
    <div class="modal-overlay" id="summaryModal">
        <div class="modal-card">
            <h2>📊 สรุปยอดขายวันนี้</h2>
            <div class="summary-row"><span>รายได้ทั้งหมด:</span><span id="sumRevenue">0 บาท</span></div>
            <div class="summary-row"><span>ค่าวัตถุดิบ:</span><span id="sumCosts">0 บาท</span></div>
            <div class="summary-row summary-total"><span>กำไรสุทธิ:</span><span id="sumProfit">0 บาท</span></div>
            <div class="summary-row" style="margin-top:8px;"><span>เสิร์ฟสำเร็จ:</span><span id="sumServed">0 ออเดอร์</span></div>
            <div class="summary-row"><span>ดาวความนิยม:</span><span id="sumStars">⭐ 5.0</span></div>
            <button class="close-modal-btn" style="margin-top: 12px;" onclick="closeModal('summaryModal')">ตกลง</button>
        </div>
    </div>

    <!-- Modal ร้านค้า -->
    <div class="modal-overlay" id="shopModal">
        <div class="modal-card">
            <h2>🛒 ร้านค้าอุปกรณ์ & ปลดล็อก</h2>
            <div class="shop-items-list" id="shopItemsList"></div>
            <button class="close-modal-btn" onclick="closeModal('shopModal')">ปิดหน้าต่าง</button>
        </div>
    </div>

    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            if (type === 'click') {
                osc.frequency.setValueAtTime(400, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
                osc.start(); osc.stop(audioCtx.currentTime + 0.05);
            } else if (type === 'cook') {
                let bufferSize = audioCtx.sampleRate * 0.3;
                let buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
                let data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
                let noise = audioCtx.createBufferSource();
                noise.buffer = buffer;
                let noiseGain = audioCtx.createGain();
                noiseGain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                noiseGain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                noise.connect(noiseGain); noiseGain.connect(audioCtx.destination); noise.start();
            } else if (type === 'serve') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(800, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
                osc.start(); osc.stop(audioCtx.currentTime + 0.4);
            }
        }

        const levelRequirements = [
            { level: 1, name: "มือใหม่", exp: 0 },
            { level: 2, name: "ขาประจำซอย", exp: 100 },
            { level: 3, name: "ขวัญใจวัยทำงาน", exp: 250 },
            { level: 4, name: "สตรีทฟู้ดเจ้าดัง", exp: 450 },
            { level: 5, name: "คาเฟ่โฮมเมด", exp: 700 },
            { level: 6, name: "ขวัญใจยามเย็น", exp: 1000 },
            { level: 7, name: "ร้านดังระดับเมือง", exp: 1400 },
            { level: 8, name: "ร้านดังระดับจังหวัด", exp: 1900 },
            { level: 9, name: "เชฟระดับประเทศ", exp: 2500 },
            { level: 10, name: "ตำนานข้าวแกงลุงสมชาย", exp: 3200 }
        ];

        let shopUpgrades = [
            { id: 'cooler', name: '🧊 ตู้แช่น้ำเย็น', price: 150, reqLevel: 2, desc: 'ปลดล็อก: น้ำเย็น, น้ำส้ม', unlocked: false },
            { id: 'fridge', name: '🥤 ตู้แช่เครื่องดื่มกระป๋อง', price: 300, reqLevel: 3, desc: 'ปลดล็อก: โค้ก, น้ำแดง, น้ำเขียว', unlocked: false },
            { id: 'juice_bar', name: '🥥 ซุ้มน้ำผลไม้สด', price: 500, reqLevel: 4, desc: 'ปลดล็อก: น้ำมะพร้าวสด', unlocked: false },
            { id: 'coffee_machine', name: '☕ เครื่องชงกาแฟโบราณ', price: 800, reqLevel: 5, desc: 'ปลดล็อก: เมล็ดกาแฟ, นมข้น', unlocked: false },
            { id: 'bar_fridge', name: '🍺 ตู้แช่เครื่องดื่มสายดื่ม', price: 1200, reqLevel: 6, desc: 'ปลดล็อก: เบียร์เย็น (ทิปหนัก)', unlocked: false },
            { id: 'dessert_case', name: '🍰 ตู้โชว์เบเกอรี & ขนมหวาน', price: 1800, reqLevel: 7, desc: 'ปลดล็อก: ขนมหวานทานเล่น', unlocked: false },
            { id: 'shaved_ice', name: '❄️ เครื่องทำน้ำแข็งไส', price: 3500, reqLevel: 8, desc: 'ปลดล็อก: เมนูน้ำแข็งไส', unlocked: false },
            { id: 'neon_sign', name: '✨ ป้ายร้านไฟนีออนวินเทจ', price: 5000, reqLevel: 10, desc: 'เพิ่มเงินและดาวความนิยม 1.5 เท่า', unlocked: false }
        ];

        const allIngredients = {
            "ไก่": { cost: 12, emoji: "🍗", category: "food" },
            "หมู": { cost: 15, emoji: "🥩", category: "food" },
            "กุ้ง": { cost: 25, emoji: "🦐", category: "food" },
            "พริกแกง": { cost: 8, emoji: "🌶️", category: "food" },
            "กะทิ": { cost: 10, emoji: "🥥", category: "food" },
            "น้ำซุป": { cost: 5, emoji: "🍲", category: "food" },
            "ใบกะเพรา": { cost: 5, emoji: "🌿", category: "food" },
            "มะเขือเปราะ": { cost: 6, emoji: "🍆", category: "food" },
            "ใบมะกรูด": { cost: 4, emoji: "🍃", category: "food" },
            "ผักกาดขาว": { cost: 6, emoji: "🥬", category: "food" },
            "เห็ด": { cost: 10, emoji: "🍄", category: "food" },
            "กระเทียม": { cost: 5, emoji: "🧄", category: "food" },
            "สมุนไพร": { cost: 8, emoji: "🌿", category: "food" },
            "ไข่": { cost: 6, emoji: "🥚", category: "food" },
            "เต้าหู้": { cost: 8, emoji: "🟡", category: "food" },
            
            "น้ำเย็น": { cost: 0, emoji: "🧊", category: "drink", reqItem: "cooler" },
            "น้ำส้ม": { cost: 10, emoji: "🍊", category: "drink", reqItem: "cooler" },
            "โค้ก": { cost: 12, emoji: "🥤", category: "drink", reqItem: "fridge" },
            "น้ำแดง": { cost: 10, emoji: "🔴", category: "drink", reqItem: "fridge" },
            "น้ำเขียว": { cost: 10, emoji: "🟢", category: "drink", reqItem: "fridge" },
            "น้ำมะพร้าว": { cost: 18, emoji: "🥥", category: "drink", reqItem: "juice_bar" },
            "เมล็ดกาแฟ": { cost: 12, emoji: "☕", category: "drink", reqItem: "coffee_machine" },
            "นมข้น": { cost: 8, emoji: "🥛", category: "drink", reqItem: "coffee_machine" },
            "เบียร์": { cost: 35, emoji: "🍺", category: "drink", reqItem: "bar_fridge" },

            "เค้ก": { cost: 25, emoji: "🍰", category: "dessert", reqItem: "dessert_case" },
            "น้ำแข็งไส": { cost: 15, emoji: "🍧", category: "dessert", reqItem: "shaved_ice" }
        };

        const recipes = {
            "แกงเขียวหวาน": { ingredients: ["ไก่", "พริกแกง", "กะทิ", "มะเขือเปราะ"], extraPrice: 5, type: "food" },
            "พะแนง": { ingredients: ["หมู", "พริกแกง", "กะทิ", "ใบมะกรูด"], extraPrice: 5, type: "food" },
            "ต้มยำกุ้ง": { ingredients: ["กุ้ง", "น้ำซุป", "เห็ด", "สมุนไพร"], extraPrice: 15, type: "food" },
            "ต้มจืด": { ingredients: ["เต้าหู้", "น้ำซุป", "ผักกาดขาว"], extraPrice: 0, type: "food" },
            "ผัดกะเพรา": { ingredients: ["หมู", "ใบกะเพรา"], extraPrice: 0, type: "food" },
            "ไข่พะโล้": { ingredients: ["หมู", "ไข่", "เต้าหู้"], extraPrice: 0, type: "food" },
            "ผัดพริกแกง": { ingredients: ["หมู", "พริกแกง", "ใบมะกรูด"], extraPrice: 0, type: "food" },
            "หมูกระเทียม": { ingredients: ["หมู", "กระเทียม", "สมุนไพร"], extraPrice: 5, type: "food" },
            
            "กาแฟเย็น": { ingredients: ["เมล็ดกาแฟ", "นมข้น"], extraPrice: 20, type: "drink" },
            "โอเลี้ยง": { ingredients: ["เมล็ดกาแฟ"], extraPrice: 15, type: "drink" },
            "น้ำส้มคั้น": { ingredients: ["น้ำส้ม"], extraPrice: 15, type: "drink" },
            "โค้กเย็น": { ingredients: ["โค้ก"], extraPrice: 18, type: "drink" },
            "น้ำแดงโซดา": { ingredients: ["น้ำแดง"], extraPrice: 15, type: "drink" },
            "น้ำเขียวโซดา": { ingredients: ["น้ำเขียว"], extraPrice: 15, type: "drink" },
            "น้ำมะพร้าวสด": { ingredients: ["น้ำมะพร้าว"], extraPrice: 25, type: "drink" },
            "เบียร์เย็น": { ingredients: ["เบียร์"], extraPrice: 45, type: "drink" },
            "เค้กโฮมเมด": { ingredients: ["เค้ก"], extraPrice: 30, type: "dessert" },
            "น้ำแข็งไสหวานเย็น": { ingredients: ["น้ำแข็งไส"], extraPrice: 25, type: "dessert" }
        };

        const handwriteClasses = ['handwrite-1', 'handwrite-2', 'handwrite-3', 'handwrite-4'];

        let currentUser = "";
        let score = 150;
        let fame = 100;
        let exp = 0;
        let level = 1;
        let isGameOpen = false;
        let orders = [];
        let cookedDishes = [];
        let selectedIngredients = [];
        let selectedEmojis = [];
        let orderAlerts = {};
        let nextOrderTimer = 15;
        let currentTab = "food";

        let gameTimeState = "morning";
        let weatherState = "sunny";

        let dailyRevenue = 0;
        let dailyCosts = 0;
        let dailyServedCount = 0;

        // ตรวจสอบข้อมูลเซฟเดิมเมื่อโหลดหน้า
        window.onload = function() {
            let savedUser = localStorage.getItem("somchai_last_user");
            if (savedUser) {
                document.getElementById("usernameInput").value = savedUser;
            }
        };

        function handleLogin() {
            let name = document.getElementById("usernameInput").value.trim();
            if (!name) {
                alert("กรุณากรอกชื่อผู้เล่นก่อนครับ!");
                return;
            }
            currentUser = name;
            localStorage.setItem("somchai_last_user", currentUser);
            document.getElementById("playerTagDisplay").innerText = `👤 ${currentUser}`;
            document.getElementById("loginModal").style.display = "none";

            loadGameData();
            renderIngredients();
            renderRecipeBook();
            updateUI();
        }

        function logout() {
            if (confirm("ต้องการเปลี่ยนผู้เล่นหรือออกจากระบบหรือไม่?")) {
                saveGameData();
                location.reload();
            }
        }

        // ระบบบันทึกข้อมูลลง localStorage
        function saveGameData() {
            if (!currentUser) return;
            let saveData = {
                score: score,
                fame: fame,
                exp: exp,
                level: level,
                upgrades: shopUpgrades.map(u => ({ id: u.id, unlocked: u.unlocked }))
            };
            localStorage.setItem("somchai_save_" + currentUser, JSON.stringify(saveData));
        }

        // โหลดข้อมูลจาก localStorage
        function loadGameData() {
            let saved = localStorage.getItem("somchai_save_" + currentUser);
            if (saved) {
                try {
                    let data = JSON.parse(saved);
                    score = data.score ?? 150;
                    fame = data.fame ?? 100;
                    exp = data.exp ?? 0;
                    level = data.level ?? 1;
                    if (data.upgrades) {
                        data.upgrades.forEach(savedItem => {
                            let item = shopUpgrades.find(u => u.id === savedItem.id);
                            if (item) item.unlocked = savedItem.unlocked;
                        });
                    }
                } catch(e) { console.error("Load save error", e); }
            }
        }

        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            renderIngredients();
        }

        function renderIngredients() {
            let html = "";
            for (let [name, data] of Object.entries(allIngredients)) {
                if (data.category === currentTab) {
                    let isUnlocked = !data.reqItem || shopUpgrades.find(u => u.id === data.reqItem)?.unlocked;
                    if (isUnlocked) {
                        html += `
                            <button class="ing-btn" onclick="selectIngredient('${name}', '${data.emoji}')">
                                ${data.emoji} ${name} <span>(${data.cost}บ.)</span>
                            </button>
                        `;
                    }
                }
            }
            if (html === "") {
                html = `<div style="grid-column: span 3; text-align:center; font-size:12px; color:#8d6e63; padding:15px;">🔒 ต้องซื้ออุปกรณ์จากร้านค้าเพื่อปลดล็อกหมวดนี้</div>`;
            }
            document.getElementById("ingredientsGrid").innerHTML = html;
        }

        function renderRecipeBook() {
            let html = "";
            for (let [name, data] of Object.entries(recipes)) {
                let allIngUnlocked = data.ingredients.every(ing => {
                    let req = allIngredients[ing]?.reqItem;
                    return !req || shopUpgrades.find(u => u.id === req)?.unlocked;
                });
                if (allIngUnlocked) {
                    html += `<li><strong>${name}:</strong> ${data.ingredients.join(' + ')}</li>`;
                }
            }
            document.getElementById("recipeList").innerHTML = html;
        }

        function toggleShopStatus() {
            isGameOpen = !isGameOpen;
            const btn = document.getElementById("shopBtn");
            if (isGameOpen) {
                btn.className = "btn-main btn-shop-status open";
                btn.innerText = "OPEN (เปิดร้านแล้ว)";
                dailyRevenue = 0; dailyCosts = 0; dailyServedCount = 0;
                weatherState = Math.random() > 0.6 ? "rainy" : "sunny";
                updateEnvDisplay();
                if (orders.length === 0) addNewOrder();
            } else {
                btn.className = "btn-main btn-shop-status close";
                btn.innerText = "CLOSE (ร้านปิด)";
                saveGameData(); // เซฟเกมอัตโนมัติเมื่อปิดร้าน
                showSummaryModal();
            }
            updateUI();
        }

        function updateEnvDisplay() {
            const body = document.body;
            body.className = `${gameTimeState} ${weatherState}`;
            let timeText = gameTimeState === "morning" ? "🌅 เช้าสดใส" : (gameTimeState === "midday" ? "☀️ กลางวัน" : "🌆 เย็นอบอุ่น");
            let weatherText = weatherState === "sunny" ? "☀️ แดดอบอุ่น" : "🌧️ ฝนตกซู่ซ่า (ลูกค้ารอนานขึ้น 20%)";
            document.getElementById("envBadge").innerText = `${timeText} | ${weatherText}`;
        }

        function createOrderObject() {
            let availableRecipes = Object.keys(recipes).filter(name => {
                return recipes[name].ingredients.every(ing => {
                    let req = allIngredients[ing]?.reqItem;
                    return !req || shopUpgrades.find(u => u.id === req)?.unlocked;
                });
            });

            let numDish = Math.floor(Math.random() * 2) + 1;
            let selectDishes = [];
            while (selectDishes.length < numDish) {
                let randomDish = availableRecipes[Math.floor(Math.random() * availableRecipes.length)];
                if (!selectDishes.map(d => d.name).includes(randomDish)) {
                    let fontClass = handwriteClasses[Math.floor(Math.random() * handwriteClasses.length)];
                    selectDishes.push({ name: randomDish, font: fontClass });
                }
            }
            
            let timeMultiplier = weatherState === "rainy" ? 1.2 : 1.0;
            let totalTime = Math.round(50 * timeMultiplier);

            return {
                id: Date.now() + Math.random(),
                dishes: selectDishes,
                timeLeft: totalTime,
                maxTime: totalTime
            };
        }

        setInterval(() => {
            if (!isGameOpen) return;

            orders.forEach(order => { order.timeLeft--; });

            if (orders.length > 0) {
                if (orders[0].timeLeft <= 0) {
                    let penalty = orders[0].dishes.length * 5;
                    fame = Math.max(0, fame - penalty);
                    showCookingAlert(`⏰ ออเดอร์บนสุดหมดเวลา! ความนิยมลดลง ${penalty}%`);
                    removeOrder(0);
                } else {
                    for (let i = orders.length - 1; i > 0; i--) {
                        if (orders[i].timeLeft <= 0) {
                            let penalty = orders[i].dishes.length * 5;
                            fame = Math.max(0, fame - penalty);
                            orderAlerts[orders[i].id] = "หมดเวลา! ลูกค้าเดินหนี";
                            setTimeout(() => { delete orderAlerts[orders[i].id]; }, 4000);
                            orders.splice(i, 1);
                        }
                    }
                }
            }

            if (orders.length < 2) {
                nextOrderTimer--;
                if (nextOrderTimer <= 0) {
                    addNewOrder();
                    nextOrderTimer = Math.floor(Math.random() * 14) + 12;
                }
            }

            updateUI();
        }, 1000);

        function addNewOrder() {
            orders.unshift(createOrderObject());
        }

        function removeOrder(index) {
            orders.splice(index, 1);
            cookedDishes = [];
            selectedIngredients = [];
            selectedEmojis = [];
        }

        function selectIngredient(ing, emoji) {
            if (!isGameOpen) {
                showCookingAlert("⚠️ กรุณากดเปิดร้าน (OPEN) ก่อน!");
                return;
            }
            playSound('click');
            selectedIngredients.push(ing);
            selectedEmojis.push(emoji);
            updateUI();
        }

        function removeSelectedIngredient(index) {
            playSound('click');
            let removedIng = selectedIngredients.splice(index, 1)[0];
            selectedEmojis.splice(index, 1);
            showCookingAlert(`ยกเลิก "${removedIng}"`);
            updateUI();
        }

        function cookDish() {
            if (!isGameOpen) { showCookingAlert("⚠️ กรุณากดเปิดร้านก่อน!"); return; }
            if (orders.length === 0) { showCookingAlert("⚠️ ยังไม่มีออเดอร์!"); return; }
            if (selectedIngredients.length === 0) { showCookingAlert("⚠️ กรุณาเลือกวัตถุดิบก่อน!"); return; }

            playSound('cook');

            const smoke = document.getElementById("smokeEffect");
            smoke.style.display = "block";
            setTimeout(() => { smoke.style.display = "none"; }, 1200);

            let matchedDish = null;
            for (let [dish, data] of Object.entries(recipes)) {
                if (data.ingredients.length === selectedIngredients.length) {
                    let isMatch = data.ingredients.every(ing => selectedIngredients.includes(ing));
                    if (isMatch) { matchedDish = dish; break; }
                }
            }

            let totalCost = 0;
            selectedIngredients.forEach(ing => { totalCost += (allIngredients[ing]?.cost || 0); });
            score -= totalCost;
            dailyCosts += totalCost;

            if (matchedDish) {
                const currentOrder = orders[0];
                const orderDishNames = currentOrder.dishes.map(d => d.name);
                if (orderDishNames.includes(matchedDish) && !cookedDishes.includes(matchedDish)) {
                    cookedDishes.push(matchedDish);
                    showCookingAlert(`✅ ทำเมนู "${matchedDish}" สำเร็จ! (ต้นทุน ${totalCost} บ.)`);
                } else {
                    showCookingAlert(`⚠️ ทำ "${matchedDish}" สำเร็จ ไม่อยู่ในคิวบนสุด! (หัก ${totalCost} บ.)`);
                }
            } else {
                showCookingAlert(`❌ ทำอาหารไม่ได้! (เสียวัตถุดิบฟรี ${totalCost} บ.)`);
            }

            selectedIngredients = []; selectedEmojis = [];
            updateUI();
        }

        function serveOrder(index) {
            if (index !== 0) return;
            playSound('serve');

            let currentOrder = orders[0];
            let numberOfDishes = currentOrder.dishes.length;

            let basePrice = numberOfDishes === 1 ? 40 : (numberOfDishes === 2 ? 60 : 75);
            let extraTotal = 0;
            currentOrder.dishes.forEach(dish => { extraTotal += recipes[dish.name].extraPrice; });

            let hasNeonBuff = shopUpgrades.find(u => u.id === 'neon_sign')?.unlocked;
            let priceMultiplier = hasNeonBuff ? 1.5 : 1.0;

            let totalPrice = Math.round((basePrice + extraTotal) * priceMultiplier);
            score += totalPrice;
            dailyRevenue += totalPrice;
            dailyServedCount++;

            addExp(numberOfDishes * 15);

            let fameGain = Math.round(numberOfDishes * 4 * priceMultiplier);
            fame = Math.min(100, fame + fameGain);

            orderAlerts[currentOrder.id] = `🎉 เสิร์ฟสำเร็จ! ได้ ${totalPrice}บ. (+${fameGain}% ⭐)`;
            setTimeout(() => { delete orderAlerts[currentOrder.id]; }, 4000);

            removeOrder(0);
            saveGameData(); // เซฟเกมอัตโนมัติหลังเสิร์ฟ
            updateUI();
        }

        function addExp(amount) {
            exp += amount;
            let currentReq = levelRequirements.find(l => l.level === level + 1);
            if (currentReq && exp >= currentReq.exp) {
                level++;
                showCookingAlert(`🎊 LEVEL UP! ร้านของคุณเลเวล ${level} (${currentReq.name}) แล้ว!`);
            }
        }

        function openShopModal() {
            let html = "";
            shopUpgrades.forEach(item => {
                let canBuy = level >= item.reqLevel && score >= item.price && !item.unlocked;
                let btnText = item.unlocked ? "✅ ซื้อแล้ว" : (level < item.reqLevel ? `🔒 ต้อง Lv.${item.reqLevel}` : `ซื้อ (${item.price}บ.)`);
                html += `
                    <div class="shop-item">
                        <div class="shop-item-info">
                            <strong>${item.name}</strong>
                            <span>${item.desc}</span>
                        </div>
                        <button class="buy-btn" ${!canBuy ? 'disabled' : ''} onclick="buyUpgrade('${item.id}')">${btnText}</button>
                    </div>
                `;
            });
            document.getElementById("shopItemsList").innerHTML = html;
            document.getElementById("shopModal").style.display = "flex";
        }

        function buyUpgrade(id) {
            let item = shopUpgrades.find(u => u.id === id);
            if (item && score >= item.price && !item.unlocked) {
                score -= item.price;
                item.unlocked = true;
                playSound('serve');
                saveGameData(); // เซฟหลังซื้ออุปกรณ์
                openShopModal();
                renderIngredients();
                renderRecipeBook();
                updateUI();
            }
        }

        function showSummaryModal() {
            let starCount = ((fame / 100) * 5).toFixed(1);
            let profit = dailyRevenue - dailyCosts;
            document.getElementById("sumRevenue").innerText = `${dailyRevenue} บาท`;
            document.getElementById("sumCosts").innerText = `${dailyCosts} บาท`;
            document.getElementById("sumProfit").innerText = `${profit} บาท`;
            document.getElementById("sumServed").innerText = `${dailyServedCount} ออเดอร์`;
            document.getElementById("sumStars").innerText = `⭐ ${starCount} (${fame}%)`;
            document.getElementById("summaryModal").style.display = "flex";
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = "none";
        }

        function showCookingAlert(msg) {
            const alertBox = document.getElementById("cookingAlert");
            alertBox.innerText = msg;
            alertBox.style.display = "block";
            setTimeout(() => { alertBox.style.display = "none"; }, 4000);
        }

        function updateUI() {
            document.getElementById("score").innerText = score;

            let starCount = ((fame / 100) * 5).toFixed(1);
            document.getElementById("fameDisplay").innerText = `⭐ ${starCount} (${fame}%)`;

            let currentLevelInfo = levelRequirements.find(l => l.level === level);
            let nextLevelInfo = levelRequirements.find(l => l.level === level + 1);
            let nextExpText = nextLevelInfo ? `/${nextLevelInfo.exp}` : ' (MAX)';
            document.getElementById("levelDisplay").innerText = `🎖️ Lv.${level} ${currentLevelInfo.name} (${exp}${nextExpText} EXP)`;

            let ordersHtml = "";
            orders.forEach((order, index) => {
                let allDone = order.dishes.every(dish => (index === 0 ? cookedDishes.includes(dish.name) : false));
                let percent = (order.timeLeft / order.maxTime) * 100;

                let dishesListHtml = "";
                order.dishes.forEach(dish => {
                    let isDone = (index === 0 && cookedDishes.includes(dish.name));
                    dishesListHtml += `<li class="order-item ${dish.font} ${isDone ? 'done' : ''}">${isDone ? '✔️' : '✏️'} ${dish.name}</li>`;
                });

                let alertMsg = orderAlerts[order.id] ? `<div class="order-alert">${orderAlerts[order.id]}</div>` : '';

                ordersHtml += `
                    <div class="order-box ${index === 0 ? 'active-box' : ''}">
                        <h3>📝 คิวที่ ${index + 1} ${index === 0 ? '(กำลังทำ)' : '(คิวถัดไป)'}</h3>
                        <div class="timer-bar-container">
                            <div class="timer-bar" style="width: ${percent}%;"></div>
                        </div>
                        <ul class="order-list">
                            ${dishesListHtml}
                        </ul>
                        <button class="serve-btn ${allDone && index === 0 ? 'active' : ''}" 
                                onclick="serveOrder(${index})" 
                                ${!(allDone && index === 0) ? 'disabled' : ''}>
                            เสิร์ฟอาหาร
                        </button>
                        ${alertMsg}
                    </div>
                `;
            });
            document.getElementById("ordersArea").innerHTML = ordersHtml;

            let tagsHtml = "";
            let plateEmojiHtml = "🍽️";
            if (selectedIngredients.length > 0) {
                plateEmojiHtml = selectedEmojis.join(" ");
                selectedIngredients.forEach((ing, idx) => {
                    tagsHtml += `<span class="selected-item-tag" onclick="removeSelectedIngredient(${idx})">${ing} ❌</span>`;
                });
                document.getElementById("currentSelection").innerText = "";
            } else {
                document.getElementById("currentSelection").innerText = "- คลิกเลือกวัตถุดิบ -";
            }
            document.getElementById("plateEmojis").innerHTML = plateEmojiHtml;
            document.getElementById("selectedTagsContainer").innerHTML = tagsHtml;
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=880, scrolling=True)
