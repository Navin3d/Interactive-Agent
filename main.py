import streamlit as st

from agent import ask_llm

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
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Assistant placeholder
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # Stream from agent
        for chunk in ask_llm(prompt):
            full_response += chunk
            response_placeholder.write(full_response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})
