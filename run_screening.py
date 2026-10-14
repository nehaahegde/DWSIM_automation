import os
import clr
import sys
import pandas as pd
import numpy as np

# Configure DWSIM installation path
DWSIM_PATH = r"C:\Users\Username\AppData\Local\DWSIM"
sys.path.append(DWSIM_PATH)

# Load DWSIM .NET Assemblies
clr.AddReference("DWSIM.Interfaces")
clr.AddReference("DWSIM.GlobalSettings")
clr.AddReference("DWSIM.SharedClasses")
clr.AddReference("DWSIM.Simulator")

from DWSIM.Interfaces.Enums.GraphicObjects import ObjectType
from DWSIM.Simulator.Automation import Automation2

def run_simulation_screening(flowsheet_path, feed_temps, output_csv):
    """
    Automates DWSIM headless execution to screen variables in a process simulation.
    """
    print(f"Initializing DWSIM Automation API...")
    interf = Automation2()
    
    print(f"Loading flowsheet: {flowsheet_path}")
    sim = interf.LoadFlowsheet(flowsheet_path)
    
    # Locate specific unit operations or streams (e.g., Feed Stream and Reactor)
    feed_stream = sim.GetFlowsheetSimulationObject("Feed")
    product_stream = sim.GetFlowsheetSimulationObject("Product")
    
    if not feed_stream or not product_stream:
        raise ValueError("Could not find required streams in the flowsheet.")

    results = []

    print("Beginning automated parameter screening...")
    for temp in feed_temps:
        # Modify feed property (Temperature in Kelvin)
        feed_stream.GetPhase("Overall").Properties.temperature = temp
        
        # Calculate Flowsheet
        error_list = interf.CalculateFlowsheet2(sim)
        if error_list:
            print(f"Simulation failed at {temp}K. Errors: {error_list}")
            continue
            
        # Extract results (e.g., Mass Flow Rate or Enthalpy)
        mass_flow = product_stream.GetPhase("Overall").Properties.massflow
        enthalpy = product_stream.GetPhase("Overall").Properties.enthalpy
        
        results.append({
            "Feed_Temperature_K": temp,
            "Product_Mass_Flow_kg_s": mass_flow,
            "Product_Enthalpy_kJ_kg": enthalpy
        })
        print(f"Calculated for Temp: {temp}K -> Mass Flow: {mass_flow:.4f}")

    # Save output to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    print(f"Screening complete. Results saved to {output_csv}")

if __name__ == "__main__":
    FLOWSHEET = "reactor_model.dwxml"
    OUTPUT_FILE = "screening_results.csv"
    
    # Generate test parameters: Feed temperatures from 300K to 400K
    test_temperatures = np.linspace(300, 400, 11)
    
    # Ensure flowsheet exists before running
    if os.path.exists(FLOWSHEET):
        run_simulation_screening(FLOWSHEET, test_temperatures, OUTPUT_FILE)
    else:
        print(f"Error: Flowsheet {FLOWSHEET} not found.")
