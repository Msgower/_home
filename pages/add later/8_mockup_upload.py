import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import io

def warp_overlay(base, overlay, dst_points, opacity=1.0):
    """
    Warp a PNG overlay (vinyl artwork) onto a base image using 4 clicked points.
    
    Parameters:
    - base      : RGB image (numpy array)
    - overlay   : RGBA image (numpy array)
    - dst_points: list of 4 points [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
                  in order: top-left, top-right, bottom-right, bottom-left
    - opacity   : float (0.1 - 1.0), scales transparency of the overlay
    """
    h, w = overlay.shape[:2]

    # Source points from artwork corners
    src = np.array([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]
    ], dtype=np.float32)

    # Destination points (clicked on base image)
    dst = np.array(dst_points, dtype=np.float32)

    # Compute perspective transform
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(overlay, M, (base.shape[1], base.shape[0]))

    # Alpha blending with slider opacity
    alpha = (warped[:, :, 3] / 255.0) * opacity

    result = base.copy()

    for c in range(3):  # RGB channels
        result[:, :, c] = alpha * warped[:, :, c] + (1 - alpha) * result[:, :, c]

    return result.astype(np.uint8)


def draw_corners_on_image(image, corners):
    """Draw corner markers on image"""
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    
    corner_labels = ["1: TL", "2: TR", "3: BR", "4: BL"]
    colors = ["red", "blue", "green", "orange"]
    
    for i, (x, y) in enumerate(corners):
        # Draw circle
        radius = 10
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                     fill=colors[i], outline="white", width=2)
        
        # Draw label
        draw.text((x+15, y-15), corner_labels[i], fill=colors[i], 
                 stroke_width=2, stroke_fill="white")
    
    # Draw lines between corners
    if len(corners) > 1:
        for i in range(len(corners)):
            next_i = (i + 1) % len(corners)
            draw.line([corners[i], corners[next_i]], fill="yellow", width=2)
    
    return img_copy


st.set_page_config(page_title="Perspective Overlay Tool", layout="wide")

st.title("📐 Perspective Overlay Tool")
st.markdown("Click 4 corners on the base image to define the perspective area.")

# Initialize session state
if 'corners' not in st.session_state:
    st.session_state.corners = []
if 'result_img' not in st.session_state:
    st.session_state.result_img = None
if 'base_img' not in st.session_state:
    st.session_state.base_img = None
if 'overlay_img' not in st.session_state:
    st.session_state.overlay_img = None

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    opacity = st.slider("Overlay Opacity", 0.1, 1.0, 1.0, 0.05)
    
    if st.button("🔄 Reset All"):
        st.session_state.corners = []
        st.session_state.result_img = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.markdown("""
    1. Upload your **base image** (mockup)
    2. **Click 4 corners** in order:
       - 🔴 Top-Left
       - 🔵 Top-Right
       - 🟢 Bottom-Right
       - 🟠 Bottom-Left
    3. Upload your **overlay image** (artwork)
    4. Click **Apply Overlay**
    5. Download the result
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Current Corners")
    if len(st.session_state.corners) == 0:
        st.info("No corners selected yet")
    else:
        for i, (x, y) in enumerate(st.session_state.corners):
            labels = ["🔴 Top-Left", "🔵 Top-Right", "🟢 Bottom-Right", "🟠 Bottom-Left"]
            st.text(f"{labels[i]}: ({x}, {y})")
    
    if len(st.session_state.corners) > 0:
        if st.button("↩️ Undo Last Corner"):
            st.session_state.corners.pop()
            st.rerun()

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("1️⃣ Base Image - Click 4 Corners")
    base_file = st.file_uploader("Upload base image", type=['png', 'jpg', 'jpeg'], key="base")
    
    if base_file:
        if st.session_state.base_img is None or base_file.name != getattr(st.session_state, 'last_base_name', ''):
            st.session_state.base_img = Image.open(base_file).convert("RGB")
            st.session_state.last_base_name = base_file.name
            st.session_state.corners = []  # Reset corners when new image uploaded
        
        # Show image with corners
        display_img = st.session_state.base_img
        if st.session_state.corners:
            display_img = draw_corners_on_image(st.session_state.base_img, st.session_state.corners)
        
        # Use streamlit-image-coordinates for clicking
        try:
            from streamlit_image_coordinates import streamlit_image_coordinates
            
            coords = streamlit_image_coordinates(
                display_img,
                key="image_coords"
            )
            
            if coords and len(st.session_state.corners) < 4:
                x, y = coords["x"], coords["y"]
                st.session_state.corners.append([x, y])
                st.rerun()
                
        except ImportError:
            st.error("⚠️ Please install: `pip install streamlit-image-coordinates`")
            st.image(display_img, use_container_width=True)
        
        width, height = st.session_state.base_img.size
        st.caption(f"📏 Image size: {width} x {height} pixels")
        st.caption(f"🎯 Corners selected: {len(st.session_state.corners)}/4")

with col2:
    st.subheader("2️⃣ Overlay Image")
    overlay_file = st.file_uploader("Upload overlay image (PNG recommended)", type=['png', 'jpg', 'jpeg'], key="overlay")
    
    if overlay_file:
        if st.session_state.overlay_img is None or overlay_file.name != getattr(st.session_state, 'last_overlay_name', ''):
            overlay_pil = Image.open(overlay_file)
            if overlay_pil.mode != 'RGBA':
                overlay_pil = overlay_pil.convert('RGBA')
            st.session_state.overlay_img = overlay_pil
            st.session_state.last_overlay_name = overlay_file.name
        
        st.image(st.session_state.overlay_img, caption="Overlay Image", use_container_width=True)

# Apply button
st.markdown("---")
if len(st.session_state.corners) == 4:
    if st.button("✨ Apply Overlay", type="primary", use_container_width=True):
        if st.session_state.base_img and st.session_state.overlay_img:
            # Convert images to numpy arrays
            base_np = np.array(st.session_state.base_img)
            overlay_np = np.array(st.session_state.overlay_img)
            
            # Apply perspective transform
            try:
                result_np = warp_overlay(base_np, overlay_np, st.session_state.corners, opacity)
                st.session_state.result_img = Image.fromarray(result_np)
                st.success("✅ Overlay applied successfully!")
            except Exception as e:
                st.error(f"❌ Error applying overlay: {str(e)}")
        else:
            st.warning("⚠️ Please upload both images first!")
else:
    st.info(f"ℹ️ Please select {4 - len(st.session_state.corners)} more corner(s) by clicking on the base image")

# Display result
if st.session_state.result_img:
    st.markdown("---")
    st.subheader("3️⃣ Result")
    st.image(st.session_state.result_img, caption="Final Result", use_container_width=True)
    
    # Download button
    buf = io.BytesIO()
    st.session_state.result_img.save(buf, format="PNG")
    st.download_button(
        label="⬇️ Download Result",
        data=buf.getvalue(),
        file_name="perspective_overlay_result.png",
        mime="image/png",
        use_container_width=True
    )