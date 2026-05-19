$ErrorActionPreference = "Stop"
$Source = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:LOCALAPPDATA "Glagol"

Write-Host "[Glagol 0.3] Installing to $InstallDir"

if (Test-Path $InstallDir) {
    Remove-Item $InstallDir -Recurse -Force
}
New-Item -ItemType Directory -Force $InstallDir | Out-Null

$items = @("glagol.py", "glagol.cmd", "glagol.exe", "uninstall.cmd", "uninstall.ps1", "template_new.гл", "README.txt")
foreach ($item in $items) {
    $src = Join-Path $Source $item
    if (Test-Path $src) {
        Copy-Item $src $InstallDir -Force
    }
}

$examplesSrc = Join-Path $Source "examples"
$examplesDst = Join-Path $InstallDir "examples"
if (Test-Path $examplesSrc) {
    Copy-Item $examplesSrc $examplesDst -Recurse -Force
}

# Add to user PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
$parts = $userPath -split ";" | Where-Object { $_ -and $_.Trim() }
if (-not ($parts | Where-Object { $_.Trim().ToLower() -eq $InstallDir.ToLower() })) {
    $newPath = ($parts + $InstallDir) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[Glagol 0.3] PATH updated."
} else {
    Write-Host "[Glagol 0.3] PATH already contains Glagol."
}

# Add .гл to PATHEXT for user
$userExt = [Environment]::GetEnvironmentVariable("PATHEXT", "User")
if (-not $userExt) { $userExt = "" }
$extParts = $userExt -split ";" | Where-Object { $_ -and $_.Trim() }
if (-not ($extParts | Where-Object { $_.Trim().ToLower() -eq ".гл" })) {
    [Environment]::SetEnvironmentVariable("PATHEXT", (($extParts + ".гл") -join ";"), "User")
}

# File association
$extKey = "HKCU:\Software\Classes\.гл"
$classKey = "HKCU:\Software\Classes\GlagolFile"
$cmdPath = Join-Path $InstallDir "glagol.cmd"
$templatePath = Join-Path $InstallDir "template_new.гл"

New-Item -Path $extKey -Force | Out-Null
Set-ItemProperty -Path $extKey -Name "(default)" -Value "GlagolFile"

New-Item -Path $classKey -Force | Out-Null
Set-ItemProperty -Path $classKey -Name "(default)" -Value "Glagol source file"

New-Item -Path "$classKey\shell\open\command" -Force | Out-Null
Set-ItemProperty -Path "$classKey\shell\open\command" -Name "(default)" -Value "`"$cmdPath`" `"%1`" %*"

New-Item -Path "$extKey\ShellNew" -Force | Out-Null
if (Test-Path $templatePath) {
    New-ItemProperty -Path "$extKey\ShellNew" -Name "FileName" -Value $templatePath -PropertyType String -Force | Out-Null
} else {
    New-ItemProperty -Path "$extKey\ShellNew" -Name "NullFile" -Value "" -PropertyType String -Force | Out-Null
}

Write-Host ""
Write-Host "[Glagol 0.3] Installed."
Write-Host "Close and reopen cmd, then test:"
Write-Host "  glagol версия"
Write-Host "  glagol `"%LOCALAPPDATA%\Glagol\examples\hello.гл`""
Write-Host ""
Write-Host "Explorer New menu item may appear after Explorer restart or PC reboot."
