import streamlit as st
import requests
import json
import time
from ui import custom_design
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MATTBOT 3",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(custom_design.CUSTOM_CSS, unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3"


# ── Helpers ───────────────────────────────────────────────────────────────────
def get_ollama_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=4)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            return models if models else [DEFAULT_MODEL]
    except Exception:
        pass
    return None


def check_ollama_status():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def stream_chat(messages, model, temperature, max_tokens):
    """Send chat to Ollama and yield streamed text chunks."""
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    try:
        with requests.post(
            f"{OLLAMA_URL}/api/chat",
            json=payload,
            stream=True,
            timeout=120,
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        delta = chunk.get("message", {}).get("content", "")
                        if delta:
                            yield delta
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue
    except requests.exceptions.ConnectionError:
        yield "\n\n⚠️  Cannot reach Ollama. Make sure `ollama serve` is running."
    except requests.exceptions.Timeout:
        yield "\n\n⚠️  Request timed out. The model may be loading — try again."
    except Exception as e:
        yield f"\n\n⚠️  Error: {e}"


def fmt_time(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M")


# ── Session state init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []      # [{role, content, ts}]
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="brand-header">
        <div class="brand-icon"></div>
        <div>
            <div class="brand-name">MATTBOT</div>
            <div class="brand-sub">Settings</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Server status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Server Status</div>', unsafe_allow_html=True)
    online = check_ollama_status()
    if online:
        st.markdown('<div class="status-pill status-online"><span class="status-dot dot-on"></span>Ollama Online</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill status-offline"><span class="status-dot dot-off"></span>Ollama Offline</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.7rem;color:#6b7280;margin-top:6px;">Run <code style="background:#1a1a2e;padding:2px 5px;border-radius:4px;color:#a855f7;">ollama serve</code> to connect.</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Model selection
    st.markdown('<div class="sidebar-label">Model</div>', unsafe_allow_html=True)
    models = get_ollama_models()
    if models:
        selected_model = st.selectbox("", models, label_visibility="collapsed")
    else:
        selected_model = DEFAULT_MODEL
        st.markdown(f'<p style="font-size:0.75rem;color:#a855f7;">Using: {DEFAULT_MODEL}</p>', unsafe_allow_html=True)

    st.markdown("---")

    # Parameters
    st.markdown('<div class="sidebar-label">Parameters</div>', unsafe_allow_html=True)
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05,
                            help="Higher = more creative, Lower = more focused")
    max_tokens = st.slider("Max Tokens", 128, 4096, 1024, 128,
                           help="Maximum tokens in the response")

    st.markdown("---")

    # System prompt
    st.markdown('<div class="sidebar-label">System Prompt</div>', unsafe_allow_html=True)
    system_prompt = st.text_area(
        "",
        value="You are Mattbot, a brilliant and thoughtful AI assistant. You give clear, insightful, and well-structured answers. My name is Akhil Jacob. You can call me Akhil",
        height=110,
        label_visibility="collapsed",
        key="sys_prompt",
    )

    st.markdown("---")

    # Stats
    st.markdown('<div class="sidebar-label">Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-val">{st.session_state.msg_count}</div>
            <div class="stat-lbl">Messages</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{st.session_state.total_tokens}</div>
            <div class="stat-lbl">Est. Tokens</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑  Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.total_tokens = 0
            st.session_state.msg_count = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Main area ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">Mattbot 3</div>
<div class="page-subtitle">Powered by HLEngine 3</div>
""", unsafe_allow_html=True)

# Chat history display
if not st.session_state.messages:
    st.markdown(custom_design.INFO, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        ts = fmt_time(msg.get("ts", time.time()))

        if role == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div>
                    <div class="bubble bubble-user">{content}</div>
                    <div class="msg-time">{ts}</div>
                </div>
                <div class="avatar avatar-user">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row ai">
                <div class="avatar avatar-ai">👽</div>
                <div>
                    <div class="bubble bubble-ai">{content}</div>
                    <div class="msg-time">{ts}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Input area ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_area(
        "Message",
        placeholder="Ask Mattbot 3 anything…  (Ctrl+Enter to send)",
        height=90,
        label_visibility="collapsed",
        key="user_input",
    )

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    send = st.button("Send →", use_container_width=True)

# ── Send logic ─────────────────────────────────────────────────────────────────
if send and user_input.strip():
    if not online:
        st.error("⚠️  Ollama is not running. Please start it with `ollama serve`.")
    else:
        prompt = user_input.strip()
        ts_now = time.time()

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt, "ts": ts_now})
        st.session_state.msg_count += 1
        st.session_state.total_tokens += len(prompt.split())

        # Build Ollama messages payload
        ollama_msgs = [{"role": "system", "content": system_prompt}]
        for m in st.session_state.messages:
            ollama_msgs.append({"role": m["role"], "content": m["content"]})

        # Stream response
        st.rerun()  # re-render to show user bubble first

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Show typing indicator + stream
    with st.spinner(""):
        st.markdown("""
        <div class="msg-row ai" style="margin-top:12px;">
            <div class="avatar avatar-ai"></div>
            <div class="bubble bubble-ai">
                <div class="typing-dots"><span></span><span></span><span></span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        ollama_msgs = [{"role": "system", "content": st.session_state.get("sys_prompt", "")}]
        for m in st.session_state.messages:
            ollama_msgs.append({"role": m["role"], "content": m["content"]})

        response_text = ""
        response_placeholder = st.empty()

        for chunk in stream_chat(ollama_msgs, selected_model, temperature, max_tokens):
            response_text += chunk
            response_placeholder.markdown(f"""
            <div class="msg-row ai">
                <div class="avatar avatar-ai"></div>
                <div>
                    <div class="bubble bubble-ai">{response_text}▌</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        response_placeholder.empty()

        if response_text:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "ts": time.time(),
            })
            st.session_state.msg_count += 1
            st.session_state.total_tokens += len(response_text.split())

        st.rerun()
