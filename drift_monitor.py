import os
import numpy as np
from scipy.stats import ks_2samp

def check_data_drift():
    print("Running Data Drift Check (KS-Test)...")
    np.random.seed(42)
    
    # Mock reference data (training baseline) and current data (production batch)
    reference_data = np.random.normal(loc=0.0, scale=1.0, size=(100, 4))
    current_data = np.random.normal(loc=0.4, scale=1.1, size=(100, 4)) # drifted batch
    
    drift_found = False
    threshold = 0.05
    
    for i in range(reference_data.shape[1]):
        stat, p_value = ks_2samp(reference_data[:, i], current_data[:, i])
        if p_value < threshold:
            print(f"Drift detected in feature {i} (p-value: {p_value:.4f})")
            drift_found = True
        else:
            print(f"Feature {i} stable (p-value: {p_value:.4f})")
            
    # Pass result to GitHub Actions environment via GITHUB_OUTPUT
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"drift_detected={'true' if drift_found else 'false'}\n")
            
    return drift_found

if __name__ == "__main__":
    check_data_drift()