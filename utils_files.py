import re
from pathlib import Path
import pickle
from unidecode import unidecode

CHAT_FOLDER = Path(__file__).parent / 'chats'
CHAT_FOLDER.mkdir(exist_ok=True)

SETTINGS_FOLDER = Path(__file__).parent / 'settings'
SETTINGS_FOLDER.mkdir(exist_ok=True)

CACHE_FILE_NAMES = {}

#  CHAT SAVE/LOAD ========================

def convert_to_file_name(chat_name):
    file_name = unidecode(chat_name)
    file_name = re.sub(r'\W+', '', file_name).lower()
    return file_name

def convert_to_chat_name(file_name):
    if not file_name in CACHE_FILE_NAMES:
        chat_name = chat_messages_from_file_name(file_name, key='chat_name')
        CACHE_FILE_NAMES[file_name] = chat_name
    return CACHE_FILE_NAMES[file_name]

def get_chat_name(messages):
    for message in messages:
        if message['role'] == 'user':
            return message['content'][:30]

def save_messages(messages):
    if len(messages) == 0:
        return False
    chat_name = get_chat_name(messages)
    file_name = convert_to_file_name(chat_name)
    save_file = {'chat_name': chat_name,
                 'file_name': file_name,
                 'messages': messages}
    with open(CHAT_FOLDER / file_name, 'wb') as f:
        pickle.dump(save_file, f)

def load_chat(messages, key='messages'):
    if len(messages) == 0:
        return []
    chat_name = get_chat_name(messages)
    file_name = convert_to_file_name(chat_name)
    with open(CHAT_FOLDER / file_name, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]

def chat_messages_from_file_name(file_name, key='messages'):
    with open(CHAT_FOLDER / file_name, 'rb') as f:
        mensagens = pickle.load(f)
    return mensagens[key]

def list_chats():
    chats = list(CHAT_FOLDER.glob('*'))
    chats = sorted(chats, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [c.stem for c in chats]

# APIKEY SAVE/LOAD ========================
def save_key(key):
    with open(SETTINGS_FOLDER / 'key', 'wb') as f:
        pickle.dump(key, f)

def read_key():
    if (SETTINGS_FOLDER / 'key').exists():
        with open(SETTINGS_FOLDER / 'key', 'rb') as f:
            return pickle.load(f)
    else:
        return ''