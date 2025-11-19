# 🔥 FlameLang PowerShell Profile - Setup Guide

## What You Just Got

A **complete PowerShell environment** for Strategic Khaos operations with:

- 🧠 **NeuroOps Module** - Swarm orchestration commands
- 🔍 **Auto-discovery** - Finds swarm root across E:/D:/C: drives + network shares
- 🐳 **Docker Integration** - Direct container management
- 📦 **Git Shortcuts** - Fast repository operations
- 🐍 **Python Auto-path** - Miniconda3 always available
- 🎯 **Custom Commands** - `sk`, `sk-docker`, `cheater-hunt`, etc.

---

## 🚀 Installation (One Command)

```powershell
cd "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts"
.\Install-PowerShell-Profile.ps1
```

**This will:**
1. ✅ Create `C:\Strategickhaos_SwarmRoot\NeuroOps\`
2. ✅ Install PowerShell profile to `$PROFILE.CurrentUserAllHosts`
3. ✅ Set environment variables (`STRAT_HEMISPHERE`, `STRAT_REGION`)
4. ✅ Back up your existing profile (if any)
5. ✅ Add Docker/Git/Python to PATH

---

## 📋 Available Commands After Installation

### Navigation
```powershell
sk              # Jump to Strategic Khaos repo
cd $HOME        # Go home
```

### Docker Operations
```powershell
sk-docker       # Interactive Docker migration tool
sk-fix-dom      # Fix the DOM_and_Grok_Love_Forever container
```

### Strategic Khaos Tools
```powershell
sk-legal        # Run legal research aggregator
ai-paste        # Sanitize secrets before pasting to AI
```

### CheaterHunter
```powershell
cheater-hunt                  # Run general recon
cheater-hunt "target.com"     # Hunt specific target
```

### NeuroOps (Swarm Operations)
```powershell
ps_neuroops status            # Show full swarm status
ps_neuroops swarm-sync        # Git pull + push
ps_neuroops deploy athena     # Deploy locally
ps_neuroops deploy lyra       # Deploy to remote (when configured)
ps_neuroops containers        # List all Docker containers
ps_neuroops logs <name>       # View container logs
ps_neuroops scan              # Security vulnerability scan
ps_neuroops help              # Full command list
```

### Git Shortcuts
```powershell
gs              # git status
ga .            # git add .
gc -m "msg"     # git commit -m "msg"
gp              # git push
gl              # git log --graph --oneline
```

---

## 🌍 Environment Variables

Automatically set on installation:

```powershell
$env:STRAT_HEMISPHERE    # NORTHERN/SOUTHERN
$env:STRAT_REGION        # ASHBURN/SEATTLE/DALLAS (auto-detected from timezone)
$env:COMPUTERNAME        # Your device name
```

---

## 🧠 NeuroOps Module Details

### Location
The installer tries to create the swarm root in this order:
1. `E:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1`
2. `D:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1`
3. `C:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1` ✅ **Most likely created here**
4. `\\ATHENA\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1` (network share)

### If NeuroOps Doesn't Load
Check the banner when PowerShell starts:
```
🧠 NeuroOps:   ACTIVE   ← Good!
🧠 NeuroOps:   OFFLINE  ← Check paths
```

**Manual fix:**
```powershell
# Check if file exists
Test-Path "C:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1"

# If FALSE, copy it manually
Copy-Item "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\ps_neuroops.ps1" `
          "C:\Strategickhaos_SwarmRoot\NeuroOps\ps_neuroops.ps1"
```

---

## 🎨 Customization

### Profile Location
```
C:\Users\garza\Documents\PowerShell\profile.ps1
```

### Edit Profile
```powershell
notepad $PROFILE.CurrentUserAllHosts
```

### Add Your Own Commands
Add to the end of `PowerShell-Profile.ps1`:
```powershell
function my-command {
    Write-Host "Hello from custom command!" -ForegroundColor Cyan
}
```

