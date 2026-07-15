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
br_v = st.number_input("Bottom-Right Vertical (BR V)", value=165, key="br_v")

bl_h = st.number_input("Bottom-Left Horizontal (BL H)", value=153, key="bl_h")
bl_v = st.number_input("Bottom-Left Vertical (BL V)", value=159, key="bl_v")

st.markdown("---")

# Settings and Action
compression_pref = st.selectbox(
    "Adjustment Target Edge",
    options=["Bottom Edge", "Top Edge"],
    index=0
)

if st.button("Calculate Perfect 16:9", type="primary"):
    # 1. Calculate overall average horizontal offset
    avg_h = (tl_h + tr_h + br_h + bl_h) / 4.0
    
    # 2. Determine target overall average vertical offset for 16:9
    target_avg_v = avg_h * 1.1044
    
    # 3. Calculate current averages of top and bottom edges
    avg_top_v = (tl_v + tr_v) / 2.0
    avg_bottom_v = (bl_v + br_v) / 2.0
    
    # Apply the target offset based on selected adjustment edge
    if compression_pref == "Bottom Edge":
        # Target average for bottom edge to balance out the top edge
        target_bottom_v = (2 * target_avg_v) - avg_top_v
        y_offset = round(target_bottom_v - avg_bottom_v)
        
        new_br_v = br_v + y_offset
        new_bl_v = bl_v + y_offset
        new_tr_v = tr_v
        new_tl_v = tl_v
    else:
        # Target average for top edge to balance out the bottom edge
        target_top_v = (2 * target_avg_v) - avg_bottom_v
        y_offset = round(target_top_v - avg_top_v)
        
        new_br_v = br_v
        new_bl_v = bl_v
        new_tr_v = tr_v + y_offset
        new_tl_v = tl_v + y_offset

    # Enforce hardware boundary constraints (0 to 355)
    new_br_v = max(0, min(355, int(new_br_v)))
    new_bl_v = max(0, min(355, int(new_bl_v)))
    new_tr_v = max(0, min(355, int(new_tr_v)))
    new_tl_v = max(0, min(355, int(new_tl_v)))

    # Output Results - Clear, explicit vertical list
    st.success("### Corrected 16:9 Coordinates:")
    
    st.markdown(f"**Top Left (TL):** `{tl_h} H, {new_tl_v} V`")
    st.markdown(f"**Top Right (TR):** `{tr_h} H, {new_tr_v} V`")
    st.markdown(f"**Bottom Right (BR):** `{br_h} H, {new_br_v} V`")
    st.markdown(f"**Bottom Left (BL):** `{bl_h} H, {new_bl_v} V`")
        
    st.caption(f"Applied a precise vertical offset adjustment of {y_offset} units.")
