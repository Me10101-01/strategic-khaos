# ============================================================================
# Strategic Khaos - PowerShell Profile
# Multi-Root Swarm Initialization System
# ============================================================================
# Copyright (c) 2025 Domenic Garza (DOM_010101)
# Part of Strategic Khaos - AGPL-3.0 License
# ============================================================================

# Helper function to safely source files
function _SK-Source {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Write-Host "✅ Sourcing: $Path" -ForegroundColor Green
        . $Path
        return $true
    }
    return $false
}

# ============================================================================
# SWARM ROOT DISCOVERY
# ============================================================================
# Attempts to locate Strategickhaos_SwarmRoot across multiple drives/locations
# Priority order: E: -> D: -> C: -> Network Share

$__sk_roots = @(
    'E:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1',
    'D:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1',
    'C:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1',
    '\\ATHENA\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1'
)

$__sk_loaded = $false
foreach ($candidate in $__sk_roots) {
    if (_SK-Source $candidate) {
        # Verify the function was actually loaded
        if (Get-Command -Name ps_neuroops -ErrorAction SilentlyContinue) {
            Write-Host "🧠 NeuroOps loaded from: $candidate" -ForegroundColor Cyan
            $__sk_loaded = $true
            break
        }
    }
}

if (-not $__sk_loaded) {
    Write-Host "⚠️  NeuroOps not found. Swarm functions unavailable." -ForegroundColor Yellow
    Write-Host "   Expected locations:" -ForegroundColor DarkGray
    foreach ($r in $__sk_roots) {
        Write-Host "   - $r" -ForegroundColor DarkGray
    }
}

# ============================================================================
# STRATEGIC KHAOS FUNCTIONS
# ============================================================================

# CheaterHunter ExamSoft Reconnaissance
function cheater-hunt {
    param([string]$Target)
    
    $reconPath = "$HOME\CheaterHunter-ExamSoft-Recon"
    
    if (-not (Test-Path $reconPath)) {
        Write-Host "❌ CheaterHunter not found at: $reconPath" -ForegroundColor Red
        return
    }
    
    Push-Location $reconPath
    try {
        if ($Target) {
            Write-Host "🎯 Hunting target: $Target" -ForegroundColor Cyan
            python .\recon.py $Target
        } else {
            Write-Host "🔍 Running general reconnaissance..." -ForegroundColor Cyan
            python .\recon.py
        }
    } finally {
        Pop-Location
    }
}

# Quick navigation to Strategic Khaos repository
function sk {
    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    Write-Host "📂 Strategic Khaos Repository" -ForegroundColor Cyan
}

# Docker migration shortcut
function sk-docker {
    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    .\scripts\docker-migration.ps1
}

# Fix DOM container
function sk-fix-dom {
    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    .\scripts\fix-dom-container.ps1
}

# Run legal research
function sk-legal {
    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    .\scripts\run-legal-research.ps1
}

# Sanitize secrets before pasting to AI
function ai-paste {
    param(
        [switch]$Clipboard,
        [string]$FilePath
    )
    
    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
    
    if ($Clipboard) {
        .\scripts\ai-safe-paste.ps1 -Clipboard
    } elseif ($FilePath) {
        .\scripts\ai-safe-paste.ps1 -FilePath $FilePath
    } else {
        Write-Host "Usage: ai-paste -Clipboard  OR  ai-paste -FilePath <path>" -ForegroundColor Yellow
    }
}

# ============================================================================
# ENVIRONMENT DETECTION
# ============================================================================

# Set hemisphere and region if not already set
if (-not $env:STRAT_HEMISPHERE) {
    $env:STRAT_HEMISPHERE = "NORTHERN"  # Default
}

if (-not $env:STRAT_REGION) {
    # Detect region from timezone or set manually
    $tz = (Get-TimeZone).Id
    if ($tz -like "*Eastern*") {
        $env:STRAT_REGION = "ASHBURN"
    } elseif ($tz -like "*Pacific*") {
        $env:STRAT_REGION = "SEATTLE"
    } elseif ($tz -like "*Central*") {
        $env:STRAT_REGION = "DALLAS"
    } else {
        $env:STRAT_REGION = "UNKNOWN"
    }
}

# ============================================================================
# BANNER
# ============================================================================

Write-Host ""
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host "   FlameLang Interface Loaded. Reignite." -ForegroundColor Yellow
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host ""
Write-Host "💻 Device:     $env:COMPUTERNAME" -ForegroundColor Cyan
Write-Host "🌍 Hemisphere: $env:STRAT_HEMISPHERE" -ForegroundColor Cyan
Write-Host "📍 Region:     $env:STRAT_REGION" -ForegroundColor Cyan
Write-Host "🧠 NeuroOps:   $($__sk_loaded ? 'ACTIVE' : 'OFFLINE')" -ForegroundColor $(if ($__sk_loaded) { 'Green' } else { 'Red' })
Write-Host ""
Write-Host "Available Commands:" -ForegroundColor Yellow
Write-Host "  sk              - Navigate to Strategic Khaos repo" -ForegroundColor White
Write-Host "  sk-docker       - Run Docker migration tool" -ForegroundColor White
Write-Host "  sk-fix-dom      - Fix DOM_and_Grok_Love_Forever container" -ForegroundColor White
Write-Host "  sk-legal        - Run legal research aggregator" -ForegroundColor White
Write-Host "  ai-paste        - Sanitize secrets before AI paste" -ForegroundColor White
Write-Host "  cheater-hunt    - Run ExamSoft reconnaissance" -ForegroundColor White
Write-Host ""

# ============================================================================
# DOCKER PATH (if needed)
# ============================================================================

# Add Docker to PATH if not already present
$dockerPath = "C:\Program Files\Docker\Docker\resources\bin"
if (Test-Path $dockerPath) {
    if ($env:PATH -notlike "*$dockerPath*") {
        $env:PATH += ";$dockerPath"
        Write-Host "✅ Docker CLI added to PATH" -ForegroundColor Green
    }
}

# ============================================================================
# PYTHON PATH (Miniconda)
# ============================================================================

$condaPath = "C:\Users\garza\Miniconda3"
if (Test-Path $condaPath) {
    if ($env:PATH -notlike "*$condaPath*") {
        $env:PATH = "$condaPath;$condaPath\Scripts;$condaPath\Library\bin;" + $env:PATH
        Write-Host "✅ Python (Miniconda3) added to PATH" -ForegroundColor Green
    }
}

# ============================================================================
# GIT ALIASES (optional)
# ============================================================================

function gs { & "C:\Program Files\Git\cmd\git.exe" status }
function ga { & "C:\Program Files\Git\cmd\git.exe" add $args }
function gc { & "C:\Program Files\Git\cmd\git.exe" commit $args }
function gp { & "C:\Program Files\Git\cmd\git.exe" push $args }
function gl { & "C:\Program Files\Git\cmd\git.exe" log --oneline --graph --decorate --all }

# ============================================================================
# AUTO-NAVIGATION (optional - comment out if you don't want this)
# ============================================================================

# Uncomment to auto-navigate to Strategic Khaos on shell startup
# Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"

# ============================================================================
# END OF PROFILE
# ============================================================================
