# 90-835 Spring 2025 Final Project: Discharge Summary Letter Generation

This repository provides tools and experiments for automating the generation of patient discharge summary letters using prompt-based techniques. 

## Overview
The goal of this project is to generate high-quality discharge summary letters by leveraging prompt engineering and LLMs. The repository includes code for both backend prompt generation and a simple Streamlit-based frontend UI.

## File Structure
├── data/   
├── experiment/  
├── evaluation/  
├── prompt_generator.py  
├── prompts.ipynb
├── UI.py   
├── log.txt   
└── README.md

## Usage
Launch the Streamlit UI to interactively generate discharge summaries: `streamlit run UI.py`

## Data
All raw data files are stored in the data/ directory. Ensure your input JSON files or other formats are placed here before running experiments or the UI.

## Logging
Execution logs including de-identified data, system prompt, user prompt, additional information and generated results are recorded in `log.txt`. Check this file for detailed run information and troubleshooting. Note that we use different logging code fore experiement(`prompts.ipynb`) and actual generator (`prompt_generator.py`)

## Experiments
We used prompts.ipynb to experiment with different 3 different Zero-shot propmting strategies, running 5 experiments for each data points. (60 files in total) Experiments results are organized in the `experiment/` folder in json format. 

## Evaluation
The quantative analysis conducted using GPT-4o are store in `evaluation/` directory. The folder contains evaluation individual evaluation results stored in json file and unified evaluation results saved in `evaluations.csv`. 

