# Strategic Khaos - Docker Migration & Deployment Script
# Migrates containers from Athena → Lyra and deploys GenAI stack

Write-Host "🚀 Strategic Khaos Docker Migration Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Docker path
$dockerPath = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"

# Check if Docker is running
try {
    & $dockerPath ps | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Menu
Write-Host ""
Write-Host "What would you like to do?" -ForegroundColor Yellow
Write-Host "1. Export all containers from Athena (backup)"
Write-Host "2. Deploy GenAI stack locally (test)"
Write-Host "3. Push images to Docker Hub (for Lyra)"
Write-Host "4. View running containers"
Write-Host "5. View logs of a container"
Write-Host "6. Stop all containers"
Write-Host "7. Clean up stopped containers"
Write-Host ""

$choice = Read-Host "Enter choice (1-7)"

switch ($choice) {
    "1" {
        Write-Host "📦 Exporting containers..." -ForegroundColor Cyan
        
        # Create export directory
        $exportDir = "C:\Users\garza\Downloads\docker-exports"
        if (-not (Test-Path $exportDir)) {
            New-Item -ItemType Directory -Path $exportDir | Out-Null
        }
        
        # Export n8n
        Write-Host "Exporting n8n..." -ForegroundColor Yellow
        & $dockerPath commit docker-n8n-1 n8n-backup:latest
        & $dockerPath save -o "$exportDir\n8n-backup.tar" n8n-backup:latest
        
        # Export AI node
        Write-Host "Exporting AI node..." -ForegroundColor Yellow
        & $dockerPath commit funny_davinci ai-node-backup:latest
        & $dockerPath save -o "$exportDir\ai-node-backup.tar" ai-node-backup:latest
        
        # Export DOM container
        Write-Host "Exporting DOM container..." -ForegroundColor Yellow
        & $dockerPath commit DOM_and_Grok_Love_Forever dom-grok-backup:latest
        & $dockerPath save -o "$exportDir\dom-grok-backup.tar" dom-grok-backup:latest
        
        Write-Host "✅ Export complete! Files saved to: $exportDir" -ForegroundColor Green
        Write-Host ""
        Write-Host "Transfer these files to Lyra using:" -ForegroundColor Cyan
        Write-Host "  scp $exportDir\*.tar user@lyra:/home/user/" -ForegroundColor White
    }
    
    "2" {
        Write-Host "🧪 Deploying GenAI stack locally..." -ForegroundColor Cyan
        
        # Navigate to genai-stack directory
        $genaiPath = "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\genai-stack"
        
        if (-not (Test-Path $genaiPath)) {
            Write-Host "❌ GenAI stack not found at: $genaiPath" -ForegroundColor Red
            exit 1
        }
        
        Set-Location $genaiPath
        
        # Check for .env file
        if (-not (Test-Path ".env")) {
            Write-Host "⚠️  No .env file found. Creating from env.example..." -ForegroundColor Yellow
            Copy-Item "env.example" ".env"
            Write-Host "📝 Please edit .env with your settings, then run this script again." -ForegroundColor Cyan
            notepad .env
            exit 0
        }
        
        # Build and start services
        Write-Host "Building services..." -ForegroundColor Yellow
        & $dockerPath compose build
        
        Write-Host "Starting services..." -ForegroundColor Yellow
        & $dockerPath compose up -d
        
        Write-Host ""
        Write-Host "✅ GenAI stack is running!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Check status with:" -ForegroundColor Cyan
        Write-Host "  docker compose ps" -ForegroundColor White
        Write-Host ""
        Write-Host "View logs with:" -ForegroundColor Cyan
        Write-Host "  docker compose logs -f" -ForegroundColor White
    }
    
    "3" {
        Write-Host "🐳 Pushing images to Docker Hub..." -ForegroundColor Cyan
        
        # Login to Docker Hub
        Write-Host "Please login to Docker Hub:" -ForegroundColor Yellow
        & $dockerPath login
        
        # Get Docker Hub username
        $username = Read-Host "Enter your Docker Hub username (e.g., dom010101)"
        
        # Tag and push images
        Write-Host "Tagging and pushing n8n..." -ForegroundColor Yellow
        & $dockerPath tag n8n-backup:latest "$username/strategic-khaos:n8n"
        & $dockerPath push "$username/strategic-khaos:n8n"
        
        Write-Host "Tagging and pushing AI node..." -ForegroundColor Yellow
        & $dockerPath tag ai-node-backup:latest "$username/strategic-khaos:ai-node"
        & $dockerPath push "$username/strategic-khaos:ai-node"
        
        Write-Host "Tagging and pushing DOM container..." -ForegroundColor Yellow
        & $dockerPath tag dom-grok-backup:latest "$username/strategic-khaos:dom-grok"
        & $dockerPath push "$username/strategic-khaos:dom-grok"
        
        Write-Host ""
        Write-Host "✅ Images pushed to Docker Hub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "On Lyra, pull with:" -ForegroundColor Cyan
        Write-Host "  docker pull $username/strategic-khaos:n8n" -ForegroundColor White
        Write-Host "  docker pull $username/strategic-khaos:ai-node" -ForegroundColor White
        Write-Host "  docker pull $username/strategic-khaos:dom-grok" -ForegroundColor White
    }
    
    "4" {
        Write-Host "📋 Running containers:" -ForegroundColor Cyan
        & $dockerPath ps
    }
    
    "5" {
        Write-Host "📋 Available containers:" -ForegroundColor Cyan
        & $dockerPath ps -a --format "table {{.Names}}\t{{.Status}}"
        
        Write-Host ""
        $containerName = Read-Host "Enter container name to view logs"
        & $dockerPath logs $containerName --tail 100 -f
    }
    
    "6" {
        Write-Host "⚠️  Stopping all containers..." -ForegroundColor Yellow
        & $dockerPath stop $(& $dockerPath ps -q)
        Write-Host "✅ All containers stopped" -ForegroundColor Green
    }
    
    "7" {
        Write-Host "🧹 Cleaning up stopped containers..." -ForegroundColor Yellow
        & $dockerPath container prune -f
        Write-Host "✅ Cleanup complete" -ForegroundColor Green
    }
    
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
