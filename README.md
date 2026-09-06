# ROCmForge

An automated codebase porting and runtime GPU performance optimization suite designed natively to accelerate application deployments on the **AMD Developer Cloud** utilizing the **AMD ROCm** framework ecosystem.

## Core Features
- **Automated Migration Engine:** Uses intelligent, isolated engineering agents to parse code repository blocks and systematically translate outdated, vendor-specific CUDA logic into clean, production-ready AMD HIP configurations.
- **GPU Profiling Diagnostics:** Reviews compute workloads to suggest highly actionable configurations covering memory tracking parameters, custom block distribution rules, and safe vRAM allocations.

## Local Installation Sequence

1. Clone the project structure repository to your current developer workstation:
   ```bash
   git clone https://github.com
   cd rocmforge
   ```

2. Establish an isolated Python environment and install the required platform configuration libraries:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure your infrastructure authentication keys inside your environment session variables:
   ```bash
   export AMD_CLOUD_API_BASE="https://together.xyz"
   export AMD_CLOUD_API_KEY="your_api_token_here"
   ```

## Usage Instructions

Execute the pipeline against any localized test script module containing target architectural layouts to observe code modernization adjustments:
```bash
python src/main.py path/to/legacy_gpu_code.py
```
# Another Method of Local Installation Sequence
```
# 1. Give the script permission to run as an executable file
chmod +x setup.sh

# 2. Execute the automated setup script
./setup.sh
````
