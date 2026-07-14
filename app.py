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

# 4-Corner Grid Layout
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top-Left Corner")
    tl_h = st.number_input("TL Horizontal (H)", value=0, key="tl_h")
    tl_v = st.number_input("TL Vertical (V)", value=0, key="tl_v")

with col_right:
    st.subheader("Top-Right Corner")
    tr_h = st.number_input("TR Horizontal (H)", value=0, key="tr_h")
    tr_v = st.number_input("TR Vertical (V)", value=0, key="tr_v")

st.markdown("---")

col_left_b, col_right_b = st.columns(2)

with col_left_b:
    st.subheader("Bottom-Left Corner")
    bl_h = st.number_input("BL Horizontal (H)", value=0, key="bl_h")
    bl_v = st.number_input("BL Vertical (V)", value=0, key="bl_v")

with col_right_b:
    st.subheader("Bottom-Right Corner")
    br_h = st.number_input("BR Horizontal (H)", value=0, key="br_h")
    br_v = st.number_input("BR Vertical (V)", value=0, key="br_v")

st.markdown("---")

# Settings and Action
compression_pref = st.selectbox(
    "Compression Preference",
    options=["Bottom Edge", "Top Edge"],
    index=0
)

if st.button("Calculate Perfect 16:9", type="primary"):
    # Calculate widths and current heights
    top_width_span = abs(tr_h - tl_h)
    bottom_width_span = abs(br_h - bl_h)
    avg_width = (top_width_span + bottom_width_span) / 2.0
    
    # Calculate target vertical height for 16:9
    target_height = avg_width * (9.0 / 16.0)
    
    # Current heights
    left_height = abs(bl_v - tl_v)
    right_height = abs(br_v - tr_v)
    avg_current_height = (left_height + right_height) / 2.0
    
    # Calculate required uniform vertical offset (Y)
    y_offset = round(avg_current_height - target_height)
    
    if y_offset == 0:
        st.info("The image is already at a perfect 16:9 ratio!")
    else:
        # Apply the logic based on the direction of coordinate values
        if compression_pref == "Bottom Edge":
            # Pushes the bottom edge UP (increases V values)
            new_br_v = br_v + y_offset
            new_bl_v = bl_v + y_offset
            new_tr_v = tr_v
            new_tl_v = tl_v
        else:
            # Pushes the top edge DOWN (decreases V values)
            new_br_v = br_v
            new_bl_v = bl_v
            new_tr_v = tr_v - y_offset
            new_tl_v = tl_v - y_offset

        # Output Results
        st.success("### Corrected 16:9 Coordinates:")
        
        col_out_l, col_out_r = st.columns(2)
        with col_out_l:
            st.markdown(f"**Top Left:** `{tl_h} H, {new_tl_v} V`")
            st.markdown(f"**Bottom Left:** `{bl_h} H, {new_bl_v} V`")
        with col_out_r:
            st.markdown(f"**Top Right:** `{tr_h} H, {new_tr_v} V`")
            st.markdown(f"**Bottom Right:** `{br_h} H, {new_br_v} V`")
            
        st.caption(f"Applied a uniform vertical offset of {abs(y_offset)} units.")
