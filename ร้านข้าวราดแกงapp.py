import streamlit as at
import streamlit.components.v1 as components

# ตั้งค่าหน้าเว็บ Streamlit แสดงผลให้เต็มหน้าจอ
st.set_page_config(page_titla="เกมขชร้านข้าวราดแกง", layuot="wide")

#แสดงผลเกมบน Streamlit
components.html(game_html, height=800, scrolling=True)

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
        h1 { color: #333; margin-bottom: 20px; }
        
        .game-container {
            display: flex;
            gap: 20px;
            width: 950px;
            position: relative;
        }

        .orders-area {
            position: absolute;
            top: 0;
            left: 0;
            display: flex;
            gap: 10px;
        }

        .order-box {
            width: 210px;
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

        .recipe-book {
            position: absolute;
            top: 0;
            right: 0;
            width: 220px;
            background: #eef2f3;
            border: 2px solid #34495e;
            padding: 15px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            border-radius: 5px;
        }
        .recipe-book h3 { margin-top: 0; color: #2c3e50; font-size: 16px; }
        .recipe-book ul { padding-left: 15px; margin: 0; font-size: 13px; color: #333; }
        .recipe-book li { margin-bottom: 4px; }

        .kitchen-area {
            margin-left: 450px;
            margin-right: 240px;
            flex: 1;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .ingredients-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        .ing-btn {
            padding: 10px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .ing-btn span { font-size: 11px; opacity: 0.9; }
        .ing-btn:hover { background: #2980b9; }

        .plate-area {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            min-height: 60px;
            border: 2px solid #bdc3c7;
        }

        .money-box {
            position: absolute;
            bottom: -60px;
            right: 0;
            background: #27ae60;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 5px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>

    <h1>ร้านข้าวราดแกงลุงสมชาย</h1>

    <div class="game-container">
        <div class="orders-area" id="ordersArea"></div>

        <div class="recipe-book">
            <h3>📖 หนังสือสูตรอาหาร</h3>
            <ul>
                <li><strong>แกงเขียวหวาน:</strong> ไก่ + พริกแกง + กะทิ + มะเขือเปราะ</li>
                <li><strong>พะแนง:</strong> หมู + พริกแกง + กะทิ + ใบมะกรูด</li>
                <li><strong>ต้มยำกุ้ง:</strong> กุ้ง + น้ำซุป + เห็ด + สมุนไพร</li>
                <li><strong>ต้มจืด:</strong> เต้าหู้ + น้ำซุป + ผักกาดขาว</li>
                <li><strong>ผัดกะเพรา:</strong> หมู + ใบกะเพรา</li>
                <li><strong>ไข่พะโล้:</strong> หมู + ไข่ + เต้าหู้</li>
                <li><strong>ผัดพริกแกง:</strong> หมู + พริกแกง + ใบมะกรูด</li>
                <li><strong>หมูกระเทียม:</strong> หมู + กระเทียม + สมุนไพร</li>
            </ul>
        </div>

        <div class="kitchen-area">
            <h3>🍳 เลือกวัตถุดิบ (ทำให้ออเดอร์ซ้ายสุดก่อน)</h3>
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

            <p><strong>วัตถุดิบที่เลือก:</strong> <span id="currentSelection">- ไม่มี -</span></p>

            <h3>🍽️ จานข้าวของคุณ (กำลังทำออเดอร์ซ้ายสุด)</h3>
            <div class="plate-area" id="plateArea">
                จานว่าง (ยังไม่มีกับข้าว)
            </div>
        </div>

        <div class="money-box">
            💰 เงิน: <span id="score">150</span> บาท
        </div>
    </div>

    <script>
        const ingredientCosts = {
            "ไก่": 12,
            "หมู": 15,
            "กุ้ง": 25,
            "พริกแกง": 8,
            "กะทิ": 10,
            "น้ำซุป": 5,
            "ใบกะเพรา": 5,
            "มะเขือเปราะ": 6,
            "ใบมะกรูด": 4,
            "ผักกาดขาว": 6,
            "เห็ด": 10,
            "กระเทียม": 5,
            "สมุนไพร": 8,
            "ไข่": 6,
            "เต้าหู้": 8
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
        let orders = []; 
        let cookedDishes = []; 
        let selectedIngredients = [];

        function createOrderObject() {
            const recipeKeys = Object.keys(recipes);
            let numDish = Math.floor(Math.random() * 3) + 1;

            let selectDishes = [];
            while (selectDishes.length < numDish) {
                let randomDish = recipeKeys[Math.floor(Math.random() * recipeKeys.length)];
                if (!selectDishes.includes(randomDish)) {
                    selectDishes.push(randomDish);
                }
            }

            return {
                dishes: selectDishes,
                timeLeft: 60,
                maxTime: 60
            };
        }

        function initGame() {
            addNewOrder();
            updateUI();

            setInterval(() => {
                if (orders.length > 0) {
                    orders[0].timeLeft--;
                    if (orders[0].timeLeft <= 0) {
                        alert("หมดเวลา! ออเดอร์ซ้ายสุดถูกยกเลิก");
                        removeActiveOrder();
                    }
                    updateUI();
                }
            }, 1000);

            setInterval(() => {
                if (orders.length < 2) {
                    addNewOrder();
                    updateUI();
                }
            }, 50000);
        }

        function addNewOrder() {
            const newOrd = createOrderObject();
            orders.unshift(newOrd);
        }

        function removeActiveOrder() {
            orders.shift();
            cookedDishes = [];
            selectedIngredients = [];
        }

        function selectIngredient(ing) {
            selectedIngredients.push(ing);
            checkRecipe();
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
                selectedIngredients.forEach(ing => {
                    totalCost += (ingredientCosts[ing] || 0);
                });

                score -= totalCost;

                const currentOrder = orders[0];
                if (currentOrder.dishes.includes(matchedDish) && !cookedDishes.includes(matchedDish)) {
                    cookedDishes.push(matchedDish);
                    alert(`ทำเมนู "${matchedDish}" สำเร็จ! (หักค่าวัตถุดิบ ${totalCost} บาท)`);
                } else {
                    alert(`ทำเมนู "${matchedDish}" สำเร็จ แต่ไม่อยู่ในออเดอร์ซ้ายสุด! (เสียค่าวัตถุดิบฟรี ${totalCost} บาท)`);
                }
                selectedIngredients = [];
            }
        }

        function serveOrder(index) {
            if (index !== 0) return;

            let currentOrder = orders[0];
            let numberOfDishes = currentOrder.dishes.length;

            let basePrice = 0;
            if (numberOfDishes === 1) basePrice = 40;
            else if (numberOfDishes === 2) basePrice = 60;
            else if (numberOfDishes === 3) basePrice = 75;
            else basePrice = numberOfDishes * 35;

            let extraTotal = 0;
            currentOrder.dishes.forEach(dish => {
                extraTotal += recipes[dish].extraPrice;
            });

            let totalPrice = basePrice + extraTotal;

            score += totalPrice;
            alert(`เสิร์ฟสำเร็จ! ข้าวราด ${numberOfDishes} อย่าง ได้รับเงิน ${totalPrice} บาท`);
            removeActiveOrder();
            updateUI();
        }

        function updateUI() {
            document.getElementById("score").innerText = score;
            
            let ordersHtml = "";
            orders.forEach((order, index) => {
                let allDone = order.dishes.every(dish => (index === 0 ? cookedDishes.includes(dish) : false));
                let percent = (order.timeLeft / order.maxTime) * 100;

                let dishesListHtml = "";
                order.dishes.forEach(dish => {
                    let isDone = (index === 0 && cookedDishes.includes(dish));
                    dishesListHtml += `<li class="order-item ${isDone ? 'done' : ''}">${isDone ? '✔️' : '⭕'} ${dish}</li>`;
                });

                ordersHtml += `
                    <div class="order-box ${index === 0 ? 'active-box' : ''}">
                        <h3>📝 คิวที่ ${index + 1} ${index === 0 ? '(กำลังทำ)' : '(คิวเก่า)'}</h3>
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
                    </div>
                `;
            });
            document.getElementById("ordersArea").innerHTML = ordersHtml;

            document.getElementById("currentSelection").innerText = selectedIngredients.length > 0 ? selectedIngredients.join(" + ") : "- ไม่มี -";
            
            let plateHtml = "จานว่าง (ยังไม่มีกับข้าว)";
            if (orders.length > 0 && cookedDishes.length > 0) {
                plateHtml = `ข้าวราดแกง (ออเดอร์ซ้าย): ${cookedDishes.join(", ")}`;
            }
            document.getElementById("plateArea").innerHTML = plateHtml;
        }

        initGame();
    </script>
</body>
</html>
