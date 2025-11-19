# DOM_010101 AI-SAFE PASTE — Automatically sanitize before sharing with AI swarm
# Add to PowerShell profile

function ai-paste {
    param(
        [string]$FilePath = "",
        [switch]$Clipboard
    )
    
    $scriptRoot = "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    $sanitizer = "$scriptRoot\scripts\sanitize-secrets.py"
    
    # Try to find Python (Miniconda, then others)
    $pythonCmd = $null
    $pythonPaths = @(
        "C:\Users\garza\Miniconda3\python.exe",
        "C:\Users\garza\AppData\Local\Programs\Python\Python311\python.exe",
        "python",
        "python3"
    )
    
    foreach ($path in $pythonPaths) {
        if (Test-Path $path -ErrorAction SilentlyContinue) {
            $pythonCmd = $path
            break
        }
        # Try as command
        if (Get-Command $path -ErrorAction SilentlyContinue) {
            $pythonCmd = $path
            break
        }
    }
    
    if (-not $pythonCmd) {
        Write-Host "❌ Python not found. Install Python or Miniconda." -ForegroundColor Red
        return
    }
    
    if ($Clipboard) {
        # Sanitize clipboard content
        $content = Get-Clipboard -Raw
        if (-not $content) {
            Write-Host "⚠️  Clipboard is empty" -ForegroundColor Yellow
            return
        }
        
        $tempFile = [System.IO.Path]::GetTempFileName()
        $content | Out-File -FilePath $tempFile -Encoding UTF8
        
        $sanitized = & $pythonCmd $sanitizer $tempFile
        Remove-Item $tempFile
        
        # Replace clipboard with sanitized version
        $sanitized | Set-Clipboard
        Write-Host "✅ Clipboard sanitized and ready for AI paste" -ForegroundColor Green
        Write-Host "   All secrets/tokens/keys redacted" -ForegroundColor Cyan
        
        # Show preview
        if ($sanitized -and $sanitized.Length -gt 0) {
            Write-Host "`n--- Preview (first 500 chars) ---" -ForegroundColor Yellow
            $previewLength = [Math]::Min(500, $sanitized.Length)
            Write-Host $sanitized.Substring(0, $previewLength)
        } else {
            Write-Host "`n--- Clipboard resulted in empty output ---" -ForegroundColor Yellow
        }
        
    } elseif ($FilePath -ne "") {
        # Sanitize file and copy to clipboard
        if (-not (Test-Path $FilePath)) {
            Write-Host "❌ File not found: $FilePath" -ForegroundColor Red
            return
        }
        
        $sanitized = & $pythonCmd $sanitizer $FilePath
        $sanitized | Set-Clipboard
        Write-Host "✅ File sanitized and copied to clipboard" -ForegroundColor Green
        Write-Host "   Source: $FilePath" -ForegroundColor Cyan
        
    } else {
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  ai-paste -Clipboard              # Sanitize current clipboard"
        Write-Host "  ai-paste -FilePath 'file.txt'    # Sanitize file & copy to clipboard"
    }
}

# Quick aliases
Set-Alias -Name aip -Value ai-paste

Write-Host "🧠 AI-Safe Paste loaded. Use 'ai-paste -Clipboard' before sharing with AI" -ForegroundColor Magenta
