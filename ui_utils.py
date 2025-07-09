import streamlit as st
from PIL import Image

def render_header():
    # No logo or heading
    st.markdown("""
    <style>
    .user-bubble {background: #e6f0ff; color: #222; border-radius: 12px; padding: 12px 16px; margin-bottom: 4px; max-width: 70%; display: inline-block;}
    .assistant-bubble {background: #f4f4f8; color: #222; border-radius: 12px; padding: 12px 16px; margin-bottom: 4px; max-width: 70%; display: inline-block;}
    .chat-row {display: flex; align-items: flex-start; margin-bottom: 12px;}
    .user-row { justify-content: flex-end; }
    .assistant-row { justify-content: flex-start; }
    </style>
    """, unsafe_allow_html=True)

def render_chat_history(messages):
    for msg in messages:
        if msg['role'] == 'user':
            st.markdown(f"<div class='chat-row user-row'><div class='user-bubble'>{msg['content'][0]['text'] if msg['content'] and msg['content'][0]['type']=='text' else ''}</div></div>", unsafe_allow_html=True)
            for part in msg['content']:
                if part['type'] == 'image_url':
                    st.image(part['image_url']['url'], caption="Uploaded Image", use_container_width=True)
        elif msg['role'] == 'assistant':
            st.markdown(f"<div class='chat-row assistant-row'><div class='assistant-bubble'>{msg['content'][0]['text'] if msg['content'] and msg['content'][0]['type']=='text' else ''}</div></div>", unsafe_allow_html=True)
