import os, time, json, requests, pandas as pd, numpy as np
import streamlit as st

# =========================
# Mobile-first page config
# =========================
st.set_page_config(
    page_title="AI Steward • Mobile",
    page_icon="🤝",
    layout="wide",   # wide + custom CSS gives us full-viewport on phones
    initial_sidebar_state="collapsed"
)

# Simple brand placeholders (leave as-is for now)
UNION_NAME = os.getenv("UNION_NAME", "Your Union Name")
LOCAL_NUM  = os.getenv("LOCAL_NUM", "Local ####")

API_URL    = os.getenv("STEWARD_API", "http://localhost:8080/ask")
API_TOKEN  = os.getenv("API_TOKEN", "")

# =========================
# Lightweight mobile styles
# =========================
st.markdown("""
<style>
/* Remove default padding and tighten layout for phones */
.block-container { padding: 0.8rem 0.8rem 5rem 0.8rem; }
header[data-testid="stHeader"] { display: none; }
footer { visibility: hidden; }
section[data-testid="stSidebar"] { display: none; }

/* Mobile cards */
.card {
  background: #ffffff;
  border: 1px solid #E6E6E6;
  border-radius: 14px;
  padding: 14px 14px 10px 14px;
  margin-bottom: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

/* Sticky top bar */
.topbar {
  position: sticky; top: 0; z-index: 99;
  background: #2E8540; color: #fff;
  padding: 10px 12px; margin: -8px -8px 10px -8px;
  display: flex; align-items: center; justify-content: space-between;
}
.topbar h1 { font-size: 1.1rem; margin: 0; }
.badge { background:#1f6f30; border-radius: 10px; padding: 3px 8px; font-size: .72rem; }

/* Big touch buttons */
button[kind="primary"] { height: 46px; font-weight: 700; }
.stTextInput > div > div > input, textarea, .stTextArea textarea {
  font-size: 1.02rem !important;
}
.metric-3 { display:flex; gap:10px; }
.metric-3 .item {
  flex: 1; text-align:center; background:#F7FBF8; border:1px solid #E1F0E6; border-radius:12px; padding:10px 6px;
}
.metric-3 .kpi { font-size:1.2rem; font-weight:800; }
.metric-3 .lbl { font-size:.78rem; color:#3a3a3a; }

.small { font-size:.84rem; color:#5a5a5a; }
.tag  { display:inline-block; background:#E7F3EA; color:#1f6f30; border:1px solid #BFE1CB; font-size:.70rem; padding:2px 7px; border-radius:16px; margin-right:6px; margin-bottom:4px;}
.qrow { border-top:1px dashed #e9e9e9; padding-top:8px; margin-top:8px; }
.chat-bubble-u { background:#F2F8F4; border:1px solid #D7EADB; border-radius:10px; padding:10px; }
.chat-bubble-a { background:#fff; border:1px solid #E6E6E6; border-radius:10px; padding:10px; }
</style>
""", unsafe_allow_html=True)

# =========================
# Fake demo data (placeholders)
# Replace with your logs/db later
# =========================
def demo_data():
    topics = ["Leave", "Scheduling", "Safety", "Benefits", "Discipline"]
    regions = ["North", "Central", "East", "South", "West"]
    rng = np.random.default_rng(42)
    heat = pd.DataFrame({
        "Region": np.repeat(regions, len(topics)),
        "Topic": topics * len(regions),
        "Count": rng.integers(2, 35, size=len(topics)*len(regions))
    })
    questions = [
        {"topic":"Leave","q":"Am I protected while on FMLA?","age":"2h"},
        {"topic":"Scheduling","q":"Can I refuse overtime when off-duty?","age":"4h"},
        {"topic":"Safety","q":"What are incident reporting timelines?","age":"1d"},
        {"topic":"Benefits","q":"When does health coverage start?","age":"1d"},
        {"topic":"Discipline","q":"Do I get union representation in an interview?","age":"2d"},
    ]
    stewards = pd.DataFrame({
        "Steward":["A","B","C","D"],
        "Open":[12,7,9,6],
        "Closed":[22,15,17,13]
    })
    wins_month = int(28 + rng.integers(-3, 6))
    return heat, questions, stewards, wins_month

