
import streamlit as st
from anthropic import Anthropic
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Claude Studio", page_icon="🎬", layout="wide")

st.sidebar.header("🔑 Claude API Settings")

if "CLAUDE_API_KEY" not in st.session_state:
    st.session_state["CLAUDE_API_KEY"] = ""

api_key = st.sidebar.text_input("Enter Claude API Key:", type="password", value=st.session_state["CLAUDE_API_KEY"])
if api_key:
    st.session_state["CLAUDE_API_KEY"] = api_key

ROLES = {
    "Video Director": "You visualize stories and direct cinematic scenes.",
    "Game Designer": "You craft interactive systems and gameplay progression.",
    "Photographer": "You plan shots based on lens, composition, and lighting.",
    "Graphic Designer": "You build visual hierarchy, layout, and brand clarity.",
    "Illustrator": "You sketch, conceptualize, and refine visual ideas.",
}

role = st.sidebar.selectbox("Choose a role:", list(ROLES.keys()))
st.sidebar.write(ROLES[role])

st.title("Claude Studio")
tab_chat, tab_image = st.tabs(["💬 Chat Assistant", "🖼 Image Studio"])

ROLE_SYSTEMS = {
    "Video Director": "You are an award-winning film director.",
    "Game Designer": "You are a game designer.",
    "Photographer": "You are a photographer.",
    "Graphic Designer": "You are a designer.",
    "Illustrator": "You are an illustrator.",
}

def has_key():
    if not st.session_state.get("CLAUDE_API_KEY"):
        st.warning("Please enter your Claude API Key in the sidebar.")
        return False
    return True

with tab_chat:
    st.subheader(f"{role} — Claude Assistant")
    user_q = st.text_area("Your question:", height=140)

    if st.button("Generate with Claude"):
        if has_key() and user_q.strip():
            try:
                client = Anthropic(api_key=st.session_state["CLAUDE_API_KEY"])
                msg = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=800,
                    system=ROLE_SYSTEMS[role],
                    messages=[{"role":"user","content":user_q}]
                )
                st.markdown(msg.content[0].text)
            except Exception as e:
                st.error(f"Claude API error: {e}")

with tab_image:
    st.subheader("Mock Image Generator")

    img_prompt = st.text_area("Describe image:", height=120)
    size = st.selectbox("Size", ["1024x1024","768x768","512x512"])

    if st.button("Generate Mock Image"):
        w,h = map(int, size.split("x"))
        arr = np.random.randint(0,255,(h,w,3),dtype=np.uint8)
        st.image(arr, caption="Mock Image", use_container_width=True)

st.caption("Claude Studio · Mock Image Mode")
