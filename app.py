import streamlit as st
import requests
import json
from datetime import datetime
import time

#Konfigurasi halaman
st.set_page_config(
    page_title="Obrolan With Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Mengambil API key dari secrets.toml
def get_api_key():
    try:
        # Coba beberapa format yang mungkin
        if 'openrouter' in st.secrets and 'api_key' in st.secrets.openrouter:
            return st.secrets.openrouter.api_key
        elif 'OPENROUTER_API_KEY' in st.secrets:
            return st.secrets['OPENROUTER_API_KEY']
        elif 'api_key' in st.secrets:
            return st.secrets.api_key
        else:
            return ""
    except Exception as e:
        st.error(f"Error accessing secrets: {e}")
        return ""

# Style CSS
def load_css():
    st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #0f1116;
        color: #e6e6e6;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #131721;
        padding: 2rem 1rem;
    }
    
    /* Header */
    .chat-header {
        background: linear-gradient(90deg, #1a5cff, #0d47a1);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 80%;
        margin: 0 auto 20px auto;
    }
    
    /* Main Chat Container */
    .main-chat-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 200px);
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
    
    /* Messages Container */
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 80%;
        margin: 0 auto;
    }
    
    /* Chat Containers */
    .chat-container {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 15px;
        display: flex;
        align-items: flex-start;
        width: 100%;
        max-width: 800px;
    }
    .user-container {
        justify-content: flex-end;
        margin-left: auto;
    }
    .bot-container {
        justify-content: flex-start;
        margin-right: auto;
    }
    
    /* Message Bubbles */
    .message-content {
        max-width: 100%;
        padding: 12px 16px;
        border-radius: 18px;
        position: relative;
        line-height: 1.5;
    }
    .user-message {
        background: linear-gradient(135deg, #1a5cff, #0d47a1);
        color: white;
        border-bottom-right-radius: 4px;
    }
    .bot-message {
        background-color: #2d3748;
        color: #e6e6e6;
        border-bottom-left-radius: 4px;
    }
    
    /* Timestamp */
    .message-timestamp {
        font-size: 0.7em;
        color: #9ca3af;
        text-align: right;
        margin-top: 5px;
    }
    
    /* Icons */
    .icon-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        flex-shrink: 0;
        margin: 0 10px;
    }
    .user-icon {
        background: linear-gradient(135deg, #1a5cff, #0d47a1);
        order: 2;
    }
    .bot-icon {
        background: linear-gradient(135deg, #4a5568, #2d3748);
        order: 0;
    }
    .icon {
        color: white;
        font-size: 18px;
    }
    
    /* History Section */
    .history-container {
        background-color: #1a202c;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        height: 400px;
        overflow-y: auto;
    }
    .history-title {
        font-weight: bold;
        border-bottom: 2px solid #1a5cff;
        padding-bottom: 8px;
        margin-bottom: 10px;
        color: #e6e6e6;
    }
    .history-item {
        padding: 10px;
        border-left: 3px solid #1a5cff;
        margin-bottom: 8px;
        background-color: #2d3748;
        border-radius: 0 5px 5px 0;
        cursor: pointer;
        transition: all 0.2s;
    }
    .history-item:hover {
        background-color: #4a5568;
        border-left: 3px solid #3b82f6;
    }
    .history-item.active {
        background-color: #2d3748;
        border-left: 3px solid #1a5cff;
    }
    .history-timestamp {
        font-size: 0.7em;
        color: #9ca3af;
    }
    .no-history {
        text-align: center;
        color: #9ca3af;
        font-style: italic;
        padding: 20px;
    }
    
    /* Input area */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        left: 70%;
        transform: translateX(-50%);
        width: 80%;
        max-width: 800px;
        background-color: #1a202c;
        border-radius: 10px;
        padding: 10px;
        z-index: 999;
        margin: 0 auto;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #1a5cff, #0d47a1);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #0d47a1, #1a5cff);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    /* Text inputs */
    .stTextInput input {
        background-color: #2d3748;
        color: #e6e6e6;
        border: 1px solid #4a5568;
    }
    
    /* Select boxes */
    .stSelectbox select {
        background-color: #2d3748;
        color: #e6e6e6;
        border: 1px solid #4a5568;
    }
    
    /* Code blocks */
    .code-block {
        background-color: #2d3748;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        overflow-x: auto;
    }
    
    /* Center align content */
    .centered {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 100%;
    }
    
    /* Welcome message - HIDDEN */
    .welcome-message {
        display: none;
    }
    
    /* Model selection in sidebar */
    .model-selector {
        margin-bottom: 20px;
        background-color: #1a202c;
        padding: 15px;
        border-radius: 10px;
    }
    .model-selector label {
        font-weight: bold;
        margin-bottom: 8px;
        display: block;
        color: #e6e6e6;
    }
    
    /* Main content area */
    .main-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    
    /* Chat input wrapper */
    .chat-input-wrapper {
        width: 80%;
        max-width: 800px;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }
    
    /* Custom container for chat input alignment */
    .chat-input-container {
        position: fixed;
        bottom: 20px;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        z-index: 999;
    }
    
    /* Adjust the main column to account for fixed input */
    .main-column {
        padding-bottom: 100px;
    }
    
    /* Alignment for header, messages and input */
    .centered-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key" not in st.session_state:
        st.session_state.api_key = get_api_key()
    if "model" not in st.session_state:
        st.session_state.model = "openai/gpt-3.5-turbo"
    if "history" not in st.session_state:
        st.session_state.history = []
    if "selected_history" not in st.session_state:
        st.session_state.selected_history = None

def send_to_openrouter(message, api_key, model, history):
    url = "https://openrouter.ai/api/v1/chat/completions"
    messages = history + [{"role": "user", "content": message}]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    except (KeyError, IndexError) as e:
        return "Error: Invalid response format from API"

def display_message(role, content, timestamp):
    if role == "user":
        st.markdown(f'''
        <div class="chat-container user-container">
            <div class="message-content user-message">
                {content}
                <div class="message-timestamp">{timestamp}</div>
            </div>
            <div class="icon-container user-icon">
                <span class="icon">👤</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        formatted_content = content
        if "```" in content:
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # This is a code block
                    parts[i] = f'<div class="code-block">{part}</div>'
            formatted_content = "".join(parts)
        st.markdown(f'''
        <div class="chat-container bot-container">
            <div class="icon-container bot-icon">
                <span class="icon">🤖</span>
            </div>
            <div class="message-content bot-message">
                {formatted_content}
                <div class="message-timestamp">{timestamp}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def display_history():
    st.sidebar.markdown("### 📜 History Pertanyaan")
    
    if not st.session_state.history:
        st.sidebar.markdown('<div class="no-history">Belum ada history percakapan</div>', unsafe_allow_html=True)
        return
    
    for i, history_item in enumerate(reversed(st.session_state.history)):
        preview_text = history_item['question']
        if len(preview_text) > 50:
            preview_text = preview_text[:47] + "..."
        
        active_class = "active" if st.session_state.selected_history == i else ""
        
        st.sidebar.markdown(f'''
        <div class="history-item {active_class}" onclick="selectHistory({i})">
            <div>{preview_text}</div>
            <div class="history-timestamp">{history_item['timestamp']}</div>
        </div>
        ''', unsafe_allow_html=True)

def main():
    load_css()
    init_session_state()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.sidebar.markdown("**🤖 Pilih Model**")
        models = [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4",
            "meta-llama/llama-3-70b-instruct",
            "google/gemini-pro",
            "anthropic/claude-2"
        ]
        selected_model = st.sidebar.selectbox(
            "Pilih model AI:",
            models,
            index=models.index(st.session_state.model) if st.session_state.model in models else 0,
            key="model_selector",
            label_visibility="collapsed"
        )
        
        if selected_model != st.session_state.model:
            st.session_state.model = selected_model
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
        display_history()
    
    with col2:
        st.markdown('<div class="chat-header"><h1>💬 Obrolan With Bot</h1></div>', unsafe_allow_html=True)
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="messages-container">', unsafe_allow_html=True)
            # Pesan selamat datang dihilangkan
            for message in st.session_state.messages:
                display_message(
                    message["role"], 
                    message["content"], 
                    message["timestamp"]
                )
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    user_input = st.chat_input("Ketik pesan Anda di sini...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if user_input and st.session_state.api_key:
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input, 
            "timestamp": timestamp
        })
        st.session_state.history.append({
            "question": user_input,
            "timestamp": timestamp
        })
        st.session_state.selected_history = None
        with col2:
            with st.container():
                st.markdown('<div class="messages-container">', unsafe_allow_html=True)
                display_message("user", user_input, timestamp)
                st.markdown('</div>', unsafe_allow_html=True)
        with st.spinner("Bot sedang mengetik..."):
            # Dapatkan respons dari OpenRouter
            bot_response = send_to_openrouter(
                user_input, 
                st.session_state.api_key, 
                st.session_state.model,
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            response_timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_response, 
                "timestamp": response_timestamp
            })
            with col2:
                with st.container():
                    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
                    display_message("assistant", bot_response, response_timestamp)
                    st.markdown('</div>', unsafe_allow_html=True)
    
    elif user_input and not st.session_state.api_key:
        st.error("API Key tidak ditemukan. Pastikan Anda telah mengonfigurasi secrets.toml dengan benar.")

if __name__ == "__main__":
    main()