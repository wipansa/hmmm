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
            padding:
