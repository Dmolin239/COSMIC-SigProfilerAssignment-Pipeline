# SigProfilerAssignment Script
# Created by: David Moline (UMN Dept. of Medicine)
# Disclosure: Created with assistance from Google Gemini provided by UMN
# Last updated 3/26/2025

# Import required libraries
import os
import sys
import shutil
import traceback
from contextlib import redirect_stdout, redirect_stderr

# Check for SigProfiler dependencies before proceeding
try:
    import SigProfilerMatrixGenerator as spmg
    from SigProfilerMatrixGenerator import install as genInstall
    from SigProfilerMatrixGenerator.scripts import SigProfilerMatrixGeneratorFunc as matGen
    from SigProfilerAssignment import Analyzer as Analyze
except ImportError as e:
    print(f"\n[-] Missing dependency: {e.name}")
    print("[!] Please install the required packages before running this script.")
    print("[!] Run: pip install SigProfilerAssignment SigProfilerMatrixGenerator\n")
    sys.exit(1)

def check_and_install_genome(genome_build):
    """
    Uses SigProfiler's built-in installer to check for the reference genome.
    It automatically skips the download if the genome is already present.
    """
    print(f"\n[*] Checking status of reference genome '{genome_build}'...")
    # The install function safely bypasses the download if already installed
    genInstall.install(genome_build)

def get_user_inputs():
    """
    Prompts the user for the necessary input paths and parameters.
    """
    print("\n" + "="*50)
    print("   SigProfilerAssignment COSMIC Signature Caller")
    print("="*50)

    # Prompt for Input Directory
    while True:
        input_dir = input("\nEnter the path to your VCF input directory:\n> ").strip()
        if os.path.isdir(input_dir):
            break
        print("[-] Error: Directory does not exist. Please check the path and try again.")

    # Prompt for Output Directory
    base_output_dir = input("\nEnter the path for your desired output directory:\n> ").strip()

    # Prompt for Genome Build
    genome_build = input("\nEnter the reference genome build (e.g., GRCh37, GRCh38) [Default: GRCh38]:\n> ").strip()
    if not genome_build:
        genome_build = "GRCh38"

    # Prompt for Sequencing Type (WES vs WGS)
    while True:
        seq_type = input("\nIs your data Whole Exome (WES) or Whole Genome (WGS)? [Default: WES]:\n> ").strip().upper()
        if not seq_type or seq_type == "WES":
            is_exome = True
            break
        elif seq_type == "WGS":
            is_exome = False
            break
        print("[-] Error: Please enter 'WES' or 'WGS'.")

    # Verify and install the genome
    check_and_install_genome(genome_build)

    # Set standard COSMIC version
    cosmic_version = 3.4 

    return input_dir, base_output_dir, genome_build, cosmic_version, is_exome

def main():
    # Gather user inputs
    input_dir, base_output_dir, user_genome_build, user_cosmic_version, is_exome = get_user_inputs()
    os.makedirs(base_output_dir, exist_ok=True)

    print(f"\n[*] Initializing setup for {'Whole Exome' if is_exome else 'Whole Genome'} sequencing data...")

    # Set dynamic file extensions based on sequencing type
    matrix_ext = "exome" if is_exome else "all"

    # Define mutation contexts and expected file paths
    mutation_types = {
        "SBS": {"context_type": "96", "collapse_to_SBS96": True, "suffix": f"SBS96.{matrix_ext}", "folder": "SBS"},
        "DBS": {"context_type": "DINUC", "collapse_to_SBS96": False, "suffix": f"DBS78.{matrix_ext}", "folder": "DBS"},
        "InDel": {"context_type": "ID", "collapse_to_SBS96": False, "suffix": f"ID83.{matrix_ext}", "folder": "ID"},
    }

    # Track processing status
    successful_samples = []
    failed_samples = {}

    # Iterate through all VCF files in the input directory
    for filename in os.listdir(input_dir):
        if not (filename.endswith(".vcf") or filename.endswith(".vcf.gz")):
            continue

        # Define sample-specific paths
        sample_name = filename.split(".vcf")[0] 
        sample_path = os.path.join(input_dir, filename)
        sample_output_dir = os.path.join(base_output_dir, sample_name)
        os.makedirs(sample_output_dir, exist_ok=True)

        print(f"\n{'-'*50}")
        print(f"=== Processing sample: {sample_name} ===")

        # Setup temporary input directory for SigProfiler
        sample_input_dir = os.path.join(sample_output_dir, "temp_input")
        os.makedirs(sample_input_dir, exist_ok=True)
        log_file_path = os.path.join(sample_output_dir, f"{sample_name}.log")

        try:
            # Stage VCF in the temporary folder
            temp_vcf_path = os.path.join(sample_input_dir, filename)
            shutil.copy2(sample_path, temp_vcf_path)

            # Open sample-specific log file
            with open(log_file_path, 'w') as log_file:
                print("--> Generating Mutational Matrices (Once per sample)...")
                log_file.write(f"Generating matrices for {sample_name}...\n")
                
                # Generate mutational matrices
                with redirect_stdout(log_file), redirect_stderr(log_file):
                    matGen.SigProfilerMatrixGeneratorFunc(
                        project=sample_name, 
                        reference_genome=user_genome_build, 
                        path_to_input_files=sample_input_dir, 
                        exome=is_exome,
                        plot=False
                    )

                # Process each mutation type (SBS, DBS, InDel)
                for mutation, params in mutation_types.items():
                    matrix_file = os.path.join(sample_input_dir, "output", params["folder"], f"{sample_name}.{params['suffix']}")
                    mutation_output_dir = os.path.join(sample_output_dir, f"{mutation}_results")
                    
                    # Skip analysis if no mutations of this type were found
                    if not os.path.exists(matrix_file):
                        print(f"--> Skipping {mutation}: No mutations of this context found in VCF.")
                        log_file.write(f"\nSkipped {mutation}: No {params['folder']} matrix generated.\n")
                        continue

                    os.makedirs(mutation_output_dir, exist_ok=True)
                    print(f"--> Running {mutation} signature analysis...")
                    
                    log_file.write(f"\n{'='*40}\nStarting {mutation} Analysis\n{'='*40}\n")
                    log_file.flush()

                    # Run COSMIC signature extraction
                    Analyze.cosmic_fit(
						samples=matrix_file,
						output=mutation_output_dir,
						input_type="matrix",
						context_type=params["context_type"],
						cosmic_version=user_cosmic_version,
						exome=is_exome,
						genome_build=user_genome_build,
						exclude_signature_subgroups=None,
						collapse_to_SBS96=params["collapse_to_SBS96"],
						make_plots=True,
					)

            print(f"[+] Completed successfully: {sample_name}")
            successful_samples.append(sample_name)

        except Exception as e:
            # Handle errors and log traceback
            print(f"[-] Error processing {sample_name}. Check log for details.")
            with open(log_file_path, 'a') as log_file:
                log_file.write("\n\n=== SCRIPT CRASHED WITH ERROR ===\n")
                traceback.print_exc(file=log_file)
            failed_samples[sample_name] = str(e)
            
        finally:
            # Clean up temporary VCF and matrix folders
            if os.path.exists(sample_input_dir):
                shutil.rmtree(sample_input_dir)

    # Print final execution summary
    print(f"\n{'='*50}")
    print("=== Processing Summary ===")
    if successful_samples:
        print(f"Successful samples ({len(successful_samples)}): {', '.join(successful_samples)}")

    if failed_samples:
        print(f"Failed samples ({len(failed_samples)}):")
        for s, err in failed_samples.items():
            print(f"   - {s}: {err}")
    else:
        print("All samples processed successfully with no errors.")

# Execute main function if run as a standalone script
if __name__ == "__main__":
	main()
	
	
	
