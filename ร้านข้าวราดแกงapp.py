import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="เกมร้านข้าวราดแกง", layout="wide")

game_html = """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>ร้านข้าวราดแกงลุงสมชาย</title>
    <style>
        body {
            font-family: 'Sarabun', sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 { color: #333; margin-bottom: 5px; text-align: center; }

        /* ปุ่ม CLOSE / OPEN */
        .shop-status-btn {
            padding: 8px 25px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            margin-bottom: 15px;
            transition: 0.3s;
        }
        .shop-status-btn.close { background: #e74c3c; color: white; }
        .shop-status-btn.open { background: #27ae60; color: white; }

        .game-container {
            display: flex;
            gap: 20px;
            width: 1000px;
            position: relative;
        }

        /* 1. พื้นที่แสดงออเดอร์ (ซ้าย - เรียงจากบนลงล่าง: ใหม่สุดอยู่บน) */
        .orders-area {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 230px;
        }

        .order-box {
            background: #fffdf0;
            border: 2px dashed #e67e22;
            padding: 12px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            border-radius: 5px;
            position: relative;
        }
        .order-box.active-box {
            border: 2px solid #e67e22;
            background: #fff9e6;
        }
        .order-box h3 { margin-top: 0; color: #d35400; font-size: 15px; }
        .order-list { list-style: none; padding: 0; margin: 0 0 10px 0; }
        .order-item { font-size: 13px; margin-bottom: 4px; color: #555; }
        .order-item.done { text-decoration: line-through; color: #27ae60; font-weight: bold; }

        .timer-bar-container {
            width: 100%;
            background: #ddd;
            height: 8px;
            border-radius: 4px;
            margin-bottom: 10px;
            overflow: hidden;
        }
        .timer-bar {
            height: 100%;
            background: #e74c3c;
            width: 100%;
            transition: width 1s linear;
        }

        .serve-btn {
            width: 100%;
            padding: 8px;
            background: #bdc3c7;
            color: #fff;
            border: none;
            font-size: 14px;
            font-weight: bold;
            border-radius: 4px;
            cursor: not-allowed;
            transition: 0.3s;
        }
        .serve-btn.active {
            background: #27ae60;
            cursor: pointer;
        }
        .serve-btn.active:hover { background: #219653; }

        /* แจ้งเตือนใต้ใบออเดอร์ */
        .order-alert {
            font-size: 12px;
            color: #c0392b;
            margin-top: 5px;
            font-weight: bold;
            text-align: center;
        }

        /* 2. พื้นที่ทำอาหาร (ตรงกลาง) */
        .kitchen-area {
            flex: 1;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .top-kitchen-row {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            width: 100%;
            justify-content: center;
            align-items: center;
        }

        .plate-box {
            width: 80px;
            height: 80px;
            border: 2px dashed #7f8c8d;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #555;
            background: #ecf0f1;
            text-align: center;
        }

        .dish-box {
            flex: 1;
            background: #ecf0f1;
            padding: 10px 15px;
            border-radius: 5px;
            border: 2px solid #bdc3c7;
            min-height: 50px;
            font-size: 14px;
        }

        /* แจ้งเตือนการทำอาหารเหนือช่องวัตถุดิบ */
        .cooking-alert {
            width: 100%;
            background: #e8f8f5;
            color: #16a085;
            padding: 8px;
            border-radius: 4px;
            font-size: 13px;
            text-align: center;
            margin-bottom: 10px;
            border: 1px solid #a3e4d7;
            display: none;
        }

        .ingredients-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            width: 100%;
            margin-bottom: 15px;
        }
        .ing-btn {
            padding: 8px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 13px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .ing-btn span { font-size: 10px; opacity: 0.9; }
        .ing-btn:hover { background: #2980b9; }

        /* ปุ่มยกเลิกวัตถุดิบที่เลือก */
        .selected-item-tag {
            display: inline-block;
            background: #fadbd8;
            color: #c0392b;
            padding: 3px 8px;
            margin: 2px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            border: 1px solid #f5b7b1;
        }
        .selected-item-tag:hover {
            background: #f5b7b1;
            text-decoration: line-through;
        }

        /* 3. หนังสือสูตรอาหาร (ขวา) */
        .recipe-book {
            width: 220px;
            background: #eef2f3;
            border: 2px solid #34495e;
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            border-radius: 5px;
            height: fit-content;
        }
        .recipe-book h3 { margin-top: 0; color: #2c3e50; font-size: 15px; }
        .recipe-book ul { padding-left: 15px; margin: 0; font-size: 12px; color: #333; }
        .recipe-book li { margin-bottom: 4px; }

        /* แผงสถานะด้านล่างขวา (เงินและความนิยม) */
        .status-panel {
            position: absolute;
            bottom: -65px;
            right: 0;
            display: flex;
            gap: 15px;
        }
        .fame-box, .money-box {
            color: white;
            padding: 8px 15px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .fame-box { background: #f39c12; }
        .money-box { background: #27ae60; }
    </style>
</head>
<body>

    <h1>ร้านข้าวราดแกงลุงสมชาย</h1>
    <button id="shopBtn" class="shop-status-btn close" onclick="toggleShopStatus()">CLOSE (ร้านปิด)</button>

    <div class="game-container">
        <!-- 1. ออเดอร์ (ซ้าย - เรียงใหม่ไปเก่า บนลงล่าง) -->
        <div class="orders-area" id="ordersArea"></div>

        <!-- 2. พื้นที่ทำอาหาร (กลาง) -->
        <div class="kitchen-area">
            <h3>🍳 เลือกวัตถุดิบ (ทำออเดอร์บนสุดก่อน)</h3>
            
            <div class="cooking-alert" id="cookingAlert">แจ้งเตือนการทำอาหารที่นี่</div>

            <div class="ingredients-grid">
                <button class="ing-btn" onclick="selectIngredient('ไก่')">🍗 ไก่ <span>(12 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('หมู')">🥩 หมู <span>(15 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กุ้ง')">🦐 กุ้ง <span>(25 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('พริกแกง')">🌶️ พริกแกง <span>(8 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กะทิ')">🥥 กะทิ <span>(10 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('น้ำซุป')">🍲 น้ำซุป <span>(5 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ใบกะเพรา')">🌿 ใบกะเพรา <span>(5 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('มะเขือเปราะ')">🍆 มะเขือเปราะ <span>(6 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ใบมะกรูด')">🍃 ใบมะกรูด <span>(4 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ผักกาดขาว')">🥬 ผักกาดขาว <span>(6 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('เห็ด')">🍄 เห็ด <span>(10 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('กระเทียม')">🧄 กระเทียม <span>(5 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('สมุนไพร')">🌿 สมุนไพร <span>(8 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('ไข่')">🥚 ไข่ <span>(6 บ.)</span></button>
                <button class="ing-btn" onclick="selectIngredient('เต้าหู้')">🟡 เต้าหู้ <span>(8 บ.)</span></button>
            </div>

            <div class="top-kitchen-row" style="width: 100%;">
                <div class="plate-box">จานข้าว</div>
                <div class="dish-box">
                    <strong>กับข้าวที่ทำได้:</strong> <span id="currentSelection" style="color: #7f8c8d;">- คลิกวัตถุดิบเพื่อเริ่มทำ (คลิกที่ชื่อวัตถุดิบด้านล่างเพื่อยกเลิก) -</span><br>
                    <div id="selectedTagsContainer" style="margin-top: 5px;"></div>
                </div>
            </div>
        </div>

        <!-- 3. หนังสือสูตรอาหาร (ขวา) -->
        <div class="recipe-book">
            <h3>📖 หนังสือสูตรอาหาร</h3>
            <ul>
                <li><strong>แกงเขียวหวาน:</strong> ไก่+พริกแกง+กะทิ+มะเขือเปราะ</li>
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
            <div class="fame-box" id="fameDisplay">⭐ ความนิยม: 5.0 (100%)</div>
            <div class="money-box">💰 เงิน: <span id="score">150</span> บาท</div>
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
        let orderAlerts = {};

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

        // รันเวลารวมและอัปเดตสถานะออเดอร์
        setInterval(() => {
            if (!isGameOpen) return;

            orders.forEach(order => {
                order.timeLeft--;
            });

            if (orders.length > 0) {
                // เช็คออเดอร์บนสุด (index 0) หมดเวลา
                if (orders[0].timeLeft <= 0) {
                    let penalty = orders[0].dishes.length * 5;
                    fame = Math.max(0, fame - penalty);
                    showCookingAlert(`⏰ ออเดอร์บนสุดหมดเวลา! ความนิยมลดลง ${penalty}%`);
                    removeOrder(0);
                } else {
                    // เช็คออเดอร์ด้านล่างที่หมดเวลา
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

            // สุ่มเพิ่มออเดอร์ใหม่ (สูงสุด 2 ออเดอร์ โดยใช้ unshift เพื่อให้ตัวใหม่มาอยู่บนสุด)
            if (orders.length < 2 && Math.random() < 0.1) {
                addNewOrder();
            }

            updateUI();
        }, 1000);

        function addNewOrder() {
            const newOrd = createOrderObject();
            orders.unshift(newOrd); // ใส่ไว้หน้าสุด (บนสุด)
        }

        function removeOrder(index) {
            orders.splice(index, 1);
            cookedDishes = [];
            selectedIngredients = [];
        }

        function selectIngredient(ing) {
            if (!isGameOpen) {
                showCookingAlert("⚠️ กรุณากดเปิดร้าน (OPEN) ก่อนเริ่มทำอาหาร!");
                return;
            }
            selectedIngredients.push(ing);
            checkRecipe();
            updateUI();
        }

        function removeSelectedIngredient(index) {
            let removedIng = selectedIngredients.splice(index, 1)[0];
            showCookingAlert(`ยกเลิกวัตถุดิบ "${removedIng}" เรียบร้อยแล้ว`);
            updateUI();
        }

        function checkRecipe() {
            if (orders.length === 0) return;

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

            if (matchedDish) {
                let totalCost = 0;
                selectedIngredients.forEach(ing => { totalCost += (ingredientCosts[ing] || 0); });

                score -= totalCost;

                const currentOrder = orders[0];
                if (currentOrder.dishes.includes(matchedDish) && !cookedDishes.includes(matchedDish)) {
                    cookedDishes.push(matchedDish);
                    showCookingAlert(`✅ ทำเมนู "${matchedDish}" สำเร็จ! (หักค่าวัตถุดิบ ${totalCost} บาท)`);
                } else {
                    showCookingAlert(`⚠️ ทำเมนู "${matchedDish}" สำเร็จ แต่ไม่อยู่ในคิวบนสุด! (เสียค่าวัตถุดิบฟรี ${totalCost} บาท)`);
                }
                selectedIngredients = [];
            }
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

            orderAlerts[currentOrder.id] = `🎉 เสิร์ฟสำเร็จ! ได้รับเงิน ${totalPrice} บาท (+ความนิยม ${fameGain}%)`;
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
            document.getElementById("fameDisplay").innerHTML = `⭐ ความนิยม: ${starCount} (${fame}%)`;

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
                        <h3>📝 คิวที่ ${index + 1} ${index === 0 ? '(กำลังทำ - บนสุด)' : '(คิวถัดไป - ล่าง)'}</h3>
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
            if (selectedIngredients.length > 0) {
                selectedIngredients.forEach((ing, idx) => {
                    tagsHtml += `<span class="selected-item-tag" onclick="removeSelectedIngredient(${idx})" title="คลิกเพื่อยกเลิกวัตถุดิบนี้">${ing} ❌</span>`;
                });
                document.getElementById("currentSelection").innerText = "กำลังเลือก:";
            } else {
                document.getElementById("currentSelection").innerText = "- คลิกวัตถุดิบเพื่อเริ่มทำ -";
            }
            document.getElementById("selectedTagsContainer").innerHTML = tagsHtml;
        }
    </script>
</body>
</html>
"""

components.html(game_html, height=850, scrolling=True)
