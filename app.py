import streamlit as st

# Page Configuration
st.set_page_config(page_title="Projector 16:9 Keystone Calculator", layout="centered")

st.title("Projector 16:9 Keystone Calculator")
st.write("Preserve physical squareness while dialing in a perfect 16:9 aspect ratio.")

# Draw a visual "Screen" box container with corner inputs
st.markdown(
    """
    <style>
    .screen-box {
        border: 3px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        background-color: #1E1E1E;
        text-align: center;
        margin-bottom: 20px;
    }
    .screen-title {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
    <div class="screen-box">
        <span class="screen-title">=== VISUAL 16:9 SCREEN LAYOUT ===</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Inputs - Structured cleanly to avoid mobile grid shifting
st.markdown("### 1. Top Edge Coordinates")
tl_h = st.number_input("Top-Left Horizontal (TL H)", value=145, key="tl_h")
tl_v = st.number_input("Top-Left Vertical (TL V)", value=150, key="tl_v")

tr_h = st.number_input("Top-Right Horizontal (TR H)", value=148, key="tr_h")
tr_v = st.number_input("Top-Right Vertical (TR V)", value=162, key="tr_v")

st.markdown("---")

st.markdown("### 2. Bottom Edge Coordinates")
br_h = st.number_input("Bottom-Right Horizontal (BR H)", value=148, key="br_h")
br_v = st.number_input("Bottom-Right Vertical (BR V)", value=172, key="br_v")

bl_h = st.number_input("Bottom-Left Horizontal (BL H)", value=153, key="bl_h")
bl_v = st.number_input("Bottom-Left Vertical (BL V)", value=166, key="bl_v")

st.markdown("---")

# Settings and Action
compression_pref = st.selectbox(
    "Adjustment Target Edge",
    options=["Bottom Edge", "Top Edge"],
    index=0
)

if st.button("Calculate Perfect 16:9", type="primary"):
    # Target scale constants based on shared boundary maximums
    H_LIMIT_MAX = 505
    V_LIMIT_MAX = 501
    
    # Calculate current width spans remaining
    top_width_span = H_LIMIT_MAX - (tl_h + tr_h)
    bottom_width_span = H_LIMIT_MAX - (bl_h + br_h)
    avg_width = (top_width_span + bottom_width_span) / 2.0
    
    # Target 16:9 Height
    target_height = avg_width * (9.0 / 16.0)
    
    # Current height spans remaining
    left_height = V_LIMIT_MAX - (tl_v + bl_v)
    right_height = V_LIMIT_MAX - (tr_v + br_v)
    avg_current_height = (left_height + right_height) / 2.0
    
    # Calculate how much physical height we must remove to get down to target height
    # Larger V offset values compress the screen inward.
    height_difference = avg_current_height - target_height
    y_offset = round(height_difference / 2.0)
    
    if y_offset == 0:
        st.info("The image is already at a perfect 16:9 ratio!")
    else:
        # Apply the offset to squeeze height
        if compression_pref == "Bottom Edge":
            # Push bottom edge UP to compress (Add offset to V)
            new_br_v = br_v + y_offset
            new_bl_v = bl_v + y_offset
            new_tr_v = tr_v
            new_tl_v = tl_v
        else:
            # Push top edge DOWN to compress (Add offset to V)
            new_br_v = br_v
            new_bl_v = bl_v
            new_tr_v = tr_v + y_offset
            new_tl_v = tl_v + y_offset

        # Enforce limits (0 to 355)
        new_br_v = max(0, min(355, int(new_br_v)))
        new_bl_v = max(0, min(355, int(new_bl_v)))
        new_tr_v = max(0, min(355, int(new_tr_v)))
        new_tl_v = max(0, min(355, int(new_tl_v)))

        # Output Results - Explicitly written as a single vertical block to prevent layout scrambling
        st.success("### Corrected 16:9 Coordinates:")
        
        st.markdown(f"**Top Left (TL):** `{tl_h} H, {new_tl_v} V`")
        st.markdown(f"**Top Right (TR):** `{tr_h} H, {new_tr_v} V`")
        st.markdown(f"**Bottom Right (BR):** `{br_h} H, {new_br_v} V`")
        st.markdown(f"**Bottom Left (BL):** `{bl_h} H, {new_bl_v} V`")
            
        st.caption(f"Applied a vertical offset adjustment of {y_offset} units.")
