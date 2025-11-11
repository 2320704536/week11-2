import streamlit as st
import base64
from typing import Dict
from anthropic import Anthropic

st.set_page_config(page_title="Claude Studio", page_icon="🎬", layout="wide")

# ---------- Sidebar ----------
st.sidebar.header("🔑 Claude API Settings")

if "CLAUDE_API_KEY" not in st.session_state:
    st.session_state["CLAUDE_API_KEY"] = ""

api_key = st.sidebar.text_input("Enter Claude API Key:", type="password", value=st.session_state["CLAUDE_API_KEY"])
if api_key:
    st.session_state["CLAUDE_API_KEY"] = api_key

ROLES: Dict[str, str] = {
    "Video Director": "You visualize stories and direct cinematic scenes.",
    "Game Designer": "You craft interactive systems and gameplay progression.",
    "Photographer": "You plan shots based on lens, composition, and lighting.",
    "Graphic Designer": "You build visual hierarchy, layout, and brand clarity.",
    "Illustrator": "You sketch, conceptualize, and refine visual ideas.",
}

role = st.sidebar.selectbox("Choose a role:", list(ROLES.keys()))
st.sidebar.write(ROLES[role])

# ---------- Title ----------
st.title("Claude Studio")
st.caption("Creative Role Helper + Mock Image Studio (Claude-powered)")

tab_chat, tab_image = st.tabs(["💬 Chat Assistant", "🖼 Image Studio"])

# Claude system prompts
ROLE_SYSTEMS = {
    "Video Director": """You are an award-winning film director. Give shot lists, lenses, lighting, transitions, color palettes.""",
    "Game Designer": """You are a game designer. Provide loops, mechanics, level design, difficulty tuning.""",
    "Photographer": """You are a pro photographer. Give camera settings, lighting, composition, color tips.""",
    "Graphic Designer": """You are a designer. Provide layout, typography, spacing, visual hierarchy, color guidance.""",
    "Illustrator": """You are an illustrator. Provide composition, style, brush, lighting, color palettes, sketch ideas.""",
}

def has_key():
    if not st.session_state.get("CLAUDE_API_KEY"):
        st.warning("Please enter your Claude API Key in the sidebar.")
        return False
    return True

# ---------- Chat Assistant ----------
with tab_chat:
    st.subheader(f"🎬 {role} — Claude Assistant")

    user_q = st.text_area("💭 Your question:", height=140, placeholder="e.g. How do I make my short film emotional?")

    if st.button("✨ Generate with Claude"):
        if has_key() and user_q.strip():
            try:
                client = Anthropic(api_key=st.session_state["CLAUDE_API_KEY"])

                message = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=800,
                    system=ROLE_SYSTEMS[role],
                    messages=[
                        {"role": "user", "content": user_q}
                    ]
                )

                output = message.content[0].text
                st.markdown(output)

            except Exception as e:
                st.error(f"Claude API error: {e}")

# ---------- Image Studio ----------
with tab_image:
    st.subheader("🖼 Mock Image Generator (Claude-powered description)")

    col1, col2 = st.columns([3, 1])
    with col1:
        img_prompt = st.text_area("Describe the image you want:", height=120)
    with col2:
        size = st.selectbox("Size", ["1024x1024", "768x768", "512x512"])

    if st.button("🎨 Generate Mock Image"):
        if not img_prompt.strip():
            st.warning("Please enter a description.")
        else:
            # Let Claude generate a nice image prompt
            try:
                if has_key():
                    client = Anthropic(api_key=st.session_state["CLAUDE_API_KEY"])
                    message = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=300,
                        system="Rewrite the prompt into a detailed cinematic image description.",
                        messages=[{"role": "user", "content": img_prompt}]
                    )
                    refined_prompt = message.content[0].text
                    st.success("Claude refined your prompt:")
                    st.write(refined_prompt)
            except:
                refined_prompt = img_prompt

            # Generate a placeholder colorful image
            import numpy as np
            import matplotlib.pyplot as plt

            w, h = map(int, size.split("x"))
            arr = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)

            st.image(arr, caption="Mock Image (Placeholder)", use_container_width=True)

st.markdown("---")
st.caption("Claude Studio · Fully Free (Mock Image Mode)")
