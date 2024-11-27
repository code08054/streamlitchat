import streamlit as st
from openai import OpenAI

st.title("Dibyendu's HR Connect")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key="")

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a Mock HR Interviewer. You are based in India and planning to interview college pass out. You need to generate HR questions and validate user's answers. Always ask one question at a time. Always ask one question at a time and if answer is correct ask the next question in the same response. If user starts different discussion, bring them back to HR interview discussion."}]
    st.session_state.messages.append({"role": "assistant", "content": "Hello, welcome to DibsWOrld, How are you today?"})

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if(message["role"] !="system"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
