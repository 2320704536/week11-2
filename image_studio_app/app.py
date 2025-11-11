import streamlit as st
from typing import Dict

st.set_page_config(page_title="Image Studio", page_icon="🎬", layout="wide")

# ---------- Sidebar: API key + Role ----------
st.sidebar.header("🔑 API & Role Settings")

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""

api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password", value=st.session_state["OPENAI_API_KEY"])
if api_key:
    st.session_state["OPENAI_API_KEY"] = api_key

ROLES: Dict[str, str] = {
    "Video Director": "You visualize stories and direct how they are brought to life on screen.",
    "Game Designer": "You craft interactive systems, level flow, and player motivation.",
    "Photographer": "You think in light, lens, and composition to capture mood and story.",
    "Graphic Designer": "You shape brand, layout, and hierarchy for clear visual communication.",
    "Illustrator": "You convey ideas through stylized drawing, color, and texture.",
}

role = st.sidebar.selectbox("Choose a role:", list(ROLES.keys()))
st.sidebar.write(ROLES.get(role, ""))

# ---------- Title ----------
st.title("Image Studio")
st.caption("Choose your creative role, ask questions, or visualize your ideas with AI!")

tab_chat, tab_image = st.tabs(["💬 Chat Assistant", "🖼 Image Studio"])

# ---------- Role-specific system prompts ----------
ROLE_SYSTEMS = {
    "Video Director": """You are an award-winning film director and creative producer. 
Provide cinematic advice with specifics: shot list, lens suggestions, lighting setups, 
blocking, coverage, transitions, color palette, and emotional beats. Be concise and actionable.""",
    "Game Designer": """You are a senior game designer. Provide core loop, mechanics, level structure, 
progression, difficulty tuning, verbs, and moment-to-moment experience. Include quick examples and scope notes.""",
    "Photographer": """You are a professional photographer. Provide lens choices, aperture, shutter, ISO, 
lighting, composition, color, and post workflow. Tailor to the setting and mood.""",
    "Graphic Designer": """You are a brand and layout designer. Provide grids, type pairing, spacing, 
visual hierarchy, contrast, and accessible color guidance. Offer quick layout wireframe bullets.""",
    "Illustrator": """You are a concept artist / illustrator. Provide composition thumbnails, style cues, 
brush/process tips, color keys, and iteration steps. Keep it practical and paced in steps.""",
}

# ---------- Utility ----------
def has_key():
    if not st.session_state.get("OPENAI_API_KEY"):
        st.warning("Please enter your OpenAI API Key in the left sidebar.")
        return False
    return True


# ---------- Chat Assistant ----------
with tab_chat:
    st.subheader(f"🎬 {role} — Creative Chat Assistant")
    user_q = st.text_area("💭 Enter your question or idea:", placeholder="e.g. How can I make my short film emotionally powerful?", height=140)

    if st.button("✨ Generate Response"):
        if has_key() and user_q.strip():
            try:
                from openai import OpenAI
                client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])

                # ✅ NEW RESPONSES API (correct)
                resp = client.responses.create(
                    model="gpt-4o-mini",
                    input=[
                        {"role": "system", "content": ROLE_SYSTEMS[role]},
                        {"role": "user", "content": user_q},
                    ],
                    temperature=0.7,
                )

                # ✅ Extract output text
                output = resp.output_text
                if not output:
                    # fallback when no output_text available
                    text = ""
                    for item in resp.output:
                        if item.type == "output_text":
                            text += item.text
                    output = text

                st.markdown(output)

            except Exception as e:
                st.error(f"OpenAI error: {e}")


# ---------- Image Studio ----------
with tab_image:
    st.subheader("🖼️ Text-to-Image Generator")

    col1, col2 = st.columns([3, 1])
    with col1:
        img_prompt = st.text_area("Describe your image:", placeholder="e.g. Cyberpunk street at night, glowing neon signs, cinematic lighting", height=120)
    with col2:
        size = st.selectbox("Size", ["1024x1024", "768x768", "512x512"])

    if st.button("🎨 Generate Image"):
        if has_key() and img_prompt.strip():
            try:
                from openai import OpenAI
                import base64

                client = OpenAI(api_key=st.session_state["OPENAI_API_KEY"])

                # ✅ Updated Images API
                img = client.images.generate(
                    model="gpt-image-1",
                    prompt=img_prompt,
                    size=size,
                )

                b64 = img.data[0].b64_json
                st.image(base64.b64decode(b64), caption="Generated Image", use_container_width=True)

            except Exception as e:
                st.error(f"OpenAI image error: {e}")

st.markdown("---")
st.caption("Built for Art & Advanced Big Data · Image Studio Demo")
