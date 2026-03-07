import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from utils import warp_overlay

st.title("📐 Vinyl Mockup Generator")

st.info("Upload a photo → click 4 corners of the surface → preview your signage instantly")

# -------------------------
# Uploads
# -------------------------

col1, col2 = st.columns(2)

with col1:
    base_file = st.file_uploader("Base photo", type=["jpg", "jpeg", "png"])

with col2:
    overlay_file = st.file_uploader("Artwork (PNG with transparency)", type=["png"])


# -------------------------
# Main Tool
# -------------------------

if base_file and overlay_file:

    base_img = Image.open(base_file).convert("RGB")
    overlay_img = Image.open(overlay_file).convert("RGBA")

    base_np = np.array(base_img)
    overlay_np = np.array(overlay_img)

    # -------------------------
    # Opacity slider (NEW)
    # -------------------------

    opacity = st.slider(
        "Vinyl / Film opacity",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.05
    )

    st.subheader("Click 4 points in this order:")
    st.write("Top-Left → Top-Right → Bottom-Right → Bottom-Left")

    # -------------------------
    # Click canvas (replaces X/Y inputs)
    # -------------------------

    canvas_result = st_canvas(
        background_image=base_img,
        drawing_mode="point",
        stroke_width=6,
        stroke_color="red",
        height=base_img.height,
        width=base_img.width,
        key="canvas",
    )

    points = []

    if canvas_result.json_data is not None:
        for obj in canvas_result.json_data["objects"]:
            x = int(obj["left"])
            y = int(obj["top"])
            points.append((x, y))

    st.write(f"Points selected: {len(points)}/4")

    # -------------------------
    # Generate mockup
    # -------------------------

    if len(points) == 4:

        result = warp_overlay(base_np, overlay_np, points, opacity)

        st.subheader("Preview")
        st.image(result, use_container_width=True)

        result_img = Image.fromarray(result)

        st.download_button(
            "Download Mockup",
            result_img.tobytes(),
            file_name="mockup.png",
            mime="image/png"
        )

    # -------------------------
    # Reset
    # -------------------------

    if st.button("Clear points"):
        st.session_state["canvas"] = None
