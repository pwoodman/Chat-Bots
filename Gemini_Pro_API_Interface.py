import streamlit as st
import google.generativeai as genai
import pathlib
import yaml
from typing import List

def load_api_key_from_yaml(file_path: str) -> str:
  api_key = None
  key_file = pathlib.Path(file_path)
  if key_file.is_file():
      with open(key_file, "r") as f:
          keys = yaml.safe_load(f)
          api_key = keys.get("API_KEY")
  return api_key

def reset_conversation():
  st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]

if "messages" not in st.session_state.keys():
  st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]
if st.button("Reset Conversation"):
  reset_conversation()

st.title("Gemini Pro Chatbot - API Interface")
st.markdown('Version:0.1.4 by Patrick Woodman')

with st.expander("Requirements"):
    st.write(
        """
        - A valid API key is required to use this app, which can be obtained from https://makersuite.google.com/app/apikey .
        - The Gemini API Package must me installed using " pip install -q -U google-generativeai"
        """
    )


default_key = load_api_key_from_yaml("key.yaml")
with st.expander("API - Key"):
  keyz = st.text_input("API - Key", value=default_key)

st.markdown('---')

if keyz != default_key:
    default_key = keyz
    st.markdown('##')
if prompt := st.chat_input(key="user_input"):
  st.session_state.messages.append({"role": "user", "content": prompt})
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
      st.write(message["content"])
if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
      with st.spinner("Thinking..."):
          genai.configure(api_key=keyz)
          model = genai.GenerativeModel('gemini-pro')
          chat = model.start_chat()
          response = chat.send_message(prompt)
          st.write(response.text)

  message = {"role": "assistant", "content": response.text}
  st.session_state.messages.append(message)