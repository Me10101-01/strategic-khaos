# ============================================================================
# NeuroOps - Strategic Khaos Swarm Operations
# ============================================================================
# Copyright (c) 2025 Domenic Garza (DOM_010101)
# Part of Strategic Khaos - AGPL-3.0 License
# ============================================================================

Write-Host "🧠 Loading NeuroOps Module..." -ForegroundColor Cyan

# ============================================================================
# CORE NEUROOPS FUNCTION
# ============================================================================

function ps_neuroops {
    param(
        [Parameter(Mandatory=$false)]
        [string]$Command,
        
        [Parameter(Mandatory=$false, ValueFromRemainingArguments=$true)]
        [string[]]$Args
    )
    
    Write-Host "🧠 NeuroOps Command: $Command" -ForegroundColor Cyan
    
    switch ($Command) {
        "status" {
            Write-Host ""
            Write-Host "═══════════════════════════════════════" -ForegroundColor Yellow
            Write-Host "   STRATEGIC KHAOS SWARM STATUS" -ForegroundColor Cyan
            Write-Host "═══════════════════════════════════════" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "🖥️  Device:     $env:COMPUTERNAME" -ForegroundColor White
            Write-Host "🌍 Hemisphere: $env:STRAT_HEMISPHERE" -ForegroundColor White
            Write-Host "📍 Region:     $env:STRAT_REGION" -ForegroundColor White
            Write-Host ""
            
            # Docker status
            try {
                $dockerRunning = & "C:\Program Files\Docker\Docker\resources\bin\docker.exe" ps -q 2>&1
                if ($LASTEXITCODE -eq 0) {
                    $containerCount = ($dockerRunning | Measure-Object).Count
                    Write-Host "🐳 Docker:     RUNNING ($containerCount containers)" -ForegroundColor Green
                } else {
                    Write-Host "🐳 Docker:     OFFLINE" -ForegroundColor Red
                }
            } catch {
                Write-Host "🐳 Docker:     NOT INSTALLED" -ForegroundColor Red
            }
            
            # Git status
            try {
                Push-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
                $gitStatus = & "C:\Program Files\Git\cmd\git.exe" status --porcelain 2>&1
                if ($LASTEXITCODE -eq 0) {
                    $changedFiles = ($gitStatus | Measure-Object).Count
                    if ($changedFiles -eq 0) {
                        Write-Host "📦 Git Repo:   CLEAN" -ForegroundColor Green
                    } else {
                        Write-Host "📦 Git Repo:   $changedFiles uncommitted changes" -ForegroundColor Yellow
                    }
                } else {
                    Write-Host "📦 Git Repo:   ERROR" -ForegroundColor Red
                }
                Pop-Location
            } catch {
                Write-Host "📦 Git Repo:   NOT FOUND" -ForegroundColor Red
            }
            
            # Python status
            try {
                $pythonVersion = & "C:\Users\garza\Miniconda3\python.exe" --version 2>&1
                Write-Host "🐍 Python:     $pythonVersion" -ForegroundColor Green
            } catch {
                Write-Host "🐍 Python:     NOT FOUND" -ForegroundColor Red
            }
            
            Write-Host ""
        }
        
        "swarm-sync" {
            Write-Host "🔄 Syncing swarm repositories..." -ForegroundColor Yellow
            
            Push-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
            try {
                Write-Host "  Pulling latest changes..." -ForegroundColor Cyan
                & "C:\Program Files\Git\cmd\git.exe" pull origin master
                
                Write-Host "  Pushing local commits..." -ForegroundColor Cyan
                & "C:\Program Files\Git\cmd\git.exe" push origin master
                
                Write-Host "✅ Sync complete!" -ForegroundColor Green
            } catch {
                Write-Host "❌ Sync failed: $_" -ForegroundColor Red
            } finally {
                Pop-Location
            }
        }
        
        "deploy" {
            $target = $Args[0]
            if (-not $target) {
                Write-Host "❌ Usage: ps_neuroops deploy <target>" -ForegroundColor Red
                Write-Host "   Targets: athena, lyra, all" -ForegroundColor Yellow
                return
            }
            
            Write-Host "🚀 Deploying to: $target" -ForegroundColor Cyan
            
            switch ($target) {
                "athena" {
                    Write-Host "  Deploying to ATHENA (local)..." -ForegroundColor Yellow
                    Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\genai-stack"
                    & "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose up -d
                }
                
                "lyra" {
                    Write-Host "  Deploying to LYRA (remote)..." -ForegroundColor Yellow
                    Write-Host "  ⚠️  Not implemented yet. Use SSH to deploy manually." -ForegroundColor Red
                    Write-Host "  ssh user@lyra 'cd strategic-khaos/genai-stack && docker compose up -d'" -ForegroundColor DarkGray
                }
                
                "all" {
                    Write-Host "  Deploying to ALL nodes..." -ForegroundColor Yellow
                    ps_neuroops deploy athena
                    ps_neuroops deploy lyra
                }
                
                default {
                    Write-Host "❌ Unknown target: $target" -ForegroundColor Red
                }
            }
        }
        
        "containers" {
            Write-Host "🐳 Docker Containers:" -ForegroundColor Cyan
            & "C:\Program Files\Docker\Docker\resources\bin\docker.exe" ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        }
        
        "logs" {
            $containerName = $Args[0]
            if (-not $containerName) {
                Write-Host "❌ Usage: ps_neuroops logs <container-name>" -ForegroundColor Red
                return
            }
            
            Write-Host "📜 Logs for: $containerName" -ForegroundColor Cyan
            & "C:\Program Files\Docker\Docker\resources\bin\docker.exe" logs $containerName --tail 100 -f
        }
        
        "scan" {
            Write-Host "🔍 Scanning for security vulnerabilities..." -ForegroundColor Yellow
            
            # Scan Git repo for secrets
            Write-Host ""
            Write-Host "  Checking for exposed secrets..." -ForegroundColor Cyan
            Set-Location "C:\Users\garza\Chaos God DOM_010101\strategic-khaos"
            
            $suspiciousFiles = @(
                ".env",
                "*.pem",
                "*.key",
                "*secret*",
                "*password*",
                "*token*"
            )
            
            foreach ($pattern in $suspiciousFiles) {
                $found = Get-ChildItem -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue
                if ($found) {
                    Write-Host "  ⚠️  Found: $($found.FullName)" -ForegroundColor Yellow
                }
            }
            
            Write-Host ""
            Write-Host "  ✅ Scan complete" -ForegroundColor Green
        }
        
        "help" {
            Write-Host ""
            Write-Host "═══════════════════════════════════════" -ForegroundColor Yellow
            Write-Host "   NEUROOPS COMMAND REFERENCE" -ForegroundColor Cyan
            Write-Host "═══════════════════════════════════════" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "ps_neuroops status" -ForegroundColor White
            Write-Host "  Show swarm status (Docker, Git, Python)" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops swarm-sync" -ForegroundColor White
            Write-Host "  Pull and push Git changes" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops deploy <target>" -ForegroundColor White
            Write-Host "  Deploy containers (athena | lyra | all)" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops containers" -ForegroundColor White
            Write-Host "  List all Docker containers" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops logs <container>" -ForegroundColor White
            Write-Host "  View container logs" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops scan" -ForegroundColor White
            Write-Host "  Scan for security issues" -ForegroundColor DarkGray
            Write-Host ""
            Write-Host "ps_neuroops help" -ForegroundColor White
            Write-Host "  Show this help message" -ForegroundColor DarkGray
            Write-Host ""
        }
        
        default {
            Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
            Write-Host "   Run 'ps_neuroops help' for available commands" -ForegroundColor Yellow
        }
    }
}

# ============================================================================
# AUTO-COMPLETE SUPPORT
# ============================================================================

Register-ArgumentCompleter -CommandName ps_neuroops -ParameterName Command -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)
    
    $commands = @('status', 'swarm-sync', 'deploy', 'containers', 'logs', 'scan', 'help')
    
    $commands | Where-Object { $_ -like "$wordToComplete*" } | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new($_, $_, 'ParameterValue', $_)
    }
}

# ============================================================================
# INITIALIZATION
# ============================================================================

Write-Host "✅ NeuroOps Module Loaded" -ForegroundColor Green
Write-Host "   Run 'ps_neuroops help' for available commands" -ForegroundColor DarkGray

# ============================================================================
# END OF NEUROOPS MODULE
# ============================================================================
