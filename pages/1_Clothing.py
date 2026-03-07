import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Clothing", layout="wide")

st.divider()
# -----------------------------
# Two-column header section
# -----------------------------
col1, col2 = st.columns([1, 1.2])  # adjust ratios if needed

with col1:
    st.title("Clothing Printing")
    st.write("Custom printed clothing, workwear, and uniforms.")

    st.subheader("Our Clothing Services")
    st.write("""
    - T-shirts, Hoodies, and Jackets  
    - Workwear and Uniforms  
    - Custom Prints & Branding  
    """)   
with col2:
    st.image("assets/clothing/clothing_hero.jpg", width=400)
    
st.divider() # horizontal divider 

#------
# Image Grid Section 
#------

st.subheader("Recent Clothing Prints")

image_folder = "assets/clothing" # adjust to your folder 

images = [
    os.path.join(image_folder, img)
    for img in os.listdir(image_folder)
    if img.lower().endswith((".png", ".jpg", ".jpeg"))
]

target_size = (225, 225) # uniform width & height - streamlit doesnt do heights 

cols = st.columns(4)

for i, img_path in enumerate(images):
    img = Image.open(img_path).resize(target_size)
    with cols[i % 4]:
        st.image(img)

st.divider()
st.page_link("pages/9_T-shirt_Mockup.py", label="Use Our Image Upload Generator", icon="➡️") # small link 

#if st.button("Image Upload Generator"):
#    st.switch_page("pages/9_T-shirt_Mockup.py") # button style link

