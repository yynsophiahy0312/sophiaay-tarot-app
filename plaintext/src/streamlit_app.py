import streamlit as st
import random
import time

# --- 0. 注入 CSS：侧边栏变窄、六爻左对齐、名称醒目 ---
st.markdown(
    """<style>
    [data-testid="stSidebar"] { min-width: 150px; max-width: 150px; }
    .gua-container { display: flex; flex-direction: column; align-items: flex-start; }
    .ben-name { color: #1E88E5; font-weight: bold; }
    .bian-name { color: #E53935; font-weight: bold; }
    </style>""",
    unsafe_allow_html=True,
)

# --- 1. 核心数据库：根据测测截图精准调色 ---
COLOR_MAP = {
    "乾(天)": "#FF9800", "兑(泽)": "#FF9800",
    "震(雷)": "#4CAF50", "巽(风)": "#4CAF50",
    "坎(水)": "#2196F3",
    "离(火)": "#F44336",
    "坤(地)": "#A1694D", "艮(山)": "#A1694D"
}

E_GUA_INFO = {
    "111": "乾(天)", "000": "坤(地)", "010": "坎(水)", "101": "离(火)",
    "001": "震(雷)", "110": "巽(风)", "100": "艮(山)", "011": "兑(泽)"
}
E_GUA_PURE = {"111": "天", "000": "地", "010": "水", "101": "火", "001": "雷", "110": "风", "100": "山", "011": "泽"}

GUA_NAME_MAP = {
    "天天": "乾为天", "地地": "坤为地", "水水": "坎为水", "火火": "离为火",
    "雷雷": "震为雷", "风风": "巽为风", "山山": "艮为山", "泽泽": "兑为泽",
    "地天": "地天泰", "天地": "天地否", "泽火": "泽火革", "水雷": "水雷屯",
    "山火": "山火贲", "风天": "风天小畜", "天风": "天风姤", "泽天": "泽天嬖",
    "火地": "火地晋", "地火": "火地明夷", "山水": "山水蒙", "水山": "水山蹇",
    "雷地": "雷地豫", "地雷": "地雷复", "天水": "天水讼", "水天": "水天需",
    "风雷": "风雷益", "雷风": "雷风恒", "山地": "山地剥", "地山": "地山谦",
    "泽水": "泽水困", "水泽": "水泽节", "天火": "天火同人", "火天": "火天大有",
    "风火": "风火家人", "火风": "火风鼎", "泽地": "泽地萃", "地泽": "地泽临",
    "山天": "山天大畜", "天山": "天山遁", "雷水": "雷水解", "泽风": "泽风大过",
    "风泽": "风泽中孚", "雷天": "雷天大壮", "天雷": "天雷无妄", "山泽": "山泽损",
    "泽山": "泽山咸", "火雷": "火雷噬嗑", "雷火": "雷火丰", "风地": "风地观",
    "地风": "地风升", "水地": "水地比", "地水": "地水师", "火泽": "火泽睽",
    "风山": "风山渐", "山风": "山风蛊", "水风": "水风井", "风水": "风水涣",
    "雷泽": "雷泽归妹", "泽雷": "泽雷随", "山雷": "山雷颐", "雷山": "雷山小过", "天泽": "天泽履"
}

def draw_yao(yao_type, color):
    if yao_type == "1":
        return f'<div style="background-color:{color}; width:140px; height:10px; border-radius:10px; margin:6px 0;"></div>'
    else:
        return f'<div style="display:flex; justify-content:space-between; width:140px; margin:6px 0;"><div style="background-color:{color}; width:65px; height:10px; border-radius:10px;"></div><div style="background-color:{color}; width:65px; height:10px; border-radius:10px;"></div></div>'

# --- 侧边栏 ---
page = st.sidebar.selectbox("", ["🔮 塔罗", "☯️ 六爻"])

