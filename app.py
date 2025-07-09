import os
import streamlit as st
from PIL import Image
import io
from llm_utils import encode_image_to_base64, send_message
from ui_utils import render_header, render_chat_history

# Load environment variables and check
api_key = os.getenv('AZURE_OPENAI_KEY')
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
api_version = os.getenv('AZURE_OPENAI_API_VERSION')
deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

st.set_page_config(page_title="openai", layout="wide")
render_header()

if not all([api_key, endpoint, api_version, deployment_name]):
    st.error("Please set all required Azure OpenAI credentials in your .env file.")
    st.stop()

# --- Chat Management ---
if 'chats' not in st.session_state:
    st.session_state['chats'] = {}
if 'current_chat' not in st.session_state:
    st.session_state['current_chat'] = None

# Sidebar for chat selection/creation/rename
with st.sidebar:
    st.markdown("## 💬 Chats")
    chat_names = list(st.session_state['chats'].keys())
    if chat_names:
        selected = st.radio("Select a chat:", chat_names, index=chat_names.index(st.session_state['current_chat']) if st.session_state['current_chat'] in chat_names else 0)
        st.session_state['current_chat'] = selected
        # Rename chat
        new_name = st.text_input("Rename chat:", value=selected, key='rename_chat')
        if new_name and new_name != selected and new_name not in chat_names:
            st.session_state['chats'][new_name] = st.session_state['chats'].pop(selected)
            st.session_state['current_chat'] = new_name
            st.rerun()
    else:
        st.session_state['current_chat'] = None
    if st.button("+ New Chat"):
        st.session_state['show_new_chat_input'] = True
    if st.session_state.get('show_new_chat_input', False):
        chat_title = st.text_input("Enter chat name:", key='new_chat_name')
        if st.button("Create Chat") and chat_title and chat_title not in chat_names:
            st.session_state['chats'][chat_title] = []
            st.session_state['current_chat'] = chat_title
            st.session_state['show_new_chat_input'] = False
            st.rerun()
        if st.button("Cancel"):
            st.session_state['show_new_chat_input'] = False
    if st.session_state['current_chat']:
        if st.button("🗑️ Delete Chat"):
            del st.session_state['chats'][st.session_state['current_chat']]
            st.session_state['current_chat'] = chat_names[0] if chat_names else None
            st.rerun()

# Use current chat's messages
if st.session_state['current_chat']:
    messages = st.session_state['chats'][st.session_state['current_chat']]
else:
    messages = []

# Display chat history for current chat (at the top)
render_chat_history(messages)

# Chat input at the bottom with only attachment icon for image upload
st.markdown("<div style='height: 30vh'></div>", unsafe_allow_html=True)

# Helper to clear input
if 'msg_input' not in st.session_state:
    st.session_state['msg_input'] = ""
if 'img_input' not in st.session_state:
    st.session_state['img_input'] = None

def send_and_clear():
    user_input = st.session_state['msg_input']
    uploaded_file = st.session_state['img_input']
    content = []
    if user_input:
        content.append({"type": "text", "text": user_input})
    if uploaded_file:
        image_bytes = uploaded_file.read()
        image_base64 = encode_image_to_base64(image_bytes)
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}})
        st.session_state['img_input'] = None
    if content:
        messages.append({"role": "user", "content": content})
        try:
            reply = send_message(messages, deployment_name)
            messages.append({"role": "assistant", "content": [{"type": "text", "text": reply}]})
        except Exception as e:
            st.error(f"Error: {e}")
    st.session_state['chats'][st.session_state['current_chat']] = messages
    st.session_state['last_sent'] = user_input
    st.session_state['msg_input'] = ""
    st.rerun()

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([10,1,1])
    with col1:
        st.text_input("Message", key='msg_input', placeholder="Type your message and press Enter...", label_visibility="collapsed")
    with col2:
        st.file_uploader("Attach image", type=["png", "jpg", "jpeg", "gif", "webp"], key='img_input', label_visibility="collapsed")
    with col3:
        st.form_submit_button("Send", on_click=send_and_clear, use_container_width=True)
