# Image-Based Circuit Solver: Series Circuit Detector (Basic Version)
# Requirements: OpenCV, Streamlit, NumPy

import cv2
import numpy as np
import streamlit as st

st.title("🔌 Image-Based Series Circuit Solver")
st.write("Upload a hand-drawn or digital image of a simple series circuit with batteries and resistors (as rectangles).")

uploaded_file = st.file_uploader("Choose a circuit image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_resized = cv2.resize(img, (600, 400))
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    component_count = 0

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 500:  # Rectangle-like
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            component_count += 1

    st.image(img_resized, channels="BGR", caption="Detected components")
    st.write(f"Detected rectangle components: **{component_count}**")

    if component_count >= 2:
        st.success("This appears to be a simple **series circuit**.")
        voltage = st.number_input("Enter Voltage of the battery (V)", min_value=1)
        resistances = []
        for i in range(component_count - 1):  # Assuming 1 battery, rest are resistors
            r = st.number_input(f"Enter Resistance R{i+1} (Ohms)", min_value=1)
            resistances.append(r)

        if resistances and voltage:
            R_total = sum(resistances)
            current = voltage / R_total
            st.write(f"**Total Resistance:** {R_total} Ω")
            st.write(f"**Current Flowing:** {current:.2f} A")
            for i, r in enumerate(resistances):
                v_drop = current * r
                st.write(f"Voltage drop across R{i+1}: {v_drop:.2f} V")
    else:
        st.warning("Not enough components detected to identify a series circuit.")

