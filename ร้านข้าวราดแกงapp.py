import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="เกมร้านข้าวราดแกง", layout="wide")

game_html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ข้าวราดแกงขายฝัน</title>
    <!-- นำเข้าฟอนต์ Prompt (หลัก), Mali, Srisakdi, Charm, Kalam, Caveat (ลายมือ) จาก Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Charm:wght@700&family=Kalam:wght@700&family=Mali:ital,wght@0,500;0,700;1,500&family=Prompt:wght@400;500;600;700&family=Srisakdi:wght@700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Prompt', sans-serif;
            background-color: #f7f3ed; /* โทนสีครีมอุ่นแบบ Cozy */
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* กรอบชื่อร้านสไตล์ไม้ Cozy */
        .shop-title-box {
            border: 2px solid #8d6e63;
            background: #fff8f0;
            padding: 10px 35px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(141, 110, 99, 0.15);
            margin-bottom: 12px;
        }
        h1 { color: #5d4037; margin: 0; font-size: 26px; font-weight: 700; text-align: center; }

        /* ป้ายเปิด-ปิดทรงสี่เหลี่ยม มินิมอล Cozy */
        .shop-status-btn {
            padding: 8px 22px;
            font-size: 14px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 15px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            transition: 0.2s;
        }
        .shop-status-btn.close { background: #e57373; color: white; }
        .shop-status-btn.open { background: #81c784; color: #1b5e20; }

        .game-container {
            display: flex;
            gap: 20px;
            width: 1000px;
            position: relative;
        }

        /* 1. ออเดอร์ (ซ้าย) */
        .orders-area {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 230px;
        }

        /* ใบออเดอร์กระดาษโน้ต Cozy */
        .order-box {
            background: #fffdf7;
            border: 1px solid #e0d7c6;
            padding: 14px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border-radius: 12px;
            position: relative;
        }
        .order-box.active-box {
            border: 2px solid #a1887f;
            background: #fffaf0;
        }
        .order-box h3 { margin-top: 0; color: #6d4c41; font-size: 15px; font-weight: 600; }
        .order-list { list-style: none; padding: 0; margin: 0 0 10px 0; }
        
        /* สไตล์ข้อความเมนูลายมือลูกค้า */
        .order-item { 
            font-size: 16px; 
            margin-bottom: 6px; 
            color: #3e2723; 
            line-height: 1.3;
        }
        
        /* สุ่มลายมือลูกค้าต่างกันในแต่ละเมนู */
        .handwrite-1 { font-family: 'Mali', cursive; font-weight: 700; }
        .handwrite-2 { font-family: 'Charm', cursive; font-size: 17px; }
        .handwrite-3 { font-family: 'Srisakdi', cursive; font-size: 17px; }
        .handwrite-4 { font-family: 'Kalam', cursive; font-size: 17px; }

        .order-item.done { text-decoration: line-through; color: #81c784; opacity: 0.8; }

        .timer-bar-container {
            width: 100%;
            background: #efebe9;
            height: 8px;
            border-radius: 4px;
            margin-bottom: 10px;
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
            padding: 7px;
            background: #cfd8dc;
            color: #fff;
            border: none;
            font-size: 13px;
            font-weight: 600;
            border-radius: 8px;
            cursor: not-allowed;
        }
        .serve-btn.active {
            background: #aed581;
            color: #33691e;
            cursor: pointer;
            box-shadow: 0 3px 6px rgba(174, 213, 129, 0.4);
        }

        .order-alert {
            font-size: 12px;
            color: #e57373;
            margin-top: 5px;
            font-weight: 500;
            text-align: center;
        }

        /* 2. พื้นที่ทำอาหาร (กลาง) */
        .kitchen-area {
            flex: 1;
            background: #ffffff;
            padding: 22px;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .kitchen-area h3 { margin-top: 0; color: #4e342e; font-size: 15px; font-weight: 600; }

        .top-kitchen-row {
            display: flex;
            gap: 12px;
            margin-bottom: 15px;
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
            font-size: 18px;
            background: #fff8e1;
            padding: 5px;
            box-sizing: border-box;
            text-align: center;
        }

        .dish-box {
            flex: 1;
            background: #fafafa;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #eee;
            min-height: 50px;
            font-size: 13px;
        }

        .cooking-alert {
            width: 100%;
            background: #f1f8e9;
            color: #558b2f;
            padding: 8px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
            text-align: center;
            margin-bottom: 10px;
            display: none;
        }

        .ingredients-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            width: 100%;
            margin-bottom: 15px;
        }
        .ing-btn {
            padding: 8px;
            background: #a1887f;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.08);
            transition: 0.1s;
        }
        .ing-btn:hover { background: #8d6e63; }
        .ing-btn span { font-size: 10px; opacity: 0.85; }

        .selected-item-tag {
            display: inline-block;
            background: #ffe0b2;
            color: #e65100;
            padding: 3px 8px;
            margin: 2px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 500;
        }
        .selected-item-tag:hover { text-decoration: line-through; }

        .cook-btn {
            width: 100%;
            padding: 10px;
            background: #d7ccc8;
            color: #4e342e;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 5px;
            transition: 0.2s;
        }
        .cook-btn:hover { background: #bcaaa4; }

        /* 3. หนังสือสูตรอาหาร (ขวา) - ลายมือสมุดบันทึก Cozy */
        .recipe-book {
            width: 220px;
            background: #fffde7;
            border: 1px solid #fff59d;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            border-radius: 12px;
            height: fit-content;
            font-family: 'Mali', cursive;
        }
        .recipe-book h3 { margin-top: 0; color: #f57f17; font-size: 16px; font-weight: 700; }
        .recipe-book ul { padding-left: 15px; margin: 0; font-size: 13px; color: #5d4037; }
        .recipe-book li { margin-bottom: 6px; line-height: 1.3; }

        /* สถานะมุมขวาล่าง */
        .status-panel {
            position: absolute;
            bottom: -60px;
            right: 0;
            display: flex;
            gap: 12px;
        }
        .fame-box, .money-box {
            color: white;
            padding: 8px 15px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .fame-box { background: #ffb74d; }
        .money-box { background: #81c784; }
    </style>
</head>
<body>

    <div class="shop-title-box">
        <h1>ร้านข้าวราดแกงลุงสมชาย</h1>
    </div>
    <button id="shopBtn" class="shop-status-btn close" onclick="toggleShopStatus()">CLOSE (ร้านปิด)</button>

    <div class="game-container">
        <!-- 1. ออเดอร์ (ซ้าย) -->
        <div class="orders-area" id="ordersArea"></div>

        <!-- 2. พื้นที่ทำอาหาร (กลาง) -->
        <div class="kitchen-area">
            <h3>🍳 เลือกวัตถุดิบลงจาน</h3>
            
            <div class="cooking-alert" id="cookingAlert">แจ้งเตือน</div>

            <div class="ingredients-grid">
                <button class="ing-btn" onclick="selectIngredient('ไก่', '🍗')">🍗 ไก่ <span>(12บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('หมู', '🥩')">🥩 หมู <span>(15บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กุ้ง', '🦐')">🦐 กุ้ง <span>(25บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('พริกแกง', '🌶️')">🌶️ พริกแกง <span>(8บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กะทิ', '🥥')">🥥 กะทิ <span>(10บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('น้ำซุป', '🍲')">🍲 น้ำซุป <span>(5บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ใบกะเพรา', '🌿')">🌿 กะเพรา <span>(5บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('มะเขือเปราะ', '🍆')">🍆 มะเขือ <span>(6บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ใบมะกรูด', '🍃')">🍃 ใบมะกรูด <span>(4บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ผักกาดขาว', '🥬')">🥬 ผักกาด <span>(6บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('เห็ด', '🍄')">🍄 เห็ด <span>(10บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กระเทียม', '🧄')">🧄 กระเทียม <span>(5บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('สมุนไพร', '🌿')">🌿 สมุนไพร <span>(8บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ไข่', '🥚')">🥚 ไข่ <span>(6บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('เต้าหู้', '🟡')">🟡 เต้าหู้ <span>(8บ.)</span></button>
            </div>

            <div class="top-kitchen-row" style="width: 100%;">
                <div class="plate-box" id="plateEmojis" title="จานข้าว">🍽️</div>
                <div class="dish-box">
                    <strong>วัตถุดิบที่เลือก:</strong> <span id="currentSelection" style="color: #a1887f;">- คลิกเลือกวัตถุดิบ -</span><br>
                    <div id="selectedTagsContainer" style="margin-top: 4px;"></div>
                </div>
            </div>

            <button class="cook-btn" onclick="cookDish()">🔥 COOK</button>
        </div>

        <!-- 3. หนังสือสูตรอาหาร (ขวา) -->
        <div class="recipe-book">
            <h3>📖 สูตรอาหาร</h3>
            <ul>
                <li><strong>เขียวหวาน:</strong> ไก่+พริกแกง+กะทิ+มะเขือ</li>
                <li><strong>พะแนง:</strong> หมู+พริกแกง+กะทิ+ใบมะกรูด</li>
                <li><strong>ต้มยำกุ้ง:</strong> กุ้ง+น้ำซุป+เห็ด+สมุนไพร</li>
                <li><strong>ต้มจืด:</strong> เต้าหู้+น้ำซุป+ผักกาดขาว</li>
                <li><strong>ผัดกะเพรา:</strong> หมู+ใบกะเพรา</li>
                <li><strong>ไข่พะโล้:</strong> หมู+ไข่+เต้าหู้</li>
                <li><strong>ผัดพริกแกง:</strong> หมู+พริกแกง+ใบมะกรูด</li>
                <li><strong>หมูกระเทียม:</strong> หมู+กระเทียม+สมุนไพร</li>
            </ul>
        </div>

        <!-- สถานะมุมขวาล่าง -->
        <div class="status-panel">
            <div class="fame-box" id="fameDisplay">⭐ 5.0 (100%)</div>
            <div class="money-box">💰 <span id="score">150</span> บาท</div>
        </div>
    </div>

    <script>
        const ingredientCosts = {
            "ไก่": 12, "หมู": 15, "กุ้ง": 25, "พริกแกง": 8, "กะทิ": 10,
            "น้ำซุป": 5, "ใบกะเพรา": 5, "มะเขือเปราะ": 6, "ใบมะกรูด": 4,
            "ผักกาดขาว": 6, "เห็ด": 10, "กระเทียม": 5, "สมุนไพร": 8, "ไข่": 6, "เต้าหู้": 8
        };

        const recipes = {
            "แกงเขียวหวาน": { ingredients: ["ไก่", "พริกแกง", "กะทิ", "มะเขือเปราะ"], extraPrice: 5 },
            "พะแนง": { ingredients: ["หมู", "พริกแกง", "กะทิ", "ใบมะกรูด"], extraPrice: 5 },
            "ต้มยำกุ้ง": { ingredients: ["กุ้ง", "น้ำซุป", "เห็ด", "สมุนไพร"], extraPrice: 15 },
            "ต้มจืด": { ingredients: ["เต้าหู้", "น้ำซุป", "ผักกาดขาว"], extraPrice: 0 },
            "ผัดกะเพรา": { ingredients: ["หมู", "ใบกะเพรา"], extraPrice: 0 },
            "ไข่พะโล้": { ingredients: ["หมู", "ไข่", "เต้าหู้"], extraPrice: 0 },
            "ผัดพริกแกง": { ingredients: ["หมู", "พริกแกง", "ใบมะกรูด"], extraPrice: 0 },
            "หมูกระเทียม": { ingredients: ["หมู", "กระเทียม", "สมุนไพร"], extraPrice: 5 }
        };

        const handwriteClasses = ['handwrite-1', 'handwrite-2', 'handwrite-3', 'handwrite-4'];

        let score = 150;
        let fame = 100;
        let isGameOpen = false;
        let orders = [];
        let cookedDishes = [];
        let selectedIngredients = [];
        let selectedEmojis = [];
        let orderAlerts = {};
        let nextOrderTimer = 15;

        function toggleShopStatus() {
            isGameOpen = !isGameOpen;
            const btn = document.getElementById("shopBtn");
            if (isGameOpen) {
                btn.className = "shop-status-btn open";
                btn.innerText = "เปิด";
                if (orders.length === 0) addNewOrder();
            } else {
                btn.className = "shop-status-btn close";
                btn.innerText = "ปิด";
            }
            updateUI();
        }

        function createOrderObject() {
            const recipeKeys = Object.keys(recipes);
            let numDish = Math.floor(Math.random() * 2) + 1;
            let selectDishes = [];
            while (selectDishes.length < numDish) {
                let randomDish = recipeKeys[Math.floor(Math.random() * recipeKeys.length)];
                if (!selectDishes.map(d => d.name).includes(randomDish)) {
                    // สุ่มฟอนต์ลายมือเฉพาะสำหรับแต่ละเมนูของลูกค้า
                    let fontClass = handwriteClasses[Math.floor(Math.random() * handwriteClasses.length)];
                    selectDishes.push({ name: randomDish, font: fontClass });
                }
            }
            return {
                id: Date.now() + Math.random(),
                dishes: selectDishes,
                timeLeft: 50,
                maxTime: 50
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
                showCookingAlert("⚠️ กรุณากดเปิดร้านก่อนเริ่มทำอาหาร!");
                return;
            }
            selectedIngredients.push(ing);
            selectedEmojis.push(emoji);
            updateUI();
        }

        function removeSelectedIngredient(index) {
            let removedIng = selectedIngredients.splice(index, 1)[0];
            selectedEmojis.splice(index, 1);
            showCookingAlert(`ยกเลิกวัตถุดิบ "${removedIng}"`);
            updateUI();
        }

        function cookDish() {
            if (!isGameOpen) {
                showCookingAlert("⚠️ กรุณากดเปิดร้านก่อน!");
                return;
            }
            if (orders.length === 0) {
                showCookingAlert("⚠️ ยังไม่มีออเดอร์ในตอนนี้!");
                return;
            }
            if (selectedIngredients.length === 0) {
                showCookingAlert("⚠️ กรุณาเลือกวัตถุดิบใส่จานก่อนกด Cook!");
                return;
            }

            let matchedDish = null;
            for (let [dish, data] of Object.entries(recipes)) {
                if (data.ingredients.length === selectedIngredients.length) {
                    let isMatch = data.ingredients.every(ing => selectedIngredients.includes(ing));
                    if (isMatch) {
                        matchedDish = dish;
                        break;
                    }
                }
            }

            let totalCost = 0;
            selectedIngredients.forEach(ing => { totalCost += (ingredientCosts[ing] || 0); });
            score -= totalCost;

            if (matchedDish) {
                const currentOrder = orders[0];
                const orderDishNames = currentOrder.dishes.map(d => d.name);
                if (orderDishNames.includes(matchedDish) && !cookedDishes.includes(matchedDish)) {
                    cookedDishes.push(matchedDish);
                    showCookingAlert(`✅ ทำเมนู "${matchedDish}" สำเร็จ! (หักต้นทุน ${totalCost} บาท)`);
                } else {
                    showCookingAlert(`⚠️ ทำเมนู "${matchedDish}" สำเร็จ แต่ไม่อยู่ในคิวบนสุด! (เสียค่าวัตถุดิบ ${totalCost} บาท)`);
                }
            } else {
                showCookingAlert(`❌ ส่วนผสมนี้ทำอาหารไม่ได้! (เสียค่าวัตถุดิบฟรี ${totalCost} บาท)`);
            }

            selectedIngredients = [];
            selectedEmojis = [];
            updateUI();
        }

        function serveOrder(index) {
            if (index !== 0) return;

            let currentOrder = orders[0];
            let numberOfDishes = currentOrder.dishes.length;

            let basePrice = numberOfDishes === 1 ? 40 : (numberOfDishes === 2 ? 60 : 75);
            let extraTotal = 0;
            currentOrder.dishes.forEach(dish => { extraTotal += recipes[dish.name].extraPrice; });

            let totalPrice = basePrice + extraTotal;
            score += totalPrice;

            let fameGain = numberOfDishes * 4;
            fame = Math.min(100, fame + fameGain);

            orderAlerts[currentOrder.id] = `🎉 เสิร์ฟสำเร็จ! ได้เงิน ${totalPrice}บ. (+ความนิยม ${fameGain}%)`;
            setTimeout(() => { delete orderAlerts[currentOrder.id]; }, 4000);

            removeOrder(0);
            updateUI();
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
