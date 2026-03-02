Param(
    [string]$AppName = "BPMN-to-Visio",
    [string]$EntryScript = "bpmn_to_visio_gui.py",
    [string]$Arch = "",
    [switch]$NoZip
)

$ErrorActionPreference = "Stop"

if (-not $IsWindows) {
    throw "This script must be run on Windows."
}

if (-not (Test-Path $EntryScript)) {
    throw "Entry script not found: $EntryScript"
}

if (-not $Arch) {
    if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") {
        $Arch = "win-arm64"
    }
    else {
        $Arch = "win-x64"
    }
}

Write-Host "Installing/upgrading PyInstaller..."
py -m pip install --upgrade pyinstaller

Write-Host "Building executable..."
py -m PyInstaller --noconfirm --clean --onefile --windowed --name $AppName $EntryScript

$distExe = Join-Path "dist" "$AppName.exe"
if (-not (Test-Path $distExe)) {
    throw "Build failed: executable not found at $distExe"
}

if (-not $NoZip) {
    $zipName = "$AppName-$Arch.zip"
    $zipPath = Join-Path "dist" $zipName
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }
    Compress-Archive -Path $distExe -DestinationPath $zipPath
    Write-Host "Done: $zipPath"
}
else {
    Write-Host "Done: $distExe"
}