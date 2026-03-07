import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

st.set_page_config(layout="wide")
st.title("Vinyl Catalogue")

# ---- Helper Function: Convert PIL image to base64 for HTML display ----
def img_to_bytes(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# ---- Load images from a folder ----
def load_images(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(folder_path, filename)
            images.append((filename, Image.open(img_path)))
    return images

# ---- Crop images to remove top/right logos ----
def crop_extra(img, top_percent=0.09, bottom_percent=0.04, left_percent=0.06, right_percent=0.09):
    width, height = img.size
    left = int(width * left_percent)
    top = int(height * top_percent)
    right = int(width * (1 - right_percent))
    bottom = int(height * (1 - bottom_percent))
    return img.crop((left, top, right, bottom))

# ---- Paths to image folders ----
wood_folder = r"assets\images\vinyl_wrap_images\wood"
stone_folder = r"assets\images\vinyl_wrap_images\stone"

# ---- Load and crop images ----
wood_images = [(name, crop_extra(img)) for name, img in load_images(wood_folder)]
stone_images = [(name, crop_extra(img)) for name, img in load_images(stone_folder)]

# ---- Display Wood & Stone Effects ----
st.header("Wood & Stone Effects")
for i in range(max(len(wood_images), len(stone_images))):
    col1, col2 = st.columns(2)

    # Wood column
    with col1:
        if i < len(wood_images):
            name, img = wood_images[i]
            st.subheader(name.replace(".jpg","").replace(".png","").title())
            st.markdown(
                f'<div style="text-align:center;"><img src="data:image/png;base64,{img_to_bytes(img)}" style="max-width:90%; height:auto;"></div>',
                unsafe_allow_html=True
            )

    # Stone column
    with col2:
        if i < len(stone_images):
            name, img = stone_images[i]
            st.subheader(name.replace(".jpg","").replace(".png","").title())
            st.markdown(
                f'<div style="text-align:center;"><img src="data:image/png;base64,{img_to_bytes(img)}" style="max-width:90%; height:auto;"></div>',
                unsafe_allow_html=True
            )

# ---- Colour Swatches ----
st.header("Colour Finishes")

# Gloss colours
gloss_colours = {
    "Gloss Red": "#FF0000",
    "Gloss Blue": "#007BFF",
    "Gloss Green": "#28A745",
    "Gloss Yellow": "#FFD700",
    "Gloss Grey": "#A9A9A9",
    "Gloss Black": "#000000",
    "Gloss White": "#FFFFFF"
}

# Matte colours
matte_colours = {
    "Matte Red": "#FF0000",
    "Matte Blue": "#007BFF",
    "Matte Green": "#28A745",
    "Matte Yellow": "#FFD700",
    "Matte Grey": "#A9A9A9",
    "Matte Black": "#000000",
    "Matte White": "#FFFFFF"
}

# ---- Display Gloss Swatches ----
st.subheader("Gloss Finishes")
cols = st.columns(len(gloss_colours))
for i, (name, hex_color) in enumerate(gloss_colours.items()):
    border_style = "1px solid #ccc" if hex_color.upper() == "#FFFFFF" else "none"
    with cols[i]:
        st.markdown(
            f'<div style="width:80px;height:80px;background:{hex_color};border-radius:15px;'
            f'border:{border_style};box-shadow: inset 0 0 20px rgba(255,255,255,0.3);position:relative;">'
            f'<div style="position:absolute;top:3px;right:3px;font-size:10px;color:white;">👆</div></div>',
            unsafe_allow_html=True
        )
        st.caption(name)

# ---- Display Matte Swatches ----
st.subheader("Matte Finishes")
cols = st.columns(len(matte_colours))
for i, (name, hex_color) in enumerate(matte_colours.items()):
    border_style = "1px solid #ccc" if hex_color.upper() == "#FFFFFF" else "none"
    with cols[i]:
        st.markdown(
            f'<div style="width:80px;height:80px;background:{hex_color};border-radius:15px;'
            f'border:{border_style};"></div>',
            unsafe_allow_html=True
        )
        st.caption(name)

# ---- Note about more colours ----
st.markdown(
    '<p style="text-align:center; font-size:14px; color:gray;">More colours are available upon request.</p>',
    unsafe_allow_html=True
)
