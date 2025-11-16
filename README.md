
# GPT Chatbot — Streamlit Demo

Lightweight Streamlit app that demonstrates a simple chat interface using the OpenAI Responses API. This project provides a minimal, local chat application with streaming responses and local chat persistence.

**Key ideas:** send user messages to an OpenAI model, stream the assistant response to the UI, and save chats locally in the `chats/` folder.

**Status:** Prototype / learning project

---

**Features**
- Simple chat UI built with `streamlit`.
- Streaming assistant responses for a responsive UX.
- Persist chats locally in `chats/` using pickled files.
- Store API key locally via the app Settings (saved to `settings/key`).
- Choose between supported models in the sidebar.

---

**Requirements**
- Python 3.8+ (recommended)
- See `requirements.txt` for Python packages used

---

**Install**
1. Create a virtual environment (optional but recommended):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```cmd
pip install -r requirements.txt
```

---

**Run (development)**
1. Start the Streamlit app:

```cmd
streamlit run main.py
```

2. Open the local URL shown by Streamlit in your browser.

---

**Configure the OpenAI API key**
- Open the app and go to the `Settings` tab in the sidebar.
- Paste your OpenAI API key in the provided input and click the confirmation; the key is saved locally using the app (`settings/key`).

---

**How it works (brief)**
- `main.py`: Streamlit app. Manages session state, chat display, streaming responses, and sidebar tabs for Chats and Settings.
- `utils_openai.py`: wraps the OpenAI call and returns streamed response chunks from `openai.responses.create(...)`.
- `utils_files.py`: utilities for converting chat names to filenames, saving/loading chats (pickle), listing chats, and saving/reading the API key in `settings/key`.

**Models available in the UI:** `gpt-5-nano-2025-08-07`, `gpt-4.1-nano-2025-04-14` (selectable in Settings).

---

**File structure (important files)**
- `main.py` — Streamlit application code (entrypoint).
- `utils_openai.py` — small wrapper for OpenAI Responses API calls.
- `utils_files.py` — chat and settings file helpers (uses `chats/` and `settings/`).
- `requirements.txt` — Python dependencies.
- `chats/` — saved chat pickles (automatically created).
- `settings/key` — saved API key (binary pickle format, created by the app).

---