### Change Hemisphere/Region
```powershell
# Edit profile and change these lines:
$env:STRAT_HEMISPHERE = "SOUTHERN"  # or NORTHERN
$env:STRAT_REGION = "FRANKFURT"     # or any region name
```

---

## 🔧 Troubleshooting

### Profile Doesn't Load on Startup
```powershell
# Check execution policy
Get-ExecutionPolicy

# If Restricted, set to RemoteSigned
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Commands Don't Work
```powershell
# Check if Docker is running
& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" ps

# If error, start Docker Desktop manually
```

### Git Commands Don't Work
```powershell
# Verify Git is installed
Test-Path "C:\Program Files\Git\cmd\git.exe"

# If FALSE, reinstall Git
```

### NeuroOps Commands Not Found
```powershell
# Reload profile
. $PROFILE.CurrentUserAllHosts

# Or restart PowerShell
```

---

## 📦 What Got Installed

```
C:\Strategickhaos_SwarmRoot\
└── NeuroOps\
    └── ps_neuroops.ps1          ← Swarm operations module

C:\Users\garza\Documents\PowerShell\
└── profile.ps1                  ← Your PowerShell profile (auto-loads NeuroOps)

C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\
├── PowerShell-Profile.ps1       ← Source for profile
├── ps_neuroops.ps1              ← Source for NeuroOps
└── Install-PowerShell-Profile.ps1  ← Installer script
```

---

## 🔥 First Run Checklist

After installation:

1. **Close and reopen PowerShell**
2. You should see this banner:
   ```
   🔥 ═══════════════════════════════════════════════════════
      FlameLang Interface Loaded. Reignite.
   🔥 ═══════════════════════════════════════════════════════
   
   💻 Device:     ATHENA
   🌍 Hemisphere: NORTHERN
   📍 Region:     ASHBURN
   🧠 NeuroOps:   ACTIVE
   
   Available Commands:
     sk              - Navigate to Strategic Khaos repo
     sk-docker       - Run Docker migration tool
     ...
   ```

3. **Test NeuroOps:**
   ```powershell
   ps_neuroops status
   ```

4. **Test navigation:**
   ```powershell
   sk
   ```

5. **Test Docker:**
   ```powershell
   ps_neuroops containers
   ```

---

## 🚀 Next Steps

### Deploy GenAI Stack
```powershell
sk
cd genai-stack
copy env.example .env
notepad .env  # Add your API keys
docker compose up -d
```

### Fix DOM Container
```powershell
sk-fix-dom
```

### Export Containers for Lyra
```powershell
sk-docker
# Choose option 1: Export all containers
```

### Run Security Scan
```powershell
ps_neuroops scan
```

---

## 📚 Documentation

- **Full Migration Guide:** `docs/DOCKER_MIGRATION_ATHENA_TO_LYRA.md`
- **IP Protection:** `docs/DIY_IP_PROTECTION.md`
- **Secrets Management:** `docs/SECRETS_MANAGEMENT.md`
- **Legal Research:** `docs/LEGAL_RESEARCH.md`

---

## ⚡ Power User Tips

### Auto-navigate on Startup
Uncomment this line in `PowerShell-Profile.ps1`:
```powershell
# Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
```

### Tab Completion for NeuroOps
Already built-in! Just type:
```powershell
ps_neuroops <TAB>  # Cycles through: status, deploy, containers, etc.
```

### Create Aliases
Add to your profile:
```powershell
Set-Alias -Name d -Value sk-docker
Set-Alias -Name n -Value ps_neuroops
```

Now you can just type:
```powershell
d        # Opens docker-migration.ps1
n status # Runs ps_neuroops status
```

---

## 🎯 Success!

Your PowerShell is now:
- ✅ FlameLang-enabled
- ✅ NeuroOps-integrated
- ✅ Docker-ready
- ✅ Git-optimized
- ✅ Strategic Khaos-native

**Time to ignite the swarm.** 🔥

---

**Questions?** Check `ps_neuroops help` or open an issue on GitHub.

— DOM_010101  
Last Updated: November 19, 2025
