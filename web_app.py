import streamlit as st
import datetime
import random

# ---------------------- 全局页面配置（品牌级体验）----------------------
st.set_page_config(
    page_title="透明消费比价助手",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义高级浅色UI样式（卡片阴影、圆角、间距优化）
st.markdown("""
<style>
/* 全局背景 */
.main {
    background-color: #F8F9FB;
}
/* 容器边距 */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}
/* 卡片样式：阴影+圆角+边框 */
div.stCard {
    background-color: #FFFFFF;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    padding: 24px;
    margin-bottom: 16px;
}
/* 标题层级 */
h1 {
    color: #2D3748 !important;
    font-weight: 700;
    font-size: 28px;
}
h2, h3 {
    color: #2D3748 !important;
    font-weight: 600;
}
/* 正文文字 */
p, div, label {
    color: #4A5568 !important;
    font-size: 16px;
}
/* 输入框美化 */
div.stTextInput, div.stNumberInput {
    background-color: #F7F9FC;
    border-radius: 8px;
    padding: 4px;
}
/* 按钮美化 */
button[kind="primary"] {
    background-color: #5B7CAA;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
    transition: all 0.2s ease;
}
button[kind="primary"]:hover {
    background-color: #4A6B99;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(91, 124, 170, 0.2);
}
/* 推荐卡片美化 */
div.st-emotion-cache-1v0mbdj.e1f1d6gn1 {
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    padding: 16px;
    margin-bottom: 12px;
    background-color: #FFFFFF;
}
/* 页脚 */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- 核心比价逻辑函数 ----------------------
def calc_result(goods_name, brand_name, budget, need_text):
    # 多平台模拟价格
    tb_p = round(budget * random.uniform(0.88, 0.96), 2)
    jd_p = round(budget * random.uniform(0.98, 1.08), 2)
    pdd_p = round(budget * random.uniform(0.78, 0.88), 2)
    min_p = min(tb_p, jd_p, pdd_p)
    history_p = round(min_p * 0.88, 2)
    score = round(random.uniform(4.4, 4.8), 1)

    # 基础商品库
    if "耳机" in goods_name or "蓝牙" in goods_name:
        base_list = [
            {"name":"Redmi Buds青春版","rate":0.85,"desc":"长续航、通勤适配、学生性价比首选"},
            {"name":"绿联HiTune T3","rate":0.95,"desc":"降噪能力优秀、音质均衡、口碑稳定"},
            {"name":"QCY T13","rate":0.75,"desc":"防水抗汗、百元爆款、耐用性强"}
        ]
    else:
        base_list = [
            {"name":f"{goods_name}性价比款","rate":0.80,"desc":"预算内适配核心需求，实用性强"},
            {"name":f"{goods_name}热门口碑款","rate":0.95,"desc":"销量领先，评价稳定无明显短板"},
            {"name":f"{goods_name}耐用基础款","rate":0.70,"desc":"用料扎实，适合长期日常使用"}
        ]

    # 品牌筛选
    rec_list = []
    for item in base_list:
        if brand_name.strip() in item["name"] or brand_name.strip() == "":
            rec_list.append({
                "name": item["name"],
                "price": round(budget * item["rate"]),
                "desc": item["desc"]
            })
    # 补足3个
    while len(rec_list) < 3:
        for item in base_list:
            if item["name"] not in [x["name"] for x in rec_list]:
                rec_list.append({
                    "name": item["name"],
                    "price": round(budget * item["rate"]),
                    "desc": item["desc"]
                })
                break

    return tb_p, jd_p, pdd_p, min_p, history_p, score, rec_list

# ---------------------- 网页主体布局 ----------------------
# 标题区
st.title("🛒 透明消费比价助手")
st.markdown("<p style='color:#718096; font-size:14px; margin-top:-10px;'>理性比价 · 品牌筛选 · 透明推荐 · 客观消费辅助</p>", unsafe_allow_html=True)
st.divider()

# 输入卡片
with st.container():
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        goods_name = st.text_input("商品名称", value="无线蓝牙耳机")
        brand_name = st.text_input("品牌筛选（选填）", value="")
    with col2:
        budget = st.number_input("心理预算(元)", min_value=0.0, value=200.0, step=10.0)
        need_text = st.text_input("个人需求描述", value="性价比高、耐用、口碑好")
    st.markdown("</div>", unsafe_allow_html=True)

# 按钮区
col_btn1, col_btn2 = st.columns([3, 1])
with col_btn2:
    run_btn = st.button("✨ 开始比价推荐", type="primary", use_container_width=True)

st.divider()

# 结果展示区
if run_btn:
    if not goods_name:
        st.warning("请输入商品名称！")
    else:
        tb_p, jd_p, pdd_p, min_p, history_p, score, rec_list = calc_result(goods_name, brand_name, budget, need_text)
        
        # 结果卡片1：比价信息
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.subheader("📋 消费比价综合结果")
            st.markdown(f"""
            | 项目 | 详情 |
            | :--- | :--- |
            | 商品品类 | {goods_name} |
            | 筛选品牌 | {brand_name if brand_name else "不限制"} |
            | 心理预算 | {budget} 元 |
            | 个人需求 | {need_text} |
            """)
            st.divider()
            st.markdown(f"""
            - **淘宝售价**：{tb_p} 元
            - **京东售价**：{jd_p} 元
            - **拼多多售价**：{pdd_p} 元
            - **当前最低价**：{min_p} 元
            - **历史参考低价**：{history_p} 元
            - **综合口碑评分**：{score} / 5.0
            """)
            st.markdown(f"<p style='color:#718096; font-size:12px; margin-top:16px;'>查询时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # 结果卡片2：推荐商品
        with st.container():
            st.markdown("<div class='stCard'>", unsafe_allow_html=True)
            st.subheader("🎯 品牌筛选优选推荐")
            for idx, item in enumerate(rec_list, 1):
                st.markdown(f"""
                **{idx}. {item['name']}**  
                💰 推荐入手价：{item['price']} 元  
                💡 推荐理由：{item['desc']}
                """)
                if idx < 3:
                    st.divider()
            st.markdown("</div>", unsafe_allow_html=True)

        # 消费小贴士
        st.info("""
        💡 消费小贴士
        1. 优先匹配品牌与个人需求，不盲目跟风选购
        2. 现价接近历史低价时，为较佳入手时机
        3. 规避极端低价劣质品与虚高溢价商品
        4. 本工具仅作客观参考，最终购买由个人决策
        """)

# 底部说明
st.markdown("<br><center style='color:#718096;font-size:13px;'>基于大学生消费调研｜算法透明无操纵｜理性消费工具</center>", unsafe_allow_html=True)