import streamlit as st

st.set_page_config(page_title="API Streaming App", page_icon="📊", layout="wide")

st.title("📊 API Streaming Demo")
st.write("Welcome to the API Streaming application!")

st.markdown("""
## Available Pages:
- **CoinGecko** - Live cryptocurrency prices (Bitcoin & Ethereum)
- **Weather** - Live weather data for Denver, CO

Use the sidebar to navigate between pages.
""")

st.info("👈 Select a page from the sidebar to get started!")