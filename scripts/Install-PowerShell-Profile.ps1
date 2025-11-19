# ============================================================================
# Strategic Khaos - PowerShell Profile Installer
# ============================================================================
# This script installs the Strategic Khaos PowerShell profile and sets up
# the Strategickhaos_SwarmRoot directory structure
# ============================================================================

Write-Host ""
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host "   Strategic Khaos PowerShell Profile Installer" -ForegroundColor Yellow
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host ""

# Require admin for some operations
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  This script should be run as Administrator for best results" -ForegroundColor Yellow
    Write-Host "   Some features may not work properly" -ForegroundColor DarkGray
    Write-Host ""
}

# ============================================================================
# STEP 1: Create Swarm Root Directory
# ============================================================================

Write-Host "📁 Step 1: Creating Strategickhaos_SwarmRoot..." -ForegroundColor Cyan

$swarmRoots = @('C:\Strategickhaos_SwarmRoot', 'D:\Strategickhaos_SwarmRoot', 'E:\Strategickhaos_SwarmRoot')
$createdRoot = $null

foreach ($root in $swarmRoots) {
    $drive = Split-Path $root -Qualifier
    if (Test-Path $drive) {
        try {
            $neuroOpsPath = Join-Path $root "NeuroOps"
            New-Item -ItemType Directory -Path $neuroOpsPath -Force | Out-Null
            
            # Copy ps_neuroops.ps1 to the swarm root
            $sourcePath = "$PSScriptRoot\ps_neuroops.ps1"
            $destPath = Join-Path $neuroOpsPath "ps_neuroops.ps1"
            
            if (Test-Path $sourcePath) {
                Copy-Item $sourcePath $destPath -Force
                Write-Host "  ✅ Created: $neuroOpsPath" -ForegroundColor Green
                Write-Host "  ✅ Copied: ps_neuroops.ps1" -ForegroundColor Green
                $createdRoot = $root
                break
            } else {
                Write-Host "  ❌ Source not found: $sourcePath" -ForegroundColor Red
            }
        } catch {
            Write-Host "  ⚠️  Cannot create: $root" -ForegroundColor Yellow
        }
    }
}

if (-not $createdRoot) {
    Write-Host "  ❌ Could not create swarm root on any drive" -ForegroundColor Red
    Write-Host "  Continuing anyway..." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "  Swarm Root: $createdRoot" -ForegroundColor Cyan
}

# ============================================================================
# STEP 2: Install PowerShell Profile
# ============================================================================

Write-Host ""
Write-Host "📝 Step 2: Installing PowerShell Profile..." -ForegroundColor Cyan

$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

# Create profile directory if it doesn't exist
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    Write-Host "  ✅ Created profile directory: $profileDir" -ForegroundColor Green
}

# Backup existing profile
if (Test-Path $profilePath) {
    $backupPath = "$profilePath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $profilePath $backupPath
    Write-Host "  ✅ Backed up existing profile to: $backupPath" -ForegroundColor Green
}

# Copy new profile
$sourceProfile = "$PSScriptRoot\PowerShell-Profile.ps1"
if (Test-Path $sourceProfile) {
    Copy-Item $sourceProfile $profilePath -Force
    Write-Host "  ✅ Installed new profile to: $profilePath" -ForegroundColor Green
} else {
    Write-Host "  ❌ Source profile not found: $sourceProfile" -ForegroundColor Red
}

# ============================================================================
# STEP 3: Set Environment Variables
# ============================================================================

Write-Host ""
Write-Host "🌍 Step 3: Setting Environment Variables..." -ForegroundColor Cyan

# Set user environment variables (persistent across sessions)
try {
    [System.Environment]::SetEnvironmentVariable('STRAT_HEMISPHERE', 'NORTHERN', 'User')
    Write-Host "  ✅ Set STRAT_HEMISPHERE=NORTHERN" -ForegroundColor Green
    
    # Auto-detect region from timezone
    $tz = (Get-TimeZone).Id
    $region = "UNKNOWN"
    if ($tz -like "*Eastern*") { $region = "ASHBURN" }
    elseif ($tz -like "*Pacific*") { $region = "SEATTLE" }
    elseif ($tz -like "*Central*") { $region = "DALLAS" }
    
    [System.Environment]::SetEnvironmentVariable('STRAT_REGION', $region, 'User')
    Write-Host "  ✅ Set STRAT_REGION=$region (detected from timezone)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Could not set environment variables: $_" -ForegroundColor Yellow
}

# ============================================================================
# STEP 4: Verify Installation
# ============================================================================

Write-Host ""
Write-Host "🔍 Step 4: Verifying Installation..." -ForegroundColor Cyan

$checks = @{
    "PowerShell Profile" = Test-Path $profilePath
    "NeuroOps Module" = Test-Path "$createdRoot\NeuroOps\ps_neuroops.ps1"
    "Docker CLI" = Test-Path "C:\Program Files\Docker\Docker\resources\bin\docker.exe"
    "Git CLI" = Test-Path "C:\Program Files\Git\cmd\git.exe"
    "Python (Miniconda)" = Test-Path "C:\Users\garza\Miniconda3\python.exe"
    "Strategic Khaos Repo" = Test-Path "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
}

foreach ($check in $checks.GetEnumerator()) {
    if ($check.Value) {
        Write-Host "  ✅ $($check.Key)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $($check.Key)" -ForegroundColor Red
    }
}

# ============================================================================
# COMPLETION
# ============================================================================

Write-Host ""
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host "   Installation Complete!" -ForegroundColor Yellow
Write-Host "🔥 ═══════════════════════════════════════════════════════" -ForegroundColor Red
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Close and reopen PowerShell to load the new profile" -ForegroundColor White
Write-Host "  2. Run 'ps_neuroops help' to see available commands" -ForegroundColor White
Write-Host "  3. Run 'sk' to navigate to Strategic Khaos repo" -ForegroundColor White
Write-Host ""
Write-Host "Available Commands:" -ForegroundColor Cyan
Write-Host "  sk              - Navigate to Strategic Khaos repo" -ForegroundColor White
Write-Host "  sk-docker       - Run Docker migration tool" -ForegroundColor White
Write-Host "  sk-fix-dom      - Fix DOM container" -ForegroundColor White
Write-Host "  sk-legal        - Run legal research aggregator" -ForegroundColor White
Write-Host "  ai-paste        - Sanitize secrets before AI paste" -ForegroundColor White
Write-Host "  cheater-hunt    - Run ExamSoft reconnaissance" -ForegroundColor White
Write-Host "  ps_neuroops     - Swarm operations" -ForegroundColor White
Write-Host ""
Write-Host "Profile Location: $profilePath" -ForegroundColor DarkGray
Write-Host ""

# Ask to reload profile now
$reload = Read-Host "Reload PowerShell profile now (y/n)"
if ($reload -eq 'y') {
    . $profilePath
    Write-Host "Profile reloaded successfully!" -ForegroundColor Green
}
