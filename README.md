# Streaming Deep Agent Chat with Streamlit

This project provides a minimal chat UI (Streamlit) that talks to a LangChain Deep Agent and streams the response live (token-by-token), instead of waiting until the agent finishes computing.

---

## Features

- Interactive chat interface using Streamlit  
- Real-time streaming from a Deep Agent (`stream_mode="messages"`)  
- Support for subagents (`subgraphs=True`)  
- Simple `ask_llm` generator you can reuse in other UIs or APIs  

---

## Requirements

- Python 3.11+  
- `deepagents` (LangChain Deep Agents)  
- `streamlit`  
- An LLM provider configured (e.g., OpenAI, Anthropic, etc.)

---

## Installation

```bash
uv sync
```

Make sure your LLM provider is configured (e.g., `OPENAI_API_KEY` in environment).

---

## Project Structure

Example minimal structure:

```text
.
├── app.py           # Streamlit app
└── agent.py         # Deep Agent definition (optional, can be in app.py)
```

You can also keep everything in `app.py` if you prefer.

---

## Usage

### 1. Define your Deep Agent

Example `agent.py`:

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.5",  # or your provider:model
    # tools=[...], subagents=[...] as needed
)
```

Adjust `model`, `tools`, and `subagents` to your needs.

---

### 2. Streamlit app

Example `app.py`:

```python
import streamlit as st
from agent import agent  # or define agent directly here

# --- Create agent once (cached) ---
@st.cache_resource
def get_agent():
    return agent

agent = get_agent()


def ask_llm(question: str):
    """
    Stream tokens from a Deep Agent as they are generated.
    Yields strings (text chunks).
    """
    for namespace, data in agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="messages",
        subgraphs=True,
    ):
        token, metadata = data  # data is (token, metadata)

        content = token.content
        if not content:
            continue

        if isinstance(content, str):
            yield content
        elif isinstance(content, list):
            # Fallback if content is a list of blocks
            for block in content:
                if isinstance(block, dict) and "text" in block:
                    yield block["text"]


# --- Chat UI ---
st.title("Deep Agent Chat (Streaming)")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for chunk in ask_llm(prompt):
            full_response += chunk
            response_placeholder.write(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
```

---

### 3. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`) and start chatting.

---

## How it works

- `agent.stream(...)` is used instead of `agent.invoke(...)` to get a stream of events.  
- `stream_mode="messages"` streams LLM tokens as they are generated.  
- `subgraphs=True` enables streaming from subagents (if you use them).  
- The `ask_llm` generator yields text chunks, which Streamlit appends to the response in real time.

---

## Customization Ideas

- Filter by `namespace` to show only main-agent output:

  ```python
  if namespace != ():
      continue
  ```

- Add `stream_mode=["messages", "updates"]` and handle tool-call events to show "thinking" or tool usage.  
- Use `get_stream_writer()` in tools to emit custom progress and stream with `stream_mode="custom"`.

---

## Notes

- Replace `"openai:gpt-5.5"` with your actual model string.  
- Ensure your environment has the necessary API keys (e.g., `OPENAI_API_KEY`).  
- This is a minimal example; you can extend it with authentication, logging, multi-user sessions, etc.
