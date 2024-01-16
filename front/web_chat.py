import streamlit as st
from page.chat import chat_page

def init_web():
    st.set_page_config(
        page_title="Text2Image",
        page_icon="🤖",
        layout="wide",
    )

if __name__ == '__main__':
    init_web()
    chat_page()