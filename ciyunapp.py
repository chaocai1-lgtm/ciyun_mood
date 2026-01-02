import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import json
import pandas as pd
from datetime import datetime
from db import Neo4jHandler

# ======================= 系统配置区 =======================
# 1. 专属标签 (通过修改这个后缀，区分不同的人)
TARGET_LABEL = "Danmu_xinli" 

# 2. 管理员密码
ADMIN_PASSWORD = "admin888"

# 3. 数据库配置
NEO4J_URI = "neo4j+s://7eb127cc.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "wE7pV36hqNSo43mpbjTlfzE7n99NWcYABDFqUGvgSrk"
# ========================================================

st.set_page_config(page_title="互动课堂系统", layout="wide", page_icon="🎓")

# 直接连接数据库（每次请求都创建新连接，确保数据同步）
def get_db():
    """获取数据库连接"""
    return Neo4jHandler(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, label=TARGET_LABEL)

db = get_db()

# ==================== 初始化 session_state ====================
if 'student_name' not in st.session_state: st.session_state.student_name = ""
if 'danmu_msg' not in st.session_state: st.session_state.danmu_msg = ""

# ==================== 侧边栏导航 ====================
st.sidebar.title("🚀 导航栏")

# 实际测试数据库连接并显示数据统计
try:
    test_result = db.test_connection()
    if test_result:
        # 获取当前数据库中的记录数量作为验证
        logs = db.get_logs()
        log_count = len(logs) if logs else 0
        st.sidebar.success(f"🟢 云数据库已连接 (共{log_count}条记录)")
        # 显示最近一条记录用于调试
        if logs and len(logs) > 0:
            latest = logs[0]
            st.sidebar.caption(f"最新: {latest.get('姓名', '?')} - {latest.get('内容', '?')[:10]}")
    else:
        st.sidebar.error("🔴 数据库连接失败")
except Exception as e:
    st.sidebar.error(f"🔴 连接错误: {e}")

page = st.sidebar.radio("选择入口", ["我是学生 (发送弹幕)", "我是老师 (后台管理)"])

# 学生输入区域放在侧边栏
st.sidebar.markdown("---")
st.sidebar.subheader("📝 发送弹幕")
st.sidebar.info("👋 欢迎同学！请留下你的大名和想法。")

# 使用回调函数来处理发送和重置
def on_send():
    name = st.session_state.get('name_input', '')
    msg = st.session_state.get('msg_input', '')
    if name and msg:
        db.add_record(name, msg)
        st.session_state.msg_input = ""  # 只清空弹幕内容
        st.toast("✅ 发送成功！", icon="🎉")

def on_reset():
    st.session_state.name_input = ""
    st.session_state.msg_input = ""

# 姓名输入框
student_name = st.sidebar.text_input("你的姓名", placeholder="例如：张三", key="name_input")

# 弹幕内容输入框
danmu_msg = st.sidebar.text_input("弹幕内容", placeholder="例如：老师讲得好！", key="msg_input")

# 发送和重置按钮
col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("🚀 发送", use_container_width=True, on_click=on_send):
        if not student_name or not danmu_msg:
            st.sidebar.error("请填写完整信息")

with col_btn2:
    st.button("🔄 重置", use_container_width=True, on_click=on_reset)

# 管理员清屏功能（只清除前端展示）
st.sidebar.markdown("---")
with st.sidebar.expander("🗑️ 管理员清屏"):
    st.caption("⚠️ 清屏只清除词云展示，不删除后台数据")
    clean_pwd = st.text_input("输入管理密码", type="password", key="clean_pwd")
    if st.button("确认清空词云", type="primary", use_container_width=True):
        if clean_pwd == ADMIN_PASSWORD:
            db.clear_cloud_only()
            st.toast("词云已清空！后台数据保留", icon="✅")
            st.rerun()
        else:
            st.error("密码错误")

st.markdown("""
<style>
    .stApp {background-color: #f8f9fa;}
    .main-title {color: #333; font-weight: bold; text-align: left;}
    div[data-testid="stMetricValue"] {font-size: 24px; color: #4F46E5;}
    /* 隐藏页面导航菜单 */
    [data-testid="stSidebarNav"] {display: none;}
    /* 手机端适配 */
    @media (max-width: 768px) {
        .main-title {font-size: 1.5rem !important;}
        iframe {min-height: 350px !important;}
        [data-testid="column"] {width: 100% !important; flex: 1 1 100% !important;}
    }
</style>
""", unsafe_allow_html=True)

