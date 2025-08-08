# Project Cleanup Script
# This script helps clean up unnecessary files while preserving essential project files

# Function to safely remove directories
function Remove-DirectoryIfExists {
    param([string]$path)
    if (Test-Path $path) {
        Write-Host "Removing: $path"
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Function to safely remove files
function Remove-FileIfExists {
    param([string]$path)
    if (Test-Path $path) {
        Write-Host "Removing: $path"
        Remove-Item -Path $path -Force -ErrorAction SilentlyContinue
    }
}

# 1. Clean Python cache and bytecode
Write-Host "[1/6] Cleaning Python cache and bytecode..."
Get-ChildItem -Path . -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include "*.pyc", "*.pyo", "*.pyd" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

# 2. Clean Node.js artifacts
Write-Host "[2/6] Cleaning Node.js artifacts..."
if (Test-Path "node_modules") {
    # Keep package-lock.json but clean node_modules
    $nodeModulesSize = (Get-ChildItem -Path "node_modules" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  Removing node_modules (Size: $([math]::Round($nodeModulesSize, 2)) MB)"
    Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
}

# 3. Clean build and distribution directories
Write-Host "[3/6] Cleaning build and distribution directories..."
Remove-DirectoryIfExists ".next"
Remove-DirectoryIfExists ".nuxt"
Remove-DirectoryIfExists "build"
Remove-DirectoryIfExists "dist"
Remove-DirectoryIfExists "*.egg-info"

# 4. Clean virtual environments
Write-Host "[4/6] Cleaning virtual environments..."
Remove-DirectoryIfExists "venv"
Remove-DirectoryIfExists ".venv"
Remove-DirectoryIfExists "env"
Remove-DirectoryIfExists ".env"

# 5. Clean IDE and editor files
Write-Host "[5/6] Cleaning IDE and editor files..."
Remove-DirectoryIfExists ".idea"
Remove-DirectoryIfExists ".vscode"
Remove-Item -Path "*.sublime-*" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.swp" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.swo" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*~" -Force -ErrorAction SilentlyContinue

# 6. Clean temporary files
Write-Host "[6/6] Cleaning temporary files..."
Remove-Item -Path "*.log" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.tmp" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.bak" -Force -ErrorAction SilentlyContinue
Remove-DirectoryIfExists ".pytest_cache"
Remove-DirectoryIfExists ".mypy_cache"

# Display cleanup summary
Write-Host "`nCleanup complete!"
Write-Host "---------------"
Write-Host "Next steps:"
Write-Host "1. Run 'npm install' to reinstall Node.js dependencies"
Write-Host "2. Create a new Python virtual environment"
Write-Host "3. Install Python dependencies: 'pip install -e .[dev]'"
Write-Host "4. Start the development environment: 'docker-compose up --build'"
Write-Host "`nNote: This script only removes build artifacts and temporary files."
Write-Host "Your source code and configuration files are preserved."
