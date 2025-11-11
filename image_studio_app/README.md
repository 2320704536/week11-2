# Image Studio — Role-Aware AI Assistant

A Streamlit app with:
- Sidebar: OpenAI API key field + role selector (Video Director, Game Designer, Photographer, Graphic Designer, Illustrator)
- Tabs: **Chat Assistant** (role-shaped guidance) and **Image Studio** (text-to-image)
- Uses OpenAI Responses API and Images API

## Quickstart
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- Put your OpenAI API key in the left sidebar.
- Models used: `gpt-4o-mini` for chat, `gpt-image-1` for images (change as you like).
