import streamlit as st
from PIL import Image
import io

st.set_page_config(layout="wide", page_title="Clothing Mockup Tool")
st.title("👕 Clothing Mockup Generator")

# -------------------------
# Load base shirt templates
# -------------------------
SHIRTS = {
    "White T-Shirt": "assets/images/tshirt_blank.png",
    # "Black T-Shirt": "assets/shirts/black.png",
    # "Hoodie": "assets/shirts/hoodie.png"
}

# -------------------------
# Caching functions
# -------------------------
@st.cache_data
def load_base_image(path, width=800):
    """Load and resize base shirt template for preview"""
    img = Image.open(path).convert("RGBA")
    img.thumbnail((width, width), Image.LANCZOS)
    return img

@st.cache_data
def process_overlay(overlay_file, max_width, max_height, opacity):
    """Load overlay, resize, and apply opacity"""
    overlay = Image.open(overlay_file).convert("RGBA")
    overlay.thumbnail((max_width, max_height), Image.LANCZOS)
    
    # Apply opacity
    alpha = overlay.split()[3].point(lambda p: int(p * opacity))
    overlay.putalpha(alpha)
    
    return overlay

# -------------------------
# Layout columns
# -------------------------
col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("⚙️ Controls")
    shirt_choice = st.selectbox("Select Garment", list(SHIRTS.keys()))
    placement = st.selectbox("Select Placement", ["Front", "Back", "Left Chest"])
    st.markdown(
        "ℹ️ Front and Back placements use the same print area size.\n"
        "Back mockup image is not included yet."
    )
    opacity = st.slider("Opacity", 0.1, 1.0, 1.0, 0.05)
    overlay_file = st.file_uploader("Upload artwork (PNG recommended)", type=["png", "jpg", "jpeg"])

# -------------------------
# Load base shirt for preview
# -------------------------
preview_width = 800
base_img = load_base_image(SHIRTS[shirt_choice], width=preview_width)
bx, by = base_img.size
result = base_img.copy()

# -------------------------
# Process overlay if uploaded
# -------------------------
if overlay_file:
    # Determine max overlay size based on placement
    placement_ratio = 0.25 if placement in ["Front", "Back"] else 0.10
    max_width, max_height = int(bx * placement_ratio), int(by * placement_ratio)
    
    overlay = process_overlay(overlay_file, max_width, max_height, opacity)
    
    # Position offsets (adjust to fit your template)
    front_back_offset = (0, -100)  # x, y for front/back
    left_chest_offset = (100, -150)  # x, y for left chest

    if placement in ["Front", "Back"]:
        pos = (bx // 2 - overlay.width // 2 + front_back_offset[0],
               by // 2 - overlay.height // 2 + front_back_offset[1])
    elif placement == "Left Chest":
        pos = (bx // 2 - overlay.width // 2 + left_chest_offset[0],
               by // 2 - overlay.height // 2 + left_chest_offset[1])
    
    result.paste(overlay, pos, overlay)

# -------------------------
# Display preview and download
# -------------------------
with col1:
    st.subheader("Preview")
    st.image(result, use_container_width=True)

    # Save full resolution for download
    full_res_base = Image.open(SHIRTS[shirt_choice]).convert("RGBA")
    full_result = full_res_base.copy()
    
    if overlay_file:
        # Use full res overlay
        full_ow, full_oh = overlay.size
        full_overlay = Image.open(overlay_file).convert("RGBA")
        # Scale overlay to same ratio as preview
        scale_x = full_res_base.width / bx
        scale_y = full_res_base.height / by
        full_overlay = full_overlay.resize(
            (int(full_ow * scale_x), int(full_oh * scale_y)), Image.LANCZOS
        )
        # Apply full opacity
        alpha = full_overlay.split()[3].point(lambda p: int(p * opacity))
        full_overlay.putalpha(alpha)
        # Position full res overlay
        if placement in ["Front", "Back"]:
            pos_full = (int(pos[0] * scale_x), int(pos[1] * scale_y))
        else:
            pos_full = (int(pos[0] * scale_x), int(pos[1] * scale_y))
        full_result.paste(full_overlay, pos_full, full_overlay)

    buf = io.BytesIO()
    full_result.save(buf, format="PNG")
    st.download_button(
        "⬇️ Download Mockup",
        buf.getvalue(),
        "shirt_mockup.png",
        "image/png",
        use_container_width=True
    )