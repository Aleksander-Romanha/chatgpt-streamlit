import streamlit as st

from utils_openai import model_response
from utils_files import *

# INITIALIZATION ==================================================

def init():
    if not 'messages' in st.session_state:
        st.session_state['messages'] = []
    if not 'current_chat' in st.session_state:
        st.session_state['current_chat'] = ''
    if not 'model' in st.session_state:
        st.session_state['model'] = 'gpt-5-nano-2025-08-07'
    if not 'api_key' in st.session_state:
        st.session_state['api_key'] = read_key()

# TABS ==================================================

def tab_chats(tab):
    tab.button('➕ New Chat', on_click=select_chat, args=('', ), use_container_width=True)
    tab.markdown('')

    file_names = list_chats()
    for file_name in file_names:
        chat_name = convert_to_chat_name(file_name).capitalize()
        if len(chat_name) == 30:
            chat_name += '...'
        tab.button(chat_name, on_click=select_chat, args=(file_name, ), disabled=file_name==st.session_state['current_chat'], use_container_width=True)

def select_chat(file_name):
    if file_name == '':
        st.session_state['messages'] = []
    else:
        messages = chat_messages_from_file_name(file_name)
        st.session_state['messages'] = messages
    st.session_state['current_chat'] = file_name

def tab_settings(tab):
    selected_model = tab.selectbox('Select Model', ['gpt-5-nano-2025-08-07', 'gpt-4.1-nano-2025-04-14'])
    st.session_state['model'] = selected_model

    key = tab.text_input('Add API key', value=st.session_state['api_key'])
    if key != st.session_state['api_key']:
        st.session_state['api_key'] = key
        save_key(key)
        tab.success('API key loaded!')

# MAIN PAGE ==================================================

def main_page():
    messages = load_chat(st.session_state['messages'])

    st.header('🤖 GPT Chatbot')

    for message in messages:
        chat = st.chat_message(message['role'])
        chat.markdown(message['content'])

    prompt = st.chat_input()
    if prompt:
        if st.session_state['api_key'] == '':
            st.error('Add an API key in the settings tab')
        else:
            new_message = {'role': 'user', 'content': prompt}
            chat = st.chat_message(new_message['role'])
            chat.markdown(new_message['content'])
            messages.append(new_message)

            chat = st.chat_message('assistant')

            # placeholder to overwrite the bot message chunks instead of doing newline prints
            placeholder = chat.empty()
            placeholder.markdown("▌")

            stream_response = model_response(messages=messages, openai_key=st.session_state['api_key'], model=st.session_state['model'], stream=True)
            full_response = ''
            for chunk in stream_response:
                if hasattr(chunk, "type") and "text.delta" in chunk.type:
                    full_response += chunk.delta
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            new_message = {'role': 'assistant', 'content': full_response}
            messages.append(new_message)

            st.session_state['messages'] = messages
            save_messages(messages)

# MAIN ==================================================

def main():
    init()
    main_page()
    tab1, tab2 = st.sidebar.tabs(['Chats', 'Settings'])
    tab_chats(tab1)
    tab_settings(tab2)

if __name__ == '__main__':
    main()