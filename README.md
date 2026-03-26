# COSMIC-SigProfilerAssignment-Pipeline
An automated, interactive Python pipeline for extracting COSMIC mutational signatures from VCF files.

A streamlined, interactive Python wrapper for the [SigProfilerAssignment]([https://github.com/AlexandrovLab](https://github.com/SigProfilerSuite/SigProfilerAssignment)). 

This script uses COSMIC version 3.4. 

It automates the extraction of Single Base Substitution (SBS), Double Base Substitution (DBS), and small Insertion/Deletion (InDel) COSMIC mutational signatures directly from somatic VCF files.

## Features
* **Interactive CLI:** Prompts the user for input/output directories, reference genomes, and WES/WGS sequencing types.
* **Genome Management:** Automatically checks for and installs the required reference genome (e.g., GRCh38) if it is missing.
* **High Efficiency:** Decouples matrix generation from signature fitting. Matrices are generated exactly *once* per sample, drastically reducing I/O overhead.
* **Dynamic Handling:** Automatically adjusts file extensions and parameters based on whether the data is Whole Exome (WES) or Whole Genome (WGS).
* **Silent Mode & Clean Logging:** Suppresses the massive console output from SigProfiler tools, redirecting it to sample-specific `.log` files to keep your terminal clean while preserving troubleshooting data.
* **Automated Housekeeping:** Cleans up temporary VCF copies and intermediate matrix folders to save disk space after each sample finishes.

## 🛠️ Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/Dmolin239/COSMIC-SigProfilerAssignment-Pipeline.git](https://github.com/Dmolin239/COSMIC-SigProfilerAssignment-Pipeline.git)
cd YOUR_REPO_NAME
```

**2. Install dependencies:**
This script requires Python 3 and the SigProfiler suite. It is highly recommended to run this within a Conda environment.
```bash
pip install SigProfilerAssignment SigProfilerMatrixGenerator
```

## Usage

**1. Organization:**
Place all of your uncompressed (.vcf) or compressed (.vcf.gz) somatic mutation files into a single input directory.

**2. Running:**
Run the script from your terminal:

```bash
python3 SigProfilerAssignment_script.py
```

The script will launch an interactive prompt asking for:

* The absolute path to your input directory.
* The absolute path to your desired output directory.
* The reference genome build (Default: GRCh38).
* Your sequencing type (WES or WGS, Default: WES)

**4. Output Structure**
The script generates a master folder for every successfully processed sample in your output directory. Inside each sample's folder, you will find:
```text
Output_Directory/
├── Sample_1/
│   ├── Sample_1.log                     # Hidden console output and error tracebacks
│   ├── SBS_results/                     # Single Base Substitution outputs
│   │   └── Assignment_Solution/
│   │       ├── Activities/
│   │       │   ├── Assignment_Solution_Activities.txt   # Raw signature contributions
│   │       │   └── ..._Plots.pdf                        # Visual bar plots of signature weights
│   │       ├── Signatures/
│   │       │   └── ..._Signatures.txt                   # The specific COSMIC signatures used in the fit
│   │       └── Solution_Stats/
│   │           └── ..._Stats.txt                        # Cosine similarity and reconstruction metrics
│   ├── DBS_results/                     # Double Base Substitution outputs
│   │   └── Assignment_Solution/...      # (Follows the same structure as SBS)
│   └── ID_results/                      # Small Insertion/Deletion outputs
│       └── Assignment_Solution/...      # (Follows the same structure as SBS)
├── Sample_2/
│   └── ...
```

Note: If a specific mutation context (e.g., DBS) is not found in a sample's VCF, the script will safely skip it and that specific results folder will not be generated.

## **⚠️ Troubleshooting**
If a sample fails, check the [Sample_Name].log file located in its output directory. 

The script appends the full Python traceback and matrix generation statistics to this file to help identify the issue without cluttering your main terminal window.


