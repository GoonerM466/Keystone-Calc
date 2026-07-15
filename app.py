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
    # Calculate average horizontal offset to determine the required offset scale factor
    avg_h_offset = (tl_h + tr_h + br_h + bl_h) / 4.0
    
    # Linear scale factor to translate H offset to vertical offset (yielding exactly +3 offset at 148.5 H)
    y_offset = round(avg_h_offset * 0.0202)
    
    if y_offset == 0:
        st.info("The image is already at a perfect 16:9 ratio!")
    else:
        # Apply the linear offset to the selected target edge
        if compression_pref == "Bottom Edge":
            new_br_v = br_v + y_offset
            new_bl_v = bl_v + y_offset
            new_tr_v = tr_v
            new_tl_v = tl_v
        else:
            new_br_v = br_v
            new_bl_v = bl_v
            new_tr_v = tr_v + y_offset
            new_tl_v = tl_v + y_offset

        # Enforce physical software boundary constraints (0 to 355)
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