# 🔮 塔罗页面 (逻辑锁死)
if page == "🔮 塔罗":
    st.title("塔罗占卜")
    name = st.text_input("请输入你的昵称")
    question = st.text_input("请输入你想占卜的问题")
    tarot = ["愚人","魔术师","女祭司","女皇","皇帝","教皇","恋人","战车","力量","隐士","命运之轮","正义","倒吊人","死神","节制","恶魔","高塔","星星","月亮","太阳","审判","世界", "权杖王牌","权杖二","权杖三","权杖四","权杖五","权杖六","权杖七","权杖八","权杖九","权杖十","权杖侍从","权杖骑士","权杖王后","权杖国王","圣杯王牌","圣杯二","圣杯三","圣杯四","圣杯五","圣杯六","圣杯七","圣杯八","圣杯九","圣杯十","圣杯侍从","圣杯骑士","圣杯王后","圣杯国王","宝剑王牌","宝剑二","宝剑三","宝剑四","宝剑五","宝剑六","宝剑七","宝剑八","宝剑九","宝剑十","宝剑侍从","宝剑骑士","宝剑王后","宝剑国王","星币王牌","星币二","星币三","星币四","星币五","星币六","星币七","星币八","星币九","星币十","星币侍从","星币骑士","星币王后","星币国王"]
    position = ["第一张牌", "第二张牌", "第三张牌"]
    if st.button("开始占卜"):
        if not name or not question: st.warning("请先输入昵称和问题！")
        else:
            available_card = tarot.copy()
            st.write(f"欢迎你 {name}，你的问题是：{question}")
            for pos in position:
                st.write(f"正在抽取 {pos} ...")
                time.sleep(1)
                card = random.choice(available_card); available_card.remove(card)
                orientation = random.choice(["正位", "逆位"])
                st.write(f"塔罗 {pos} - 牌: {card} ({orientation})")
            st.write("占卜结束，祝你好运！")

            # ==========================
            # 人工占卜服务
            # ==========================

            st.markdown("---")

            st.subheader(
                "🔮 人工占卜服务"
            )

            st.markdown("""
            <div style="font-size: 15px; line-height: 1.7;">

            如果你希望获得更加深入的牌面分析，  
            欢迎联系人工占卜服务。  
           （水青蔷老师精通塔罗八字星盘）  
            水青蔷老师 Wechat：aquataurus0429

            <div style="font-size: 14px; font-weight: bold; margin-top: 10px;">服务内容</div>

            ✨ **常规牌阵**　99元/问  
            ✨ **关系牌阵**　198元/问  
            ✨ **二选一牌阵**　132元/问  
            ✨ **三选一牌阵**　198元/问  

            可免费代抽 + 同一事件补充提问（不接急单）

            ---

            <div style="font-size: 14px; font-weight: bold;">🐰 急单服务</div>

            急单可找🐰塔罗师主占卜感情运势  
            Wechat：sjlydz2006  

            **兔子塔罗**

            可急单，擅长感情问题，均包含心理咨询和售后。

            <div style="font-size: 14px; font-weight: bold;">具体问题类</div>

            **感情问题：108元/次**  
            **事业或学业：88元/次**

            <div style="font-size: 14px; font-weight: bold;">运势类</div>

            **感情运**  
            周运：每周88元  
            月运：每月288元  

            
            **事业或学业**  
            周运：每周68元  
            月运：每月228元  

            
            ###详情请添加Wechat咨询
            <div style="font-size: 14px; font-weight: bold;">详情请添加Wechat咨询</div>

            </div>
            """, unsafe_allow_html=True)  
            
            

            st.code(
                "aquataurus0429"
            )

            st.caption(
                "长按微信号即可复制"
            )

            st.code(
                "sjlydz2006"
            )
            st.caption(
                "长按微信号即可复制"
            )

# ☯️ 六爻页面 (五行色对应测测版)
elif page == "☯️ 六爻":
    st.title("六爻占卜")
    name_g = st.text_input("请输入昵称", key="g_n")
    question_g = st.text_input("请输入问题", key="g_q")
    if st.button("开始占卜", key="gua_start"):
        if not name_g or not question_g: st.warning("请填写信息")
        else:
            st.write(f"欢迎你 {name_g}，占卜开始...")
            # 下卦
            sc_l = []
            for i in range(1, 4):
                st.write(f"正在投掷 第 {i} 爻..."); time.sleep(1)
                sc_l.append(sum([random.choice([2, 3]) for _ in range(3)]))
            bt_l = "".join(["1" if s in [7, 9] else "0" for s in sc_l])
            name_l = E_GUA_INFO[bt_l]; col_l = COLOR_MAP[name_l]
            st.write(f"**下卦为：{name_l}**")
            st.markdown(f'<div class="gua-container">{"".join([draw_yao(b, col_l) for b in reversed(bt_l)])}</div>', unsafe_allow_html=True)
            # 上卦
            sc_u = []
            for i in range(4, 7):
                st.write(f"正在投掷 第 {i} 爻..."); time.sleep(1)
                sc_u.append(sum([random.choice([2, 3]) for _ in range(3)]))
            bt_u = "".join(["1" if s in [7, 9] else "0" for s in sc_u])
            name_u = E_GUA_INFO[bt_u]; col_u = COLOR_MAP[name_u]
            st.write(f"**上卦为：{name_u}**")
            st.markdown(f'<div class="gua-container">{"".join([draw_yao(b, col_u) for b in reversed(bt_u)])}</div>', unsafe_allow_html=True)
            # 本卦
            sc_total = sc_l + sc_u; ben_l = ["1" if s in [7, 9] else "0" for s in sc_total]
            st.markdown("---")
            pure = GUA_NAME_MAP.get(E_GUA_PURE[bt_u] + E_GUA_PURE[bt_l], "卦象")
            st.markdown(f'您的六爻本卦为：<span class="ben-name">{pure}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="gua-container">{"".join([draw_yao(ben_l[i], col_u if i >= 3 else col_l) for i in range(5, -1, -1)])}</div>', unsafe_allow_html=True)
            # 变卦
            dong = [i for i, s in enumerate(sc_total) if s in [6, 9]]
            if dong:
                bian_l = ["0" if s == 9 else ("1" if s == 6 else ben_l[i]) for i, s in enumerate(sc_total)]
                b_up = "".join(bian_l[3:]); b_low = "".join(bian_l[:3])
                bian_name = GUA_NAME_MAP.get(E_GUA_PURE[b_up] + E_GUA_PURE[b_low])
                c_u_b = COLOR_MAP[E_GUA_INFO[b_up]]; c_l_b = COLOR_MAP[E_GUA_INFO[b_low]]
                st.markdown(f'您的变卦为：<span class="bian-name">{bian_name}</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="gua-container">{"".join([draw_yao(bian_l[i], c_u_b if i >= 3 else c_l_b) for i in range(5, -1, -1)])}</div>', unsafe_allow_html=True)
            else: st.write("此为静卦，无变卦。")
            st.write("占卜结束，祝你好运！")

            st.markdown("<hr><div style='text-align: center; color: #888; font-size: 13px;'>&copy; 2026 Anita Jingyu. All Rights Reserved.</div>", unsafe_allow_html=True)