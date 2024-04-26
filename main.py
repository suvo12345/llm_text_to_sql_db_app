import streamlit as st
from langchain_helper import get_few_shot_db_chain

### Git check

st.title("AtliQ T Shirts: Database Q&A 👕")

question = st.text_input("Question: ")

if question:
    # pass
    chain = get_few_shot_db_chain()
    response = chain.run(question)

    st.header("Answer: ")
    st.write(response)

