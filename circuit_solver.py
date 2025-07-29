# Image-Based Circuit Solver: Imgur-Styled Version + Enhanced UI
# Requirements: OpenCV, Streamlit, NumPy, streamlit-lottie, requests

import cv2
import numpy as np
import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title="⚡ Circuit Solver", page_icon="🧠", layout="centered")

@st.cache_data(show_spinner=False)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_zrqthn6o.json")

st.markdown("""
<style>
body {
    background: linear-gradient(270deg, #0f2027, #203a43, #2c5364);
    background-size: 600% 600%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Segoe UI', sans-serif;
    color: #E5E7EB;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%}
    50% {background-position: 100% 50%}
    100% {background-position: 0% 50%}
}

h1, h2, h3, h4 {
    color: #F9FAFB;
    font-weight: 800;
    text-shadow: 1px 1px 2px #000000;
}

.stFileUploader > label {
    font-size: 1.1rem;
    font-weight: 600;
    color: #10B981;
    transition: all 0.3s ease-in-out;
}

.stFileUploader > label:hover {
    color: #22c55e;
    text-shadow: 0 0 10px #22c55e;
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
    background-color: rgba(39, 39, 42, 0.85);
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

st_lottie(lottie_ai, height=250, key="ai_intro")

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
    aspect_ratio = img.shape[1] / img.shape[0]
    width = 600
    height = int(width / aspect_ratio)
    img_resized = cv2.resize(img, (width, height))

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
