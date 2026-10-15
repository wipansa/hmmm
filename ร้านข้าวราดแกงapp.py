import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="เกมร้านข้าวราดแกง", layout="wide")

game_html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ร้านข้าวราดแกงขายฝัน</title>
    <!-- นำเข้าฟอนต์ Prompt จาก Google Fonts ให้ดูทันสมัยและวัยรุ่นขึ้น -->
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Prompt', sans-serif;
            background-color: #fdfbf7;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* กรอบชื่อร้านสไตล์ไทยโมเดิร์น */
        .shop-title-box {
            border: 3px solid #d35400;
            background: #fff5e6;
            padding: 8px 30px;
            border-radius: 12px;
            box-shadow: 3px 3px 0px #b9770e;
            margin-bottom: 12px;
        }
        h1 { color: #b9770e; margin: 0; font-size: 26px; font-weight: 700; text-align: center; text-shadow: 1px 1px 0px #fad7a0; }

        /* ป้ายเปิด-ปิดทรงสี่เหลี่ยม */
        .shop-status-btn {
            padding: 8px 20px;
            font-size: 15px;
            font-weight: 600;
            border: 2px solid #555;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 15px;
            box-shadow: 2px 2px 0px #333;
            transition: 0.1s;
        }
        .shop-status-btn:active { transform: translate(2px, 2px); box-shadow: none; }
        .shop-status-btn.close { background: #e74c3c; color: white; }
        .shop-status-btn.open { background: #27ae60; color: white; }

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

        .order-box {
            background: #fffdf0;
            border: 2px solid #e67e22;
            padding: 12px;
            box-shadow: 3px 3px 0px rgba(230, 126, 34, 0.3);
            border-radius: 8px;
            position: relative;
        }
        .order-box.active-box {
            border: 2px solid #d35400;
            background: #fff9e6;
        }
        .order-box h3 { margin-top: 0; color: #d35400; font-size: 14px; font-weight: 600; }
        .order-list { list-style: none; padding: 0; margin: 0 0 10px 0; }
        .order-item { font-size: 13px; margin-bottom: 4px; color: #555; font-weight: 400; }
        .order-item.done { text-decoration: line-through; color: #27ae60; font-weight: 600; }

        .timer-bar-container {
            width: 100%;
            background: #ddd;
            height: 8px;
            border-radius: 4px;
            margin-bottom: 10px;
            overflow: hidden;
            border: 1px solid #ccc;
        }
        .timer-bar {
            height: 100%;
            background: #e74c3c;
            width: 100%;
            transition: width 1s linear;
        }

        .serve-btn {
            width: 100%;
            padding: 6px;
            background: #bdc3c7;
            color: #fff;
            border: none;
            font-size: 13px;
            font-weight: 600;
            border-radius: 6px;
            cursor: not-allowed;
        }
        .serve-btn.active {
            background: #27ae60;
            cursor: pointer;
            box-shadow: 2px 2px 0px #1e8449;
        }

        .order-alert {
            font-size: 11px;
            color: #c0392b;
            margin-top: 5px;
            font-weight: 600;
            text-align: center;
        }

        /* 2. พื้นที่ทำอาหาร (กลาง) */
        .kitchen-area {
            flex: 1;
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #d5dbdb;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .kitchen-area h3 { margin-top: 0; color: #2c3e50; font-size: 15px; font-weight: 600; }

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
            border: 2px dashed #e67e22;
            border-radius: 50%;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            background: #fcf3cf;
            padding: 5px;
            box-sizing: border-box;
            text-align: center;
        }

        .dish-box {
            flex: 1;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ddd;
            min-height: 55px;
            font-size: 13px;
        }

        .cooking-alert {
            width: 100%;
            background: #eafaf1;
            color: #27ae60;
            padding: 6px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            text-align: center;
            margin-bottom: 10px;
            border: 1px solid #a9dfbf;
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
            padding: 7px;
            background: #2980b9;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-shadow: 1px 1px 0px #1b4f72;
            transition: 0.1s;
        }
        .ing-btn:active { transform: translate(1px, 1px); box-shadow: none; }
        .ing-btn span { font-size: 10px; opacity: 0.9; }

        .selected-item-tag {
            display: inline-block;
            background: #fadbd8;
            color: #c0392b;
            padding: 2px 6px;
            margin: 2px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 500;
            border: 1px solid #f5b7b1;
        }
        .selected-item-tag:hover { text-decoration: line-through; }

        .cook-btn {
            width: 100%;
            padding: 8px;
            background: #d35400;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 2px 2px 0px #935116;
            margin-top: 5px;
            transition: 0.1s;
        }
        .cook-btn:active { transform: translate(2px, 2px); box-shadow: none; }

        /* 3. หนังสือสูตรอาหาร (ขวา) */
        .recipe-book {
            width: 220px;
            background: #fef9e7;
            border: 2px solid #d4ac0d;
            padding: 12px;
            box-shadow: 3px 3px 0px rgba(212, 172, 13, 0.3);
            border-radius: 8px;
            height: fit-content;
        }
        .recipe-book h3 { margin-top: 0; color: #b7950b; font-size: 14px; font-weight: 600; }
        .recipe-book ul { padding-left: 15px; margin: 0; font-size: 11px; color: #444; }
        .recipe-book li { margin-bottom: 4px; }

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
            padding: 6px 12px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 6px;
            box-shadow: 2px 2px 0px rgba(0,0,0,0.2);
        }
        .fame-box { background: #d4ac0d; }
        .money-box { background: #27ae60; }
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
                    <strong>วัตถุดิบที่เลือก:</strong> <span id="currentSelection" style="color: #7f8c8d;">- คลิกเลือกวัตถุดิบ (คลิกชื่อเพื่อยกเลิก) -</span><br>
                    <div id="selectedTagsContainer" style="margin-top: 4px;"></div>
                </div>
            </div>

            <button class="cook-btn" onclick="cookDish()">🔥 COOK </button>
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
                btn.innerText = "OPEN (เปิดร้านแล้ว)";
                if (orders.length === 0) addNewOrder();
            } else {
                btn.className = "shop-status-btn close";
                btn.innerText = "CLOSE (ร้านปิด)";
            }
            updateUI();
        }

        function createOrderObject() {
            const recipeKeys = Object.keys(recipes);
            let numDish = Math.floor(Math.random() * 2) + 1;
            let selectDishes = [];
            while (selectDishes.length < numDish) {
                let randomDish = recipeKeys[Math.floor(Math.random() * recipeKeys.length)];
                if (!selectDishes.includes(randomDish)) selectDishes.push(randomDish);
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
                showCookingAlert("⚠️ กรุณากดเปิดร้าน (OPEN) ก่อนเริ่มทำอาหาร!");
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
                if (currentOrder.dishes.includes(matchedDish) && !cookedDishes.includes(matchedDish)) {
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
            currentOrder.dishes.forEach(dish => { extraTotal += recipes[dish].extraPrice; });

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
                let allDone = order.dishes.every(dish => (index === 0 ? cookedDishes.includes(dish) : false));
                let percent = (order.timeLeft / order.maxTime) * 100;

                let dishesListHtml = "";
                order.dishes.forEach(dish => {
                    let isDone = (index === 0 && cookedDishes.includes(dish));
                    dishesListHtml += `<li class="order-item ${isDone ? 'done' : ''}">${isDone ? '✔️' : '⭕'} ${dish}</li>`;
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
                document.getElementById("currentSelection").innerText = "- คลิกเลือกวัตถุดิบ (คลิกชื่อเพื่อยกเลิก) -";
            }
            document.getElementById("plateEmojis").innerHTML = plateEmojiHtml;
            document.getElementById("selectedTagsContainer").innerHTML = tagsHtml;
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=880, scrolling=True)
