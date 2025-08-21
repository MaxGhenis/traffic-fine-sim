#!/usr/bin/env python3
"""
Test memory usage of PolicyEngine-US for household calculations and microsimulations.
"""

import psutil
import os
import gc
import time
from policyengine_us import Microsimulation
from policyengine_us.data import CPS_2022

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def test_household_calculations():
    """Test memory usage for household calculations."""
    print("\n=== Testing Household Calculations ===")
    
    # Baseline memory
    gc.collect()
    baseline_mem = get_memory_usage()
    print(f"Baseline memory: {baseline_mem:.1f} MB")
    
    # Create a simple household simulation (default uses synthetic data)
    start_mem = get_memory_usage()
    sim = Microsimulation()
    
    # Calculate some household values
    total_income = sim.calculate("household_net_income", 2024)
    tax_liability = sim.calculate("income_tax", 2024)
    benefits = sim.calculate("household_benefits", 2024)
    
    after_calc_mem = get_memory_usage()
    print(f"After household calculations: {after_calc_mem:.1f} MB")
    print(f"Memory used: {after_calc_mem - baseline_mem:.1f} MB")
    
    del sim
    gc.collect()
    
    return after_calc_mem - baseline_mem

def test_microsimulation():
    """Test memory usage for full microsimulation with CPS data."""
    print("\n=== Testing Full Microsimulation ===")
    
    # Baseline memory
    gc.collect()
    baseline_mem = get_memory_usage()
    print(f"Baseline memory: {baseline_mem:.1f} MB")
    
    # Load CPS microsimulation
    print("Loading CPS microsimulation...")
    start_time = time.time()
    sim = Microsimulation(dataset=CPS_2022)
    load_time = time.time() - start_time
    
    after_load_mem = get_memory_usage()
    print(f"After loading CPS data: {after_load_mem:.1f} MB")
    print(f"Memory for dataset: {after_load_mem - baseline_mem:.1f} MB")
    print(f"Load time: {load_time:.1f} seconds")
    
    # Run some calculations
    print("\nRunning population-wide calculations...")
    start_time = time.time()
    
    # Calculate various metrics
    total_income = sim.calculate("household_net_income", 2024).sum()
    total_tax = sim.calculate("income_tax", 2024).sum()
    total_benefits = sim.calculate("household_benefits", 2024).sum()
    poverty_rate = (sim.calculate("in_poverty", 2024) * sim.calculate("person_weight", 2024)).sum() / sim.calculate("person_weight", 2024).sum()
    
    calc_time = time.time() - start_time
    after_calc_mem = get_memory_usage()
    
    print(f"After calculations: {after_calc_mem:.1f} MB")
    print(f"Peak memory usage: {after_calc_mem - baseline_mem:.1f} MB")
    print(f"Calculation time: {calc_time:.1f} seconds")
    
    # Print some results
    print(f"\nResults:")
    print(f"  Total household income: ${total_income/1e9:.1f}B")
    print(f"  Total income tax: ${total_tax/1e9:.1f}B")
    print(f"  Total benefits: ${total_benefits/1e9:.1f}B")
    print(f"  Poverty rate: {poverty_rate*100:.1f}%")
    
    del sim
    gc.collect()
    
    return after_calc_mem - baseline_mem

def test_multiple_simulations():
    """Test memory usage with multiple simultaneous simulations."""
    print("\n=== Testing Multiple Simultaneous Simulations ===")
    
    gc.collect()
    baseline_mem = get_memory_usage()
    print(f"Baseline memory: {baseline_mem:.1f} MB")
    
    sims = []
    for i in range(3):
        print(f"\nCreating simulation {i+1}...")
        sim = Microsimulation()
        sim.calculate("household_net_income", 2024)
        sims.append(sim)
        
        current_mem = get_memory_usage()
        print(f"  Memory after sim {i+1}: {current_mem:.1f} MB (+{current_mem - baseline_mem:.1f} MB)")
    
    total_mem = get_memory_usage() - baseline_mem
    print(f"\nTotal memory for 3 simulations: {total_mem:.1f} MB")
    print(f"Average per simulation: {total_mem/3:.1f} MB")
    
    # Cleanup
    for sim in sims:
        del sim
    gc.collect()
    
    return total_mem

def main():
    print("PolicyEngine-US Memory Usage Test")
    print("="*50)
    print(f"System memory: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print(f"Available memory: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.1f} GB")
    
    # Test different scenarios
    household_mem = test_household_calculations()
    multiple_mem = test_multiple_simulations()
    
    try:
        microsim_mem = test_microsimulation()
    except Exception as e:
        print(f"\nCPS microsimulation failed: {e}")
        print("This might require downloading the CPS dataset first.")
        microsim_mem = None
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Household calculations: {household_mem:.1f} MB")
    print(f"Three simultaneous simulations: {multiple_mem:.1f} MB")
    if microsim_mem:
        print(f"Full CPS microsimulation: {microsim_mem:.1f} MB")
    
    # Estimate for multiple Claude sessions
    claude_mem_per_session = 2000  # Estimated 2GB per Claude session
    print(f"\nEstimated memory with multiple Claude Code sessions:")
    print(f"  1 Claude + household calcs: {claude_mem_per_session + household_mem:.0f} MB")
    print(f"  3 Claude + household calcs: {3*claude_mem_per_session + household_mem:.0f} MB")
    if microsim_mem:
        print(f"  1 Claude + microsim: {claude_mem_per_session + microsim_mem:.0f} MB")
        print(f"  3 Claude + microsim: {3*claude_mem_per_session + microsim_mem:.0f} MB")

if __name__ == "__main__":
    main()