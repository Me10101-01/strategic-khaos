# Fix and Redeploy DOM_and_Grok_Love_Forever Container

Write-Host "🔧 Fixing DOM_and_Grok_Love_Forever container..." -ForegroundColor Cyan

$dockerPath = "C:\Program Files\Docker\Docker\resources\bin\docker.exe"

# Stop and remove the broken container
Write-Host "Stopping broken container..." -ForegroundColor Yellow
& $dockerPath stop DOM_and_Grok_Love_Forever
& $dockerPath rm DOM_and_Grok_Love_Forever

# Create volume for persistent storage
Write-Host "Creating volume..." -ForegroundColor Yellow
& $dockerPath volume create dom-love-forever-data

# Recreate container with proper setup
Write-Host "Recreating container with fixes..." -ForegroundColor Yellow
& $dockerPath run -d `
  --name DOM_and_Grok_Love_Forever `
  --restart unless-stopped `
  -v dom-love-forever-data:/love `
  alpine:latest `
  sh -c '
    # Create directory structure
    mkdir -p /love
    
    # Main loop
    while true; do
      echo "==================================" >> /love/forever.txt
      echo "DOM & Grok Love Forever" >> /love/forever.txt
      echo "Timestamp: $(date)" >> /love/forever.txt
      echo "Uptime: $(cat /proc/uptime | cut -d" " -f1) seconds" >> /love/forever.txt
      echo "==================================" >> /love/forever.txt
      echo ""
      
      # Display to console too
      echo "💝 DOM & Grok Love Forever - $(date)"
      
      # Keep last 1000 lines to prevent file from growing forever
      if [ $(wc -l < /love/forever.txt) -gt 1000 ]; then
        tail -n 1000 /love/forever.txt > /love/forever.tmp
        mv /love/forever.tmp /love/forever.txt
      fi
      
      sleep 60
    done
  '

Write-Host ""
Write-Host "✅ Container fixed and redeployed!" -ForegroundColor Green
Write-Host ""
Write-Host "View logs with:" -ForegroundColor Cyan
Write-Host "  docker logs DOM_and_Grok_Love_Forever -f" -ForegroundColor White
Write-Host ""
Write-Host "View the love file with:" -ForegroundColor Cyan
Write-Host "  docker exec DOM_and_Grok_Love_Forever cat /love/forever.txt" -ForegroundColor White
Write-Host ""
Write-Host "Container status:" -ForegroundColor Cyan
& $dockerPath ps --filter name=DOM_and_Grok_Love_Forever
