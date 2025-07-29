# Image-Based Circuit Solver: General Circuit Detector (Improved Version)
# Requirements: OpenCV, Streamlit, NumPy

import cv2
import numpy as np
import streamlit as st

st.title("🔌 Image-Based Circuit Solver (General Circuits)")
st.write("Upload a hand-drawn or digital image of a circuit with batteries and resistors. This version attempts to detect all types of rectangular components and connection lines.")

uploaded_file = st.file_uploader("Choose a circuit image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_resized = cv2.resize(img, (600, 400))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Detect lines (wires) using Hough Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img_resized, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Detect rectangles (components)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    component_count = 0

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            component_count += 1

    st.image(img_resized, channels="BGR", caption="Detected components and wires")
    st.write(f"Detected rectangle components: **{component_count}**")

    if component_count >= 2:
        st.success("Multiple components detected. Assuming general circuit.")
        voltage = st.number_input("Enter Voltage of the battery (V)", min_value=1)
        resistances = []
        for i in range(component_count - 1):
            r = st.number_input(f"Enter Resistance R{i+1} (Ohms)", min_value=1)
            resistances.append(r)

        if resistances and voltage:
            R_total = sum(resistances)
            current = voltage / R_total
            st.write(f"**Total Resistance (assuming series):** {R_total} Ω")
            st.write(f"**Current Flowing:** {current:.2f} A")
            for i, r in enumerate(resistances):
                v_drop = current * r
                st.write(f"Voltage drop across R{i+1}: {v_drop:.2f} V")
    else:
        st.warning("Not enough components detected to solve the circuit.")
