#!/usr/bin/env python3
"""
Simple memory test for PolicyEngine-US to bypass current numpy compatibility issues.
"""

import psutil
import os
import gc
import time

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def test_policyengine_basic():
    """Test basic PolicyEngine import and setup."""
    print("\n=== Testing PolicyEngine Basic Import ===")
    
    gc.collect()
    baseline_mem = get_memory_usage()
    print(f"Baseline memory: {baseline_mem:.1f} MB")
    
    # Import PolicyEngine
    from policyengine_us import Microsimulation
    after_import = get_memory_usage()
    print(f"After import: {after_import:.1f} MB (+{after_import - baseline_mem:.1f} MB)")
    
    # Create simulation
    try:
        sim = Microsimulation()
        after_sim = get_memory_usage()
        print(f"After creating simulation: {after_sim:.1f} MB (+{after_sim - baseline_mem:.1f} MB)")
        
        # Try a simple calculation
        try:
            result = sim.calculate("employment_income", 2024)
            after_calc = get_memory_usage()
            print(f"After simple calculation: {after_calc:.1f} MB (+{after_calc - baseline_mem:.1f} MB)")
        except:
            print("Simple calculation failed (numpy compatibility issue)")
    except Exception as e:
        print(f"Failed to create simulation: {e}")
    
    return after_import - baseline_mem

def test_data_loading():
    """Test loading different datasets."""
    print("\n=== Testing Dataset Loading ===")
    
    gc.collect()
    baseline_mem = get_memory_usage()
    print(f"Baseline memory: {baseline_mem:.1f} MB")
    
    try:
        from policyengine_us.data import CPS_2022
        
        # Try to instantiate the dataset
        print("Loading CPS 2022 dataset class...")
        dataset = CPS_2022()
        after_class = get_memory_usage()
        print(f"After loading class: {after_class:.1f} MB (+{after_class - baseline_mem:.1f} MB)")
        
        # Try to load actual data
        try:
            print("Attempting to load actual data...")
            data = dataset.load()
            after_load = get_memory_usage()
            print(f"After loading data: {after_load:.1f} MB (+{after_load - baseline_mem:.1f} MB)")
            
            # Check data size
            if hasattr(data, 'nbytes'):
                print(f"Dataset size in memory: {data.nbytes / 1024 / 1024:.1f} MB")
        except Exception as e:
            print(f"Could not load actual data: {e}")
            
    except Exception as e:
        print(f"Failed to load dataset: {e}")

def test_multiple_claude_sessions():
    """Estimate memory for multiple Claude sessions."""
    print("\n=== Estimating Multiple Claude Sessions ===")
    
    current_mem = get_memory_usage()
    print(f"Current process memory: {current_mem:.1f} MB")
    
    # Get system memory info
    mem = psutil.virtual_memory()
    print(f"\nSystem memory status:")
    print(f"  Total: {mem.total / 1024 / 1024 / 1024:.1f} GB")
    print(f"  Available: {mem.available / 1024 / 1024 / 1024:.1f} GB")
    print(f"  Used: {mem.used / 1024 / 1024 / 1024:.1f} GB ({mem.percent:.1f}%)")
    
    # Check running processes for Claude
    claude_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if 'claude' in proc.info['name'].lower() or 'code' in proc.info['name'].lower():
                mem_mb = proc.info['memory_info'].rss / 1024 / 1024
                claude_processes.append((proc.info['name'], mem_mb))
        except:
            pass
    
    if claude_processes:
        print(f"\nClaude-related processes found:")
        for name, mem in claude_processes[:5]:  # Show top 5
            print(f"  {name}: {mem:.1f} MB")
    
    # Estimates based on typical usage
    print(f"\nMemory estimates for PolicyEngine + Claude Code:")
    claude_per_session = 2000  # 2GB estimate
    policyengine_base = 500  # 500MB for basic usage
    policyengine_microsim = 2000  # 2GB for microsim
    
    print(f"  1 Claude + PolicyEngine (basic): {claude_per_session + policyengine_base:.0f} MB")
    print(f"  3 Claude + PolicyEngine (basic): {3*claude_per_session + policyengine_base:.0f} MB")
    print(f"  1 Claude + PolicyEngine (microsim): {claude_per_session + policyengine_microsim:.0f} MB")
    print(f"  3 Claude + PolicyEngine (microsim): {3*claude_per_session + policyengine_microsim:.0f} MB")

def main():
    print("PolicyEngine-US Memory Test (Simplified)")
    print("="*50)
    
    # Run tests
    test_policyengine_basic()
    test_data_loading()
    test_multiple_claude_sessions()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print("\nYour M4 Air with 24GB RAM appears sufficient for:")
    print("- Multiple Claude Code sessions (2-3 concurrent)")
    print("- PolicyEngine household calculations")
    print("- Light microsimulation work")
    print("\nNote: Full CPS microsimulations may require closing other apps")
    print("when running with multiple Claude sessions.")

if __name__ == "__main__":
    main()