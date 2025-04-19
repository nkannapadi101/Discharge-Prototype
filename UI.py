import streamlit as st
import json
from prompt_generator import DischargeSummaryGenerator  # Assuming the class is in prompt_generator.py
# from some_llm_library import generate_response  # Replace with your LLM library

# Title of the app
st.title("Discharge Summary Letter Generator")

# File uploader for JSON
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file is not None:
    # Load and display the JSON content
    try:
        data = json.load(uploaded_file)
        st.json(data)
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Please upload a valid JSON file.")

# Text input for clinician to add to the existing prompt
additional_input = st.text_area("Add to the existing prompt", placeholder="Enter additional input here...")

# Submit button
if st.button("Generate"):
    if uploaded_file is None:
        st.error("Please upload a JSON file before generating.")
    # elif not additional_input.strip():
    #     st.error("Please provide additional input before generating.")
    else:
        
        # Call the LLM to generate a response
        try:
            model = DischargeSummaryGenerator()
            response = model.generate_letter(data=data, additional_info=additional_input)  # Replace with your LLM function
            st.success("Generation successful!")
            st.text_area("Generated Response", value=response, height=200)
        except Exception as e:
            st.error(f"An error occurred during generation: {e}")