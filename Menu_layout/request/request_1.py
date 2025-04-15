import streamlit as st

st.header("Request1")
st.write(f"Você está logado em {st.session_state.role}.")