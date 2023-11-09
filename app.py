"""
FILE is for UI
"""
from genta import GentaAPI
import streamlit as st
from PIL import Image

logo = Image.open("assets\genta_logo.png")

with st.sidebar:
    # Genta Logo in sidebar
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image(logo, use_column_width="always")

    # Ask user to input their API Token
    genta_api_key = st.text_input(
        "Genta API key", key="chatbot_api_key", type="password"
    )

    # Ask user to select their model of choice
    model_selected = st.selectbox(
        "Choose your LLM you would like to try:", ("Merak", "Starstreak", "DukunLM")
    )

    # Add Clear Chat button
    if st.button("Clear chat"):
        st.session_state.messages = st.session_state.messages[0:1]

    # Add advanced option
    advanced = st.toggle("Advanced mode")
    if advanced:
        # Set the model temperature
        temperature = st.slider(":blue[Temperature]", 0.0, 2.0, 1.0)

        # Set the model max token to be generated
        max_length = st.slider(":blue[Maximum lenght]", 0, 4096, 2048)

        # Set the model top P value
        top_p = st.slider(":blue[Top P]", 0.0, 0.1, 0.95)

        # Set the model repetition penalty
        rep_penalty = st.slider(":blue[Repetition penalty]", 0.0, 2.0, 1.03)

# App title and caption
st.title("GentaChat")
st.caption("A simple demonstration of GentaAPI for chat purposes")

# Initialize a new message if there isnt a message in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": "Halo, saya adalah asisten anda, ada yang bisa saya bantu?",
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# If user inputted something in the chat input, call the API for the response
if prompt := st.chat_input():
    if not genta_api_key:
        st.info("Please add your GentaAPI key to continue")
        st.stop()

    API = GentaAPI(genta_api_key)

    # Chat dictionary format
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Call the API for response
    # If the user use advanced feature
    if advanced:
        response = API.ChatCompletion(
            chat_history=st.session_state.messages[1:],
            model_name=model_selected,
            max_new_tokens=max_length,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=rep_penalty,
        )
    else:
        response = API.ChatCompletion(
            chat_history=st.session_state.messages[1:],
            model_name=model_selected,
            max_new_tokens=1024,
        )
    response = response[0][0]["generated_text"]

    # Display the response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
