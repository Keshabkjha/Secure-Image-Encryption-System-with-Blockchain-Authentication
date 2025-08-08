# Cleanup script for Secure Image Encryption System

# Remove Python cache files and bytecode
Write-Host "Removing Python cache files..."
Get-ChildItem -Path . -Include __pycache__,*.pyc,*.pyo,*.pyd -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Include *.pyc,*.pyo,*.pyd -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

# Remove Node.js cache and build artifacts
Write-Host "Removing Node.js cache and build artifacts..."
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
}
if (Test-Path ".next") {
    Remove-Item -Recurse -Force .next -ErrorAction SilentlyContinue
}
if (Test-Path ".nuxt") {
    Remove-Item -Recurse -Force .nuxt -ErrorAction SilentlyContinue
}

# Remove virtual environments
Write-Host "Removing virtual environments..."
if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv -ErrorAction SilentlyContinue
}
if (Test-Path ".venv") {
    Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue
}

# Remove IDE specific files
Write-Host "Removing IDE specific files..."
if (Test-Path ".idea") {
    Remove-Item -Recurse -Force .idea -ErrorAction SilentlyContinue
}
if (Test-Path ".vscode") {
    # Keep .vscode directory but clean up launch configurations
    Get-ChildItem -Path .vscode -Include *.code-workspace,launch.json,settings.json -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue
}

# Remove build and distribution directories
Write-Host "Removing build and distribution directories..."
Remove-Item -Recurse -Force build, dist, *.egg-info -ErrorAction SilentlyContinue

# Remove temporary files
Write-Host "Removing temporary files..."
Remove-Item -Force *.log, *.tmp, *.bak -ErrorAction SilentlyContinue

# Clean up Docker
Write-Host "Cleaning up Docker..."
if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker-compose down -v --remove-orphans
    docker system prune -f
}

Write-Host "Cleanup complete!"
Write-Host "Next steps:"
Write-Host "1. Run 'npm install' to reinstall Node.js dependencies"
Write-Host "2. Create a new virtual environment and install Python dependencies"
Write-Host "3. Run 'docker-compose up --build' to rebuild containers"
