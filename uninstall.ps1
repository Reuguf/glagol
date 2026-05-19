$ErrorActionPreference = "SilentlyContinue"
$InstallDir = Join-Path $env:LOCALAPPDATA "Glagol"

Write-Host "[Glagol 0.3] Uninstalling..."

if (Test-Path $InstallDir) {
    Remove-Item $InstallDir -Recurse -Force
}

foreach ($scope in @("User","Machine")) {
    $p = [Environment]::GetEnvironmentVariable("Path", $scope)
    if ($p) {
        $parts = $p -split ";" | Where-Object { $_ -and ($_.Trim().ToLower() -ne $InstallDir.ToLower()) }
        [Environment]::SetEnvironmentVariable("Path", ($parts -join ";"), $scope)
    }
}

$pathext = [Environment]::GetEnvironmentVariable("PATHEXT", "User")
if ($pathext) {
    $parts = $pathext -split ";" | Where-Object { $_ -and ($_.Trim().ToLower() -ne ".гл") }
    [Environment]::SetEnvironmentVariable("PATHEXT", ($parts -join ";"), "User")
}

Remove-Item "HKCU:\Software\Classes\.гл" -Recurse -Force
Remove-Item "HKCU:\Software\Classes\GlagolFile" -Recurse -Force

Write-Host "[Glagol 0.3] Removed. Close and reopen cmd."
