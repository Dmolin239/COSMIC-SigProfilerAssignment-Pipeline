# COSMIC-SigProfilerAssignment-Pipeline
An automated, interactive Python pipeline for extracting COSMIC mutational signatures from VCF files.

A streamlined, interactive Python wrapper for the [SigProfiler](https://github.com/AlexandrovLab) suite. This script automates the extraction of Single Base Substitution (SBS), Double Base Substitution (DBS), and small Insertion/Deletion (InDel) COSMIC mutational signatures directly from somatic VCF files.

## Features
* **Interactive CLI:** Prompts the user for input/output directories, reference genomes, and WES/WGS sequencing types.
* **Smart Genome Management:** Automatically checks for and installs the required reference genome (e.g., GRCh38) if it is missing.
* **High Efficiency:** Decouples matrix generation from signature fitting. Matrices are generated exactly *once* per sample, drastically reducing I/O overhead.
* **Dynamic Handling:** Automatically adjusts file extensions and parameters based on whether the data is Whole Exome (WES) or Whole Genome (WGS).
* **Silent Mode & Clean Logging:** Suppresses the massive console output from SigProfiler tools, redirecting it to sample-specific `.log` files to keep your terminal clean while preserving troubleshooting data.
* **Automated Housekeeping:** Cleans up temporary VCF copies and intermediate matrix folders to save disk space after each sample finishes.

## 🛠️ Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
