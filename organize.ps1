# organize.ps1
$ProjectDir = "E:\Spark-1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Функція для переміщення з логуванням
function Move-And-Log($pattern, $destination) {
    $files = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        Move-Item $file.FullName $destination -ErrorAction SilentlyContinue
        Write-Host "➡️ $($file.Name) → $destination"
    }
}

# Створення папок
$folders = "agents","config","core","data","edge_tts-master","ffmpeg-8.0","finance","interfaces","logs","ml","storage","tests"
foreach ($f in $folders) {
    New-Item -ItemType Directory -Force -Path "$ProjectDir\$f" | Out-Null
}

# Переміщення файлів з логуванням
# Agents
Move-And-Log "$ProjectDir\agent_*.py" "$ProjectDir\agents"
Move-And-Log "$ProjectDir\ai_delegate.py" "$ProjectDir\agents"
Move-And-Log "$ProjectDir\run_once.py" "$ProjectDir\agents"
Move-And-Log "$ProjectDir\self_upgrade.py" "$ProjectDir\agents"

# Config
Move-And-Log "$ProjectDir\*.cfg" "$ProjectDir\config"
Move-And-Log "$ProjectDir\*.ini" "$ProjectDir\config"
Move-And-Log "$ProjectDir\*.yml" "$ProjectDir\config"
Move-And-Log "$ProjectDir\LICENSE" "$ProjectDir\config"
Move-And-Log "$ProjectDir\.gitignore" "$ProjectDir\config"
Move-And-Log "$ProjectDir\py.typed" "$ProjectDir\config"

# Core
Move-And-Log "$ProjectDir\__main__.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\constants.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\exceptions.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\version.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\util.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\typing.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\memory.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\communicate.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\drm.py" "$ProjectDir\core"
Move-And-Log "$ProjectDir\mobile_mode.py" "$ProjectDir\core"

# Data
Move-And-Log "$ProjectDir\*.json" "$ProjectDir\data"
Move-And-Log "$ProjectDir\*.txt" "$ProjectDir\data"

# Edge TTS
Move-And-Log "$ProjectDir\voice_engine*.py" "$ProjectDir\edge_tts-master"
Move-And-Log "$ProjectDir\voices.py" "$ProjectDir\edge_tts-master"
Move-And-Log "$ProjectDir\win32_playback.py" "$ProjectDir\edge_tts-master"
Move-And-Log "$ProjectDir\srt_composer.py" "$ProjectDir\edge_tts-master"
Move-And-Log "$ProjectDir\submaker.py" "$ProjectDir\edge_tts-master"

# Finance
Move-And-Log "$ProjectDir\binance*.py" "$ProjectDir\finance"
Move-And-Log "$ProjectDir\risk_manager.py" "$ProjectDir\finance"
Move-And-Log "$ProjectDir\cloud_*.py" "$ProjectDir\finance"

# Interfaces
Move-And-Log "$ProjectDir\telegram*.py" "$ProjectDir\interfaces"
Move-And-Log "$ProjectDir\server.js" "$ProjectDir\interfaces"

# Logs
Move-And-Log "$ProjectDir\log_manager.py" "$ProjectDir\logs"
Move-And-Log "$ProjectDir\*.mp3" "$ProjectDir\logs"

# ML
Move-And-Log "$ProjectDir\ml_*.py" "$ProjectDir\ml"
Move-And-Log "$ProjectDir\*_core.py" "$ProjectDir\ml"
Move-And-Log "$ProjectDir\data_classes.py" "$ProjectDir\ml"

# Storage
Move-And-Log "$ProjectDir\*.sh" "$ProjectDir\storage"
Move-And-Log "$ProjectDir\*.doc" "$ProjectDir\storage"

# Tests
Move-And-Log "$ProjectDir\test_*.py" "$ProjectDir\tests"

Write-Host "✅ Files have been organized into folders!"

