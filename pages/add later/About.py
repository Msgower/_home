import streamlit as st

st.set_page_config(page_title="About", layout="wide")

st.title("About Shane & Etchellent Designs")

st.write("""
Hi, I'm Shane. I run a vinyl signage and printing business,
creating graphics and tools to help business grow.
""")

st.divider()

st.subheader("Our Experience")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Years Experience", "5+")
with col2:
    st.metric("Happy Clients", "100+")
with col3:
    st.metric("Projects completed", "250+")
    