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

# ——— Sidebar Inputs ———
with st.sidebar:
    st.header("📂 Inputs")

    # 1) Replace select_slider with a dropdown
    discipline = st.selectbox(
        "Select your discipline",
        options=["Cardiology", "Neurology", "Pediatrics", "Oncology"]
    )

    uploaded_file = st.file_uploader("Upload Patient Info (.json)", type=["json"])
    extra_notes   = st.text_area("Extra clinician notes", height=120)
    st.markdown("---")
    generate_btn = st.button("📝 Generate Summary")

# ——— Main ———
st.markdown("Use this tool to draft patient discharge letters based on patient data + tailored notes.\n\n---")

if uploaded_file:
    try:
        data = json.load(uploaded_file)
        with st.expander("🔍 View Patient Data"):
            st.json(data)
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON. Please upload a well-formed file.")

# ——— Map each discipline to its own prompt/example ———
prompt_templates = {
    "Cardiology": {
        "system_prompt": "You are an expert cardiologist drafting discharge summaries. Focus on cardiac metrics, med changes, follow-up ECHO, etc.",
        "example_letter": "Example Cardiology Discharge:\nPatient X was admitted for NSTEMI…"
    },
    "Neurology": {
        "system_prompt": "You are a neurologist. Emphasize neuro exams, imaging findings, seizure precautions, follow-up MRI, etc.",
        "example_letter": "Example Neurology Discharge:\nPatient Y presented with acute CVA…"
    },
    "Pediatrics": {
        "system_prompt": "You are a pediatrician writing in family-friendly language. Highlight growth charts, immunizations, feeding plans, etc.",
        "example_letter": "Example Pediatrics Discharge:\nBaby Z was evaluated for bronchiolitis…"
    },
    "Oncology": {
        "system_prompt": "You are an oncologist. Cover chemo regimens, tumor markers, radiation plans, and survivorship care.",
        "example_letter": "Example Oncology Discharge:\nMr. A completed cycle 2 of R-CHOP…"
    }
}

# ——— Generation Logic ———
if generate_btn:
    if not uploaded_file:
        st.error("❌ Please upload the patient information file first.")
    else:
        with st.spinner("Generating discharge summary…"):
            try:
                # pick the right prompt for this discipline
                tpl = prompt_templates[discipline]

                # pass it into your generator class
                model = DischargeSummaryGenerator(
                    system_prompt   = tpl["system_prompt"],
                    example_discharge = tpl["example_letter"]
                )

                response = model.generate_letter(
                    data            = data,
                    additional_info = extra_notes
                )

                st.success("✅ Done!")
                st.markdown(
                    f"<div class='card'><h3>Generated ({discipline}):</h3>"
                    f"<pre>{response}</pre></div>",
                    unsafe_allow_html=True
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
