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
        padding: 20px;
        background-color: #1E1E1E;
        text-align: center;
        margin-bottom: 20px;
    }
    .screen-title {
        color: #4CAF50;
        font-weight: bold;
        font-size: 1.2rem;
    }
    </style>
    <div class="screen-box">
        <span class="screen-title">=== VISUAL 16:9 SCREEN LAYOUT ===</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Input Coordinates in preferred sequence: TL, TR, BR, BL
col_left_top, col_right_top = st.columns(2)

with col_left_top:
    st.subheader("Top-Left Corner (TL)")
    tl_h = st.number_input("TL Horizontal (H)", value=145, key="tl_h")
    tl_v = st.number_input("TL Vertical (V)", value=150, key="tl_v")

with col_right_top:
    st.subheader("Top-Right Corner (TR)")
    tr_h = st.number_input("TR Horizontal (H)", value=148, key="tr_h")
    tr_v = st.number_input("TR Vertical (V)", value=162, key="tr_v")

st.markdown("---")

col_left_bottom, col_right_bottom = st.columns(2)

with col_left_bottom:
    st.subheader("Bottom-Right Corner (BR)")
    br_h = st.number_input("BR Horizontal (H)", value=148, key="br_h")
    br_v = st.number_input("BR Vertical (V)", value=172, key="br_v")

with col_right_bottom:
    st.subheader("Bottom-Left Corner (BL)")
    bl_h = st.number_input("BL Horizontal (H)", value=153, key="bl_h")
    bl_v = st.number_input("BL Vertical (V)", value=166, key="bl_v")

st.markdown("---")

# Settings and Action
compression_pref = st.selectbox(
    "Adjustment Target Edge",
    options=["Bottom Edge", "Top Edge"],
    index=0
)

if st.button("Calculate Perfect 16:9", type="primary"):
    # Shared horizontal limit: H_left + H_right <= 505
    H_LIMIT_MAX = 505
    # Shared vertical limit: V_top + V_bottom <= 501
    V_LIMIT_MAX = 501
    
    # Calculate physical width dimensions based on shared offsets
    top_width_span = H_LIMIT_MAX - (tl_h + tr_h)
    bottom_width_span = H_LIMIT_MAX - (bl_h + br_h)
    avg_width = (top_width_span + bottom_width_span) / 2.0
    
    # Calculate target vertical height for a clean 16:9 screen
    target_height = avg_width * (9.0 / 16.0)
    
    # Calculate current height dimensions based on vertical offsets
    left_height = V_LIMIT_MAX - (tl_v + bl_v)
    right_height = V_LIMIT_MAX - (tr_v + br_v)
    avg_current_height = (left_height + right_height) / 2.0
    
    # Calculate required vertical adjustment (Y)
    # y_offset > 0: current image too tall (add value to V to compress)
    # y_offset < 0: current image too wide (subtract value from V to expand)
    y_offset = round(avg_current_height - target_height)
    
    if y_offset == 0:
        st.info("The image is already at a perfect 16:9 ratio!")
    else:
        # Apply offset to the selected edge
        if compression_pref == "Bottom Edge":
            new_br_v = br_v + y_offset
            new_bl_v = bl_v + y_offset
            new_tr_v = tr_v
            new_tl_v = tl_v
        else:
            new_br_v = br_v
            new_bl_v = bl_v
            new_tr_v = tr_v - y_offset
            new_tl_v = tl_v - y_offset

        # Enforce physical software boundary constraints
        new_br_v = max(0, min(355, new_br_v))
        new_bl_v = max(0, min(355, new_bl_v))
        new_tr_v = max(0, min(355, new_tr_v))
        new_tl_v = max(0, min(355, new_tl_v))

        # Output Results in sequence: TL -> TR -> BR -> BL
        st.success("### Corrected 16:9 Coordinates:")
        
        col_out_l, col_out_r = st.columns(2)
        with col_out_l:
            st.markdown(f"**Top Left:** `{tl_h} H, {new_tl_v} V`")
            st.markdown(f"**Bottom Right:** `{br_h} H, {new_br_v} V`")
        with col_out_r:
            st.markdown(f"**Top Right:** `{tr_h} H, {new_tr_v} V`")
            st.markdown(f"**Bottom Left:** `{bl_h} H, {new_bl_v} V`")
            
        action_word = "compressed" if y_offset > 0 else "expanded"
        st.caption(f"Adjusted physical vertical space by {abs(y_offset)} units to align with constraints.")
