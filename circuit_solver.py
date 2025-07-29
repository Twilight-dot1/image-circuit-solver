# Image-Based Circuit Solver: General Circuit Detector with Enhanced UI
# Requirements: OpenCV, Streamlit, NumPy

import cv2
import numpy as np
import streamlit as st

st.set_page_config(page_title="⚡ AI Circuit Solver", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #0f2027;
        background-image: linear-gradient(to right, #2c5364, #203a43, #0f2027);
        color: white;
    }
    .main {
        background-color: #ffffff10;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.15);
        color: white;
    }
    .stFileUploader > label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #00f7ff;
    }
    h1, h2, h3, h4 {
        color: #ffffff;
        text-shadow: 1px 1px 4px #000000;
    }
    .stButton > button {
        background-color: #00f7ff;
        color: #0f2027;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        background-color: #0ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# 🧠 AI-Powered Circuit Solver
Upload a **hand-drawn** or **digital image** of a circuit with batteries and resistors.

✨ This intelligent tool detects components, wires, and solves for current and voltage drops in real-time.

📤 Just drag & drop your image below:
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

    st.image(img_resized, channels="BGR", caption="🖼️ Detected Components and Wires")
    st.markdown(f"## 🔍 Detected Components: `{component_count}`")

    if component_count >= 2:
        st.success("✅ Circuit identified! Please enter voltage and resistances below:")
        voltage = st.number_input("🔋 Voltage (in Volts)", min_value=1)
        resistances = []
        for i in range(component_count - 1):
            r = st.number_input(f"🔧 Resistance R{i+1} (Ω)", min_value=1)
            resistances.append(r)

        if resistances and voltage:
            R_total = sum(resistances)
            current = voltage / R_total
            st.markdown(f"### 🧮 Total Resistance: `{R_total} Ω`")
            st.markdown(f"### ⚡ Current: `{current:.2f} A`")
            for i, r in enumerate(resistances):
                v_drop = current * r
                st.markdown(f"- Voltage Drop across R{i+1}: `{v_drop:.2f} V`")
    else:
        st.warning("⚠️ Not enough components detected to solve the circuit.")
