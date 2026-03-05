import streamlit as st
import os

st.set_page_config(layout="wide")




# Title
st.markdown("""
<h1 style="font-size: 52px; margin-bottom: 10px; font-weight: 700; text-align: center;">
Etchellent Designs
</h1>
""", unsafe_allow_html=True)

# Tagline
st.markdown("""
<p style="font-size: 22px; color: #555; margin-top: 0px; text-align: center;">
Signs • Clothing • Wraps • Design • Digital Tools
</p>
""", unsafe_allow_html=True)

# Description
st.markdown("""
<p style="font-size: 18px; color: #666; max-width: 600px; margin: 20px auto 30px auto; text-align: center;">
Professional signage, clothing printing and design services.
</p>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# 3) FOUR-BUTTON NAVIGATION ROW
# -------------------------------
nav = st.columns(4)

with nav[0]:
    if st.button("Clothing"):
        st.switch_page("pages/1_Clothing.py")

with nav[1]:
    if st.button("Signage"):
        st.switch_page("pages/2_Vinyl_Signage.py")

with nav[2]:
    if st.button("Gallery"):
        st.switch_page("pages/Gallery.py")

with nav[3]:
    if st.button("Mockup"):
        st.switch_page("pages/9_T-shirt_Mockup.py")