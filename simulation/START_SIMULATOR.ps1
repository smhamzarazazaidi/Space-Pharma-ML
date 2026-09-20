# Run from any directory; bind only to localhost. Models/data are built separately.
$simulatorRoot = $PSScriptRoot
$simulatorPython = 'C:\Users\SRT\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (!(Test-Path -LiteralPath $simulatorPython)) { $simulatorPython = 'python' }
& $simulatorPython (Join-Path $simulatorRoot 'src/serve_phase_d.py') --port 8765
