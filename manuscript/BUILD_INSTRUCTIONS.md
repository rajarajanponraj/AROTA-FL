# Build and Reproduction Instructions

This document provides exact, reproducible commands to compile the IEEE manuscript and re-run all underlying physical-layer and federated learning simulations.

---

## 1. System Requirements

### LaTeX Toolchain
- **Distribution:** MiKTeX (24.x+) or TeX Live (2023+)
- **Engines:** `pdflatex`, `bibtex`
- **Required Packages:** `IEEEtran`, `amsmath`, `amssymb`, `amsfonts`, `graphicx`, `booktabs`, `cite`, `subcaption`, `epstopdf`

### Python Environment
- **Python:** 3.10+
- **Core Dependencies:**
  ```bash
  pip install numpy scipy matplotlib torch torchvision pytest pymupdf
  ```
- **Local Package Installation:**
  ```bash
  pip install -e .
  ```

---

## 2. Manuscript Compilation

To build the five-page publication PDF from source, execute the following commands in PowerShell from the repository root:

```powershell
cd "c:\Users\raja\Documents\HICET\Literature review\AROTA-FL\manuscript"

# 1. First compilation pass
& "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode -halt-on-error --disable-installer main.tex

# 2. Compile bibliography with BibTeX
& "C:\Program Files\MiKTeX\miktex\bin\x64\bibtex.exe" main

# 3. Second compilation pass (resolve citations)
& "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode -halt-on-error --disable-installer main.tex

# 4. Third compilation pass (resolve cross-references and page bounds)
& "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode -halt-on-error --disable-installer main.tex

# 5. Copy to official deliverable name
cp main.pdf manuscript.pdf
```

### Verification of Page Count
To verify that the output renders to **exactly 5 pages**:
```powershell
python -c "import fitz; doc=fitz.open('manuscript.pdf'); print(f'Rendered Page Count: {len(doc)} pages')"
```
Expected output:
```
Rendered Page Count: 5 pages
```

---

## 3. Test Suite Execution

All core mathematical functions, Zero-Forcing calculations, and objective estimators are covered by unit tests in `tests/`:

```powershell
cd "c:\Users\raja\Documents\HICET\Literature review\AROTA-FL"
pytest tests/ -v
```
Expected output: `23 passed in ~17.6s`.

---

## 4. Experiment Reproduction

All experiments can be reproduced from source using the scripts in `experiments/` and `src/arota_fl/experiments/`:

### Physical-Layer Sweeps (Figures 2a, 2b, 2c)
1. **Experiment 1 (Amplification Sweep vs. MSE):**
   ```powershell
   python experiments/exp1_amplification_gain_sweep.py --seeds 500 --output output/exp1_results.csv
   ```
2. **Experiment 2 & 3 (SNR Sweep & Gain Adaptation):**
   ```powershell
   python experiments/exp2_snr_sweep.py --output output/exp2_results.csv
   python experiments/exp3_optimal_amplification_vs_snr.py --output output/exp3_results.csv
   ```
3. **Experiment 4 (CSI Error Sweep):**
   ```powershell
   python experiments/exp4_csi_error_sweep.py --seeds 500 --output output/exp4_results.csv
   ```
4. **Experiment 5 & 6 (RIS Array Size & Client Count Sweeps):**
   ```powershell
   python experiments/exp5_ris_elements_sweep.py --output output/exp5_results.csv
   python experiments/exp6_num_clients_sweep.py --output output/exp6_results.csv
   ```

### PyTorch Federated Learning Convergence (Figure 3)
1. **Experiments 7, 8, & 9 (MNIST & CIFAR-10 FL Benchmarks):**
   ```powershell
   python experiments/exp7_fl_mnist_convergence.py --rounds 60 --clients 20 --alpha 0.5
   python experiments/exp8_fl_cifar10_convergence.py --rounds 100 --clients 20 --alpha 0.5
   python experiments/exp9_fl_non_iid_degree.py
   ```

### Figure Regeneration
To regenerate the vectorized EPS and PNG figures used in the manuscript:
```powershell
python -m arota_fl.visualization.plot_results --input-dir output/ --output-dir manuscript/figures/
```

---

## 5. File Manifest

- `manuscript/main.tex`: Master LaTeX document.
- `manuscript/references.bib`: Verified IEEE bibliography database with 21 reference entries.
- `manuscript/manuscript.pdf`: Compiled camera-ready IEEE paper (5 pages).
- `manuscript/tables/sim_parameters.tex`: Simulation configuration table source.
- `manuscript/figures/`: Vector `.eps` and `.png` figures.
- `manuscript/PROJECT_AUDIT.md`: Project catalog and file status.
- `manuscript/EVIDENCE_REGISTER.md`: Scientific claim and experiment linkage.
- `manuscript/CLAIM_TRACEABILITY.md`: Traceability audit table.
- `manuscript/EQUATION_REGISTER.md`: Mathematical ledger and derivation register.
- `manuscript/EXPERIMENT_REPRODUCIBILITY.md`: Experiment execution guide.
- `manuscript/FINAL_VALIDATION_REPORT.md`: Comprehensive audit report.
- `manuscript/BUILD_INSTRUCTIONS.md`: This file.
