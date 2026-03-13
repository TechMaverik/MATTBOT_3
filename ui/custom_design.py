CUSTOM_CSS="""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

/* Reset & base */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4f0 !important;
    font-family: 'Space Mono', monospace !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #2a2a3d !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }

/* ── Main container ── */
[data-testid="stMain"] { background: #0a0a0f !important; }
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 900px !important;
}

/* ── Brand header ── */
.brand-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 28px 24px 20px;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 24px;
}
.brand-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 18px rgba(124,58,237,0.45);
}
.brand-name {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800;
    font-size: 1.35rem;
    letter-spacing: -0.02em;
    color: #f0ecff;
    line-height: 1;
}
.brand-sub {
    font-size: 0.65rem;
    color: #6b7280;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 3px;
}

/* ── Sidebar sections ── */
.sidebar-section {
    padding: 0 16px 16px;
}
.sidebar-label {
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 8px;
    padding: 12px 0 4px;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.status-online  { background: rgba(16,185,129,.15); color: #34d399; border: 1px solid rgba(52,211,153,.25); }
.status-offline { background: rgba(239,68,68,.13);  color: #f87171; border: 1px solid rgba(248,113,113,.25); }
.status-dot { width: 7px; height: 7px; border-radius: 50%; }
.dot-on  { background: #34d399; box-shadow: 0 0 6px #34d399; animation: pulse-dot 2s infinite; }
.dot-off { background: #f87171; }
@keyframes pulse-dot { 0%,100%{opacity:1} 50%{opacity:.4} }

/* ── Page title ── */
.page-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #f0ecff;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.78rem;
    color: #6b7280;
    margin-bottom: 2rem;
}

/* ── Chat container ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 32px;
}

/* ── Message bubbles ── */
.msg-row { display: flex; gap: 12px; align-items: flex-start; }
.msg-row.user  { flex-direction: row-reverse; }

.avatar {
    width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.avatar-user { background: linear-gradient(135deg, #7c3aed, #a855f7); }
.avatar-ai   { background: linear-gradient(135deg, #1e293b, #334155); border: 1px solid #2a2a3d; }

.bubble {
    max-width: 78%;
    padding: 13px 17px;
    border-radius: 14px;
    font-size: 0.88rem;
    line-height: 1.65;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble-user {
    background: linear-gradient(135deg, #5b21b6, #7c3aed);
    color: #f0e6ff;
    border-bottom-right-radius: 4px;
}
.bubble-ai {
    background: #13131f;
    border: 1px solid #1e1e30;
    color: #d1cce8;
    border-bottom-left-radius: 4px;
}

.msg-time {
    font-size: 0.6rem;
    color: #374151;
    margin-top: 5px;
    letter-spacing: 0.05em;
}
.msg-row.user  .msg-time { text-align: right; }
.msg-row.ai    .msg-time { text-align: left; }

/* ── Typing indicator ── */
.typing-dots { display: flex; gap: 5px; padding: 6px 2px; }
.typing-dots span {
    width: 7px; height: 7px; border-radius: 50%;
    background: #7c3aed;
    animation: bounce 1.2s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: .2s; }
.typing-dots span:nth-child(3) { animation-delay: .4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-8px)} }

/* ── Input area ── */
.stTextArea textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 12px !important;
    color: #e8e4f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: 14px 16px !important;
    resize: none !important;
    transition: border-color .2s !important;
}
.stTextArea textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.18) !important;
}
.stTextArea textarea::placeholder { color: #374151 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 10px 22px !important;
    letter-spacing: 0.04em !important;
    transition: all .2s !important;
    box-shadow: 0 4px 14px rgba(124,58,237,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Clear button style */
.clear-btn > button {
    background: transparent !important;
    border: 1px solid #2a2a3d !important;
    color: #6b7280 !important;
    box-shadow: none !important;
}
.clear-btn > button:hover {
    border-color: #f87171 !important;
    color: #f87171 !important;
    box-shadow: none !important;
}

/* ── Selectbox / sliders ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] select {
    background: #0f0f1a !important;
    border: 1px solid #2a2a3d !important;
    color: #e8e4f0 !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
}
.stSlider [data-testid="stSlider"] > div { color: #a855f7 !important; }
label, .stSlider label { color: #9ca3af !important; font-size: 0.72rem !important; }

/* ── Welcome card ── */
.welcome-card {
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin: 40px auto;
    max-width: 500px;
}
.welcome-icon { font-size: 3rem; margin-bottom: 16px; }
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ecff;
    margin-bottom: 10px;
}
.welcome-text { font-size: 0.8rem; color: #6b7280; line-height: 1.7; }

/* ── Token stats ── */
.stat-row { display: flex; gap: 10px; margin-top: 12px; }
.stat-box {
    flex: 1;
    background: #0f0f1a;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 10px 12px;
}
.stat-val { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #a855f7; }
.stat-lbl { font-size: 0.6rem; color: #4b5563; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 2px; }

/* ── Dividers ── */
hr { border-color: #1e1e2e !important; margin: 12px 0 !important; }
</style>
"""
INFO="""
    <div class="welcome-card">
        <div class="welcome-icon"></div>
        <div class="welcome-title">Welcome Akhil Jacob</div>
        <div class="welcome-text">
            Your data never leaves your machine.
        </div>
    </div>
    """
