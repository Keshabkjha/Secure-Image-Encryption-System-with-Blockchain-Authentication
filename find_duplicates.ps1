# Script to find and analyze duplicate content in the project

# Function to calculate file hash
function Get-FileHashString {
    param([string]$filePath)
    $hash = Get-FileHash -Path $filePath -Algorithm MD5
    return $hash.Hash
}

# Function to get file content without whitespace
function Get-FileContentWithoutWhitespace {
    param([string]$filePath)
    try {
        $content = Get-Content -Path $filePath -Raw -ErrorAction Stop
        # Remove all whitespace and convert to lowercase for better comparison
        return ($content -replace '\s', '').ToLower()
    }
    catch {
        Write-Warning "Could not read file: $filePath"
        return $null
    }
}

# Function to check if file is text-based
function Test-IsTextFile {
    param([string]$filePath)
    $textExtensions = @('.md', '.txt', '.py', '.js', '.json', '.yaml', '.yml', '.toml', '.ps1', '.sh', '.html', '.css', '.scss', '.ts', '.tsx', '.jsx', '.vue')
    $extension = [System.IO.Path]::GetExtension($filePath).ToLower()
    return $textExtensions -contains $extension
}

# Get all text files in the project
try {
    $files = Get-ChildItem -Path . -Recurse -File | 
             Where-Object { Test-IsTextFile $_.FullName -and $_.FullName -notmatch '\\node_modules\\|\\venv\\|\\.git\\' } |
             Select-Object FullName, Length, LastWriteTime

    Write-Host "Found $($files.Count) text files to analyze..."

    # Group files by size first (quick check)
    $sizeGroups = $files | Group-Object Length | Where-Object { $_.Count -gt 1 }
    
    $potentialDuplicates = @()
    $processedHashes = @{}
    $duplicateGroups = @()

    foreach ($group in $sizeGroups) {
        $fileGroup = $group.Group
        
        foreach ($file in $fileGroup) {
            $filePath = $file.FullName
            
            # Skip already processed files
            if ($processedHashes.ContainsKey($filePath)) { continue }
            
            $fileContent = Get-FileContentWithoutWhitespace $filePath
            if (-not $fileContent) { continue }
            
            $fileHash = $processedHashes[$filePath] = (Get-FileHashString $filePath)
            
            # Find other files with the same content
            $duplicates = @()
            foreach ($otherFile in $fileGroup | Where-Object { $_.FullName -ne $filePath }) {
                $otherPath = $otherFile.FullName
                if ($processedHashes.ContainsKey($otherPath)) { continue }
                
                $otherContent = Get-FileContentWithoutWhitespace $otherPath
                if ($otherContent -eq $fileContent) {
                    $duplicates += $otherPath
                    $processedHashes[$otherPath] = $fileHash
                }
            }
            
            if ($duplicates.Count -gt 0) {
                $allDups = @($filePath) + $duplicates
                $duplicateGroups += [PSCustomObject]@{
                    Hash = $fileHash
                    Size = $file.Length
                    Files = $allDups
                }
            }
        }
    }

    # Generate report
    if ($duplicateGroups.Count -gt 0) {
        $reportPath = "./duplicate_files_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
        $report = @()
        
        $report += "# Duplicate Files Report"
        $report += "Generated: $(Get-Date)"
        $report += "=" * 80
        
        $totalSpace = 0
        $groupNum = 1
        
        foreach ($group in $duplicateGroups) {
            $report += "`n[Group $groupNum] (Hash: $($group.Hash), Size: $($group.Size) bytes)"
            $report += "-" * 80
            
            $group.Files | ForEach-Object {
                $report += "- $_"
            }
            
            $spaceSaved = $group.Size * ($group.Files.Count - 1)
            $totalSpace += $spaceSaved
            $report += "Potential space saved: $spaceSaved bytes"
            
            $groupNum++
        }
        
        $report += "`nTotal potential space saved: $totalSpace bytes ($([math]::Round($totalSpace/1KB, 2)) KB)"
        
        # Write report to file
        $report | Out-File -FilePath $reportPath -Encoding utf8
        Write-Host "Duplicate files report generated: $reportPath"
        
        # Show summary
        Write-Host "`nFound $($duplicateGroups.Count) groups of duplicate files"
        Write-Host "Total potential space savings: $totalSpace bytes ($([math]::Round($totalSpace/1KB, 2)) KB)"
    }
    else {
        Write-Host "No duplicate files found."
    }
}
catch {
    Write-Error "An error occurred: $_"
    Write-Error $_.ScriptStackTrace
}

# Check for similar content in README files
Write-Host "`nChecking for similar content in documentation files..."
$readmeFiles = Get-ChildItem -Path . -Recurse -Include "README*.md", "*.md" -File | 
               Where-Object { $_.FullName -notmatch '\\node_modules\\|\\venv\\|\\.git\\' }

$readmeContent = @{}
foreach ($file in $readmeFiles) {
    try {
        $content = (Get-Content -Path $file.FullName -Raw -ErrorAction Stop) -replace '\s', ''
        $readmeContent[$file.FullName] = $content
    }
    catch {
        Write-Warning "Could not read file: $($file.FullName)"
    }
}

# Find similar content
$similarGroups = @()
$processedFiles = @()

foreach ($file1 in $readmeFiles) {
    if ($processedFiles -contains $file1.FullName) { continue }
    
    $group = @($file1.FullName)
    $content1 = $readmeContent[$file1.FullName]
    
    foreach ($file2 in $readmeFiles) {
        if ($file1.FullName -eq $file2.FullName) { continue }
        if ($processedFiles -contains $file2.FullName) { continue }
        
        $content2 = $readmeContent[$file2.FullName]
        $similarity = 0
        
        # Simple similarity check (can be improved with more advanced algorithms)
        if ($content1.Length -gt 0 -and $content2.Length > 0) {
            $shorter = [Math]::Min($content1.Length, $content2.Length)
            $longer = [Math]::Max($content1.Length, $content2.Length)
            $common = 0
            
            for ($i = 0; $i -lt $shorter; $i++) {
                if ($content1[$i] -eq $content2[$i]) { $common++ }
            }
            
            $similarity = $common / $longer
        }
        
        if ($similarity > 0.8) {  # 80% similarity threshold
            $group += $file2.FullName
            $processedFiles += $file2.FullName
        }
    }
    
    if ($group.Count -gt 1) {
        $similarGroups += $group
        $processedFiles += $file1.FullName
    }
}

# Report similar files
if ($similarGroups.Count -gt 0) {
    Write-Host "`nFound $($similarGroups.Count) groups of similar documentation files:"
    foreach ($group in $similarGroups) {
        Write-Host "`nSimilar files (${$group.Count}):"
        $group | ForEach-Object { Write-Host "- $_" }
    }
}
else {
    Write-Host "No similar documentation files found."
}
