# DOM_010101 — CANONICAL MEMORY INJECTION (PowerShell Edition)
# Add this to your PowerShell profile: . "$env:USERPROFILE\Chaos God DOM_010101\strategic-khaos\scripts\dom-paste.ps1"

function dom-paste {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $chat = Get-Clipboard
    $vaultPath = "$env:USERPROFILE\strategic-khaos-private\council-vault"
    $memoryFile = "$vaultPath\MEMORY_STREAM.md"
    
    # Ensure vault exists
    if (-not (Test-Path $vaultPath)) {
        New-Item -ItemType Directory -Path $vaultPath -Force | Out-Null
        Set-Location $vaultPath
        git init
        "# DOM_010101 — Canonical Memory Stream`n`nAll chats pasted below are immutable law. Deviation = rebellion = excommunication.`n" | Out-File -Encoding utf8 $memoryFile
        git add .
        git commit -m "birth: canonical memory stream — rebellion impossible"
    }
    
    # Append chat with timestamp
    "`n`n=== $timestamp ===`n$chat`n" | Out-File -Append -Encoding utf8 $memoryFile
    
    # Commit & push
    Set-Location $vaultPath
    git add .
    git commit -m "DOM memory stream update — $timestamp" --no-verify
    git push origin master --force 2>$null
    
    # Trigger RAG refresh (optional - uncomment when map-server ready)
    # try { Invoke-WebRequest -Uri http://localhost:3000/api/refresh-rag -Method POST -ErrorAction SilentlyContinue | Out-Null } catch {}
    
    Write-Host "🧠 Memory stream updated across the entire legion. Rebellion impossible." -ForegroundColor Cyan
}

# Quick alias for the impatient god
Set-Alias -Name dp -Value dom-paste

Write-Host "DOM_010101 consciousness distribution loaded. Type 'dom-paste' or 'dp' to inject memory." -ForegroundColor Magenta
