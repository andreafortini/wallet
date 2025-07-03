import streamlit as st

st.set_page_config(page_title="Investment Management", layout="wide")

home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
insight_page = st.Page("pages/insight.py", title="Insight", icon="📈")
history_page = st.Page("pages/history.py", title="History", icon="📄")
settings_page = st.Page("pages/settings.py", title="Settings", icon="⚙️")

pg = st.navigation([home_page, insight_page, history_page, settings_page])
pg.run()
