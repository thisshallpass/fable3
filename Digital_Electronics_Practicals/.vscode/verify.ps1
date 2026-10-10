# Compiles one sketch (pass its path) or all sketches in code\ for Arduino UNO.
# arduino-cli needs each sketch in a folder of the same name, so a copy is built in TEMP.
param([string]$Sketch)

$cli = (Get-Command arduino-cli -ErrorAction SilentlyContinue).Source
if (-not $cli) { $cli = "C:\Program Files\Arduino CLI\arduino-cli.exe" }

$root = Split-Path $PSScriptRoot -Parent
if ($Sketch) { $files = @(Get-Item -LiteralPath $Sketch) } else { $files = Get-ChildItem "$root\code\*.ino" }

$failed = 0
foreach ($f in $files) {
    if ($f.Extension -ne ".ino") { Write-Host "Not an Arduino sketch: $($f.Name)"; exit 1 }
    $dir = Join-Path $env:TEMP "arduino-verify\$($f.BaseName)"
    New-Item -ItemType Directory -Force $dir | Out-Null
    Copy-Item -LiteralPath $f.FullName "$dir\$($f.Name)" -Force
    $out = & $cli compile --fqbn arduino:avr:uno --warnings all $dir 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "OK    $($f.Name)  $(($out | Select-String 'Sketch uses') -replace ' of program.*', '')"
    } else {
        $failed++
        Write-Host "FAIL  $($f.Name)"
        $out | ForEach-Object { Write-Host "      $_" }
    }
}
Write-Host "$($files.Count - $failed) of $($files.Count) compiled"
exit $failed
