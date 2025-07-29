import streamlit as st
from PIL import Image
import time

# Page setup
st.set_page_config(
    page_title="Image-Based Circuit Solver",
    page_icon="🔌",
    layout="centered"
)

st.markdown("""
    <h1 style='text-align: center; color: #39ff14;'>🔌 Image-Based Circuit Solver</h1>
    <p style='text-align: center; color: #AAAAAA;'>Upload a circuit OR type in resistor values to calculate resistance, current, and voltage.</p>
    <hr>
""", unsafe_allow_html=True)

# ========== Image Upload + Mock AI Analysis ==========
st.subheader("📷 Upload Mode (Mock AI Solver)")

uploaded_file = st.file_uploader("Upload a circuit image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Circuit", use_container_width=True)

    if st.button("⚡ Analyze Image (Mock)"):
        with st.spinner("Analyzing image..."):
            time.sleep(2)
        st.success("✅ Analysis Complete (Mock)")
        st.markdown("**Total Resistance:** 8.5 Ω")
        st.markdown("**Current:** 1.2 A")
        st.markdown("**Voltage:** 10.2 V")

st.markdown("---")

# ========== Manual Input Mode ==========
st.subheader("✍️ Manual Input Calculator")

with st.form("manual_calc_form"):
    st.markdown("Enter resistor values and total voltage to get real calculations.")

    circuit_type = st.radio("Circuit Type", ["Series", "Parallel"])
    voltage = st.number_input("🔋 Total Voltage (V)", min_value=0.0, value=12.0)
    resistors = st.text_input("🧮 Enter resistor values (comma-separated, e.g., 4, 6, 8)", "4,6,8")

    submitted = st.form_submit_button("🔍 Calculate")

if submitted:
    try:
        resistor_list = [float(r.strip()) for r in resistors.split(",") if r.strip()]
        if not resistor_list:
            st.error("Please enter at least one valid resistor value.")
        else:
            if circuit_type == "Series":
                total_resistance = sum(resistor_list)
            else:  # Parallel
                total_resistance = 1 / sum(1/r for r in resistor_list)

            current = voltage / total_resistance

            st.success("✅ Calculation Results:")
            st.markdown(f"**Total Resistance:** {round(total_resistance, 2)} Ω")
            st.markdown(f"**Current:** {round(current, 2)} A")

            st.markdown("**Voltage Drop Across Each Resistor:**")
            for i, r in enumerate(resistor_list):
                v_drop = current * r if circuit_type == "Series" else voltage
                st.write(f"• R{i+1} = {r} Ω → {round(v_drop, 2)} V")

    except Exception as e:
        st.error(f"Error: {str(e)}")
