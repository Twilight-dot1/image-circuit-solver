# Image-Based Circuit Solver: Imgur-Styled Version
# Requirements: OpenCV, Streamlit, NumPy

import cv2
import numpy as np
import streamlit as st

st.set_page_config(page_title="⚡ Circuit Solver", page_icon="🧠", layout="centered")

st.markdown("""
<style>
body {
    background-color: #18181B;
    font-family: 'Segoe UI', sans-serif;
    color: #E5E7EB;
}

h1, h2, h3, h4 {
    color: #F9FAFB;
    font-weight: 800;
}

.stFileUploader > label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #10B981;
}

.stButton > button {
    background: linear-gradient(to right, #22C55E, #16A34A);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: bold;
    border-radius: 6px;
    transition: background 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(to right, #16A34A, #15803D);
    transform: scale(1.02);
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    background-color: #27272A;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🧠 Circuit Solver
Welcome to the AI-powered circuit detection tool.

💡 Upload a **hand-drawn** or **digital** circuit with basic components.

📤 **Drag and drop** your image into the uploader below to get started:
""")

uploaded_file = st.file_uploader("Drop or Upload a Circuit Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_resized = cv2.resize(img, (600, 400))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Detect lines (wires)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img_resized, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Detect rectangle components
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    component_count = 0
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            component_count += 1

    st.image(img_resized, channels="BGR", caption="📷 Detected Components and Wires")
    st.markdown(f"## 🔍 Components Detected: `{component_count}`")

    if component_count >= 2:
        st.success("✅ Circuit recognized! Please enter the electrical parameters:")
        voltage = st.number_input("🔋 Voltage (V)", min_value=1)
        resistances = []
        for i in range(component_count - 1):
            r = st.number_input(f"🔧 Resistance R{i+1} (Ω)", min_value=1)
            resistances.append(r)

        if resistances and voltage:
            R_total = sum(resistances)
            current = voltage / R_total
            st.markdown(f"### 🧮 Total Resistance: `{R_total} Ω`")
            st.markdown(f"### ⚡ Current Flowing: `{current:.2f} A`")
            for i, r in enumerate(resistances):
                v_drop = current * r
                st.markdown(f"- 🔋 Voltage Drop across R{i+1}: `{v_drop:.2f} V`")
    else:
        st.warning("⚠️ Not enough components detected to calculate the circuit.")
