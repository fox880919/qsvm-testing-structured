"""
QSVM Structure Testing - Web Interface
Launch with: streamlit run app.py
"""

import os
import sys
import subprocess
import streamlit as st

# Ensure we run from the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)
sys.path.insert(0, PROJECT_DIR)

# Dataset options: value -> display name
DATASET_OPTIONS = {
    0: "Wine",
    1: "Load Digits",
    2: "Credit Card",
    3: "MNIST",
}

# Output files
STEP1_CSV = os.path.join(PROJECT_DIR, "saved_data", "my_data_frame_Jan_all.csv")
STEP2_CSV = os.path.join(PROJECT_DIR, "results_v41_kernel_test.csv")


def run_tests_subprocess(dataset: int, kfold: int):
    """Run main.py as subprocess with given config."""
    cmd = [
        sys.executable,
        os.path.join(PROJECT_DIR, "main.py"),
        "--dataset", str(dataset),
        "--kfold", str(kfold),
    ]
    return subprocess.run(
        cmd,
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )


st.set_page_config(
    page_title="QSVM Structure Testing",
    page_icon="🔬",
    layout="centered",
)

st.title("QSVM Structure Testing")
st.markdown("Configure and run the two-step mutation and metamorphic testing pipeline.")

st.divider()

# Sidebar or main area for config
with st.form("config_form"):
    st.subheader("Configuration")
    
    dataset = st.selectbox(
        "Dataset",
        options=list(DATASET_OPTIONS.keys()),
        format_func=lambda x: DATASET_OPTIONS[x],
        index=0,
    )
    
    kfold = st.slider(
        "K-fold value (Step 1)",
        min_value=2,
        max_value=20,
        value=5,
    )
    
    submitted = st.form_submit_button("Run Tests")

if submitted:
    st.info(f"Running with **{DATASET_OPTIONS[dataset]}** dataset and **K={kfold}** folds.")
    
    # Ensure output directory exists
    os.makedirs(os.path.join(PROJECT_DIR, "saved_data"), exist_ok=True)
    
    with st.spinner("Running Step 1 & Step 2... This may take several minutes."):
        result = run_tests_subprocess(dataset, kfold)
    
    if result.returncode == 0:
        st.success("Tests completed successfully.")
        
        # Show output files
        st.subheader("Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if os.path.exists(STEP1_CSV):
                try:
                    with open(STEP1_CSV, "rb") as f:
                        csv1 = f.read()
                    st.download_button(
                        "Download Step 1 Results (CSV)",
                        data=csv1,
                        file_name="my_data_frame_Jan_all.csv",
                        mime="text/csv",
                        key="step1_dl",
                    )
                except Exception as e:
                    st.write(f"Could not read Step 1 CSV: {e}")
            else:
                st.write("Step 1 CSV not found (check `saved_data/`).")
        
        with col2:
            if os.path.exists(STEP2_CSV):
                try:
                    with open(STEP2_CSV, "rb") as f:
                        csv2 = f.read()
                    st.download_button(
                        "Download Step 2 Results (CSV)",
                        data=csv2,
                        file_name="results_v41_kernel_test.csv",
                        mime="text/csv",
                        key="step2_dl",
                    )
                except Exception as e:
                    st.write(f"Could not read Step 2 CSV: {e}")
            else:
                st.write("Step 2 CSV not found.")
        
        # Expandable log
        with st.expander("View run output"):
            st.code(result.stdout if result.stdout else "(no output)")
            if result.stderr:
                st.code(result.stderr)
    else:
        st.error("Tests failed. See output below.")
        st.code(result.stdout or "(no stdout)")
        st.code(result.stderr or "(no stderr)")

st.divider()
st.caption("Step 1: 30 mutants, angle + amplitude embeddings, 12 MRs, statistical testing. Step 2: Quantum kernel only, 14 MRs.")
