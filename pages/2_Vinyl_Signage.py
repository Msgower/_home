import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Vinyl & Signage", layout="wide")

# -----------------------------
# Two-column header section
# -----------------------------
col1, col2 = st.columns([1, 1.2])  # adjust ratios if needed

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
    
st.divider() # horizontal divider 

#------
# Image Layout Section 
#------

st.subheader("Recent Vinyl Signage")

# Load images

image_folder = "assets/signs"
images = [
    os.path.join(image_folder, img)
    for img in os.listdir(image_folder)
    if img.lower().endswith((".png", ".jpg", ".jpeg"))
]

# Sort or maually assign if needed

tall_image = images[0] # Book shop sign (tall)
grid_images = images[1:4] # next 4 images for 2x2 grid

# Main layout: talll image left, 2x2 grid right

left, right = st.columns([1, 2])

# Tall image on the left
left, right = st.columns([1, 2])

# Left: tall image
with left:
    st.image(Image.open(tall_image), width=287)

# Right: 2×2 grid with button in bottom-right
with right:
    row1 = st.columns(2)
    row2 = st.columns(2)

    # First row
    with row1[0]:
        st.image(Image.open(grid_images[0]), width=300)
    with row1[1]:
        st.image(Image.open(grid_images[1]), width=300)

    # Second row
    with row2[0]:
        st.image(Image.open(grid_images[2]), width=300)

    # Bottom-right: blank space + button
    with row2[1]:
        st.write("")      # spacer
        st.write("")      # spacer
        st.write("")      # spacer
        
        #st.page_link("pages/gallery.py", label="View Full Gallery", icon="🖼️")
        
        if st.button("View Our Gallery"):
            st.switch_page("pages/gallery.py") # button style link

