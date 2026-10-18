import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables early so configuration is ready
load_dotenv()
MODEL_NAME = os.getenv("MODEL", "qwen2.5:7b")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")

# Ensure Ollama server is running (with terminal log prints)
from src.ollama_manager import ensure_ollama_running
ollama_ok, ollama_status = ensure_ollama_running(BASE_URL)

from src.stark_kernel import run_stark_kernel

# Streamlit Page configuration with custom tab title and dark theme settings
st.set_page_config(
    page_title="S.T.A.R.K. | Stock Testing, Analytics & Ratio Kernel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling injecting Carbon Obsidian palette and typography
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global Dark Theme Tokens */
    :root {
        --carbon-obsidian: #0B0F17;
        --surface-card: #111827;
        --surface-border: #1F2937;
        --reactor-cyan: #00F0FF;
        --quant-emerald: #10B981;
        --amber-signal: #F59E0B;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
    }

    /* Background and typography overrides */
    .stApp {
        background-color: var(--carbon-obsidian);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, sans-serif;
    }

    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #0E131F !important;
        border-right: 1px solid var(--surface-border);
    }

    /* Code blocks and monospace telemetry */
    code, pre, .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Custom Header Container */
    .stark-header-container {
        display: flex;
        align-items: center;
        gap: 18px;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid var(--surface-border);
        margin-bottom: 24px;
    }

    .stark-brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.1;
    }

    .stark-brand-title span {
        color: var(--reactor-cyan);
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }

    .stark-tagline {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: var(--text-muted);
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    /* Telemetry pill badges */
    .telemetry-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid var(--surface-border);
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }
    .status-dot.online {
        background-color: var(--quant-emerald);
        box-shadow: 0 0 8px var(--quant-emerald);
    }
    .status-dot.offline {
        background-color: #EF4444;
        box-shadow: 0 0 8px #EF4444;
    }

    /* Chat input styling */
    .stChatInputContainer {
        border-color: var(--surface-border) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# "Ratio Slash" S-Monogram SVG Logo
RATIO_SLASH_SVG = """
<svg width="48" height="48" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F0FF" />
      <stop offset="100%" stop-color="#0080FF" />
    </linearGradient>
    <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" mode="over" />
    </filter>
  </defs>
  <!-- Top Geometric Chevron of the 'S' -->
  <path d="M78 22 H32 C24 22 18 28 18 36 C18 44 24 50 34 50 L46 50" 
        stroke="url(#cyanGlow)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" />
  
  <!-- Bottom Geometric Chevron of the 'S' -->
  <path d="M54 50 L66 50 C76 50 82 56 82 64 C82 72 76 78 68 78 H22" 
        stroke="url(#cyanGlow)" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" />
  
  <!-- Glowing Ratio Division Slash (/) -->
  <line x1="72" y1="14" x2="28" y2="86" 
        stroke="#00F0FF" stroke-width="7" stroke-linecap="round" filter="url(#glowFilter)" />
</svg>
"""

# Render Header with SVG Logo and STARK Branding
status_class = "online" if ollama_ok else "offline"
status_label = "ONLINE" if ollama_ok else "OFFLINE"

st.markdown(
    f"""
    <div class="stark-header-container">
        <div>{RATIO_SLASH_SVG}</div>
        <div>
            <div class="stark-brand-title">S.T.A.R.K. <span>KERNEL</span></div>
            <div class="stark-tagline">Stock Testing, Analytics &amp; Ratio Kernel [v1.0]</div>
        </div>
        <div style="margin-left: auto;">
            <div class="telemetry-badge">
                <span class="status-dot {status_class}"></span>
                <span>{status_label}</span>
                <span style="color: #64748B;">|</span>
                <span style="color: #00F0FF;">{MODEL_NAME}</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Warning banner if Ollama offline
if not ollama_ok:
    st.warning(f"⚠️ {ollama_status} (You may need to run `ollama serve` manually).")

# Sidebar Configuration
with st.sidebar:
    if os.path.exists("assets/stark_logo.jpg"):
        st.image("assets/stark_logo.jpg", width=80)
    else:
        st.markdown(RATIO_SLASH_SVG, unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="margin-top: -10px; margin-bottom: 15px;">
            <strong style="color: #F8FAFC; font-size: 1.2rem; letter-spacing: -0.02em;">S.T.A.R.K.</strong><br/>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">v1.0 Quantitative Kernel</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    st.markdown("### 📡 Telemetry & Specs")
    st.markdown(
        f"""
        - **Engine:** `{MODEL_NAME}`
        - **Endpoint:** `{BASE_URL}`
        - **Architecture:** `Deterministic Math & Intel`
        - **Status:** <span style="color: {'#10B981' if ollama_ok else '#EF4444'}; font-weight: bold;">{status_label}</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🧮 Ratio Suite")
    st.markdown(
        """
        - **Valuation:** P/E, P/B, EV/EBITDA, DCF
        - **Solvency:** Debt-to-Equity, Quick Ratio
        - **Profitability:** ROE, ROIC, Gross Margin
        """
    )

    st.markdown("---")
    if st.button("🔄 Reset Telemetry Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "**S.T.A.R.K. Kernel Online.** Initialized for fundamental stock analytics, "
                "ratio verification, and financial telemetry synthesis. Ready for prompt or raw data ingestion."
            ),
        }
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("[STARK-INPUT] Enter ticker, financial data, or ratio telemetry..."):
    # Display user message in chat message container
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare chat history for OpenAI-compatible endpoint
    history_for_llm = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
        if m["role"] in ("user", "assistant")
    ]

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="⚡"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Stream response directly from run_stark_kernel
            stream = run_stark_kernel(
                prompt=prompt,
                conversation_history=history_for_llm,
                stream=True
            )
            for chunk in stream:
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
        except Exception as e:
            error_message = (
                f"⚠️ **[STARK-ERROR] Telemetry link failure ({BASE_URL}):** {e}\n\n"
                f"*Verify local Ollama status (`ollama serve`) or inspect `.env` configurations.*"
            )
            response_placeholder.markdown(error_message)
            full_response = error_message

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
