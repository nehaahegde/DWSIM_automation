# DWSIM Process Simulation Automation

This project provides a headless execution pipeline for DWSIM, allowing chemical process simulations to be run programmatically via Python. It is designed to automate parameter screening, calculate process outputs across variable ranges, and aggregate results for analysis.

## Tech Stack
*   **Language:** Python 3.x
*   **Simulation Engine:** DWSIM (Open Source Chemical Process Simulator)
*   **Libraries:** `pythonnet` (clr), `pandas`, `numpy`

## Features
*   **Headless Execution:** Interfaces directly with the DWSIM .NET API (`DWSIM.Automation`) to bypass the GUI.
*   **Parameter Screening:** Programmatically sweeps through feed temperatures (or other user-defined variables).
*   **Automated Data Extraction:** Retrieves calculated phase properties (e.g., mass flow, enthalpy) from target streams.
*   **CSV Reporting:** Compiles all iteration results into a structured Pandas DataFrame and exports them.

## Usage
1.  Ensure DWSIM is installed on your system.
2.  Update the `DWSIM_PATH` in `run_screening.py` to point to your local DWSIM installation directory.
3.  Place your configured `.dwxml` flowsheet in the project directory.
4.  Run the script:
    ```bash
    python run_screening.py
    ```
5.  Results will be output to `screening_results.csv`.

---
**Author:** Neha Umapati Hegde
