# Cleanup Duplicates Script
# This script helps identify and clean up duplicate and unnecessary files

# Function to safely remove directories
function Remove-DirectoryIfExists {
    param([string]$path)
    if (Test-Path $path) {
        $size = (Get-ChildItem -Path $path -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "Removing: $path (Size: $([math]::Round($size, 2)) MB)"
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Function to get directory size
function Get-DirectorySize {
    param([string]$path)
    if (Test-Path $path) {
        $size = (Get-ChildItem -Path $path -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
        return [math]::Round($size, 2)
    }
    return 0
}

# 1. Check for duplicate backend directories
$backendDirs = @("backend", "Backend") | Where-Object { Test-Path $_ }
if ($backendDirs.Count -gt 1) {
    Write-Host "Found multiple backend directories:"
    $backendDirs | ForEach-Object { 
        $size = Get-DirectorySize $_
        Write-Host "- $_ (Size: ${size}MB)" 
    }
    
    # Keep the one with latest modification time
    $latestBackend = $backendDirs | Sort-Object { (Get-Item $_).LastWriteTime } -Descending | Select-Object -First 1
    Write-Host "`nKeeping the most recent directory: $latestBackend"
    
    # Remove others
    $backendDirs | Where-Object { $_ -ne $latestBackend } | ForEach-Object {
        Write-Host "Removing duplicate: $_"
        Remove-DirectoryIfExists $_
    }
}

# 2. Check for Python source directories
$pythonDirs = @("python", "secure_image_encryption") | Where-Object { Test-Path $_ }
if ($pythonDirs.Count -gt 1) {
    Write-Host "`nFound multiple Python source directories:"
    $pythonDirs | ForEach-Object { 
        $size = Get-DirectorySize $_
        Write-Host "- $_ (Size: ${size}MB)" 
    }
    
    # Keep secure_image_encryption as it's the standard Python package name
    $pythonDirToKeep = "secure_image_encryption"
    Write-Host "`nKeeping the standard Python package directory: $pythonDirToKeep"
    
    # Remove others
    $pythonDirs | Where-Object { $_ -ne $pythonDirToKeep } | ForEach-Object {
        Write-Host "Removing duplicate: $_"
        Remove-DirectoryIfExists $_
    }
}

# 3. Clean up development artifacts
Write-Host "`nCleaning up development artifacts..."
$artifactsToRemove = @(
    "node_modules",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".coverage",
    "htmlcov"
)

$artifactsToRemove | ForEach-Object {
    if (Test-Path $_) {
        $size = Get-DirectorySize $_
        if ($size -gt 0) {
            Write-Host "Removing: $_ (Size: ${size}MB)"
            Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

# 4. Clean up duplicate files
$filesToCheck = @(
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "Makefile",
    "package.json",
    "server.js"
)

Write-Host "`nChecking for duplicate files..."
$filesToCheck | ForEach-Object {
    $file = $_
    $duplicates = Get-ChildItem -Path . -Filter $file -Recurse -File | Where-Object { $_.FullName -notlike "*\node_modules\*" }
    if ($duplicates.Count -gt 1) {
        Write-Host "`nFound multiple copies of $file :"
        $duplicates | ForEach-Object { 
            $size = [math]::Round(($_.Length / 1KB), 2)
            Write-Host "- $($_.FullName) (Size: ${size}KB)" 
        }
        
        # Keep the one in the root directory
        $fileToKeep = $duplicates | Where-Object { $_.DirectoryName -eq (Get-Item .).FullName } | Select-Object -First 1
        if (-not $fileToKeep) {
            $fileToKeep = $duplicates | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        }
        
        Write-Host "Keeping: $($fileToKeep.FullName)"
        
        # Remove others
        $duplicates | Where-Object { $_.FullName -ne $fileToKeep.FullName } | ForEach-Object {
            Write-Host "Removing duplicate: $($_.FullName)"
            Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
        }
    }
}

Write-Host "`nCleanup complete!"
Write-Host "---------------"
Write-Host "Next steps:"
Write-Host "1. Review the changes made"
Write-Host "2. Run 'npm install' to reinstall Node.js dependencies"
Write-Host "3. Create a new Python virtual environment"
Write-Host "4. Install Python dependencies: 'pip install -e .[dev]'"
Write-Host "5. Start the development environment: 'docker-compose up --build'"