heat, questions, stewards, wins_month = demo_data()

# =========================
# Top bar
# =========================
st.markdown(
    f"""
    <div class="topbar">
      <h1>AI Steward • <span class="badge">{UNION_NAME} | {LOCAL_NUM}</span></h1>
      <div class="badge">Mobile</div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# KPI row
# =========================
total_q = int(heat["Count"].sum())
open_cases = int(stewards["Open"].sum())
delta_wins = "+4 from last week"

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="metric-3">', unsafe_allow_html=True)
st.markdown(f'<div class="item"><div class="kpi">{total_q}</div><div class="lbl">Questions (30d)</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="item"><div class="kpi">{open_cases}</div><div class="lbl">Open Cases</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="item"><div class="kpi">{wins_month}</div><div class="lbl">Union Wins • <span class="small">{delta_wins}</span></div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Member Sentiment (compact heat “chips”)
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**Member Sentiment**")
cols = st.columns(5)
for i, r in enumerate(["North","Central","East","South","West"]):
    with cols[i]:
        sub = heat[heat["Region"]==r]
        # Simple compact indicator: sum of counts to keep it lightweight on phones
        score = int(sub["Count"].mean())
        color = "#D84E4E" if score>22 else ("#F3A93D" if score>14 else "#2E8540")
        st.markdown(f"""
            <div style="border:1px solid #eee;border-radius:10px;padding:10px;text-align:center;">
               <div style="font-size:.78rem;color:#444;">{r}</div>
               <div style="font-weight:800;color:{color};">{score}</div>
            </div>
        """, unsafe_allow_html=True)
st.caption("Higher score = higher concern. Tap a steward if your area is red.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Voice of the Members
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**Voice of the Members**")
for row in questions:
    st.markdown(
        f"""<div class="qrow">
               <span class="tag">{row['topic']}</span>
               <span class="small">{row['age']} ago</span>
               <div style="margin-top:6px;">{row['q']}</div>
            </div>""",
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Steward activity (compact bars)
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**Steward Activity**")
bar_cols = st.columns(len(stewards))
for i, r in stewards.iterrows():
    with bar_cols[i]:
        total = r["Open"] + r["Closed"]
        pct = 0 if total==0 else int(100 * r["Closed"]/total)
        st.markdown(f"""
            <div style="text-align:center;">
              <div style="font-size:.8rem;margin-bottom:6px;">{r['Steward']}</div>
              <div style="height:90px;width:24px;margin:0 auto;border:1px solid #ddd;border-radius:6px;overflow:hidden;background:#f8f8f8;">
                <div style="height:{pct}%;background:#2E8540;"></div>
              </div>
              <div class="small" style="margin-top:6px;">Closed {pct}%</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Chat preview + Ask box
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**AI Steward Chat**")

with st.container():
    st.markdown('<div class="chat-bubble-u">Am I allowed representation at my evaluation?</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-bubble-a">Yes. If you reasonably believe discipline may result, you may request a union representative.</div>', unsafe_allow_html=True)

q = st.text_input("Type your question…", placeholder="Example: What article covers overtime?")
colA, colB = st.columns([1,1])
with colA:
    verbatim = st.toggle("Exact quote", value=False, help="Return verbatim contract text with citation")
with colB:
    ask = st.button("Ask Steward", use_container_width=True)

if ask and q.strip():
    headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
    try:
        r = requests.post(API_URL, headers=headers, json={"question": q, "verbatim": verbatim}, timeout=25)
        if r.ok:
            data = r.json()
            st.success("Response ready")
            st.markdown(f'<div class="chat-bubble-a">{data.get("answer","(no answer)")}</div>', unsafe_allow_html=True)
            if data.get("citations"):
                with st.expander("Citations"):
                    st.write("\n".join(map(str, data["citations"])))
        else:
            st.error(f"Service error: {r.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# Solidarity Spotlight
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("**Solidarity Spotlight**")
st.write("“Because of the union, I kept my job and my dignity.” — Member Story")
st.caption("Replace with your own rotating spotlights, images, or short videos.")
st.markdown('</div>', unsafe_allow_html=True)

# Bottom spacer for mobile scroll
st.write("")
st.write("")
