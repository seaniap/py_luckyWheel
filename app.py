import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
from datetime import datetime
import os
import random

# 設置頁面配置
st.set_page_config(
    page_title="幸運輪盤",
    page_icon="🎡",
    layout="wide"
)

# 確保資料目錄存在
if not os.path.exists("data"):
    os.makedirs("data")

# 獲取獲獎歷史
def get_winners_history():
    if not os.path.exists("data/winners.json"):
        return []
    try:
        with open("data/winners.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

# 保存獲獎者
def save_winner(name):
    winners = get_winners_history()
    winners.append({
        "name": name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open("data/winners.json", "w", encoding="utf-8") as f:
        json.dump(winners, f, ensure_ascii=False, indent=2)

# 主題顏色
colors = [
    "#FF5252", "#FF4081", "#E040FB", "#7C4DFF", "#536DFE", 
    "#448AFF", "#40C4FF", "#18FFFF", "#64FFDA", "#69F0AE", 
    "#B2FF59", "#EEFF41", "#FFFF00", "#FFD740", "#FFAB40", "#FF6E40"
]

# 嵌入 JavaScript 及 CSS
def get_wheel_js():
    return """
    function getWheel(names) {
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 10;
        
        const totalNames = names.length;
        const arc = 2 * Math.PI / totalNames;
        
        // 清除畫布
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 繪製輪盤
        for (let i = 0; i < totalNames; i++) {
            const angle = i * arc;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, angle, angle + arc);
            ctx.closePath();
            ctx.fillStyle = names[i].color;
            ctx.fill();
            ctx.stroke();
            
            // 繪製名稱
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(angle + arc / 2);
            ctx.textAlign = 'right';
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 14px sans-serif';
            ctx.shadowColor = 'rgba(0,0,0,0.5)';
            ctx.shadowBlur = 3;
            ctx.fillText(names[i].name, radius - 10, 5);
            ctx.restore();
        }
        
        // 繪製輪盤中心
        ctx.beginPath();
        ctx.arc(centerX, centerY, 15, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();
        
        // 繪製指針
        ctx.beginPath();
        ctx.moveTo(centerX + radius + 10, centerY);
        ctx.lineTo(centerX + radius - 10, centerY - 15);
        ctx.lineTo(centerX + radius - 10, centerY + 15);
        ctx.closePath();
        ctx.fillStyle = '#FF5252';
        ctx.fill();
    }
    
    // 抽獎功能
    let isSpinning = false;
    let spinTimeout = null;
    let startAngle = 0;
    let spinAngleStart = 0;
    let currentRotation = 0;
    let ctx;
    let spinTime = 0;
    let spinTimeTotal = 0;
    let wheelNames = [];
    
    function spin() {
        if (isSpinning) return;
        isSpinning = true;
        
        // 播放旋轉聲音
        document.getElementById('spinSound').play();
        
        // 隱藏獲獎者
        document.getElementById('winner').style.display = 'none';
        
        // 設定旋轉參數
        spinAngleStart = Math.random() * 10 + 10;
        spinTime = 0;
        spinTimeTotal = Math.random() * 3000 + 4000;
        rotateWheel();
    }
    
    function rotateWheel() {
        spinTime += 30;
        if (spinTime >= spinTimeTotal) {
            stopRotateWheel();
            return;
        }
        
        const spinAngle = spinAngleStart - easeOut(spinTime, 0, spinAngleStart, spinTimeTotal);
        currentRotation += spinAngle * Math.PI / 180;
        
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        
        // 清除畫布
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // 保存狀態
        ctx.save();
        ctx.translate(canvas.width / 2, canvas.height / 2);
        ctx.rotate(currentRotation);
        ctx.translate(-canvas.width / 2, -canvas.height / 2);
        
        // 重新繪製輪盤
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 10;
        
        const totalNames = wheelNames.length;
        const arc = 2 * Math.PI / totalNames;
        
        for (let i = 0; i < totalNames; i++) {
            const angle = i * arc;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, angle, angle + arc);
            ctx.closePath();
            ctx.fillStyle = wheelNames[i].color;
            ctx.fill();
            ctx.stroke();
            
            // 繪製名稱
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(angle + arc / 2);
            ctx.textAlign = 'right';
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 14px sans-serif';
            ctx.shadowColor = 'rgba(0,0,0,0.5)';
            ctx.shadowBlur = 3;
            ctx.fillText(wheelNames[i].name, radius - 10, 5);
            ctx.restore();
        }
        
        // 繪製輪盤中心
        ctx.beginPath();
        ctx.arc(centerX, centerY, 15, 0, 2 * Math.PI);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
        
        // 繪製指針（固定位置）
        ctx.beginPath();
        ctx.moveTo(centerX + radius + 10, centerY);
        ctx.lineTo(centerX + radius - 10, centerY - 15);
        ctx.lineTo(centerX + radius - 10, centerY + 15);
        ctx.closePath();
        ctx.fillStyle = '#FF5252';
        ctx.fill();
        
        spinTimeout = setTimeout(rotateWheel, 30);
    }
    
    function stopRotateWheel() {
        clearTimeout(spinTimeout);
        isSpinning = false;
        
        // 停止旋轉聲音
        document.getElementById('spinSound').pause();
        document.getElementById('spinSound').currentTime = 0;
        
        // 播放獲獎聲音
        document.getElementById('winSound').play();
        
        // 計算獲獎者
        const canvas = document.getElementById('wheel');
        const degrees = currentRotation * 180 / Math.PI + 90; // 加90度是因為指針在右側
        const arcd = 360 / wheelNames.length;
        const index = Math.floor(((360 - degrees % 360) % 360) / arcd);
        const winnerName = wheelNames[index].name;
        
        // 顯示獲獎者
        const winnerElement = document.getElementById('winner');
        winnerElement.textContent = '恭喜：' + winnerName;
        winnerElement.style.display = 'block';
        
        // 獲獎者已經展示在頁面中，同時加入全域變數以便需要時使用
        window.latestWinner = winnerName;
        
        // 調用一個自定義函數，將獲獎者資訊寫入本地儲存
        try {
            localStorage.setItem('latestWinner', winnerName);
            localStorage.setItem('winnerTime', new Date().toISOString());
        } catch (e) {
            console.error('無法儲存獲獎者資訊', e);
        }
    }
    
    function easeOut(t, b, c, d) {
        const ts = (t /= d) * t;
        const tc = ts * t;
        return b + c * (tc + -3 * ts + 3 * t);
    }
    
    function setWheelNames(names) {
        wheelNames = names;
        getWheel(names);
    }
    """

def get_html_content(names):
    # 為每個名稱分配顏色
    name_data = []
    for i, name in enumerate(names):
        color_index = i % len(colors)
        name_data.append({"name": name, "color": colors[color_index]})
    
    html = f"""
    <html>
    <head>
        <style>
            #wheel-container {{
                text-align: center;
                margin: 20px 0;
            }}
            #wheel {{
                border: 2px solid #333;
                border-radius: 50%;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
            }}
            #spin-button {{
                background-color: #FF5252;
                color: white;
                border: none;
                padding: 12px 30px;
                font-size: 18px;
                border-radius: 30px;
                cursor: pointer;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                transition: all 0.3s;
            }}
            #spin-button:hover {{
                background-color: #FF8A80;
                transform: scale(1.05);
            }}
            #winner {{
                display: none;
                font-size: 24px;
                font-weight: bold;
                color: #FF5252;
                margin: 20px 0;
                padding: 10px;
                border-radius: 5px;
                background-color: #FFF8E1;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
        </style>
    </head>
    <body>
        <div id="wheel-container">
            <canvas id="wheel" width="500" height="500"></canvas>
            <div>
                <button id="spin-button" onclick="spin()">開始抽獎</button>
            </div>
            <div id="winner"></div>
        </div>
        
        <audio id="spinSound" preload="auto">
            <source src="data:audio/mpeg;base64,{get_base64_spin_sound()}" type="audio/mpeg">
        </audio>
        <audio id="winSound" preload="auto">
            <source src="data:audio/mpeg;base64,{get_base64_win_sound()}" type="audio/mpeg">
        </audio>
        
        <script>
            {get_wheel_js()}
            
            // 初始化輪盤數據
            let wheelNameData = {json.dumps(name_data, ensure_ascii=False)};
            
            // 等待頁面載入
            window.onload = function() {{
                // 確保Canvas元素已存在
                if (document.getElementById('wheel')) {{
                    // 初始化輪盤
                    setWheelNames(wheelNameData);
                    console.log('輪盤初始化完成');
                }}
                
                // 監聽事件處理
                window.addEventListener('message', function(event) {{
                    if (event.data.type === 'updateNames') {{
                        setWheelNames(event.data.names);
                    }}
                }});
            }};
        </script>
    </body>
    </html>
    """
    return html

# 獲取按鈕音效的base64編碼
def get_base64_spin_sound():
    # 這裡使用較短的base64編碼
    return "SUQzAwAAAAAXdlRZRVIAAAAGAAAAMjAyMwBUREFUAAAABgAAADIwMjMAVElUMgAAAAYAAAAyMDIzAFRDT04AAAAGAAAA"

def get_base64_win_sound():
    # 這裡使用較短的base64編碼
    return "SUQzAwAAAAAXdlRZRVIAAAAGAAAAMjAyMwBUREFUAAAABgAAADIwMjMAVElUMgAAAAYAAAAyMDIzAFRDT04AAAAGAAAA"

# 主應用程式
def main():
    st.title("幸運輪盤 🎡")
    
    # 側邊欄 - 檔案上傳
    with st.sidebar:
        st.header("參與者名單")
        
        uploaded_file = st.file_uploader("上傳Excel或CSV檔案", type=["xlsx", "csv"])
        
        if uploaded_file is not None:
            try:
                # 讀取上傳的檔案
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # 檢查是否有名稱欄位
                if "name" in df.columns:
                    name_column = "name"
                elif "姓名" in df.columns:
                    name_column = "姓名"
                elif "Name" in df.columns:
                    name_column = "Name"
                else:
                    name_column = df.columns[0]  # 使用第一欄作為名稱欄位
                
                names = df[name_column].tolist()
                st.session_state.names = names
                st.success(f"已成功加載 {len(names)} 位參與者")
                
                # 顯示名單
                st.subheader("參與者名單")
                st.dataframe(df[[name_column]])
                
            except Exception as e:
                st.error(f"無法讀取檔案: {e}")
        
        # 手動輸入名單
        st.subheader("或手動輸入名單")
        manual_names = st.text_area("每行一個名稱")
        
        if st.button("確認名單"):
            if manual_names:
                names = [name.strip() for name in manual_names.split("\n") if name.strip()]
                st.session_state.names = names
                st.success(f"已成功加載 {len(names)} 位參與者")
        
        # 獲獎歷史
        st.header("獲獎歷史")
        if st.button("刷新獲獎歷史"):
            st.rerun() 
        
        winners = get_winners_history()
        
        if winners:
            winners_df = pd.DataFrame(winners)
            st.dataframe(winners_df)
        else:
            st.info("尚無獲獎記錄")
    
    # 主區域 - 輪盤
    if "names" in st.session_state and st.session_state.names:
        names = st.session_state.names
        
        # 使用HTML組件顯示輪盤
        html_content = get_html_content(names)
        components.html(html_content, height=600)
        
        # 添加一個按鈕來刷新並保存獲獎者
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 使用Streamlit的回調處理獲獎者
            if st.button("手動獲取獲獎者"):
                winner = random.choice(names)
                st.success(f"獲獎者: {winner}")
                save_winner(winner)
                st.rerun()
        
        with col2:
            winner_name = st.text_input("保存輪盤獲獎者 (輸入獲獎者姓名後按Enter鍵)", "")
            if winner_name and winner_name.strip():
                # 確保輸入的是字符串並且不是空的
                save_winner(winner_name.strip())
                st.success(f"獲獎者：{winner_name.strip()} 已保存！")
                st.rerun()
    else:
        st.info("請上傳參與者名單或手動輸入名單")

if __name__ == "__main__":
    main()
    