# ==================== 页面 1: 学生端 (实时弹幕) ====================
if page == "我是学生 (发送弹幕)":
    # 自动刷新 (3秒一次)
    st_autorefresh(interval=3000, key="student_refresh")
    
    st.markdown("<h1 class='main-title'>🎬 实时弹幕</h1>", unsafe_allow_html=True)
    
    # 获取数据
    logs = db.get_logs()
    data = db.get_cloud_data()
    
    # 左右布局：词云墙 + 排行榜
    col_cloud, col_rank = st.columns([3, 1])
    
    with col_cloud:
        if not data:
            st.warning("暂无数据，快来发送第一条弹幕！")
        else:
            word_list = [[item['name'], item['value']] for item in data]
            html_code = f"""
            <!DOCTYPE html><html><head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <script src="https://cdn.jsdelivr.net/npm/wordcloud@1.1.1/src/wordcloud2.js"></script>
            <style>
                html, body {{margin:0;padding:0;background:transparent;overflow:hidden;width:100%;height:100%;}}
                #canvas{{width:100%;height:100%;display:block;}}
                .word-item {{
                    animation: float 3s ease-in-out infinite;
                    font-weight: bold;
                }}
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-6px); }}
                }}
            </style>
            </head><body><div id="canvas"></div><script>
            const list = {json.dumps(word_list, ensure_ascii=False)};
            const colors = ['#2563eb','#9333ea','#db2777','#ea580c','#16a34a','#0891b2','#f59e0b','#10b981'];
            function getColor(){{ return colors[Math.floor(Math.random()*colors.length)]; }}
            
            function renderCloud() {{
                const canvasEl = document.getElementById('canvas');
                const width = canvasEl.offsetWidth || window.innerWidth || 350;
                const height = canvasEl.offsetHeight || window.innerHeight || 400;
                const isMobile = width < 600;
                
                // 清空之前的内容
                canvasEl.innerHTML = '';
                
                WordCloud(canvasEl, {{
                    list: list, 
                    gridSize: isMobile ? 16 : 28,
                    weightFactor: function(s){{ 
                        const base = isMobile ? 16 : 25;
                        const factor = isMobile ? 22 : 35;
                        return base + Math.log(s+1) * factor; 
                    }},
                    fontFamily: '-apple-system, BlinkMacSystemFont, Microsoft YaHei, Arial, sans-serif', 
                    fontWeight: 'bold',
                    color: getColor, 
                    backgroundColor: 'transparent',
                    rotateRatio: 0, 
                    shuffle: false, 
                    drawOutOfBound: false,
                    classes: 'word-item',
                    origin: [width/2, height/2],
                    wait: 50
                }});
            }}
            
            // 延迟渲染确保容器尺寸正确
            setTimeout(renderCloud, 100);
            
            // 监听窗口变化重新渲染
            window.addEventListener('resize', function() {{
                clearTimeout(window.resizeTimer);
                window.resizeTimer = setTimeout(renderCloud, 300);
            }});
            
            setTimeout(function() {{
                const words = document.querySelectorAll('#canvas span, #canvas text');
                words.forEach((word, i) => {{
                    word.style.animation = `float ${{2.5 + Math.random()*2}}s ease-in-out infinite ${{Math.random()*2}}s`;
                    word.style.transition = 'all 0.3s ease';
                }});
            }}, 1500);
            </script></body></html>
            """
            components.html(html_code, height=450, scrolling=False)
    
    with col_rank:
        st.markdown("<h3 style='text-align:center;'>🏆 发言排行榜</h3>", unsafe_allow_html=True)
        # 统计每个人发送弹幕的数量
        if logs:
            from collections import Counter
            name_counts = Counter([log['姓名'] for log in logs])
            top10 = name_counts.most_common(10)
            
            # 构建居中对齐的排行榜HTML
            rank_html = "<div style='text-align:center; font-size:16px; line-height:2;'>"
            for i, (name, count) in enumerate(top10, 1):
                if i == 1:
                    medal = "🥇"
                elif i == 2:
                    medal = "🥈"
                elif i == 3:
                    medal = "🥉"
                else:
                    medal = f"<span style='display:inline-block;width:24px;'>{i}.</span>"
                rank_html += f"<div><span style='display:inline-block;width:28px;'>{medal}</span><span style='display:inline-block;width:80px;text-align:left;'>{name}</span> <span style='color:#666;'>{count}条</span></div>"
            rank_html += "</div>"
            st.markdown(rank_html, unsafe_allow_html=True)
        else:
            st.caption("暂无数据")

# ==================== 页面 2: 管理端 ====================
elif page == "我是老师 (后台管理)":
    st.title("🔐 教师后台管理")
    
    if 'is_admin' not in st.session_state: st.session_state.is_admin = False
    
    if not st.session_state.is_admin:
        pwd = st.text_input("请输入管理员密码", type="password")
        if st.button("登录"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("密码错误")
    else:
        st.success("✅ 管理员已登录")
        if st.button("退出登录"):
            st.session_state.is_admin = False
            st.rerun()
        
        st.divider()
        
        logs = db.get_logs()
        df = pd.DataFrame(logs if logs else [])
        
        m1, m2 = st.columns(2)
        m1.metric("总弹幕数", len(logs) if logs else 0)
        m2.metric("参与人数", len(df["姓名"].unique()) if not df.empty else 0)
        
        st.subheader("📋 详细记录表")
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("📥 导出Excel/CSV", df.to_csv(index=False).encode('utf-8-sig'), "class_log.csv", "text/csv")
        else:
            st.info("暂无数据")
            
        st.markdown("---")
        with st.expander("⚠️ 危险区域"):
            if st.button("🗑️ 清空所有数据 (慎点)", type="primary"):
                db.clear_all()
                st.warning("所有数据已清空！")
                st.rerun()
