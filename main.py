import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
# Now we can instantiate our model object and generate chat completions:
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)



output_parser = StrOutputParser()

# Initialize Streamlit app
st.title("Chat with Llama3.2 (via Ollama)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input box
if prompt := st.chat_input("Say something..."):
# if prompt := st.text_input("Say something..."):
    # Show user message
    with st.chat_message("user"):
         st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Format full conversation into prompt
    chat_history = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages if m["role"] == "user"])

    # Create prompt template
    template = ChatPromptTemplate.from_template(
        "You are a helpful assistant.\n\nUser said: {question}"
    )

    chain = template | llm | output_parser

    # Generate response
    response = chain.invoke({"question": prompt})

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
