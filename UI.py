import streamlit as st
import json
from prompt_generator import DischargeSummaryGenerator  # Assuming the class is in prompt_generator.py


st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;500&display=swap" rel="stylesheet">
    <style>
    /* Base */
    body, .css-18e3th9, .stApp { font-family: 'Roboto Slab', serif; }
    /* Gradient Header */
    .header {
        background: linear-gradient(90deg, #0066cc, #0099ff);
        padding: 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
    }
    /* Card style */
    .card {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }
    .btn-gradient {
        background: linear-gradient(45deg, #00bfa5, #1de9b6);
        border: none;
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
    }
    .btn-gradient:hover { opacity: 0.9; }
    .footer { text-align: center; color: #888; margin-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ——— Header ———
st.markdown("<div class='header'><h1>Discharge Letter Studio</h1>"
            "<p style='opacity:0.9;'>Your AI-powered, custom‑styled discharge summaries</p></div>",
            unsafe_allow_html=True)

# ——— Sidebar ———
with st.sidebar:
    st.header("📂 Inputs")
    uploaded_file = st.file_uploader("Upload Patient Information File(.json)", type=["json"])
    additional_input = st.text_area(
        "Extra clinician notes",
        placeholder="Type any additional context here...",
        height=120
    )
    st.markdown("---")
    generate_btn = st.button("📝 Generate Summary")

# ——— Main header ———
st.markdown("Use this tool to automatically draft patient discharge letters based on patient data + additional tailored notes.\n\n---")

# ——— Display uploaded JSON ———
if uploaded_file:
    try:
        data = json.load(uploaded_file)
        with st.expander("🔍 View Uploaded Patient Information", expanded=False):
            st.json(data)
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON. Please upload a well-formed file.")

# ——— Generation logic ———
if generate_btn:
    if not uploaded_file:·
        st.error("Please upload the patient information(.json) file first.")
    else:
        with st.spinner("Generating discharge summary…"):
            try:
                model = DischargeSummaryGenerator()
                response = model.generate_letter(data=data, additional_info=additional_input)
                st.success("✅ Generation successful!")
                st.markdown("<div class='generated-response'>"
                            "<h3>Generated Letter:</h3>"
                            f"<pre>{response}</pre>"
                            "</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
