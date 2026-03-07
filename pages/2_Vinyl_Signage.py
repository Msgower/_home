import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Vinyl & Signage", layout="wide")

# -----------------------------
# Two-column header section
# -----------------------------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.image("assets/images/sign_hero.jpg", width=400)

with col2:
    st.title("Vinyl & Signage")
    st.write("High-quality vinyl signs, decals and window films")

    st.subheader("Our Services")
    st.write("""
    - Vinyl Signs & Decals
    - Window Films & Privacy Films
    - Shopfront & Office Signage
    """)

st.divider()

# -----------------------------
# Image Layout Section
# -----------------------------
st.subheader("Recent Vinyl Signage")

# Load images
image_folder = "assets/signs"
images = [
    os.path.join(image_folder, img)
    for img in os.listdir(image_folder)
    if img.lower().endswith((".png", ".jpg", ".jpeg"))
]

# Sort or manually assign if needed
tall_image = images[0]          # left tall image
top_right_1 = images[1]         # top-right image 1
top_right_2 = images[2]         # top-right image 2
bottom_right = images[3]        # bottom-left image

# -----------------------------
# Main layout: tall left + 3 images + button
# -----------------------------
left, right = st.columns([1, 2])

# LEFT: Tall image
with left:
    st.image(Image.open(tall_image), use_column_width=True)

# RIGHT: 2×2 grid (3 images + button)
with right:
    row1 = st.columns(2)
    row2 = st.columns(2)

    # Top row
    with row1[0]:
        st.image(Image.open(top_right_1), use_column_width=True)

    with row1[1]:
        st.image(Image.open(top_right_2), use_column_width=True)

    # Bottom-left image
    with row2[0]:
        st.image(Image.open(bottom_right), use_column_width=True)

    # Bottom-right button
    with row2[1]:
        st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
        if st.button("View Our Gallery"):
            st.switch_page("pages/gallery.py")
